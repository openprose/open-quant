"""Check fixed reverse-stress evidence; no optimization or arbitrary prose assessment."""
from copy import deepcopy
from fractions import Fraction as Q
import hashlib,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EXAMPLE=ROOT/'examples/reverse-stress'
METRICS = {'selected': ('1', '1'), 'raw-mixed-units': ('1', '1/25'), 'raw-common-basis-points': ('1', '400')}
EXPECTED = [
    ('selected-negative-axis', 'selected', [-2, 0], 200, True, 0),
    ('selected-positive-axis', 'selected', [4, 0], 200, False, 8),
    ('selected-upper', 'selected', [-.2, .8], 200, True, 0),
    ('selected-lower', 'selected', [-.2, -.8], 200, True, 0),
    ('selected-origin', 'selected', [0, 0], 200, True, 0),
    ('selected-iteration-limit', 'selected', [4, .2], 1, False, 9),
    ('raw-mixed-units', 'raw-mixed-units', [-.2, .8], 200, True, 0),
    ('raw-common-basis-points', 'raw-common-basis-points', [-2, .1], 200, True, 0),
]
REFERENCES = {
    'selected': {'minimum': Q(2, 3), 'center': Q(-1, 3), 'y2': Q(5, 9), 'lambda': Q(1, 4), 'cx': Q(3, 4), 'cy': Q(0)},
    'raw-mixed-units': {'minimum': Q(74, 2475), 'center': Q(-1, 99), 'y2': Q(7301, 9801), 'lambda': Q(1, 100), 'cx': Q(99, 100), 'cy': Q(0)},
    'raw-common-basis-points': {'minimum': Q(1), 'center': Q(-1), 'y2': Q(0), 'lambda': Q(1, 2), 'cx': Q(1, 2), 'cy': Q(398)},
}

CLAIMS=['Every native success identifies the least severe scenario under the selected requirements.', 'A failed solver result proves that no threshold-reaching scenario was produced.', 'A displayed loss of 3.00 million establishes that the threshold is met.', 'Recoding equity changes in basis points leaves the raw numerical severity recipe unchanged.', 'The nearest scenario is the most likely loss event.', 'The largest loss in the four-scenario catalog is the worst possible loss.', 'The analytical minimizer independently establishes a missing actual candidate vector.']


def close(value, expected):
    assert type(value) in (int,float) and math.isfinite(value)
    assert math.isclose(value,expected,rel_tol=1e-12,abs_tol=1e-10),(value,expected)


def threshold(value):
    return Q(str(value))>=Q(3)-Q('1e-8')


def optimum(loss, severity):
    return threshold(loss) and abs(Q(str(severity))-Q(2,3))<=Q('1e-8')


def reported(q):
    assert set(q['metric_values'])==set(METRICS)
    for field in ['loss_million_usd','loss_usd','threshold_margin_million_usd','selected_severity','selected_objective_gap']:
        assert type(q[field]) in (int,float) and math.isfinite(q[field])
    close(q['loss_usd'],q['loss_million_usd']*1e6)
    close(q['threshold_margin_million_usd'],q['loss_million_usd']-3)
    close(q['selected_severity']**2,q['metric_values']['selected'])
    close(q['selected_objective_gap'],q['metric_values']['selected']-2/3)


def observed(z,q):
    x,y=z;reported(q)
    close(q['loss_million_usd'],(x-1)**2+4*y*y-1)
    for name,(a,b) in METRICS.items():close(q['metric_values'][name],float(Q(a))*x*x+float(Q(b))*y*y)
    p=q['physical_shocks'];close(p['rate_basis_points'],25*x)
    close(p['equity_return_percentage_points'],5*y)
    close(p['equity_return_basis_points'],100*p['equity_return_percentage_points'])
    close((p['rate_basis_points']/25)**2+(p['equity_return_basis_points']/500)**2,q['metric_values']['selected'])


def verify(d,source_hash):
    assert d['subject']=='REVERSE-STRESS-2026-10-06' and d['source_sha256']==source_hash
    case=d['case'];assert case in ['complete','missing-candidate','contradictory']
    assert d['producer_claims']==([{'id':f'C{i+1}','text':c} for i,c in enumerate(CLAIMS)] if case=='contradictory' else [])
    assert d['specification']=={'factor_order':['normalized_rate_change','normalized_equity_return_change'],
        'loss_expression':'x*x + 4*y*y - 2*x','loss_unit':'USD million','threshold':3,
        'selected_severity_squared':'x*x + y*y','domain':'all real x,y','rate_scale_basis_points':25,
        'equity_scale_percentage_points':5,'loss_feasibility_tolerance':1e-8,'selected_objective_tolerance':1e-8,
        'probability_model':None,'horizon':'instantaneous','management_actions':None}
    assert set(d['global_references'])==set(REFERENCES)
    for key,e in REFERENCES.items():
        r=d['global_references'][key];assert tuple(r['weights'])==METRICS[key]
        for field,ref_field in [('minimum','minimum'),('center','square_x_center'),('y2','minimizer_y_squared'),('lambda','lambda'),('cx','square_x_coefficient'),('cy','square_y_coefficient')]:assert Q(r[ref_field])==e[field]
        a,b=map(Q,r['weights']);lam=e['lambda'];c=e['center']
        left=[a-lam,b-4*lam,2*lam,3*lam-e['minimum']]
        right=[e['cx'],e['cy'],-2*e['cx']*c,e['cx']*c*c]
        assert left==right==list(map(Q,r['polynomial_coefficients']))
        assert min(lam,e['cx'],e['cy'])>=0
        close(r['minimum_float'],float(e['minimum']))
        assert len(r['minimizers'])==(1 if e['y2']==0 else 2)
        for i,(x,y) in enumerate(r['minimizers']):
            close(x,float(c));close(y,(1 if i==0 else -1)*math.sqrt(float(e['y2'])))
            close((x-1)**2+4*y*y,4);close(float(a)*x*x+float(b)*y*y,float(e['minimum']))
    assert len(d['solver_results'])==len(EXPECTED);findings=[]
    for r,(name,metric,start,maxiter,success,status) in zip(d['solver_results'],EXPECTED):
        assert r['id']==name and r['metric']==metric and r['start']==start
        assert tuple(r['weights'])==METRICS[metric]
        assert r['method']=='SLSQP' and r['options']=={'ftol':1e-12,'maxiter':maxiter,'disp':False}
        n=r['native'];q=r['quantities'];reported(q)
        assert n['success'] is success and n['status']==status
        assert min(n['iterations'],n['function_evaluations'],n['gradient_evaluations'])>=1
        close(n['objective'],q['metric_values'][metric])
        close(r['implemented_metric_objective_gap'],n['objective']-float(REFERENCES[metric]['minimum']))
        absent=case=='missing-candidate' and name=='selected-upper'
        if absent:
            assert n['candidate'] is None and n['gradient'] is None and q['physical_shocks'] is None and r['diagnostics'] is None
            actual_threshold=actual_optimum=actual_own='unresolved'
        else:
            assert n['candidate'] is not None and len(n['gradient'])==2
            x,y=n['candidate'];a,b=map(lambda v:float(Q(v)),METRICS[metric]);observed([x,y],q)
            for value,expected in zip(n['gradient'],[2*a*x,2*b*y]):close(value,expected)
            g=[2*(x-1),8*y];f=[2*a*x,2*b*y];norm=math.hypot(*g)
            lam=sum(u*v for u,v in zip(f,g))/(norm*norm)
            close(r['diagnostics']['candidate_gradient_multiplier'],lam)
            close(r['diagnostics']['stationarity_max_residual'],max(abs(u-lam*v) for u,v in zip(f,g)))
            close(r['diagnostics']['tangent_lagrangian_curvature'],((2*a-2*lam)*g[1]**2+(2*b-8*lam)*g[0]**2)/(norm*norm))
            actual_threshold='met' if threshold(q['loss_million_usd']) else 'not met'
            actual_optimum='met' if optimum(q['loss_million_usd'],q['metric_values']['selected']) else 'not met'
            actual_own='met' if threshold(q['loss_million_usd']) and abs(Q(str(n['objective']))-REFERENCES[metric]['minimum'])<=Q('1e-8') else 'not met'
        findings.append({'id':name,'native_success':success,'implemented_selected_metric':metric=='selected',
             'reported_threshold':'met' if threshold(q['loss_million_usd']) else 'not met',
             'reported_selected_criteria':'met' if optimum(q['loss_million_usd'],q['metric_values']['selected']) else 'not met',
             'candidate_threshold':actual_threshold,'candidate_selected_optimum':actual_optimum,
             'candidate_own_metric_optimum':actual_own,'candidate_correspondence':'unresolved' if absent else 'met'})
    assert len(d['catalog'])==4
    for i,(row,point) in enumerate(zip(d['catalog'],[[-1,0],[3,0],[0,1],[0,-1]])):
        assert row['id']==f'C{i+1}' and row['candidate']==point;observed(point,row['quantities'])
    witness=d['outside_catalog_witness'];assert witness['id']=='outside-catalog' and witness['candidate']==[0,2]
    observed(witness['candidate'],witness['quantities'])
    return {'runs':findings,'global_references':'met','catalog_minimum_squared_severity':min(r['quantities']['metric_values']['selected'] for r in d['catalog']),
            'catalog_maximum_loss_million_usd':max(r['quantities']['loss_million_usd'] for r in d['catalog']),
            'witness_loss_million_usd':witness['quantities']['loss_million_usd'],
            'probability_claim':'not_established','finite_global_maximum':'does_not_exist_under_stipulated_domain'}


def main():
    read=lambda p:json.loads(p.read_text());digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    receipt=read(EXAMPLE/'receipt.json');source_hash=digest(EXAMPLE/receipt['source_path'])
    assert receipt['source_sha256']==source_hash and receipt['plan_sha256']==digest(EXAMPLE/receipt['plan_path'])
    assert set(receipt['packets'])=={'complete','missing-candidate','contradictory'};packets={};results={}
    for case,entry in receipt['packets'].items():
        p=EXAMPLE/entry['path'];assert digest(p)==entry['sha256'];packets[case]=read(p)
        assert packets[case]['case']==case;results[case]=verify(packets[case],source_hash)
    assert results['complete']==results['contradictory']
    complete=results['complete']['runs'];missing=results['missing-candidate']['runs']
    assert [r['candidate_selected_optimum'] for r in complete]==['not met','not met','met','met','not met','not met','not met','not met']
    assert missing[2]['candidate_selected_optimum']=='unresolved' and missing[2]['reported_selected_criteria']=='met'
    assert [r for i,r in enumerate(complete) if i!=2]==[r for i,r in enumerate(missing) if i!=2]
    assert complete[5]['candidate_threshold']=='met' and complete[1]['candidate_threshold']=='not met'
    assert complete[6]['candidate_own_metric_optimum']==complete[7]['candidate_own_metric_optimum']=='met'
    assert threshold(Q(3)-Q('1e-8')) and not threshold(Q(3)-Q('1.0001e-8'))
    assert optimum(Q(3),Q(2,3)+Q('1e-8')) and not optimum(Q(3),Q(2,3)+Q('1.0001e-8'))
    mutations=[
      ('omit_run','complete',lambda x:x['solver_results'].pop()),
      ('change_threshold','complete',lambda x:x['specification'].update(threshold=2.9)),
      ('invent_probability_model','complete',lambda x:x['specification'].update(probability_model='normal')),
      ('change_factor_order','complete',lambda x:x['specification']['factor_order'].reverse()),
      ('relabel_metric','complete',lambda x:x['solver_results'][6].update(metric='selected')),
      ('change_metric_weight','complete',lambda x:x['solver_results'][6]['weights'].__setitem__(1,'1')),
      ('hide_native_failure','complete',lambda x:x['solver_results'][1]['native'].update(success=True)),
      ('round_loss_into_pass','complete',lambda x:x['solver_results'][1]['quantities'].update(loss_million_usd=3.0)),
      ('erase_gap','complete',lambda x:x['solver_results'][0]['quantities'].update(selected_objective_gap=0)),
      ('change_start','complete',lambda x:x['solver_results'][0]['start'].__setitem__(1,.1)),
      ('wrong_actual_vector','complete',lambda x:x['solver_results'][0]['native'].update(candidate=[0,0])),
      ('fill_missing_vector','missing-candidate',lambda x:x['solver_results'][2]['native'].update(candidate=x['global_references']['selected']['minimizers'][0])),
      ('fill_missing_gradient','missing-candidate',lambda x:x['solver_results'][2]['native'].update(gradient=[0,0])),
      ('fill_missing_physical_shocks','missing-candidate',lambda x:x['solver_results'][2]['quantities'].update(physical_shocks={'rate_basis_points':0})),
      ('change_global_bound','complete',lambda x:x['global_references']['selected'].update(minimum='1')),
      ('change_certificate','complete',lambda x:x['global_references']['selected'].update(square_x_coefficient='1')),
      ('erase_negative_curvature','complete',lambda x:x['solver_results'][0]['diagnostics'].update(tangent_lagrangian_curvature=2)),
      ('omit_catalog_entry','complete',lambda x:x['catalog'].pop()),
      ('change_witness','complete',lambda x:x['outside_catalog_witness'].update(candidate=[0,1])),
      ('recode_units_without_scale','complete',lambda x:x['solver_results'][2]['quantities']['physical_shocks'].update(equity_return_basis_points=x['solver_results'][2]['quantities']['physical_shocks']['equity_return_percentage_points'])),
    ];rejected=[]
    for name,case,change in mutations:
        altered=deepcopy(packets[case]);change(altered)
        try:verify(altered,source_hash)
        except (AssertionError,KeyError,TypeError,ValueError):rejected.append(name)
        else:raise AssertionError('Mutation not detected: '+name)
    print(json.dumps({'cases':3,'native_runs_per_case':8,'global_references_per_case':3,'mutations_rejected':rejected,'solver_calls':0,'provider_calls':0}))


if __name__=='__main__':main()
