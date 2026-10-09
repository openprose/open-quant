"""Fixed synthetic historical selections; standard library, no network."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import sqlite3
import time

FIELDS=['id','entity','observation_date','revision','published_at','available_at','value']
FEATURES=[dict(zip(FIELDS,row)) for row in [
    ('R01','A','2025-12-31',1,'2026-01-02T09:00:00Z','2026-01-02T09:05:00Z',.02),
    ('R02','A','2025-12-31',2,'2026-01-05T09:00:00Z','2026-01-05T09:05:00Z',.08),
    ('R03','B','2025-12-31',1,'2026-01-02T09:00:00Z','2026-01-02T10:00:00Z',-.01),
    ('R04','B','2025-12-31',2,'2026-01-05T09:00:00Z','2026-01-05T09:05:00Z',.04),
    ('R05','A','2026-01-02',1,'2026-01-03T09:00:00Z','2026-01-03T09:05:00Z',.03),
    ('R06','A','2026-01-02',2,'2026-01-06T09:00:00Z','2026-01-06T09:05:00Z',-.02),
    ('R07','B','2026-01-02',1,'2026-01-03T09:00:00Z','2026-01-03T09:10:00Z',.05),
    ('R08','B','2026-01-02',2,'2026-01-06T09:00:00Z','2026-01-06T09:05:00Z',-.04),
    ('R09','A','2025-11-30',1,'2026-01-03T09:20:00Z','2026-01-03T09:25:00Z',.99),
    ('R10','C','2025-12-31',1,'2026-01-02T09:00:00Z',None,.06),
    ('R11','D','2025-12-31',1,'2026-01-02T09:00:00Z','2026-01-02T09:05:00Z',.02),
    ('R12','D','2025-12-31',1,'2026-01-02T09:00:00Z','2026-01-02T09:05:00Z',.07),
    ('R13','A','2025-12-31',1,'2026-01-02T09:00:00Z','2026-01-06T09:30:00Z',.02),
]]
DECISIONS=[dict(zip(['id','entity','observation_date','cutoff','outcome'],row),outcome_published_at='2026-01-10T10:00:00Z') for row in [
    ('D01','A','2025-12-31','2026-01-02T09:02:00Z',.08),
    ('D02','A','2025-12-31','2026-01-02T09:05:00Z',.08),
    ('D03','B','2025-12-31','2026-01-02T09:30:00Z',.04),
    ('D04','B','2025-12-31','2026-01-02T10:00:00Z',.04),
    ('D05','A','2026-01-02','2026-01-03T09:15:00Z',-.02),
    ('D06','B','2026-01-02','2026-01-03T09:15:00Z',-.04),
    ('D07','A','2026-01-02','2026-01-03T10:00:00Z',-.02),
    ('D08','C','2025-12-31','2026-01-02T10:00:00Z',.06),
    ('D09','D','2025-12-31','2026-01-02T10:00:00Z',.07),
    ('D10','A','2025-12-31','2026-01-06T10:00:00Z',.08),
]]
COMMON=['D02','D04','D05','D06','D07','D10']
HISTORICAL=[[],['R01'],[],['R03'],['R05'],['R07'],['R05'],[],['R11','R12'],['R02']]
EXACT='f.entity=d.entity AND f.observation_date=d.observation_date'
TIME="f.published_at<=d.cutoff AND f.available_at IS NOT NULL AND f.available_at<=d.cutoff"
SELECTORS={
    'point_in_time':(EXACT+' AND '+TIME,'DENSE_RANK','f.revision DESC'),
    'latest_revision':(EXACT,'ROW_NUMBER','f.revision DESC, f.id DESC'),
    'published_only':(EXACT+' AND f.published_at<=d.cutoff','ROW_NUMBER','f.revision DESC, f.id DESC'),
    'latest_arrival':(EXACT+' AND '+TIME,'ROW_NUMBER','f.available_at DESC, f.id DESC'),
    'unscoped_arrival':('f.entity=d.entity AND '+TIME,'ROW_NUMBER','f.available_at DESC, f.id DESC'),
    'observation_date_asof':('f.entity=d.entity AND f.observation_date<=substr(d.cutoff,1,10)','ROW_NUMBER','f.observation_date DESC, f.revision DESC, f.id DESC'),
}


def reference(name,decision):
    candidates=[r for r in FEATURES if r['entity']==decision['entity']]
    if name=='observation_date_asof':
        candidates=[r for r in candidates if r['observation_date']<=decision['cutoff'][:10]]
    elif name!='unscoped_arrival':
        candidates=[r for r in candidates if r['observation_date']==decision['observation_date']]
    if name in ['point_in_time','published_only','latest_arrival','unscoped_arrival']:
        candidates=[r for r in candidates if r['published_at']<=decision['cutoff']]
    if name in ['point_in_time','latest_arrival','unscoped_arrival']:
        candidates=[r for r in candidates if r['available_at'] is not None and r['available_at']<=decision['cutoff']]
    if not candidates:return []
    if name=='point_in_time':
        revision=max(r['revision'] for r in candidates)
        return sorted(r['id'] for r in candidates if r['revision']==revision)
    key=(lambda r:(r['observation_date'],r['revision'],r['id'])) if name=='observation_date_asof' else ((lambda r:(r['available_at'],r['id'])) if name in ['latest_arrival','unscoped_arrival'] else (lambda r:(r['revision'],r['id'])))
    return [max(candidates,key=key)['id']]


def describe(decision,ids,expected):
    index={r['id']:r for r in FEATURES}
    unknown=any(r['entity']==decision['entity'] and r['observation_date']==decision['observation_date'] and r['published_at']<=decision['cutoff'] and r['available_at'] is None for r in FEATURES)
    state='selected' if len(ids)==1 else ('ambiguous' if len(ids)>1 else ('unknown_availability' if unknown else 'unavailable'))
    violations=[]
    for identity in ids:
        r=index[identity]
        if r['observation_date']!=decision['observation_date']:violations.append({'record':identity,'reason':'wrong_observation_date'})
        if r['published_at']>decision['cutoff']:violations.append({'record':identity,'reason':'published_after_cutoff'})
        if r['available_at'] is None:violations.append({'record':identity,'reason':'unknown_local_availability'})
        elif r['available_at']>decision['cutoff']:violations.append({'record':identity,'reason':'available_after_cutoff'})
        if len(expected)==1 and r['entity']==decision['entity'] and r['observation_date']==decision['observation_date'] and r['revision']<index[expected[0]]['revision']:
            violations.append({'record':identity,'reason':'older_than_selected_eligible_revision'})
    if len(expected)>1 and len(ids)==1:violations.append({'record':ids[0],'reason':'unapproved_conflict_resolution'})
    value=index[ids[0]]['value'] if len(ids)==1 else None
    return {'decision_id':decision['id'],'selected_record_ids':ids,'selection_state':state,
            'matches_selected_history':ids==expected,'policy_violations':violations,
            'prediction':value,'outcome':decision['outcome'],
            'absolute_error':None if value is None else abs(value-decision['outcome'])}


def metric(rows,expected_ids):
    chosen=[r for r in rows if r['decision_id'] in expected_ids]
    available=[r for r in chosen if r['absolute_error'] is not None]
    total=sum(r['absolute_error'] for r in available)
    return {'expected_decisions':len(expected_ids),'evaluated_decisions':len(available),
            'decision_ids':[r['decision_id'] for r in available],
            'unavailable_decision_ids':[r['decision_id'] for r in chosen if r['absolute_error'] is None],
            'absolute_error_sum':total,'mean_absolute_error':None if not available else total/len(available),
            'evaluated_inputs_meet_selected_history':all(r['matches_selected_history'] and not r['policy_violations'] for r in available)}


def measure():
    start=time.monotonic();connection=sqlite3.connect(':memory:')
    connection.executescript('CREATE TABLE features(id TEXT,entity TEXT,observation_date TEXT,revision INTEGER,published_at TEXT,available_at TEXT,value REAL); CREATE TABLE decisions(id TEXT,entity TEXT,observation_date TEXT,cutoff TEXT);')
    connection.executemany('INSERT INTO features VALUES(?,?,?,?,?,?,?)',[tuple(r[k] for k in FIELDS) for r in FEATURES])
    connection.executemany('INSERT INTO decisions VALUES(?,?,?,?)',[tuple(r[k] for k in ['id','entity','observation_date','cutoff']) for r in DECISIONS])
    results,controls=[],[]
    for name,(condition,ranking,order) in SELECTORS.items():
        sql=f'WITH ranked AS (SELECT d.id AS decision_id,f.id AS record_id,{ranking}() OVER(PARTITION BY d.id ORDER BY {order}) AS rank FROM decisions d JOIN features f ON {condition}) SELECT decision_id,record_id FROM ranked WHERE rank=1 ORDER BY decision_id,record_id'
        pairs=connection.execute(sql).fetchall();rows=[]
        for decision,expected in zip(DECISIONS,HISTORICAL):
            ids=[record for identity,record in pairs if identity==decision['id']]
            controls.append({'selector':name,'decision':decision['id'],'check':'sqlite_python_selection','passed':ids==reference(name,decision)})
            if name=='point_in_time':controls.append({'selector':name,'decision':decision['id'],'check':'prespecified_historical_selection','passed':ids==expected})
            rows.append(describe(decision,ids,expected))
        results.append({'id':name,'sql':sql,'rows':rows,'own_population':metric(rows,[d['id'] for d in DECISIONS]),'common_population':metric(rows,COMMON)})
    controls.append({'check':'all_outcomes_published_after_decision','passed':all(d['outcome_published_at']>d['cutoff'] for d in DECISIONS)})
    controls.append({'check':'common_population_matches_unique_historical_inputs','passed':[d['id'] for d,ids in zip(DECISIONS,HISTORICAL) if len(ids)==1]==COMMON})
    connection.close()
    return {'recorded_at':datetime.now(timezone.utc).isoformat(),'environment':{'python':platform.python_version(),'sqlite':sqlite3.sqlite_version},
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'scope':{'timestamps':'UTC, second precision','eligibility_boundary':'publication and known local availability <= decision cutoff',
                     'identity':['entity','observation_date'],'version_rule':'highest eligible revision; conflicting ties remain ambiguous',
                     'prediction_rule':'uniquely selected dimensionless feature value','expected_decisions':[d['id'] for d in DECISIONS],
                     'common_decisions':COMMON,'outcomes':'synthetic; later than all decision cutoffs; corrected feature values deliberately equal outcomes',
                     'financial_operations':False},
            'features':FEATURES,'decisions':DECISIONS,'prespecified_historical_ids':HISTORICAL,
            'selectors':results,'controls':controls,'all_controls_passed':all(r['passed'] for r in controls),
            'calculation_seconds':time.monotonic()-start}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('output',type=Path);args=parser.parse_args()
    if args.output.exists():parser.error('Output exists; preserve prior evidence')
    result=measure()
    with args.output.open('x') as file:json.dump(result,file,indent=2,allow_nan=False);file.write('\n')
    print(json.dumps({'all_controls_passed':result['all_controls_passed'],'controls':len(result['controls']),'selectors':len(result['selectors']),'selection_rows':sum(len(r['rows']) for r in result['selectors']),'calculation_seconds':result['calculation_seconds']}))
    raise SystemExit(0 if result['all_controls_passed'] else 1)
