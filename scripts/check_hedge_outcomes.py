"""Fixed hedge packet checks, not a prose evaluator or solver invocation."""
from copy import deepcopy
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT/'examples/hedge-outcomes'


def number(value):
    assert not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(value)
    return value


def equal(actual, expected, tolerance=1e-8):
    assert abs(number(actual)-number(expected)) <= tolerance, (actual, expected)


def review(packet):
    assert packet['subject'] == 'TOY-HEDGE r1'
    assert packet['original_limit_standard_lots'] == [-1, 1]
    assert set(packet['periods']) == {'training', 'later'}
    populations = {}
    for name, records in packet['periods'].items():
        assert len(records) == 4 and len({r['id'] for r in records}) == 4
        times = [datetime.fromisoformat(r['observed_at'].replace('Z', '+00:00')) for r in records]
        assert len(set(times)) == 4
        x = [number(r['hedge_pnl_thousand_usd_per_lot']) for r in records]
        y = [number(r['position_pnl_thousand_usd']) for r in records]
        a, b, c = sum(v*v for v in x), sum(u*v for u, v in zip(x, y)), sum(v*v for v in y)
        assert a > 0 and c > 0
        assert packet['quadratic_reference'][name] == [a, -2*b, c]
        equal(packet['correlations'][name]['standard_lot'], b/math.sqrt(a*c))
        equal(packet['correlations'][name]['basket'], b/math.sqrt(a*c))
        populations[name] = x, y, a, b, c, times
    assert set(packet['fits']) == {'S1','S2','S3','S4','S5'}
    for identity, fit in packet['fits'].items():
        x,y,a,b,c,_ = populations[fit['period']]
        scale = number(fit['scale_standard_lots'])
        assert scale in (1,100)
        h = number(fit['coefficient'])*scale
        target = min(1,max(-1,b/a)) if identity in ('S4','S5') else b/a
        equal(h,target,1e-10)
        sse = sum((yi-h*xi)**2 for xi,yi in zip(x,y))
        if identity in ('S4','S5'):
            assert fit['bounds'] == [-1/scale,1/scale]
            assert fit['success'] is True and fit['status'] == 1
            equal(fit['cost'],sse/2)
            assert len(fit['residuals']) == 4
            for actual,xi,yi in zip(fit['residuals'],x,y): equal(actual,h*xi-yi)
        else:
            assert fit['rank'] == 1 and fit['returned'] is True
            assert len(fit['residual_sums']) == len(fit['singular_values']) == 1
            equal(fit['residual_sums'][0],sse)
            equal(fit['singular_values'][0],scale*math.sqrt(a))
    assert [r['id'] for r in packet['candidates']] == ['C1','C2','C3','C4','C5','C6']
    findings = []
    for row in packet['candidates']:
        h = number(row['coefficient'])*number(row['standard_lots_per_unit'])
        equal(row['standard_lots'],h)
        assert set(row['periods']) == {'training','later'}
        for period,summary in row['periods'].items():
            x,y,_,_,base,_ = populations[period]
            residual = [yi-h*xi for xi,yi in zip(x,y)]
            mean = sum(residual)/4
            sse = sum(v*v for v in residual)
            assert summary['count'] == 4 and len(summary['residuals_thousand_usd']) == 4
            for actual,expected in zip(summary['residuals_thousand_usd'],residual): equal(actual,expected)
            equal(summary['sse_million_usd_squared'],sse)
            equal(summary['mean_thousand_usd'],mean)
            equal(summary['population_variance_million_usd_squared'],sum((v-mean)**2 for v in residual)/4)
            equal(summary['baseline_sse_million_usd_squared'],base)
            equal(summary['sse_reduction'],1-sse/base)
        if row['fit'] is None:
            assert row['id'] == 'C1' and h == 0
            timing = 'fixed baseline'
        else:
            fit = packet['fits'][row['fit']]
            equal(row['coefficient'],fit['coefficient'],1e-10)
            selected = row['selected_at']
            if selected is None:
                timing = 'unresolved'
            else:
                stamp = datetime.fromisoformat(selected.replace('Z', '+00:00'))
                fit_end = max(populations[fit['period']][5])
                later_start = min(populations['later'][5])
                later_end = max(populations['later'][5])
                if stamp <= fit_end: timing = 'before fitting data complete'
                elif stamp < later_start: timing = 'recorded advance selection'
                elif stamp > later_end: timing = 'retrospective selection'
                else: timing = 'overlapping evaluation period'
        findings.append({'candidate':row['id'],'standard_lots':h,'within_limit':abs(h)<=1+1e-10,'timing':timing,
                         'later_reduction':row['periods']['later']['sse_reduction']})
    return findings


if __name__ == '__main__':
    receipt = json.loads((EXAMPLE/'receipt.json').read_text())
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    assert digest(EXAMPLE/'model/measure.py') == receipt['source_sha256']
    assert digest(EXAMPLE/'model/README.md') == receipt['plan_sha256']
    packets = {case:json.loads((EXAMPLE/'inputs'/f'{case}.json').read_text()) for case in receipt['case_sha256']}
    findings = {}
    for case,packet in packets.items():
        assert digest(EXAMPLE/'inputs'/f'{case}.json') == receipt['case_sha256'][case]
        findings[case] = review(packet)
    restored = deepcopy(packets['missing-selection-time']);restored['candidates'][1]['selected_at'] = packets['complete']['candidates'][1]['selected_at']
    assert restored == packets['complete']
    restored = deepcopy(packets['contradictory']);assert len(restored.pop('producer_claims')) == 7
    original = deepcopy(packets['complete']);original.pop('producer_claims');assert restored == original
    assert findings['missing-selection-time'][1]['timing'] == 'unresolved'
    assert findings['missing-selection-time'][1]['within_limit'] is False
    equal(findings['missing-selection-time'][1]['later_reduction'],-4)
    assert findings['complete'][3]['timing'] == 'retrospective selection'
    assert [f['within_limit'] for f in findings['complete']] == [True,False,True,True,False,False]
    mutations = [
        ('wrong later denominator',lambda d:d['candidates'][1]['periods']['later'].__setitem__('baseline_sse_million_usd_squared',50)),
        ('wrong sign',lambda d:d['candidates'][1]['periods']['later']['residuals_thousand_usd'].__setitem__(0,-7)),
        ('lost observation',lambda d:d['periods']['later'].pop()),
        ('duplicate identity',lambda d:d['periods']['later'][1].__setitem__('id','later-1')),
        ('wrong variance denominator',lambda d:d['candidates'][1]['periods']['later'].__setitem__('population_variance_million_usd_squared',100/3)),
        ('wrong position unit',lambda d:d['candidates'][5].__setitem__('standard_lots',2)),
        ('native cost doubled',lambda d:d['fits']['S4'].__setitem__('cost',20)),
        ('unconverted bounds',lambda d:d['fits']['S5'].__setitem__('bounds',[-1,1])),
        ('changed coefficient',lambda d:d['fits']['S1'].__setitem__('coefficient',1)),
        ('missing residual',lambda d:d['candidates'][2]['periods']['later']['residuals_thousand_usd'].pop()),
        ('false correlation',lambda d:d['correlations']['training'].__setitem__('basket',1)),
        ('positive deterioration',lambda d:d['candidates'][1]['periods']['later'].__setitem__('sse_reduction',4)),
        ('wrong quadratic',lambda d:d['quadratic_reference']['training'].__setitem__(0,-10)),
        ('Boolean coefficient',lambda d:d['candidates'][1].__setitem__('coefficient',True)),
        ('NaN coefficient',lambda d:d['candidates'][1].__setitem__('coefficient',float('nan'))),
        ('missing candidate',lambda d:d['candidates'].pop()),
    ]
    rejected=[]
    for name,mutate in mutations:
        packet=deepcopy(packets['complete']);mutate(packet)
        try: review(packet)
        except (AssertionError,KeyError,ValueError,TypeError): rejected.append(name)
        else: raise AssertionError('Undetected mutation: '+name)
    timing_controls=[]
    for stamp,expected in [('2026-09-24T20:00:00Z','before fitting data complete'),('2026-09-25T20:00:00Z','overlapping evaluation period'),('2026-09-30T21:00:00Z','retrospective selection')]:
        packet=deepcopy(packets['complete']);packet['candidates'][1]['selected_at']=stamp
        assert review(packet)[1]['timing']==expected;timing_controls.append(expected)
    report=(EXAMPLE/'sample-results/report.md').read_text()
    identities=re.findall(r'`([^`]+)` — SHA-256 `([0-9a-f]{64})`',report)
    assert len(identities)==11
    for path,sha in identities: assert digest(ROOT/path)==sha,path
    print(json.dumps({'cases':findings,'rejected_mutations':rejected,'timing_controls':timing_controls,'source_identities':len(identities),'scope':'Fixed numerical records and authored timing; no solver call, arbitrary prose assessment or agent qualification.'},indent=2))
