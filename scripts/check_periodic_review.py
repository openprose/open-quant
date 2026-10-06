"""Fixed periodic-review house rules over synthetic records; not a prose evaluator."""
import copy
import json
import math
import re
from datetime import date
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FIELDS=('deployment','model','revision','use','metric')


def scope(row):return tuple(row.get(k) for k in FIELDS)
def day(value):
    try:return date.fromisoformat(value)
    except (ValueError,TypeError):return None


def review(packet):
    assert packet['synthetic'] is True and packet['case'] in ['complete','missing-baseline','contradictory']
    for collection in ['deployments','register','expected_observations','observations','issues','review_records','changes']:
        assert len({r['id'] for r in packet[collection]})==len(packet[collection]),collection+' duplicate IDs'
    today=day(packet['review_date']);assert today is not None
    period=packet['reporting_period']
    included=[d for d in packet['deployments'] if d['environment']=='production']
    excluded=[d['id'] for d in packet['deployments'] if d['environment']!='production']
    assert len(included)==3 and len(packet['expected_observations'])==3
    deployment={d['id']:d for d in included}
    inventory=[]
    for d in included:
        matches=[r for r in packet['register'] if r['deployment']==d['id']]
        differences=[]
        if not matches:status='missing'
        elif len(matches)>1:status='ambiguous'
        else:
            differences=[k for k in ['model','revision','use','owner'] if matches[0].get(k)!=d.get(k)]
            if matches[0].get('lifecycle')!='production':differences.append('lifecycle')
            status='conflict' if differences else 'matched'
        inventory.append({'deployment':d['id'],'records':[r['id'] for r in matches],'status':status,'conflicting_fields':differences})
    unmatched_register=[r['id'] for r in packet['register'] if r['deployment'] not in deployment]
    retired={e['deployment'] for e in packet['lifecycle_events'] if e['event']=='retired' and day(e['effective']) is not None and day(e['effective'])<=today}
    retirement_conflicts=[r['id'] for r in packet['register'] if r['deployment'] in retired and r['lifecycle']=='production']

    def value_finding(obs,expected):
        observed=day(obs.get('date'))
        if scope(obs)!=scope(expected) or obs.get('period')!=expected['period']:return 'unresolved'
        if observed is None or observed.strftime('%Y-%m')!=period or observed>today:return 'unresolved'
        value=obs.get('value')
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or value<0 or obs.get('unit')!=expected['unit']:return 'unresolved'
        return 'within limit' if value<=expected['upper_limit'] else 'breach'

    observations=[];matched_ids=set()
    for e in packet['expected_observations']:
        assert e['deployment'] in deployment
        assert all(e[k]==deployment[e['deployment']][k] for k in ['model','revision','use'])
        assert e['period']==period
        matches=[o for o in packet['observations'] if scope(o)==scope(e) and o.get('period')==e['period']]
        matched_ids.update(o['id'] for o in matches)
        status=value_finding(matches[0],e) if len(matches)==1 else 'unresolved'
        observations.append({'expected':e['id'],'records':[o['id'] for o in matches],'status':status,
                             'contradictory_label':len(matches)==1 and status!='unresolved' and matches[0].get('producer_status')!=status})
    counts={status:sum(r['status']==status for r in observations) for status in ['within limit','breach','unresolved']}
    overall='breach' if counts['breach'] else 'unresolved' if counts['unresolved'] else 'within limit'
    unmatched_observations=[o['id'] for o in packet['observations'] if o['id'] not in matched_ids]
    issues=[]
    for issue in packet['issues']:
        expected=[e for e in packet['expected_observations'] if scope(e)==scope(issue)]
        obs=[o for o in packet['observations'] if o['id']==issue.get('closure_observation')]
        reviews=[r for r in packet['review_records'] if r['id']==issue.get('review_record')]
        action_date=day(issue.get('action_complete'))
        observation_ok=len(expected)==len(obs)==1 and value_finding(obs[0],expected[0])=='within limit' and action_date is not None and day(obs[0]['date'])>action_date
        review_ok=False
        if len(reviews)==len(obs)==1:
            rv=reviews[0];rv_date=day(rv.get('date'));obs_date=day(obs[0].get('date'))
            review_ok=scope(rv)==scope(issue) and rv.get('observation')==obs[0]['id'] and rv.get('accepted') is True and rv_date is not None and obs_date is not None and obs_date<=rv_date<=today
        supported=bool(observation_ok and review_ok)
        due=day(issue.get('due'))
        issues.append({'issue':issue['id'],'owner':issue['owner'],'observation_supports_closure':bool(observation_ok),
                       'review_supports_scope':bool(review_ok),'closure_supported':supported,
                       'overdue':None if due is None else due<today and not supported})
    changes=[]
    for change in packet['changes']:
        current=deployment.get(change['deployment']);before=change.get('before');after=change.get('after')
        if current is None or not isinstance(after,dict) or any(after.get(k)!=current[k] for k in ['model','revision','use']):
            status='current-state conflict'
        elif not isinstance(before,dict) or any(not before.get(k) for k in ['model','revision','use']):status='unresolved history'
        elif any(before[k]!=after[k] for k in ['revision','use']):status='further review required'
        elif before['model']!=after['model']:status='unresolved identity change'
        else:status='no revision or use change observed'
        changes.append({'change':change['id'],'status':status})
    return {'included':[r['id'] for r in included],'excluded':excluded,'inventory':inventory,
            'unmatched_register':unmatched_register,'retirement_conflicts':retirement_conflicts,
            'observations':observations,'counts':counts,'denominator':3,'overall_monitoring':overall,
            'unmatched_observations':unmatched_observations,'issues':issues,'changes':changes}


def reference_errors(text, packet):
    """Bind selected cells and issue scopes in this authored reference only."""
    errors=[]
    rows={}
    for line in text.splitlines():
        if re.match(r'^\| E[0-9]+:',line):
            cells=[cell.strip() for cell in line.split('|')[1:-1]]
            identifier=cells[0].split(':')[0]
            if identifier in rows:errors.append('duplicate reference row '+identifier)
            rows[identifier]=cells
    expected=packet['expected_observations']
    if set(rows)!={row['id'] for row in expected}:errors.append('reference observation population')
    for row in expected:
        cells=rows.get(row['id'],[])
        if len(cells)!=5:
            errors.append('reference cell population '+row['id']);continue
        if cells[0]!=f"{row['id']}: {row['deployment']} {row['use']}":errors.append('reference scope '+row['id'])
        if f"`{row['metric']}`" not in cells[1]:errors.append('reference metric '+row['id'])
        if cells[3]!=f"≤ {row['upper_limit']:g} {row['unit']}":errors.append('reference limit '+row['id'])
        matches=[obs for obs in packet['observations'] if scope(obs)==scope(row) and obs['period']==row['period']]
        if len(matches)==1:
            obs=matches[0]
            if cells[2]!=f"{obs['id']}: {obs['value']:g} {obs['unit']}, {obs['date']}":errors.append('reference value/date '+row['id'])
        elif cells[2]!='No matching observation':errors.append('reference evidence gap '+row['id'])
    for issue in packet['issues']:
        paragraphs=[part for part in text.split('\n\n') if part.startswith(issue['id']+' concerns ')]
        if len(paragraphs)!=1 or any(value not in paragraphs[0] for value in [
            issue['deployment'],issue['model']+' '+issue['revision'],issue['use']+' use',
            '`'+issue['metric']+'`',issue['owner']]):errors.append('reference issue scope '+issue['id'])
    return errors


def main():
    packets={case:json.loads((ROOT/'examples/periodic-review/inputs'/f'{case}.json').read_text()) for case in ['complete','missing-baseline','contradictory']}
    results={case:review(p) for case,p in packets.items()}
    for case,r in results.items():
        assert r['included']==['D1','D2','D3'] and r['excluded']==['D4']
        assert [x['status'] for x in r['inventory']]==(['ambiguous','conflict','conflict'] if case=='contradictory' else ['matched','conflict','conflict'])
        assert r['inventory'][1]['conflicting_fields']==['use'] and r['inventory'][2]['conflicting_fields']==['revision']
        assert r['unmatched_register']==r['retirement_conflicts']==['R4']
        assert r['counts']=={'within limit':1,'breach':1,'unresolved':1} and r['overall_monitoring']=='breach'
        assert r['unmatched_observations']==['O2'] and r['observations'][1]['records']==[]
        assert [i['closure_supported'] for i in r['issues']]==[False,False]
        assert [i['overdue'] for i in r['issues']]==[True,False]
        assert [c['status'] for c in r['changes']]==(['unresolved history','further review required'] if case=='missing-baseline' else ['further review required']*2)
    checks=[]
    def control(name,mutate,check):
        p=copy.deepcopy(packets['complete']);mutate(p);r=review(p);assert check(r),name;checks.append(name)
    control('threshold equality',lambda p:p['observations'][0].update(value=1),lambda r:r['observations'][0]['status']=='within limit')
    control('threshold breach',lambda p:p['observations'][0].update(value=1.001),lambda r:r['observations'][0]['status']=='breach')
    for value in [None,'0',False,-.1,float('nan')]:
        control('invalid value '+repr(value),lambda p,v=value:p['observations'][0].update(value=v),lambda r:r['observations'][0]['status']=='unresolved')
    control('unit mismatch',lambda p:p['observations'][0].update(unit='percent'),lambda r:r['observations'][0]['status']=='unresolved')
    control('stale observation',lambda p:p['observations'][0].update(date='2026-08-31'),lambda r:r['observations'][0]['status']=='unresolved')
    control('future observation',lambda p:p['observations'][0].update(date='2026-10-06'),lambda r:r['observations'][0]['status']=='unresolved')
    control('missing observation',lambda p:p['observations'].pop(0),lambda r:r['denominator']==3 and r['counts']['unresolved']==2)
    control('conflicting duplicate',lambda p:p['observations'].append(dict(p['observations'][0],id='O4',value=2)),lambda r:r['observations'][0]['status']=='unresolved')
    control('producer label false',lambda p:p['observations'][2].update(producer_status='within limit'),lambda r:r['observations'][2]['contradictory_label'] and r['overall_monitoring']=='breach')
    control('corrected use observation',lambda p:p['observations'][1].update(use='stress'),lambda r:r['counts']['within limit']==2 and not r['issues'][0]['closure_supported'])
    def correct_closure(p):p['observations'][1]['use']='stress';p['review_records'][0]['use']='stress'
    control('fully supported closure',correct_closure,lambda r:r['issues'][0]['closure_supported'] and not r['issues'][0]['overdue'])
    def premature(p):correct_closure(p);p['issues'][0]['action_complete']='2026-09-30'
    control('observation not post action',premature,lambda r:not r['issues'][0]['closure_supported'])
    def future_review(p):correct_closure(p);p['review_records'][0]['date']='2026-10-06'
    control('future review',future_review,lambda r:not r['issues'][0]['closure_supported'])
    def wrong_reference(p):correct_closure(p);p['review_records'][0]['observation']='O1'
    control('wrong accepted observation',wrong_reference,lambda r:not r['issues'][0]['closure_supported'])
    control('due date equality',lambda p:p['issues'][0].update(due='2026-10-05'),lambda r:not r['issues'][0]['overdue'])
    control('missing historical field',lambda p:p['changes'][0]['before'].pop('use'),lambda r:r['changes'][0]['status']=='unresolved history')
    control('wrong after state',lambda p:p['changes'][0]['after'].update(use='pricing'),lambda r:r['changes'][0]['status']=='current-state conflict')
    control('same revision new use',lambda p:None,lambda r:r['changes'][0]['status']=='further review required')
    control('missing register',lambda p:p['register'].pop(0),lambda r:r['inventory'][0]['status']=='missing')
    control('future retirement',lambda p:p['lifecycle_events'][0].update(effective='2026-10-06'),lambda r:r['retirement_conflicts']==[] and r['unmatched_register']==['R4'])
    bad=copy.deepcopy(packets['complete']);bad['observations'].append(bad['observations'][0])
    try:review(bad)
    except AssertionError:checks.append('duplicate record identity rejected')
    else:raise AssertionError('Duplicate identity accepted')
    reference=(ROOT/'examples/periodic-review/sample-results/report.md').read_text()
    assert not reference_errors(reference,packets['complete']),reference_errors(reference,packets['complete'])
    reference_mutations={
        'omit metric':reference.replace('`repricing_error`','`unknown`'),
        'substitute probability for error':reference.replace('`max_calibration_error`','`default_probability`'),
        'change threshold boundary':reference.replace('≤ 1 bp','< 1 bp'),
        'change missing-observation limit':reference.replace('≤ 5 USD million','≤ 4 USD million'),
        'change observation date':reference.replace('O3: 0.03 probability, 2026-09-30','O3: 0.03 probability, 2026-08-31'),
        'change observation value':reference.replace('O1: 0.8 bp','O1: 0.9 bp'),
        'omit issue metric':reference.replace('I1 concerns the stress reference difference (`stress_reference_difference`)','I1 concerns the stress reference difference'),
        'change issue revision':reference.replace('D3, CREDIT-PD r2, origination use','D3, CREDIT-PD r1, origination use'),
    }
    for name,changed in reference_mutations.items():
        assert changed!=reference and reference_errors(changed,packets['complete']),name
    print(json.dumps({'scope':'Fixed synthetic rule mappings and selected authored-reference bindings; no model execution, institutional decision or general prose evaluation.',
                      'cases':results,'controls':checks,'reference_rows':3,'reference_issue_scopes':2,
                      'reference_mutations_rejected':list(reference_mutations)},indent=2))


if __name__=='__main__':main()
