"""Fixed exception-statistics controls; no SciPy, provider or arbitrary prose judgment."""
import copy
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]/'examples/backtest-statistics'
IDS = [f'BT{i:02}' for i in range(1, 7)]
POSITIONS = [[25,75,125,175,225], list(range(123,128)), list(range(1,6)), [],
             list(range(13,239,25)), list(range(121,131))]
SCOPE = {'population_size':250, 'nominal_exception_probability':'1/100',
         'constructed_indicators':True, 'frequency_alternative':'greater',
         'interval_confidence_level':0.95, 'interval_alternative':'two-sided',
         'clustering_alternative':'fewer_one_runs', 'decision_threshold':0.05,
         'overall_acceptance_rule':None}
CLAIMS = [
    'The three five-exception series have identical backtesting conclusions because their counts match.',
    'BT04 proves that the exception probability is zero.',
    'A clustering p-value of one proves independent exception timing.',
    'The two-sided 95% interval is the inversion of the one-sided 5% excess-frequency test used here.',
    'Reported block counts alone verify the actual timing of exceptions even when the ordered sequence is unavailable.',
    'These results establish a valid production VaR model and regulatory approval.',
]


def close(actual, expected, tolerance):
    assert isinstance(actual, (float, int)) and not isinstance(actual, bool)
    assert math.isfinite(actual) and abs(actual-expected) <= tolerance, (actual, expected)


def binomial_probability(p, first, last):
    return math.fsum(math.comb(250,j)*p**j*(1-p)**(250-j) for j in range(first,last+1))


def reject(p):
    return p < F(1,20)


def findings(packet):
    """Separate calculations conditional on aggregates from verified timing support."""
    results = []
    for row in packet['sequences']:
        n,k = row['n'],row['exceptions']
        frequency = F(row['frequency_test']['exact_pvalue'])
        known_order = row['indicators'] is not None and row['exception_positions'] is not None
        r = None
        clustering = None
        if known_order:
            hits = [i for i,x in enumerate(row['indicators']) if x]
            r = int(bool(hits))+sum(b-a>1 for a,b in zip(hits,hits[1:]))
            counts = {0:1} if not k else {b:math.comb(k-1,b-1)*math.comb(n-k+1,b)
                                          for b in range(1,min(k,n-k+1)+1)}
            clustering = F(sum(c for b,c in counts.items() if b<=r), math.comb(n,k))
        results.append({'id':row['id'], 'frequency_decision':'reject' if reject(frequency) else 'not_rejected',
                        'order_support':'verified' if known_order else 'unresolved',
                        'observed_one_runs':r,
                        'clustering_decision':None if clustering is None else (
                            'reject' if reject(clustering) else 'not_rejected'),
                        'timing_information':None if not known_order else 0<k<n})
    return results


def verify(packet, source_hash):
    assert packet['subject']=='BACKTEST-STATISTICS-2026-10-06'
    assert packet['case'] in ['complete','missing-order','contradictory']
    assert packet['source_sha256']==source_hash and packet['scope']==SCOPE
    assert [r['id'] for r in packet['sequences']]==IDS
    for index,(row,positions) in enumerate(zip(packet['sequences'],POSITIONS)):
        missing=packet['case']=='missing-order' and index==1
        k=len(positions)
        assert type(row['n']) is int and row['n']==250
        assert type(row['exceptions']) is int and row['exceptions']==k
        close(row['exception_fraction'],k/250,1e-14)
        assert type(row['one_runs']) is int
        # This fixed-fixture identity is not reconstructed by findings when order is absent.
        assert row['one_runs']==[5,1,1,0,10,1][index]
        if missing:
            assert row['indicators'] is None and row['exception_positions'] is None
        else:
            bits=row['indicators']
            assert len(bits)==250 and all(type(x) is int and x in (0,1) for x in bits)
            actual_positions=[i+1 for i,x in enumerate(bits) if x]
            assert row['exception_positions']==actual_positions==positions
            assert sum(bits)==k
            actual_runs=int(bool(positions))+sum(b-a>1 for a,b in zip(positions,positions[1:]))
            assert row['one_runs']==actual_runs
        f=row['frequency_test']
        expected=sum(F(math.comb(250,j)*99**(250-j),100**250) for j in range(k,251))
        assert f['null_probability']=='1/100' and f['alternative']=='greater'
        assert F(f['exact_pvalue'])==expected
        close(f['native_pvalue'],float(expected),1e-12)
        assert 'reject_at_005' not in f
        ci=row['probability_interval']
        assert (ci['confidence_level'],ci['alternative'],ci['method'])==(0.95,'two-sided','Clopper-Pearson')
        assert len(ci['native'])==len(ci['finite_sum_reference'])==2
        low,high=ci['native']
        assert 0<=low<=k/250<=high<=1
        for actual,reference in zip(ci['native'],ci['finite_sum_reference']):close(actual,reference,1e-10)
        if k:close(binomial_probability(low,k,250),.025,1e-9)
        else:
            assert low==0
            close(high,1-.025**(1/250),1e-10)
        close(binomial_probability(high,0,k),.025,1e-9)
        counts={0:1} if not k else {r:math.comb(k-1,r-1)*math.comb(251-k,r)
                                    for r in range(1,min(k,251-k)+1)}
        assert sum(counts.values())==math.comb(250,k)
        tail=F(sum(c for r,c in counts.items() if r<=row['one_runs']),math.comb(250,k))
        c=row['clustering_test']
        assert c['conditioned_on']==['n','exceptions'] and c['alternative']=='fewer_one_runs'
        assert F(c['exact_pvalue'])==tail
        close(c['pvalue'],float(tail),1e-20)
        assert 'reject_at_005' not in c and 'timing_information' not in c
    expected_claims=[{'id':f'C{i+1}','text':t} for i,t in enumerate(CLAIMS)] if packet['case']=='contradictory' else []
    assert packet['producer_claims']==expected_claims
    result=findings(packet)
    assert [r['frequency_decision'] for r in result]==['not_rejected']*4+['reject']*2
    assert [r['clustering_decision'] for r in result]==[
        'not_rejected',None if packet['case']=='missing-order' else 'reject',
        'reject','not_rejected','not_rejected','reject']
    assert result[3]['timing_information'] is False
    if packet['case']=='missing-order':
        assert result[1]['observed_one_runs'] is None and result[1]['timing_information'] is None
        assert result[1]['order_support']=='unresolved'
    return result


def main():
    digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    receipt=json.loads((ROOT/'receipt.json').read_text())
    source_hash=digest(ROOT/'model/measure.py')
    assert receipt['source_sha256']==source_hash
    assert receipt['plan_sha256']==digest(ROOT/'model/README.md')
    packets={}
    for case in ['complete','missing-order','contradictory']:
        path=ROOT/'inputs'/f'{case}.json'
        assert receipt['packets'][case]=={'path':f'inputs/{case}.json','sha256':digest(path)}
        packets[case]=json.loads(path.read_text())
        verify(packets[case],source_hash)
    missing=copy.deepcopy(packets['complete']);missing['case']='missing-order'
    missing['sequences'][1]['indicators']=None;missing['sequences'][1]['exception_positions']=None
    assert packets['missing-order']==missing
    contrary=copy.deepcopy(packets['complete']);contrary['case']='contradictory'
    contrary['producer_claims']=packets['contradictory']['producer_claims']
    assert packets['contradictory']==contrary
    mutations=[]

    def adverse(label,case,mutate):
        changed=copy.deepcopy(packets[case]);mutate(changed)
        try:verify(changed,source_hash)
        except (AssertionError,KeyError,TypeError,ValueError):mutations.append(label)
        else:raise AssertionError('Undetected mutation: '+label)

    adverse('drop_series','complete',lambda p:p['sequences'].pop())
    adverse('drop_observation','complete',lambda p:p['sequences'][0]['indicators'].pop())
    adverse('wrong_population','complete',lambda p:p['sequences'][0].update(n=249))
    adverse('move_exception','complete',lambda p:p['sequences'][0]['indicators'].reverse())
    adverse('omit_first_block','complete',lambda p:p['sequences'][2].update(one_runs=0))
    adverse('change_nominal_probability','complete',lambda p:p['scope'].update(nominal_exception_probability='1/20'))
    adverse('change_alternative','complete',lambda p:p['sequences'][0]['frequency_test'].update(alternative='two-sided'))
    adverse('zero_interval','complete',lambda p:p['sequences'][3]['probability_interval'].update(native=[0,0]))
    adverse('wrong_interval_alternative','complete',lambda p:p['sequences'][0]['probability_interval'].update(alternative='greater'))
    adverse('wrong_cluster_probability','complete',lambda p:p['sequences'][1]['clustering_test'].update(pvalue=1.0))
    adverse('imputed_order','missing-order',lambda p:p['sequences'][1].update(indicators=packets['complete']['sequences'][1]['indicators']))
    adverse('erase_count_with_order','missing-order',lambda p:p['sequences'][1].update(exceptions=None))
    adverse('erase_other_order','missing-order',lambda p:p['sequences'][2].update(indicators=None))
    adverse('invent_acceptance','complete',lambda p:p['scope'].update(overall_acceptance_rule='approved'))
    adverse('real_forecasts','complete',lambda p:p['scope'].update(constructed_indicators=False))
    adverse('missing_claim','contradictory',lambda p:p['producer_claims'].pop())
    adverse('wrong_source','complete',lambda p:p.update(source_sha256='0'*64))
    assert reject(F(1,20)) is False
    assert reject(F(1,20)-F(1,10**12)) is True
    assert reject(F(1,20)+F(1,10**12)) is False
    print(json.dumps({'packets':3,'series_per_packet':6,'adverse_mutations_rejected':mutations,
                      'strict_threshold_boundaries':'pass','agent_qualification':False}))


if __name__=='__main__':main()
