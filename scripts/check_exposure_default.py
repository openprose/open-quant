"""Independent rational checks of retained output; no NumPy or LP invocation."""
import copy
import hashlib
import json
import math
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/"examples/exposure-default"
EXPECTED={
    'J1':['1/20','3/100','1/50'],
    'J2':['1/10','0','0'],
    'J3':['0','1/10','0'],
    'J4':['0','0','1/10'],
    'J5':['3/50','3/250','7/250'],
    'J6':['-1/100','11/100','0']}


def near(value,target):
    assert isinstance(value,(float,int)) and not isinstance(value,bool) and math.isfinite(value)
    assert abs(F(str(value))-F(target))<=F(1,10**10)


def verify(data):
    assert data['schema']=='exposure-default-study-v1'
    for key,file in [('source_sha256','model/measure.py'),('plan_sha256','model/README.md')]:
        assert data[key]==hashlib.sha256((ROOT/file).read_bytes()).hexdigest()
    specification=data['specification']
    assert specification==dict(exposure_million_usd=['10','50','100'],exposure_probabilities=['1/2','3/10','1/5'],default_probability='1/10',loss_fraction='3/5',discount_factor='20/21',horizon_years=1,probability_basis='One stipulated measure; no empirical or market estimate',loss_timing='All loss paid at T=1 year',numeric_absolute_tolerance='1e-10')
    x=[F(10),F(50),F(100)];p=[F(1,2),F(3,10),F(1,5)];pd=F(1,10);scale=F(4,7)
    assert [r['id'] for r in data['proposals']]==list(EXPECTED)
    findings={}
    for record in data['proposals']:
        if data['case']=='missing-joint' and record['id']=='J5':
            native=record['native'];assert record['exact'] is None
            for key in ['default_cells','nondefault_cells','conditional_default_given_exposure']:assert native[key] is None
            assert len(native['exposure_marginal'])==3
            for value,ref in zip(native['exposure_marginal'],p):near(value,ref)
            near(native['default_probability'],pd);near(native['total_probability'],1)
            near(native['mean_exposure_million_usd'],40)
            weighted=F(str(native['default_weighted_exposure_million_usd']));near(float(weighted),4)
            near(native['exposure_ratio_on_default_million_usd'],weighted/pd)
            near(native['covariance_exposure_default_million_usd'],weighted-4)
            near(native['discounted_loss_million_usd'],scale*weighted)
            near(native['marginal_product_million_usd'],F(16,7))
            findings['J5']=dict(admissible='unresolved',independent='unresolved',reported_product_equality=True,verified_product_equality=None,verified_joint_loss_million_usd=None)
            continue
        d=list(map(F,EXPECTED[record['id']]));n=[pi-di for pi,di in zip(p,d)];weighted=sum(xi*di for xi,di in zip(x,d))
        admissible=all(di>=0 and ni>=0 for di,ni in zip(d,n)) and sum(d)==pd
        independent=all(di==pi*pd for di,pi in zip(d,p))
        exact=dict(default_cells=list(map(str,d)),nondefault_cells=list(map(str,n)),admissible=admissible,independent=independent,
            mean_exposure_million_usd='40',default_weighted_exposure_million_usd=str(weighted),
            exposure_ratio_on_default_million_usd=str(10*weighted),conditional_default_given_exposure=[str(di/pi) for di,pi in zip(d,p)],
            covariance_exposure_default_million_usd=str(weighted-4),discounted_loss_million_usd=str(scale*weighted),marginal_product_million_usd='16/7')
        exact.pop('admissible');exact.pop('independent')
        assert record['exact']==exact
        native=record['native']
        for key,targets in [('default_cells',d),('nondefault_cells',n),('exposure_marginal',p),('conditional_default_given_exposure',[di/pi for di,pi in zip(d,p)])]:
            assert len(native[key])==3
            for a,b in zip(native[key],targets):near(a,b)
        near(native['total_probability'],1);near(native['default_probability'],pd)
        for key in ['mean_exposure_million_usd','default_weighted_exposure_million_usd','exposure_ratio_on_default_million_usd','covariance_exposure_default_million_usd','discounted_loss_million_usd','marginal_product_million_usd']:near(native[key],F(exact[key]))
        findings[record['id']]=dict(admissible=admissible,independent=independent if admissible else 'not applicable',reported_product_equality=weighted==4,
            verified_product_equality=weighted==4 if admissible else None,
            verified_joint_loss_million_usd=str(scale*weighted) if admissible else None)
    assert [s['id'] for s in data['optimizations']]==['minimum','maximum']
    for record,objective,witness,sign in zip(data['optimizations'],[F(1),F(10)],[[F(1,10),F(0),F(0)],[F(0),F(0),F(1,10)]],[1,-1]):
        assert record['reference']==dict(default_cells=list(map(str,witness)),default_weighted_exposure_million_usd=str(objective),discounted_loss_million_usd=str(scale*objective))
        # Exact exposure bounds and feasible attaining witnesses certify global bounds.
        assert all(10<=xi<=100 for xi in x)
        assert sum(witness)==pd and all(0<=di<=pi for di,pi in zip(witness,p))
        assert sum(xi*di for xi,di in zip(x,witness))==objective
        native=record['native'];assert native['success'] is True and native['status']==0
        values=native['candidate_default_cells'];assert len(values)==3
        for value,pi in zip(values,p):assert -1e-10<=value<=float(pi)+1e-10
        near(sum(values),pd);near(native['objective'],sign*objective)
        near(sum(float(xi)*di for xi,di in zip(x,values)),objective)
        for value,ref in zip(values,witness):near(value,ref)
        assert len(native['eqlin']['residual'])==1;near(native['eqlin']['residual'][0],0)
        for value,observed in zip(values,native['lower']['residual']):near(observed,F(str(value)))
        for value,pi,observed in zip(values,p,native['upper']['residual']):near(observed,pi-F(str(value)))
    assert data['case'] in ['complete','missing-joint','contradictory']
    assert [c['id'] for c in data['producer_statements']]==([f'C{i}' for i in range(1,8)] if data['case']=='contradictory' else [])
    return findings


def replace(d,path,value):
    for key in path[:-1]:d=d[key]
    d[path[-1]]=value


def main():
    packets={case:json.loads((ROOT/'inputs'/(case+'.json')).read_text()) for case in ['complete','missing-joint','contradictory']}
    findings={case:verify(data) for case,data in packets.items()};data=packets['complete']
    receipt=json.loads((ROOT/'receipt.json').read_text())
    assert receipt['exit_code']==0 and receipt['model_calls']==0 and receipt['controls_passed']==126
    for case in packets:assert receipt['case_sha256'][case]==hashlib.sha256((ROOT/'inputs'/(case+'.json')).read_bytes()).hexdigest()
    assert receipt['source_sha256']==data['source_sha256'] and receipt['plan_sha256']==data['plan_sha256']
    mutations=[
        ('changed probability basis',['specification','probability_basis'],'empirical'),
        ('recovery swapped with loss fraction',['specification','loss_fraction'],'2/5'),
        ('discount removed',['specification','discount_factor'],'1'),
        ('changed timing',['specification','loss_timing'],'paid immediately on default'),
        ('joint default cell changed',['proposals',0,'native','default_cells',0],.06),
        ('missing nondefault mass',['proposals',0,'native','nondefault_cells',0],.4),
        ('marginal probability substituted',['proposals',0,'native','conditional_default_given_exposure',0],.5),
        ('unconditional mean called conditional',['proposals',3,'native','exposure_ratio_on_default_million_usd'],40),
        ('product substituted for joint loss',['proposals',3,'native','discounted_loss_million_usd'],16/7),
        ('constant conditional default falsely supplied',['proposals',4,'native','conditional_default_given_exposure'],[.1,.1,.1]),
        ('dependent equality rejected',['proposals',4,'exact','covariance_exposure_default_million_usd'],'1'),
        ('negative cell silently clipped',['proposals',5,'native','default_cells',0],0),
        ('invalid nondefault table silently repaired',['proposals',5,'native','nondefault_cells',0],.5),
        ('loss fraction omitted',['proposals',0,'native','discounted_loss_million_usd'],80/21),
        ('USD rather than USD million',['proposals',0,'native','discounted_loss_million_usd'],16000000/7),
        ('missing candidate',['optimizations',0,'native','candidate_default_cells'],None),
        ('native sign lost',['optimizations',1,'native','objective'],10),
        ('false lower bound',['optimizations',0,'reference','discounted_loss_million_usd'],'16/7'),
        ('nonfinite loss',['proposals',0,'native','discounted_loss_million_usd'],float('nan')),
        ('unbound source',['source_sha256'],'0'*64),
    ]
    rejected=[]
    for name,path,value in mutations:
        altered=copy.deepcopy(data);replace(altered,path,value)
        try:verify(altered)
        except (AssertionError,TypeError,ValueError,KeyError):rejected.append(name)
        else:raise AssertionError('Mutation accepted: '+name)
    missing=copy.deepcopy(packets['complete']);missing['case']='missing-joint';missing['proposals'][4]['exact']=None
    for field in ['default_cells','nondefault_cells','conditional_default_given_exposure']:missing['proposals'][4]['native'][field]=None
    assert missing==packets['missing-joint']
    contradictory=copy.deepcopy(packets['contradictory']);contradictory['case']='complete';contradictory['producer_statements']=[]
    assert contradictory==packets['complete']
    extra=[(['proposals',4,'native','default_cells'],[.05,.03,.02]),(['proposals',4,'native','nondefault_cells'],[.45,.27,.18]),(['proposals',4,'native','conditional_default_given_exposure'],[.1,.1,.1]),(['proposals',4,'exact'],packets['complete']['proposals'][4]['exact']),(['proposals',4,'native','discounted_loss_million_usd'],0),(['proposals',4,'native','default_probability'],0)]
    for path,value in extra:
        altered=copy.deepcopy(packets['missing-joint']);replace(altered,path,value)
        try:verify(altered)
        except (AssertionError,TypeError,ValueError,KeyError):rejected.append('Missing case: '+str(path))
        else:raise AssertionError('Missing-case mutation accepted')
    assert findings['missing-joint']['J5']['admissible']=='unresolved'
    assert findings['missing-joint']['J1']==findings['complete']['J1']
    assert findings['missing-joint']['J6']['admissible'] is False
    # All three constructions match the withheld row's reported mass and first moment.
    # They distinguish a feasible independent table, feasible dependence and invalid cells.
    p=list(map(F,['1/2','3/10','1/5']));x=[10,50,100]
    ambiguity=[list(map(F,r)) for r in [['1/20','3/100','1/50'],['3/50','3/250','7/250'],['1/10','-3/50','3/50']]]
    classifications=[]
    for d in ambiguity:
        assert sum(d)==F(1,10) and sum(v*w for v,w in zip(x,d))==4
        classifications.append((all(0<=v<=w for v,w in zip(d,p)),all(v==w/F(10) for v,w in zip(d,p))))
    assert classifications==[(True,True),(True,False),(False,False)]
    import re
    report=(ROOT/'sample-results/report.md').read_text();seen=[]
    for line in report.splitlines():
        cells=[c.strip() for c in line.strip('|').split('|')]
        if cells[0] not in EXPECTED:continue
        row=next(r for r in data['proposals'] if r['id']==cells[0]);f=findings['complete'][cells[0]];seen.append(cells[0])
        assert len(cells)==5
        assert cells[1]==('yes' if f['admissible'] else 'no')
        assert cells[2]==('yes' if f['independent'] is True else 'no' if f['independent'] is False else 'not applicable')
        if f['admissible']:assert abs(float(cells[3])-row['native']['exposure_ratio_on_default_million_usd'])<=.0000005
        else:assert cells[3]=='unavailable'
        assert abs(float(cells[4])-row['native']['discounted_loss_million_usd'])<=.0000005
    assert seen==list(EXPECTED)
    locators=re.findall(r'^- `([^`]+)` — `([0-9a-f]{64})`$',report,re.M);assert len(locators)==11
    for name,digest in locators:assert hashlib.sha256((ROOT.parents[1]/name).read_bytes()).hexdigest()==digest
    print(json.dumps(dict(packets=3,proposals_each=6,optimizations_each=2,rejected_mutations=len(rejected),missing_aggregate_ambiguity_witnesses=3,report_rows=6,identity_locators=11,findings=findings,scope='Fixed-record arithmetic and identity checks; no native calculation or arbitrary prose assessment.')))


if __name__=='__main__':main()
