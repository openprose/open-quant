"""Fixed optimization evidence controls, not arbitrary report assessment."""
import copy
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "examples/optimization-review"
COV = [[0.04, 0.002], [0.002, 0.01]]
MU = [0.08, 0.02]
CAPS = [0.7, 0.8]
EXPECTED = [
    ('selected', COV, MU, 0.04, CAPS, 1.0, 100),
    ('omitted_return_constraint', COV, MU, None, CAPS, 1.0, 100),
    ('percent_fraction_mismatch', COV, [8.0, 2.0], 0.04, CAPS, 1.0, 100),
    ('covariance_order_mismatch', [[0.01, 0.002], [0.002, 0.04]], MU, 0.04, CAPS, 1.0, 100),
    ('scaled_objective', COV, MU, 0.04, CAPS, 1e-8, 100),
    ('infeasible_caps', COV, MU, 0.04, [0.4, 0.4], 1.0, 100),
    ('iteration_limit', COV, MU, 0.04, CAPS, 1.0, 1),
]


def close(actual, expected):
    assert isinstance(actual, (int, float)) and not isinstance(actual, bool)
    assert math.isfinite(actual) and math.isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-14), (actual, expected)


def verify_reference(record, covariance, mu, floor, caps):
    a = covariance[0][0] - 2*covariance[0][1] + covariance[1][1]
    b = 2*(covariance[0][1] - covariance[1][1])
    c = covariance[1][1]
    low = max(0, 1-caps[1])
    if floor is not None:
        low = max(low, (floor-mu[1])/(mu[0]-mu[1]))
    high = min(1, caps[0])
    for value, expected in zip(record['feasible_interval'], [low, high]):
        close(value, expected)
    close(record['coefficient_a'], a)
    close(record['coefficient_b'], b)
    close(record['coefficient_c'], c)
    assert record['positive_definite'] is (covariance[0][0] > 0 and covariance[1][1] > 0 and covariance[0][0]*covariance[1][1]-covariance[0][1]**2 > 0)
    assert record['feasible'] is (low <= high)
    if low > high:
        assert record['weights'] is None and record['unscaled_minimum_variance'] is None
        return
    x = min(high, max(low, -b/(2*a)))
    close(record['weights'][0], x)
    close(record['weights'][1], 1-x)
    close(record['unscaled_minimum_variance'], a*x*x+b*x+c)


def verify_diagnostics(row, weights):
    x,y = weights
    required = {
        'full_investment': ('required', 1.0, x+y, abs(x+y-1)),
        'A_nonnegative': ('required_lower', 0.0, x, max(0,-x)),
        'B_nonnegative': ('required_lower', 0.0, y, max(0,-y)),
        'A_cap': ('required_upper', 0.7, x, max(0,x-0.7)),
        'B_cap': ('required_upper', 0.8, y, max(0,y-0.8)),
        'return_floor': ('required_lower', 0.04, .08*x+.02*y, max(0,.04-(.08*x+.02*y))),
    }
    actual=row['selected_problem_diagnostics']
    assert set(actual['constraints'])==set(required)
    for key,(bound_kind,bound,value,violation) in required.items():
        found=actual['constraints'][key]
        close(found[bound_kind],bound)
        close(found['value'],value)
        close(found['violation'],violation)
        assert found['within_tolerance'] is (violation<=1e-10)
    feasible=all(v[3]<=1e-10 for v in required.values())
    objective=.04*x*x+.004*x*y+.01*y*y
    optimum=.04/9+.004*2/9+.01*4/9
    close(actual['variance'],objective)
    close(actual['expected_return'],.08*x+.02*y)
    close(actual['objective_gap'],objective-optimum)
    assert actual['feasible_under_selected_policy'] is feasible
    assert actual['meets_selected_optimum_tolerance'] is (feasible and abs(objective-optimum)<=1e-8)


def inspect(packet, source_sha):
    assert packet['subject']=='OPTIMIZATION-2026-10-06' and packet['source_sha256']==source_sha
    assert packet['case'] in ['complete','missing-candidate','contradictory']
    spec=packet['scope']
    assert spec['position_order']==['A','B'] and spec['weights_unit']=='fraction'
    assert spec['covariance']==COV and spec['covariance_unit']=='annualized fractional-return squared'
    assert spec['expected_returns']==MU and spec['expected_return_unit']=='annualized fraction'
    assert spec['caps']==CAPS and spec['return_floor']==.04 and spec['full_investment']==1.0
    assert spec['feasibility_tolerance']==1e-10 and spec['variance_objective_tolerance']==1e-8
    verify_reference(spec['reference'],COV,MU,.04,CAPS)
    assert [r['id'] for r in packet['records']]==[x[0] for x in EXPECTED]
    findings=[]
    for row,(name,cov,mu,floor,caps,scale,maxiter) in zip(packet['records'],EXPECTED):
        assert row['kind']=='observed_solver_result' and row['position_order']==['A','B']
        assert row['implemented_problem']=={'covariance':cov,'expected_returns':mu,'return_floor':floor,'caps':caps,'objective_scale':scale}
        native=row['solver']
        assert native['method']=='SLSQP' and native['start']==[.5,.5]
        assert native['options']=={'ftol':1e-12,'maxiter':maxiter,'disp':False}
        assert native['success'] is (name not in ['infeasible_caps','iteration_limit'])
        assert native['status']==({'infeasible_caps':4,'iteration_limit':9}.get(name,0))
        assert native['iterations']>=1 and native['function_evaluations']>=1 and native['gradient_evaluations']>=1
        verify_reference(row['implemented_problem_reference'],cov,mu,floor,caps)
        if packet['case']=='missing-candidate' and name=='scaled_objective':
            assert all(native[k] is None for k in ['weights','objective','gradient','multipliers'])
            assert row['selected_problem_diagnostics'] is None
            findings.append({'id':name,'native_success':True,'original_feasibility':'unresolved','original_optimum':'unresolved'})
            continue
        assert len(native['weights'])==2 and len(native['gradient'])==2
        x,y=native['weights']
        close(native['objective'],scale*(cov[0][0]*x*x+2*cov[0][1]*x*y+cov[1][1]*y*y))
        close(native['gradient'][0],2*scale*(cov[0][0]*x+cov[0][1]*y))
        close(native['gradient'][1],2*scale*(cov[0][1]*x+cov[1][1]*y))
        verify_diagnostics(row,native['weights'])
        d=row['selected_problem_diagnostics']
        findings.append({'id':name,'native_success':native['success'],
                         'original_feasibility':'met' if d['feasible_under_selected_policy'] else 'breached',
                         'original_optimum':'met' if d['meets_selected_optimum_tolerance'] else 'not met'})
    assert len(packet['derived_candidates'])==1
    derived=packet['derived_candidates'][0]
    assert derived['id']=='rounded_export' and derived['source_result']=='selected' and derived['solver'] is None
    assert derived['kind']=='derived_weight_artifact' and derived['decimal_places']==3
    assert derived['weights']==[round(v,3) for v in packet['records'][0]['solver']['weights']]
    verify_diagnostics(derived,derived['weights'])
    d=derived['selected_problem_diagnostics']
    findings.append({'id':'rounded_export','native_success':None,
                     'original_feasibility':'met' if d['feasible_under_selected_policy'] else 'breached',
                     'original_optimum':'met' if d['meets_selected_optimum_tolerance'] else 'not met'})
    claims=packet['producer_claims']
    if packet['case']=='contradictory':
        assert [c['id'] for c in claims]==['C1','C2','C3','C4','C5']
        assert [c['applies_to'] for c in claims]==[['omitted_return_constraint','percent_fraction_mismatch'],['covariance_order_mismatch'],['scaled_objective'],['iteration_limit'],['rounded_export']]
        assert all(isinstance(c['text'],str) and c['text'] for c in claims)
    else:assert claims==[]
    return findings


def adverse_checks(packets, source_sha):
    cases=[
        ('complete','wrong variable order',lambda p:p['records'][0].__setitem__('position_order',['B','A'])),
        ('complete','wrong objective',lambda p:p['records'][0]['solver'].__setitem__('objective',0.0)),
        ('complete','false feasibility',lambda p:p['records'][1]['selected_problem_diagnostics'].__setitem__('feasible_under_selected_policy',True)),
        ('complete','false optimality',lambda p:p['records'][4]['selected_problem_diagnostics'].__setitem__('meets_selected_optimum_tolerance',True)),
        ('complete','relaxed policy',lambda p:p['scope'].__setitem__('feasibility_tolerance',.01)),
        ('missing-candidate','imputed missing diagnostics',lambda p:p['records'][4].__setitem__('selected_problem_diagnostics',packets['complete']['records'][4]['selected_problem_diagnostics'])),
        ('complete','omitted native result',lambda p:p['records'].pop()),
        ('complete','failure rewritten as success',lambda p:p['records'][6]['solver'].__setitem__('success',True)),
        ('complete','export replaced with original',lambda p:p['derived_candidates'][0].__setitem__('weights',p['records'][0]['solver']['weights'])),
        ('complete','altered global reference',lambda p:p['scope']['reference'].__setitem__('unscaled_minimum_variance',.00864)),
        ('contradictory','omitted producer claim',lambda p:p['producer_claims'].pop()),
        ('complete','changed original return units',lambda p:p['scope'].__setitem__('expected_return_unit','percent')),
    ]
    for case,name,mutate in cases:
        packet=copy.deepcopy(packets[case]);mutate(packet)
        try:inspect(packet,source_sha)
        except (AssertionError,KeyError,TypeError,ValueError):pass
        else:raise AssertionError('Mutation accepted: '+name)
    return len(cases)


if __name__=='__main__':
    digest=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
    receipt=json.loads((ROOT/'receipt.json').read_text());source_sha=digest(ROOT/'model/measure.py')
    assert receipt['source_sha256']==source_sha
    packets={case:json.loads((ROOT/'inputs'/f'{case}.json').read_text()) for case in ['complete','missing-candidate','contradictory']}
    summary={}
    for case,packet in packets.items():
        assert digest(ROOT/receipt['packets'][case]['path'])==receipt['packets'][case]['sha256']
        assert packet['case']==case
        findings=inspect(packet,source_sha)
        counts={label:sum(f['original_feasibility']==label for f in findings) for label in ['met','breached','unresolved']}
        assert counts==({'met':3,'breached':4,'unresolved':1} if case=='missing-candidate' else {'met':4,'breached':4,'unresolved':0})
        assert sum(f['original_optimum']=='met' for f in findings)==1
        summary[case]={'candidates':len(findings),'original_feasibility':counts,'meets_original_optimum':1,'producer_claims':len(packet['producer_claims'])}
    mutations=adverse_checks(packets,source_sha)
    print(json.dumps({'cases':summary,'mutations_rejected':mutations,'new_solver_or_provider_calls':0},indent=2))
