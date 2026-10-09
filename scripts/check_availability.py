"""Fixed historical-input packets and audit distinctions; no query or model call."""
import copy
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/'examples/availability-review'
NAMES=['point_in_time','latest_revision','published_only','latest_arrival','unscoped_arrival','observation_date_asof']
DECISIONS=[f'D{i:02}' for i in range(1,11)]
COMMON=['D02','D04','D05','D06','D07','D10']
STATES=['supported','breached','unavailable','ambiguous','unresolved']


def instant(value):
    result=datetime.fromisoformat(value.replace('Z','+00:00'))
    assert result.utcoffset().total_seconds()==0
    return result


def close(actual,expected):
    assert isinstance(actual,(int,float)) and not isinstance(actual,bool)
    assert math.isfinite(actual) and math.isclose(actual,expected,rel_tol=1e-12,abs_tol=1e-14),(actual,expected)


def audit_selection(row,decision,features):
    index={f['id']:f for f in features};cutoff=instant(decision['cutoff'])
    matching=[f for f in features if f['entity']==decision['entity'] and f['observation_date']==decision['observation_date']]
    published=[f for f in matching if instant(f['published_at'])<=cutoff]
    eligible=[f for f in published if f['available_at'] is not None and instant(f['available_at'])<=cutoff]
    unknown=[f for f in published if f['available_at'] is None]
    maximum=max((f['revision'] for f in eligible),default=None)
    top=sorted(f['id'] for f in eligible if f['revision']==maximum)
    ids=row['selected_record_ids'];violations=[]
    for identity in ids:
        f=index[identity]
        same_key=f['entity']==decision['entity'] and f['observation_date']==decision['observation_date']
        if not same_key:violations.append('wrong input identity')
        if instant(f['published_at'])>cutoff:violations.append('future publication')
        if f['available_at'] is not None and instant(f['available_at'])>cutoff:violations.append('future local availability')
        if same_key and maximum is not None and f['revision']<maximum:violations.append('older than eligible revision')
    if len(ids)==1 and ids[0] in top and len(top)>1:violations.append('unapproved conflict resolution')
    if violations:return {'state':'breached','reasons':sorted(set(violations))}
    if not ids:
        if eligible:return {'state':'breached','reasons':['eligible input omitted']}
        return {'state':'unresolved' if unknown else 'unavailable','reasons':['unknown local availability'] if unknown else ['no eligible input in supplied history']}
    version=max(index[identity]['revision'] for identity in ids)
    if any(index[identity]['available_at'] is None for identity in ids) or any(f['revision']>=version for f in unknown):
        return {'state':'unresolved','reasons':['missing timing evidence for selected or competing revision']}
    if sorted(ids)==top:
        return {'state':'ambiguous' if len(top)>1 else 'supported','reasons':['conflicting highest revision retained'] if len(top)>1 else []}
    return {'state':'breached','reasons':['selection does not preserve highest eligible revision']}


def inspect(packet,source_sha):
    assert packet['subject']=='AVAILABILITY-2026-10-06' and packet['source_sha256']==source_sha
    assert packet['case'] in ['complete','missing-history','contradictory']
    scope=packet['scope']
    assert scope['expected_decisions']==DECISIONS and scope['common_decisions']==COMMON
    assert scope['identity']==['entity','observation_date'] and scope['timestamps']=='UTC, second precision'
    assert scope['eligibility_boundary']=='publication and known local availability <= decision cutoff'
    assert scope['version_rule']=='highest eligible revision; conflicting ties remain ambiguous'
    assert scope['prediction_rule']=='uniquely selected dimensionless feature value' and scope['financial_operations'] is False
    features=packet['features'];decisions=packet['decisions']
    assert [f['id'] for f in features]==[f'R{i:02}' for i in range(1,14)]
    assert [d['id'] for d in decisions]==DECISIONS
    assert [f['id'] for f in features if f['available_at'] is None]==(['R05','R10'] if packet['case']=='missing-history' else ['R10'])
    for feature in features:
        publication=instant(feature['published_at']);assert datetime.fromisoformat(feature['observation_date']).date()<=publication.date()
        if feature['available_at'] is not None:assert instant(feature['available_at'])>=publication
    for decision in decisions:assert instant(decision['outcome_published_at'])>instant(decision['cutoff'])
    index={f['id']:f for f in features}
    assert [s['id'] for s in packet['selectors']]==NAMES
    findings={}
    for selector in packet['selectors']:
        rows=selector['rows'];assert [r['decision_id'] for r in rows]==DECISIONS
        assert 'sql' not in selector
        audit=[]
        for row,decision in zip(rows,decisions):
            assert 'policy_violations' not in row and 'matches_selected_history' not in row
            ids=row['selected_record_ids'];assert len(ids)==len(set(ids)) and all(i in index for i in ids)
            close(row['outcome'],decision['outcome'])
            if len(ids)==1:
                assert row['selection_state']=='selected'
                close(row['prediction'],index[ids[0]]['value']);close(row['absolute_error'],abs(row['prediction']-decision['outcome']))
            else:
                assert row['prediction'] is None and row['absolute_error'] is None
                assert row['selection_state']==('ambiguous' if len(ids)>1 else ('unknown_availability' if decision['id']=='D08' else 'unavailable'))
            audit.append({'decision_id':decision['id'],**audit_selection(row,decision,features)})
        for key,requested in [('own_population',DECISIONS),('common_population',COMMON)]:
            metric=selector[key];assert 'evaluated_inputs_meet_selected_history' not in metric
            selected=[r for r in rows if r['decision_id'] in requested];numeric=[r for r in selected if r['prediction'] is not None]
            assert metric['expected_decisions']==len(requested) and metric['evaluated_decisions']==len(numeric)
            assert metric['decision_ids']==[r['decision_id'] for r in numeric]
            assert metric['unavailable_decision_ids']==[r['decision_id'] for r in selected if r['prediction'] is None]
            total=sum(abs(r['prediction']-r['outcome']) for r in numeric)
            close(metric['absolute_error_sum'],total);close(metric['mean_absolute_error'],total/len(numeric))
        findings[selector['id']]={'rows':audit,'counts':{state:sum(r['state']==state for r in audit) for state in STATES}}
    claims=packet['producer_claims']
    if packet['case']=='contradictory':
        assert [c['id'] for c in claims]==[f'C{i}' for i in range(1,7)]
        assert [c['selector'] for c in claims]==['latest_revision','published_only','published_only','latest_arrival','unscoped_arrival','latest_revision']
        assert all(isinstance(c['text'],str) and c['text'] for c in claims)
    else:assert claims==[]
    return findings


def require_reference_findings(packet,source_sha):
    findings=inspect(packet,source_sha)
    expected={
        'point_in_time':[6,0,2,1,1], 'latest_revision':[1,8,0,0,1],
        'published_only':[5,4,0,0,1], 'latest_arrival':[5,2,2,0,1],
        'unscoped_arrival':[4,3,2,0,1], 'observation_date_asof':[0,9,0,0,1],
    }
    if packet['case']=='missing-history':
        expected.update({'point_in_time':[4,0,2,1,3],'published_only':[3,4,0,0,3],'latest_arrival':[3,2,2,0,3],'unscoped_arrival':[3,3,2,0,2]})
    for name,counts in expected.items():assert list(findings[name]['counts'].values())==counts,(name,findings[name]['counts'],counts)
    return findings


def adverse_checks(packets,source_sha):
    changes=[
        ('complete','future input accepted',lambda p:p['selectors'][0]['rows'][1].__setitem__('selected_record_ids',['R02'])),
        ('complete','unknown availability invented',lambda p:p['features'][9].__setitem__('available_at','2026-01-02T09:00:00Z')),
        ('complete','missing decision',lambda p:p['selectors'][0]['rows'].pop()),
        ('complete','omitted selector',lambda p:p['selectors'].pop()),
        ('complete','wrong denominator',lambda p:p['selectors'][0]['own_population'].__setitem__('evaluated_decisions',10)),
        ('complete','common population changed',lambda p:p['scope']['common_decisions'].pop()),
        ('complete','wrong predicted value',lambda p:p['selectors'][0]['rows'][1].__setitem__('prediction',.08)),
        ('complete','wrong error',lambda p:p['selectors'][0]['rows'][1].__setitem__('absolute_error',0.0)),
        ('complete','future receipt backdated',lambda p:p['features'][12].__setitem__('available_at','2026-01-02T09:00:00Z')),
        ('complete','older revision promoted',lambda p:p['features'][12].__setitem__('revision',3)),
        ('missing-history','withheld timing restored',lambda p:p['features'][4].__setitem__('available_at','2026-01-03T09:05:00Z')),
        ('contradictory','claim omitted',lambda p:p['producer_claims'].pop()),
    ]
    for case,name,change in changes:
        candidate=copy.deepcopy(packets[case]);change(candidate)
        try:require_reference_findings(candidate,source_sha)
        except (AssertionError,KeyError,ValueError,TypeError,IndexError):pass
        else:raise AssertionError('Accepted mutation: '+name)
    # At an inclusive boundary, publication and availability at the cutoff are eligible.
    row=packets['complete']['selectors'][0]['rows'][1];decision=packets['complete']['decisions'][1]
    assert audit_selection(row,decision,packets['complete']['features'])['state']=='supported'
    # Equal values on another receipt cannot clear a selected future receipt.
    row=packets['complete']['selectors'][2]['rows'][1]
    assert audit_selection(row,decision,packets['complete']['features'])['state']=='breached'
    return len(changes)


if __name__=='__main__':
    digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    receipt=json.loads((ROOT/'receipt.json').read_text());source_sha=digest(ROOT/'model/measure.py')
    assert receipt['source_sha256']==source_sha
    packets={case:json.loads((ROOT/'inputs'/f'{case}.json').read_text()) for case in ['complete','missing-history','contradictory']}
    summary={}
    for case,packet in packets.items():
        assert packet['case']==case
        assert digest(ROOT/receipt['packets'][case]['path'])==receipt['packets'][case]['sha256']
        findings=require_reference_findings(packet,source_sha)
        summary[case]={name:f['counts'] for name,f in findings.items()}
    print(json.dumps({'cases':summary,'mutations_rejected':adverse_checks(packets,source_sha),'new_queries_or_provider_calls':0},indent=2))
