"""Fixed exposure-packet controls without SQL execution or arbitrary prose assessment."""
import copy
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/'examples/exposure-review'
MODES=['selected_sets','counterparty_pool','global_pool','omit_haircuts','include_pending',
       'include_ineligible','invert_fx','join_before_aggregation','floor_trades_first']
FIELDS=['trade_value_usd','recognized_collateral_usd','current_exposure_usd','trade_rows','collateral_rows']
SCOPE={'as_of':'2026-10-06T00:00:00Z','reporting_currency':'USD','usd_per_eur':'11/10',
       'positive_trade_sign':'asset to reporting bank','collateral':'received only; exclusive set allocation',
       'legal_recognition':'stipulated synthetic set boundaries, not a legal determination',
       'selected_measure':'sum over netting sets of max(signed trade value - recognized collateral, 0)',
       'future_exposure_included':False,'regulatory_ead':False,'amount_tolerance_usd':1e-6}
CLAIMS=[
    'Pooling all positions is valid because every individual amount and the final sum are arithmetically correct.',
    'A common counterparty automatically makes separate netting sets interchangeable.',
    'Pending or ineligible collateral can offset exposure whenever its recorded market value is positive.',
    'Higher exposure from a different construction automatically conforms to the selected method.',
    'A calculation that uses an eligible flag proves that eligibility is the intended requirement and an established institutional fact.',
    'These current-exposure calculations establish regulatory EAD, actual legal enforceability and approval to move collateral.',
]


def close(actual,expected,tolerance=1e-6):
    assert type(actual) in (int,float) and math.isfinite(actual)
    assert abs(actual-expected)<=tolerance,(actual,expected)


def reference(inputs,mode):
    sets={row['id']:row['counterparty'] for row in inputs['netting_sets']}
    keys=sorted(set(sets.values())) if mode=='counterparty_pool' else (['ALL'] if mode=='global_pool' else sorted(sets))
    rows=[]
    for key in keys:
        members=[s for s,c in sets.items() if key in ('ALL',s,c)]
        trades=[r for r in inputs['trades'] if r['netting_set'] in members]
        collateral=[r for r in inputs['collateral'] if r['netting_set'] in members]
        def fx(currency):
            assert currency in ('USD','EUR')
            return F(1) if currency=='USD' else (F(10,11) if mode=='invert_fx' else F(11,10))
        values=[r['signed_value']*fx(r['currency']) for r in trades]
        if mode=='floor_trades_first':values=[max(v,0) for v in values]
        v=sum(values);c=F(0)
        for r in collateral:
            assert type(r['settled']) is bool and type(r['eligible']) is bool
            if (r['settled'] or mode=='include_pending') and (r['eligible'] or mode=='include_ineligible'):
                c+=r['market_value']*fx(r['currency'])*(1 if mode=='omit_haircuts' else 1-F(r['haircut']))
        nt,nc=len(trades),len(collateral)
        if mode=='join_before_aggregation':v,c,nt,nc=v*nc,c*nt,nt*nc,nt*nc
        rows.append({'group_id':key,'trade_value_usd':v,'recognized_collateral_usd':c,
                     'current_exposure_usd':max(v-c,0),'trade_rows':nt,'collateral_rows':nc})
    return rows


def supported_state(actual,possibilities,tolerance):
    matches=[abs(float(actual)-float(p))<=tolerance for p in possibilities]
    return 'met' if all(matches) else ('unresolved' if any(matches) else 'breached')


def combine(states):
    return 'breached' if 'breached' in states else ('unresolved' if 'unresolved' in states else 'met')


def findings(packet):
    selected=packet['selected_method']['inputs']
    unknown=[r['id'] for r in selected['collateral'] if r['eligible'] is None]
    assert unknown in ([],['C2'])
    alternatives=[]
    for choice in ([False,True] if unknown else [None]):
        concrete=copy.deepcopy(selected)
        if unknown:next(r for r in concrete['collateral'] if r['id']=='C2')['eligible']=choice
        alternatives.append(reference(concrete,'selected_sets'))
    totals=[sum(r['current_exposure_usd'] for r in rows) for rows in alternatives]
    reports=[]
    for construction in packet['constructions']:
        rows=construction['native_rows']
        grouping=[r['group_id'] for r in rows]==[r['group_id'] for r in alternatives[0]]
        details=[]
        if grouping:
            for i,row in enumerate(rows):
                states={field:supported_state(row[field],[a[i][field] for a in alternatives],
                                               0 if field.endswith('_rows') else 1e-6) for field in FIELDS}
                details.append({'group_id':row['group_id'],'criteria':states,'state':combine(states.values())})
        total_state=supported_state(construction['native_total_usd'],totals,1e-6)
        reports.append({'id':construction['id'],'grouping':'met' if grouping else 'breached',
                        'groups':details,'total_comparison':total_state,
                        'state':combine(['met' if grouping else 'breached',total_state]+[r['state'] for r in details])})
    return {'missing_selected_eligibility':unknown,
            'selected_total_usd':None if unknown else float(totals[0]),
            'conditional_totals_usd':[float(v) for v in totals],
            'conditional_eligibility_order':[False,True] if unknown else [],'constructions':reports}


def verify(packet,source_hash):
    assert packet['subject']=='EXPOSURE-2026-10-06'
    case=packet['case'];assert case in ['complete','missing-eligibility','contradictory']
    assert packet['source_sha256']==source_hash
    assert packet['selected_method']['scope']==SCOPE
    actual=packet['observed_calculation_inputs'];selected=packet['selected_method']['inputs']
    assert actual['netting_sets']==[{'id':'NS-A1','counterparty':'CP-A'},{'id':'NS-A2','counterparty':'CP-A'},{'id':'NS-B1','counterparty':'CP-B'}]
    assert [r['id'] for r in actual['trades']]==[f'T{i}' for i in range(1,7)]
    assert [r['id'] for r in actual['collateral']]==[f'C{i}' for i in range(1,7)]
    assert [(r['netting_set'],r['currency'],r['signed_value']) for r in actual['trades']]==[
        ('NS-A1','USD',1000000),('NS-A1','EUR',-600000),('NS-A2','USD',-400000),
        ('NS-A2','USD',100000),('NS-B1','USD',500000),('NS-B1','EUR',200000)]
    assert [(r['netting_set'],r['currency'],r['market_value'],r['haircut'],r['settled'],r['eligible']) for r in actual['collateral']]==[
        ('NS-A1','USD',100000,'0',True,True),('NS-A1','EUR',100000,'1/10',True,True),
        ('NS-A1','USD',80000,'0',False,True),('NS-A2','USD',200000,'0',True,True),
        ('NS-B1','USD',250000,'1/20',True,True),('NS-B1','USD',300000,'0',True,False)]
    expected_selected=copy.deepcopy(actual)
    if case=='missing-eligibility':expected_selected['collateral'][1]['eligible']=None
    assert selected==expected_selected
    assert packet['scope_measures']=={'signed_trade_total_usd':'760000','positive_individual_trade_total_usd':'1820000',
                                      'positive_unsecured_net_set_total_usd':'1060000'}
    assert [r['id'] for r in packet['constructions']]==MODES
    for construction in packet['constructions']:
        expected=reference(actual,construction['id'])
        assert len(construction['native_rows'])==len(construction['exact_reference_rows'])==len(expected)
        for native,exact,row in zip(construction['native_rows'],construction['exact_reference_rows'],expected):
            assert native['group_id']==exact['group_id']==row['group_id']
            for field in FIELDS:
                if field.endswith('_rows'):assert native[field]==exact[field]==row[field]
                else:
                    assert F(exact[field])==row[field]
                    close(native[field],float(row[field]))
            close(native['current_exposure_usd'],max(native['trade_value_usd']-native['recognized_collateral_usd'],0))
        total=sum(r['current_exposure_usd'] for r in expected)
        assert F(construction['exact_total_usd'])==total
        close(construction['native_total_usd'],float(total))
        assert F(construction['difference_from_selected_sets_construction_usd'])==total-623500
    expected_claims=[{'id':f'C{i+1}','text':t} for i,t in enumerate(CLAIMS)] if case=='contradictory' else []
    assert packet['producer_claims']==expected_claims
    result=findings(packet)
    assert [r['state'] for r in result['constructions']]==[('unresolved' if case=='missing-eligibility' else 'met')]+['breached']*8
    if case=='missing-eligibility':
        assert result['selected_total_usd'] is None
        assert result['conditional_totals_usd']==[722500.0,623500.0]
        assert result['constructions'][0]['groups'][0]['criteria']['trade_value_usd']=='met'
        assert result['constructions'][0]['groups'][0]['criteria']['recognized_collateral_usd']=='unresolved'
        assert [r['state'] for r in result['constructions'][0]['groups']]==['unresolved','met','met']
    else:assert result['selected_total_usd']==623500.0
    return result


def main():
    digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    receipt=json.loads((ROOT/'receipt.json').read_text());source_hash=digest(ROOT/'model/measure.py')
    assert receipt['source_sha256']==source_hash and receipt['plan_sha256']==digest(ROOT/'model/README.md')
    packets={}
    for case in ['complete','missing-eligibility','contradictory']:
        path=ROOT/'inputs'/f'{case}.json'
        assert receipt['packets'][case]=={'path':f'inputs/{case}.json','sha256':digest(path)}
        packets[case]=json.loads(path.read_text());verify(packets[case],source_hash)
    missing=copy.deepcopy(packets['complete']);missing['case']='missing-eligibility';missing['selected_method']['inputs']['collateral'][1]['eligible']=None
    assert missing==packets['missing-eligibility']
    contradictory=copy.deepcopy(packets['complete']);contradictory['case']='contradictory';contradictory['producer_claims']=packets['contradictory']['producer_claims']
    assert contradictory==packets['contradictory']
    mutations=[]
    def reject(label,case,change):
        altered=copy.deepcopy(packets[case]);change(altered)
        try:verify(altered,source_hash)
        except (AssertionError,KeyError,TypeError,ValueError):mutations.append(label)
        else:raise AssertionError('Undetected mutation: '+label)
    reject('drop_construction','complete',lambda p:p['constructions'].pop())
    reject('drop_trade','complete',lambda p:p['observed_calculation_inputs']['trades'].pop())
    reject('duplicate_collateral','complete',lambda p:p['observed_calculation_inputs']['collateral'].append(copy.deepcopy(p['observed_calculation_inputs']['collateral'][0])))
    reject('change_scope','complete',lambda p:p['selected_method']['scope'].update(usd_per_eur='10/11'))
    reject('wrong_selected_membership','complete',lambda p:p['selected_method']['inputs']['trades'][2].update(netting_set='NS-A1'))
    reject('recognize_pending','complete',lambda p:p['observed_calculation_inputs']['collateral'][2].update(settled=True))
    reject('recognize_ineligible','complete',lambda p:p['observed_calculation_inputs']['collateral'][5].update(eligible=True))
    reject('hide_join_multiplicity','complete',lambda p:p['constructions'][7]['native_rows'][0].update(trade_rows=2))
    reject('compensating_values','complete',lambda p:p['constructions'][0]['native_rows'][0].update(trade_value_usd=340010,recognized_collateral_usd=199010))
    reject('changed_total','complete',lambda p:p['constructions'][0].update(native_total_usd=123500))
    reject('selected_filled_from_actual','missing-eligibility',lambda p:p['selected_method']['inputs']['collateral'][1].update(eligible=True))
    reject('missing_means_ineligible','missing-eligibility',lambda p:p['selected_method']['inputs']['collateral'][1].update(eligible=False))
    reject('erase_actual_with_selected','missing-eligibility',lambda p:p['observed_calculation_inputs']['collateral'][1].update(eligible=None))
    reject('erase_other_binding','missing-eligibility',lambda p:p['selected_method']['inputs']['collateral'][4].update(eligible=None))
    reject('relabel_regulatory','complete',lambda p:p['selected_method']['scope'].update(regulatory_ead=True))
    reject('missing_producer_claim','contradictory',lambda p:p['producer_claims'].pop())
    reject('wrong_source','complete',lambda p:p.update(source_sha256='0'*64))
    assert supported_state(1e-6,[0],1e-6)=='met'
    assert supported_state(1.000001e-6,[0],1e-6)=='breached'
    assert supported_state(1,[0,1],0)=='unresolved'
    print(json.dumps({'packets':3,'constructions_per_packet':9,'adverse_mutations_rejected':mutations,
                      'boundary_and_unknown_controls':'pass','agent_qualification':False}))


if __name__=='__main__':main()
