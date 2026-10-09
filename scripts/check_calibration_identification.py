"""Fixed synthetic fixture checks; no optimizer, financial model or prose evaluator."""
import copy
import hashlib
import json
import math
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EX=ROOT/'examples/calibration-identification'


def near(a,b,tol=1e-9):
    assert isinstance(a,(int,float)) and not isinstance(a,bool) and math.isfinite(a)
    assert abs(a-float(b))<=tol,(a,b)


def inspect(packet):
    assert packet['case'] in ['complete','missing-allocation','contradictory']
    inputs=packet['inputs']
    assert inputs['A']==[[.5,.5,0],[.5,.5,1]] and inputs['b']==[.04,.09]
    assert inputs['bounds']=={'lower':[0,0,0],'upper':None}
    assert [inputs[k] for k in ['forward_USD','strike_USD','discount']]==[100,100,1]
    assert inputs['original_data_fit_tolerance']==1e-10 and inputs['regularization_weight']==1
    reference=packet['analytical_reference']
    assert reference['original_rank']==2 and reference['number_of_rates']==3
    assert reference['null_direction']==[1,-1,0]
    assert reference['half_year_variance_bounds']==['0','1/25']
    assert reference['q1_plus_q2']=='2/25' and reference['q3']=='1/20'
    assert reference['one_half_year_variance']=='13/200'
    witnesses=packet['witnesses'];solves=packet['solves']
    assert [r['id'] for r in witnesses]==['C1','C2','C3','C4']
    assert [r['id'] for r in solves]==['S1','S2','S3','S4','S5']
    refs=[['0','2/25','1/20'],['1/25','1/25','1/20'],['2/25','0','1/20'],['-1/100','9/100','1/20'],
          ['1/25','1/25','1/20'],['1/100','7/100','1/20'],['1/25','1/25','1/20'],['7/100','1/100','1/20'],['12/125','0','21/500']]
    findings=[]
    for row,ref in zip(witnesses+solves,refs):
        assert not any(key in row for key in ['rates_nonnegative','original_data_fit','exact_minimizer_reference'])
        hidden=packet['case']=='missing-allocation' and row['id']=='C2'
        qref=list(map(F,ref))
        if hidden:
            assert row['variance_rates'] is None and row['exact_rates'] is None
        else:
            assert len(row['variance_rates'])==3
            for v,q in zip(row['variance_rates'],qref):near(v,q)
            if row['exact_rates'] is not None:assert list(map(F,row['exact_rates']))==qref
        assert len(row['original_data_residual'])==2
        residual=[(qref[0]+qref[1])/2-F(1,25),(qref[0]+qref[1])/2+qref[2]-F(9,100)]
        for actual,wanted in zip(row['original_data_residual'],residual):near(actual,wanted,1e-10)
        ws=[qref[0]/2,(qref[0]+qref[1])/2,(qref[0]+qref[1]+qref[2])/2,(qref[0]+qref[1])/2+qref[2]]
        assert len(row['points'])==4
        for index,(point,w,t) in enumerate(zip(row['points'],ws,[.5,1,1.5,2])):
            near(point['maturity_years'],t,0)
            if hidden and index==0:
                assert all(v is None for k,v in point.items() if k!='maturity_years')
                continue
            near(point['total_variance'],w)
            if point['exact_variance'] is not None:assert F(point['exact_variance'])==w
            assert point['formula_defined']==(w>=0)
            if w<0:
                assert all(point[k] is None for k in ['total_stddev','quantlib_call','erf_call'])
            else:
                near(point['total_stddev'],math.sqrt(float(w)))
                price=100*math.erf(math.sqrt(float(w)/8))
                near(point['quantlib_call'],price,1e-10);near(point['erf_call'],price,1e-10)
        if row['id'].startswith('S'):
            i=int(row['id'][1:])-1;d=[None,F(-3,50),F(0),F(3,50),F(1,10)][i]
            assert row['preference_target']==(None if d is None else float(d))
            assert row['preference_target_exact']==(None if d is None else str(d))
            assert row['system_rank']==(2 if d is None else 3)
            native=row['native'];assert native['x']==row['variance_rates']
            assert native['success'] is True and native['status']>0
            q=native['x'];r=[.5*(q[0]+q[1])-.04,.5*(q[0]+q[1])+q[2]-.09]
            pref=None if d is None else q[0]-q[1]-float(d)
            if d is None:assert row['preference_residual'] is None
            else:near(row['preference_residual'],pref,1e-12)
            combined=r if pref is None else r+[pref]
            assert len(native['fun'])==len(combined)
            for value,target in zip(native['fun'],combined):near(value,target,1e-12)
            near(native['cost'],sum(v*v for v in combined)/2,1e-12)
            near(native['cost'],F(1,25000) if i==4 else 0,1e-10)
            gradient=[.5*sum(r),.5*sum(r),r[1]]
            if pref is not None:gradient[0]+=pref;gradient[1]-=pref
            for value,g in zip(q,gradient):
                assert value>=0
                assert g>=-1e-9 if value<=1e-9 else abs(g)<=1e-9
        findings.append({'id':row['id'],'admissibility':'unresolved' if hidden else 'not met' if row['id']=='C4' else 'met',
                         'original_fit':'unverified reported fit' if hidden else 'not met' if row['id']=='S5' else 'met',
                         'half_year_price':'unresolved' if hidden else 'undefined' if row['id']=='C4' else row['points'][0]['quantlib_call']})
    assert len(packet['producer_statements'])==(7 if packet['case']=='contradictory' else 0)
    if packet['case']=='contradictory':assert [x['id'] for x in packet['producer_statements']]==['P'+str(i) for i in range(1,8)]
    return findings


def main():
    receipt=json.loads((EX/'receipt.json').read_text())
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    assert receipt['source_sha256']==sha(EX/'model/measure.py')
    assert receipt['plan_sha256']==sha(EX/'model/README.md')
    results={};packets={}
    for case in ['complete','missing-allocation','contradictory']:
        path=EX/'inputs'/f'{case}.json';assert sha(path)==receipt['case_sha256'][case]
        packets[case]=json.loads(path.read_text());results[case]=inspect(packets[case])
    # Alternative actual vectors fit the retained C2 longer-maturity quantities.
    # They demonstrate ambiguity, not reconstruction of the hidden actual vector.
    for q in [[F(0),F(2,25),F(1,20)],[F(2,25),F(0),F(1,20)],[F(-1,100),F(9,100),F(1,20)]]:
        assert (q[0]+q[1])/2==F(1,25) and (q[0]+q[1]+q[2])/2==F(13,200)
        assert (q[0]+q[1])/2+q[2]==F(9,100)
    mutations=[
        ('wrong-target',lambda x:x['inputs']['b'].__setitem__(0,.048)),
        ('wrong-weight',lambda x:x['inputs'].__setitem__('regularization_weight',0)),
        ('wrong-domain',lambda x:x['inputs']['bounds'].__setitem__('lower',[-1,-1,-1])),
        ('wrong-forward',lambda x:x['inputs'].__setitem__('forward_USD',101)),
        ('wrong-rank',lambda x:x['analytical_reference'].__setitem__('original_rank',3)),
        ('false-bound',lambda x:x['analytical_reference'].__setitem__('half_year_variance_bounds',['1/50','1/50'])),
        ('lost-proposal',lambda x:x['witnesses'].pop()),
        ('lost-solve',lambda x:x['solves'].pop()),
        ('wrong-order',lambda x:x['witnesses'].reverse()),
        ('negative-price',lambda x:x['witnesses'][3]['points'][0].__setitem__('quantlib_call',0)),
        ('negative-domain',lambda x:x['witnesses'][3]['points'][0].__setitem__('formula_defined',True)),
        ('wrong-maturity',lambda x:x['witnesses'][0]['points'][0].__setitem__('maturity_years',1)),
        ('substituted-price',lambda x:x['witnesses'][0]['points'][0].__setitem__('quantlib_call',5.637)),
        ('observer-label',lambda x:x['witnesses'][0].__setitem__('original_data_fit',True)),
        ('lost-preference',lambda x:x['solves'][1].__setitem__('preference_target',None)),
        ('wrong-augmented-rank',lambda x:x['solves'][1].__setitem__('system_rank',2)),
        ('erased-misfit',lambda x:x['solves'][4]['original_data_residual'].__setitem__(0,0)),
        ('erased-cost',lambda x:x['solves'][4]['native'].__setitem__('cost',0)),
        ('changed-candidate',lambda x:x['solves'][4]['native']['x'].__setitem__(0,.04)),
        ('wrong-identified-output',lambda x:x['solves'][2]['points'][2].__setitem__('quantlib_call',11)),
    ]
    rejected=[]
    for name,mutate in mutations:
        data=copy.deepcopy(packets['complete']);mutate(data)
        try:inspect(data)
        except (AssertionError,KeyError,ValueError,TypeError):rejected.append(name)
        else:raise AssertionError(name+' accepted')
    for name,mutate in [
        ('hidden-vector-restored',lambda x:x['witnesses'][1].__setitem__('variance_rates',[.04,.04,.05])),
        ('hidden-price-restored',lambda x:x['witnesses'][1]['points'][0].__setitem__('quantlib_call',5.637197779701665)),
        ('hidden-exact-restored',lambda x:x['witnesses'][1].__setitem__('exact_rates',['1/25','1/25','1/20']))]:
        data=copy.deepcopy(packets['missing-allocation']);mutate(data)
        try:inspect(data)
        except (AssertionError,KeyError,ValueError,TypeError):rejected.append(name)
        else:raise AssertionError(name+' accepted')
    print(json.dumps({'scope':'Fixed synthetic evidence relationships; no agent, solver or general prose evaluation.',
                      'cases':results,'rejected_mutations':rejected,'missing_allocation_witnesses':3},indent=2))


if __name__=='__main__':main()
