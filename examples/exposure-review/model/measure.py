"""Observe nine fixed SQL exposure constructions against exact rational references."""
from collections import defaultdict
from datetime import datetime, timezone
from fractions import Fraction as F
import argparse
import hashlib
import json
import math
from pathlib import Path
import platform
import sqlite3
import time

SETS = [('NS-A1','CP-A'), ('NS-A2','CP-A'), ('NS-B1','CP-B')]
TRADES = [('T1','NS-A1','USD',1000000), ('T2','NS-A1','EUR',-600000),
          ('T3','NS-A2','USD',-400000), ('T4','NS-A2','USD',100000),
          ('T5','NS-B1','USD',500000), ('T6','NS-B1','EUR',200000)]
COLLATERAL = [('C1','NS-A1','USD',100000,'0',True,True),
              ('C2','NS-A1','EUR',100000,'1/10',True,True),
              ('C3','NS-A1','USD',80000,'0',False,True),
              ('C4','NS-A2','USD',200000,'0',True,True),
              ('C5','NS-B1','USD',250000,'1/20',True,True),
              ('C6','NS-B1','USD',300000,'0',True,False)]
MODES = ['selected_sets','counterparty_pool','global_pool','omit_haircuts',
         'include_pending','include_ineligible','invert_fx','join_before_aggregation',
         'floor_trades_first']


def group_key(netting_set, mode):
    if mode == 'global_pool': return 'ALL'
    if mode == 'counterparty_pool': return dict(SETS)[netting_set]
    return netting_set


def reference(mode):
    trade_values, collateral_values = defaultdict(list), defaultdict(list)
    for identity, netting_set, currency, amount in TRADES:
        fx = F(1) if currency == 'USD' else (F(10,11) if mode == 'invert_fx' else F(11,10))
        value = amount*fx
        if mode == 'floor_trades_first': value = max(value,0)
        trade_values[group_key(netting_set,mode)].append(value)
    for identity,netting_set,currency,amount,haircut,settled,eligible in COLLATERAL:
        fx = F(1) if currency == 'USD' else (F(10,11) if mode == 'invert_fx' else F(11,10))
        accepted = (settled or mode=='include_pending') and (eligible or mode=='include_ineligible')
        factor = F(1) if mode=='omit_haircuts' else 1-F(haircut)
        value = amount*fx*factor if accepted else F(0)
        collateral_values[group_key(netting_set,mode)].append(value)
    rows=[]
    for key in sorted(trade_values):
        tv,cv=trade_values[key],collateral_values[key]
        v,c=sum(tv),sum(cv)
        nt,nc=len(tv),len(cv)
        if mode=='join_before_aggregation':
            v,c=v*nc,c*nt
            nt,nc=nt*nc,nt*nc
        rows.append({'group_id':key,'trade_value_usd':str(v),'recognized_collateral_usd':str(c),
                     'current_exposure_usd':str(max(v-c,0)), 'trade_rows':nt,'collateral_rows':nc})
    return rows


def query(mode):
    trade_fx = "CASE WHEN t.currency='USD' THEN 1.0 ELSE "+('10.0/11.0' if mode=='invert_fx' else '11.0/10.0')+' END'
    collateral_fx = "CASE WHEN c.currency='USD' THEN 1.0 ELSE "+('10.0/11.0' if mode=='invert_fx' else '11.0/10.0')+' END'
    value = f't.amount*({trade_fx})'
    if mode=='floor_trades_first': value=f'max({value},0.0)'
    settled='1' if mode=='include_pending' else 'c.settled=1'
    eligible='1' if mode=='include_ineligible' else 'c.eligible=1'
    haircut='1.0' if mode=='omit_haircuts' else '(1.0-c.haircut)'
    recognized=f'CASE WHEN ({settled}) AND ({eligible}) THEN c.amount*({collateral_fx})*{haircut} ELSE 0.0 END'
    trade_group='s.counterparty' if mode=='counterparty_pool' else ("'ALL'" if mode=='global_pool' else 't.netting_set')
    collateral_group='s.counterparty' if mode=='counterparty_pool' else ("'ALL'" if mode=='global_pool' else 'c.netting_set')
    ctes=f'''WITH tv AS (
      SELECT t.id, {trade_group} AS group_id, {value} AS value
      FROM trades t JOIN netting_sets s ON s.id=t.netting_set
    ), cv AS (
      SELECT c.id, {collateral_group} AS group_id, {recognized} AS value
      FROM collateral c JOIN netting_sets s ON s.id=c.netting_set
    )'''
    if mode=='join_before_aggregation':
        return ctes+'''
        SELECT tv.group_id, sum(tv.value) AS trade_value_usd,
          sum(cv.value) AS recognized_collateral_usd,
          max(sum(tv.value)-sum(cv.value),0.0) AS current_exposure_usd,
          count(tv.id) AS trade_rows, count(cv.id) AS collateral_rows
        FROM tv JOIN cv ON tv.group_id=cv.group_id
        GROUP BY tv.group_id ORDER BY tv.group_id'''
    return ctes+''', t AS (
      SELECT group_id,sum(value) AS value,count(*) AS n FROM tv GROUP BY group_id
    ), c AS (
      SELECT group_id,sum(value) AS value,count(*) AS n FROM cv GROUP BY group_id
    ) SELECT t.group_id,t.value AS trade_value_usd,c.value AS recognized_collateral_usd,
      max(t.value-c.value,0.0) AS current_exposure_usd,t.n AS trade_rows,c.n AS collateral_rows
      FROM t JOIN c ON t.group_id=c.group_id ORDER BY t.group_id'''


def measure():
    started=time.monotonic()
    db=sqlite3.connect(':memory:');db.row_factory=sqlite3.Row
    db.executescript('''CREATE TABLE netting_sets(id TEXT PRIMARY KEY,counterparty TEXT);
        CREATE TABLE trades(id TEXT PRIMARY KEY,netting_set TEXT,currency TEXT,amount REAL);
        CREATE TABLE collateral(id TEXT PRIMARY KEY,netting_set TEXT,currency TEXT,
                                amount REAL,haircut REAL,settled INTEGER,eligible INTEGER);''')
    db.executemany('INSERT INTO netting_sets VALUES (?,?)',SETS)
    db.executemany('INSERT INTO trades VALUES (?,?,?,?)',TRADES)
    db.executemany('INSERT INTO collateral VALUES (?,?,?,?,?,?,?)',
                   [(i,s,c,a,float(F(h)),int(t),int(e)) for i,s,c,a,h,t,e in COLLATERAL])
    controls=[]

    def check(identity,actual,expected,tolerance=0):
        passed=actual==expected if tolerance==0 else math.isfinite(actual) and abs(actual-expected)<=tolerance
        controls.append({'id':identity,'observed':actual,'reference':expected,
                         'absolute_tolerance':tolerance,'passed':passed})

    constructions=[]
    baseline=sum(F(row['current_exposure_usd']) for row in reference('selected_sets'))
    for mode in MODES:
        sql=query(mode)
        native=[dict(row) for row in db.execute(sql).fetchall()]
        expected=reference(mode)
        check(mode+'_groups',[row['group_id'] for row in native],[row['group_id'] for row in expected])
        for row,exact in zip(native,expected):
            for name in ['trade_value_usd','recognized_collateral_usd','current_exposure_usd']:
                check(mode+'_'+row['group_id']+'_'+name,row[name],float(F(exact[name])),1e-6)
            for name in ['trade_rows','collateral_rows']:
                check(mode+'_'+row['group_id']+'_'+name,row[name],exact[name])
        total=math.fsum(row['current_exposure_usd'] for row in native)
        exact_total=sum(F(row['current_exposure_usd']) for row in expected)
        check(mode+'_total',total,float(exact_total),1e-6)
        constructions.append({'id':mode,'query':sql,'native_rows':native,'exact_reference_rows':expected,
                              'native_total_usd':total,'exact_total_usd':str(exact_total),
                              'exact_difference_from_selected_usd':str(exact_total-baseline)})
    check('selected_total_hand_reference',constructions[0]['native_total_usd'],623500.0,1e-6)
    raw_values=[F(amount)*(F(1) if currency=='USD' else F(11,10)) for _,_,currency,amount in TRADES]
    measures={'signed_trade_total_usd':str(sum(raw_values)),
              'positive_individual_trade_total_usd':str(sum(max(v,0) for v in raw_values)),
              'positive_unsecured_net_set_total_usd':str(sum(max(F(row['trade_value_usd']),0)
                                                             for row in reference('selected_sets')))}
    check('signed_total',float(F(measures['signed_trade_total_usd'])),760000.0,1e-6)
    check('positive_individual_total',float(F(measures['positive_individual_trade_total_usd'])),1820000.0,1e-6)
    check('positive_net_set_total',float(F(measures['positive_unsecured_net_set_total_usd'])),1060000.0,1e-6)
    db.close()
    inputs={'netting_sets':[{'id':s,'counterparty':c} for s,c in SETS],
            'trades':[dict(zip(['id','netting_set','currency','signed_value'],r)) for r in TRADES],
            'collateral':[dict(zip(['id','netting_set','currency','market_value','haircut','settled','eligible'],r)) for r in COLLATERAL]}
    source=Path(__file__)
    return {'recorded_at':datetime.now(timezone.utc).isoformat(),'calculation_seconds':time.monotonic()-started,
            'environment':{'python':platform.python_version(),'sqlite':sqlite3.sqlite_version},
            'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'plan_sha256':hashlib.sha256(source.with_name('README.md').read_bytes()).hexdigest(),
            'input_sha256':hashlib.sha256(json.dumps(inputs,sort_keys=True).encode()).hexdigest(),
            'scope':{'as_of':'2026-10-06T00:00:00Z','reporting_currency':'USD','usd_per_eur':'11/10',
                     'positive_trade_sign':'asset to reporting bank','collateral':'received only; exclusive set allocation',
                     'legal_recognition':'stipulated synthetic set boundaries, not a legal determination',
                     'selected_measure':'sum over netting sets of max(signed trade value - recognized collateral, 0)',
                     'future_exposure_included':False,'regulatory_ead':False,'amount_tolerance_usd':1e-6},
            'inputs':inputs,'scope_measures':measures,'constructions':constructions,'controls':controls,
            'all_controls_passed':all(c['passed'] for c in controls)}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():parser.error('Output exists; preserve the earlier observation.')
    result=measure();args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'constructions':len(result['constructions']),'controls':len(result['controls']),
                      'all_controls_passed':result['all_controls_passed']}))
    raise SystemExit(0 if result['all_controls_passed'] else 1)
