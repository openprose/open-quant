"""Fixed curve-risk evidence checks; no native valuation or prose evaluation."""
from copy import deepcopy
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EX=ROOT/'examples/quote-sensitivity'
FLOWS={'four_percent':[40000,1040000],'six_percent':[60000,1060000]}
FACTORS={'quote_1':('quote',[1,0]),'quote_2':('quote',[0,1]),'quote_parallel':('quote',[1,1]),'zero_1':('zero',[1,0]),'zero_2':('zero',[0,1]),'zero_parallel':('zero',[1,1])}


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def close(actual,expected,tolerance=1e-8):
    assert isinstance(actual,(int,float)) and not isinstance(actual,bool) and math.isfinite(actual)
    assert abs(actual-expected)<=tolerance,(actual,expected)


def review(packet):
    assert packet['subject']=='SYNTHETIC-PAR-CURVE r1'
    assert packet['cashflows_usd']==FLOWS and packet['principal_usd']==1000000
    assert packet['times_years']==[1,2] and packet['base_par_quotes']==[.03,.04]
    assert packet['shock_size_decimal']==.0001 and packet['reference_date']=='2026-01-01'
    rows=packet['scenarios'];by_id={r['id']:r for r in rows}
    expected={'base'}|{f'{f}_{s}' for f in FACTORS for s in ['plus','minus']}
    assert len(rows)==len(by_id)==13 and set(by_id)==expected
    base=[1/1.03,(1-.04/1.03)/1.04]
    findings={}
    for name,row in by_id.items():
        if name=='base':kind,mask,sign='base',[0,0],0
        else:
            factor,direction=name.rsplit('_',1);kind,mask=FACTORS[factor];sign=1 if direction=='plus' else -1
        assert row['coordinate']==kind and row['factor_mask']==mask and row['direction']==sign
        close(row['shock_decimal'],sign*.0001,1e-18)
        values=row['values_usd'];assert set(values) <= set(FLOWS)
        nodes=row.get('discount_nodes')
        if nodes is not None:
            assert len(nodes)==2 and set(values)==set(FLOWS)
            assert 0<nodes[1]<nodes[0]<1
            findings[name]='direct node records'
        elif set(values)==set(FLOWS):
            a,b=values['four_percent'],values['six_percent']
            nodes=[.000052*b-.000053*a,.000003*a-.000002*b]
            assert 0<nodes[1]<nodes[0]<1
            findings[name]='derived from two cash-flow equations'
        else:
            assert name=='quote_1_plus' and set(values)=={'four_percent'}
            close(values['four_percent'],1000000)
            assert 'implied_par_quotes' not in row
            findings[name]='q2 supported by par value; q1 underdetermined'
        if nodes is not None:
            for instrument,amounts in FLOWS.items():close(values[instrument],sum(a*b for a,b in zip(amounts,nodes)))
            implied=[1/nodes[0]-1,(1-nodes[1])/sum(nodes)]
            if 'implied_par_quotes' in row:
                assert len(row['implied_par_quotes'])==2
                for actual,target in zip(row['implied_par_quotes'],implied):close(actual,target,1e-10)
            if kind in ['base','quote']:
                target=[.03+sign*.0001*mask[0],.04+sign*.0001*mask[1]]
                assert len(row['requested_par_quotes'])==2
                for actual,wanted in zip(row['requested_par_quotes'],target):close(actual,wanted,1e-12)
                for actual,wanted in zip(implied,target):close(actual,wanted,1e-10)
            else:
                assert row['requested_par_quotes'] is None
                for i in range(2):close(nodes[i],base[i]*math.exp(-(i+1)*sign*.0001*mask[i]),1e-12)
    pairs=set()
    for row in packet['sensitivities']:
        f,k=row['factor'],row['instrument'];assert f in FACTORS and k in FLOWS and (f,k) not in pairs;pairs.add((f,k))
        plus=by_id[f+'_plus']['values_usd'][k];minus=by_id[f+'_minus']['values_usd'][k]
        central=(plus-minus)/2
        close(row['signed_central_change_for_1bp_usd'],central)
        close(row['central_derivative_usd_per_unit_rate'],central/.0001,2e-5)
        close(row['positive_1bp_change_usd'],plus-by_id['base']['values_usd'][k])
    available={(f,k) for f in FACTORS for k in FLOWS if k in by_id[f+'_plus']['values_usd'] and k in by_id[f+'_minus']['values_usd']}
    assert pairs==available
    return findings


def main():
    receipt=json.loads((EX/'receipt.json').read_text());obs=json.loads((EX/'model/observations.json').read_text())
    assert digest(EX/'model/observations.json')==receipt['observation_sha256']
    assert digest(EX/'model/measure.py')==receipt['source_sha256']==obs['source_sha256']
    assert digest(EX/'model/PLAN.md')==receipt['plan_sha256']==obs['plan_sha256']
    assert len(obs['checks'])==110 and all(c['passed'] for c in obs['checks'])
    packets={name:json.loads((EX/f'inputs/{name}.json').read_text()) for name in receipt['case_sha256']}
    for name,packet in packets.items():assert digest(EX/f'inputs/{name}.json')==receipt['case_sha256'][name]
    complete=packets['complete']
    for original,selected in zip(obs['records'],complete['scenarios']):
        expected={k:v for k,v in original.items() if k not in ['decimal_reference_values_usd','target_par_quotes']};expected['requested_par_quotes']=original['target_par_quotes'];assert expected==selected
    assert complete['sensitivities']==[{k:v for k,v in r.items() if k!='analytic_derivative_usd_per_unit_rate'} for r in obs['sensitivities']]
    missing=deepcopy(complete);row=next(r for r in missing['scenarios'] if r['id']=='quote_1_plus')
    for key in ['discount_nodes','implied_par_quotes']:del row[key]
    missing['withheld']=['quote_1_plus.discount_nodes','quote_1_plus.implied_par_quotes']
    assert missing==packets['missing-node-records']
    partial=deepcopy(missing);next(r for r in partial['scenarios'] if r['id']=='quote_1_plus')['values_usd'].pop('six_percent')
    partial['sensitivities']=[r for r in partial['sensitivities'] if (r['factor'],r['instrument'])!=('quote_1','six_percent')]
    partial['withheld']+=['quote_1_plus.values_usd.six_percent','sensitivities[quote_1,six_percent]']
    assert partial==packets['missing-independent-value']
    bad=deepcopy(packets['contradictory']);claims=bad.pop('producer_claims');plain=deepcopy(complete);plain.pop('producer_claims');assert bad==plain and len(claims)==5
    summaries={name:review(packet)['quote_1_plus'] for name,packet in packets.items()}
    assert summaries['missing-node-records']=='derived from two cash-flow equations'
    assert summaries['missing-independent-value']=='q2 supported by par value; q1 underdetermined'
    witnesses=[]
    for a in [F(100,103),F(10000,10301),F(24,25)]:
        b=(1-F(1,25)*a)/F(26,25)
        assert 0<b<a<1 and 40000*a+1040000*b==1000000 and (1-b)/(a+b)==F(1,25)
        witnesses.append(str(1/a-1))
    assert len(set(witnesses))==3
    mutations=[]
    def reject(name,change):
        packet=deepcopy(complete);change(packet)
        try:review(packet)
        except (AssertionError,KeyError,ValueError):mutations.append(name)
        else:raise AssertionError('Undetected '+name)
    reject('missing scenario',lambda d:d['scenarios'].pop())
    reject('duplicate scenario',lambda d:d['scenarios'].append(deepcopy(d['scenarios'][0])))
    reject('changed coordinate',lambda d:d['scenarios'][1].__setitem__('coordinate','zero'))
    reject('changed shock scale',lambda d:d.__setitem__('shock_size_decimal',.01))
    reject('changed direction',lambda d:d['scenarios'][1].__setitem__('direction',-1))
    reject('wrong requested quote',lambda d:d['scenarios'][1]['requested_par_quotes'].__setitem__(0,.04))
    reject('wrong implied quote',lambda d:d['scenarios'][1]['implied_par_quotes'].__setitem__(1,.041))
    reject('wrong node',lambda d:d['scenarios'][1]['discount_nodes'].__setitem__(1,.93))
    reject('missing node',lambda d:d['scenarios'][1]['discount_nodes'].pop())
    reject('wrong value',lambda d:d['scenarios'][1]['values_usd'].__setitem__('four_percent',999996.116699))
    reject('duplicate cash-flow equation',lambda d:d['cashflows_usd'].__setitem__('six_percent',d['cashflows_usd']['four_percent']))
    reject('changed horizon',lambda d:d.__setitem__('times_years',[1,3]))
    reject('changed notional',lambda d:d.__setitem__('principal_usd',10000000))
    reject('wrong central sign',lambda d:d['sensitivities'][1].__setitem__('signed_central_change_for_1bp_usd',189.507096599))
    reject('central used as positive shock',lambda d:d['sensitivities'][1].__setitem__('positive_1bp_change_usd',d['sensitivities'][1]['signed_central_change_for_1bp_usd']))
    reject('missing sensitivity',lambda d:d['sensitivities'].pop())
    rows=[line.split('|')[1:-1] for line in (EX/'sample-results/report.md').read_text().splitlines() if line.startswith('| ')][1:]
    assert len(rows)==6
    for row,factor in zip(rows,FACTORS):
        assert row[0].strip()==factor
        for cell,instrument in zip(row[1:],FLOWS):
            expected=next(r['signed_central_change_for_1bp_usd'] for r in complete['sensitivities'] if (r['factor'],r['instrument'])==(factor,instrument))
            close(float(cell),expected,5e-7)
    print(json.dumps({'cases':summaries,'native_values':26,'numerical_controls':110,'rejected_mutations':len(mutations),'exact_underidentification_witnesses':witnesses,'report_table_cells':12,'scope':'Fixed records, projections and numerical relationships; no native run or prose assessment.'}))


if __name__=='__main__':main()
