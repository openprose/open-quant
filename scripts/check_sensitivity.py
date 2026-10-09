"""Fixed sensitivity records and caller bindings, not arbitrary report assessment."""
import copy
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/'examples/sensitivity-review'
BUMPS=[1e-6,1e-4,.01,.1,1.,5.]
CASES=[('ATM',100.,100.,.3,2.,.05),('OTM',60.,100.,.3,2.,.05),('short-ATM',100.,100.,.2,1/365,.05)]
SCOPE={'position':'one receiving unit of synthetic European call','changed_factor':'forward',
       'held_fixed':['strike','volatility','maturity','discount'],'recalibration':False,
       'price_unit':'USD PV','delta_unit':'USD PV per USD forward','gamma_unit':'USD PV per squared USD forward',
       'rounding':'Python round(price, 2)','rounding_epsilon_usd':.005,'bumps_usd_forward':BUMPS,
       'illustrative_absolute_derivative_tolerance':1e-4}


def close(a,b,tol=1e-10):
    assert isinstance(a,(int,float)) and math.isfinite(a) and abs(a-b)<=tol,(a,b)


def meets(error):
    return error is not None and math.isfinite(error) and abs(error)<=1e-4


def inspect(packet,source_sha):
    assert packet['subject']=='SENSITIVITY-2026-10-06' and packet['source_sha256']==source_sha
    assert packet['scope']==SCOPE
    assert packet['case'] in ['complete','missing-unrounded','contradictory']
    missing=packet['case']=='missing-unrounded'
    assert len(packet['records'])==3
    findings=[]
    for record,(identity,f,k,sigma,t,r) in zip(packet['records'],CASES):
        assert record['id']==identity
        discount,stddev=math.exp(-r*t),sigma*math.sqrt(t)
        assert record['inputs']=={'forward_usd':f,'strike_usd':k,'annual_volatility':sigma,'maturity_years':t,
                                 'continuous_rate':r,'discount':discount,'stddev':stddev}
        cdf=lambda z: .5*math.erfc(-z/math.sqrt(2))
        d1=math.log(f/k)/stddev+stddev/2
        derivatives={'delta':discount*cdf(d1),'gamma':discount*math.exp(-d1*d1/2)/math.sqrt(2*math.pi)/(f*stddev)}
        for metric,value in derivatives.items():
            close(record['reference'][metric],value); close(record['quantlib_analytic'][metric],value)
        if missing: assert record['reference']['value'] is None
        else: close(record['reference']['value'],discount*(f*cdf(d1)-k*cdf(d1-stddev)))

        def price(observation,level):
            assert observation['forward']==level
            assert math.isfinite(observation['rounded_price_usd'])
            if missing:
                for key in ['quantlib_price_usd','reference_price_usd','rounding_error_usd']: assert observation[key] is None
            else:
                z=math.log(level/k)/stddev+stddev/2
                expected=discount*(level*cdf(z)-k*cdf(z-stddev))
                close(observation['quantlib_price_usd'],expected); close(observation['reference_price_usd'],expected)
                assert observation['rounded_price_usd']==round(observation['quantlib_price_usd'],2)
                close(observation['rounding_error_usd'],observation['rounded_price_usd']-observation['quantlib_price_usd'])
                assert abs(observation['rounding_error_usd'])<=.005+1e-12

        price(record['base'],f)
        assert [x['h_usd_forward'] for x in record['perturbations']]==BUMPS
        for row in record['perturbations']:
            h=row['h_usd_forward']; price(row['minus'],f-h); price(row['plus'],f+h)
            for name,key in [('unrounded','quantlib_price_usd'),('cent_rounded','rounded_price_usd')]:
                view=row['views'][name]
                if missing and name=='unrounded':
                    assert view is None
                    findings.append([identity,h,name,'unresolved','unresolved'])
                    continue
                a,b,c=row['minus'][key],record['base'][key],row['plus'][key]
                calculated={'delta':(c-a)/(2*h),'gamma':(c-2*b+a)/(h*h)}
                outcome=[]
                for metric,value in calculated.items():
                    close(view[metric],value)
                    close(view[metric+'_error'],value-record['reference'][metric])
                    assert view[metric+'_within_illustrative_tolerance']==meets(view[metric+'_error'])
                    outcome.append('met' if meets(view[metric+'_error']) else 'not met')
                close(view['up_premium_change_usd'],c-b); close(view['down_premium_change_usd'],a-b)
                findings.append([identity,h,name,*outcome])
            for metric,bound in [('delta',.005/h),('gamma',.02/(h*h))]:
                e=row['rounding_envelopes'][metric]
                close(e['bound'],bound); close(e['floating_allowance'],1e-7*max(1,bound))
                if missing: assert e['rounding_difference'] is None
                else:
                    difference=row['views']['cent_rounded'][metric]-row['views']['unrounded'][metric]
                    close(e['rounding_difference'],difference)
                    assert abs(difference)<=bound+e['floating_allowance']
    return findings


def main():
    receipt=json.loads((ROOT/'receipt.json').read_text())
    assert hashlib.sha256((ROOT/'model/measure.py').read_bytes()).hexdigest()==receipt['source_sha256']
    packets={}
    for name,entry in receipt['projection']['packets'].items():
        assert entry['path']==f'inputs/{name}.json'
        data=(ROOT/entry['path']).read_bytes()
        assert hashlib.sha256(data).hexdigest()==entry['sha256']
        packets[name]=json.loads(data)
    results={name:inspect(p,receipt['source_sha256']) for name,p in packets.items()}
    full=packets['complete']; missing=packets['missing-unrounded']; contradiction=packets['contradictory']
    assert full['records']==contradiction['records']
    assert full['producer_claims']==missing['producer_claims']==[]
    assert [x['id'] for x in contradiction['producer_claims']]==['P1','P2','P3','P4']
    assert results['complete']==results['contradictory']
    assert len(results['complete'])==36
    for a,b in zip(results['complete'],results['missing-unrounded']):
        assert a[:3]==b[:3]
        assert b[3:]==(['unresolved','unresolved'] if b[2]=='unrounded' else a[3:])
    for original,partial in zip(full['records'],missing['records']):
        assert original['base']['rounded_price_usd']==partial['base']['rounded_price_usd']
        for x,y in zip(original['perturbations'],partial['perturbations']):
            assert x['views']['cent_rounded']==y['views']['cent_rounded']
            for key in ['minus','plus']: assert x[key]['rounded_price_usd']==y[key]['rounded_price_usd']
    assert meets(1e-4) and meets(-1e-4) and not meets(1.000001e-4) and not meets(None)
    mutations=[
        ('wrong subject',lambda x:x.update(subject='OTHER')),
        ('forward relabeled spot',lambda x:x['scope'].update(changed_factor='spot')),
        ('changed discount',lambda x:x['records'][0]['inputs'].update(discount=1.)),
        ('basis-point relabel',lambda x:x['scope'].update(delta_unit='USD PV per bp')),
        ('favorable bump selection',lambda x:x['records'][0]['perturbations'].pop(0)),
        ('incorrect central divisor',lambda x:x['records'][0]['perturbations'][2]['views']['unrounded'].update(delta=1.)),
        ('negative gamma hidden',lambda x:x['records'][2]['perturbations'][2]['views']['cent_rounded'].update(gamma=100.)),
        ('zero derivative called met',lambda x:x['records'][0]['perturbations'][0]['views']['cent_rounded'].update(delta_within_illustrative_tolerance=True)),
        ('rounding error erased',lambda x:x['records'][0]['base'].update(rounding_error_usd=0.)),
        ('rounding envelope inflated',lambda x:x['records'][0]['perturbations'][0]['rounding_envelopes']['gamma'].update(bound=1e30)),
        ('finite change called derivative',lambda x:x['records'][0]['perturbations'][3]['views']['unrounded'].update(up_premium_change_usd=.528)),
        ('case relabel hides observations',lambda x:x.update(case='missing-unrounded')),
    ]
    for name,mutate in mutations:
        x=copy.deepcopy(full); mutate(x)
        try: inspect(x,receipt['source_sha256'])
        except AssertionError: pass
        else: raise AssertionError('Mutation escaped: '+name)
    print('PASS: three fixed packets, 36 derivative views, units, precision, missing observations and twelve adverse mutations')
    print('No QuantLib execution, arbitrary prose assessment, hedge or agent qualification.')


if __name__=='__main__':
    main()
