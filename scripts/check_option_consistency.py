"""Verify retained quotes, strategy payoffs and spread costs without QuantLib calls."""
import copy
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EXAMPLE=ROOT/"examples/option-consistency"
KS=[80,90,105,110,130]
NODES=[0]+KS+[230]
SPREADS=[F(0),F(1,20),F(1,5)]


def near(a,b,tol=1e-8):
    assert type(a) in (int,float) and math.isfinite(a) and abs(a-b)<=tol,(a,b)


def price(k,s):
    d1=math.log(100/k)/s+s/2;d2=d1-s
    phi=lambda z:(1+math.erf(z/math.sqrt(2)))/2
    return 100*phi(d1)-k*phi(d2)



CLAIMS=[
    'Every quote fits and satisfies parity, so the entire slice is arbitrage-free.',
    'Any negative-cost equal-wing portfolio is an arbitrage opportunity.',
    'A half-spread of 0.20 establishes global absence of arbitrage.',
    'The calculation assumes a shared underlying, which establishes the identity of every selected instrument.',
    'These numerical checks authorize trading and establish production readiness.'
]


def joint_terms_support(legs):
    fields=['underlying','expiry','time_years','style','currency','notional','settlement']
    if any(len({leg[field] for leg in legs if leg[field] is not None})>1 for field in fields):
        return 'breached'
    if any(leg[field] is None for leg in legs for field in fields):return 'unresolved'
    return 'met'


def witness_state(cost,minimum,joint):
    # This particular witness requires a strictly negative cost. Missing terms
    # cannot change known cost, but they limit applicability of the common-S payoff.
    if cost>=0:return 'not_present'
    if joint!='met':return 'unresolved'
    return 'supported' if minimum>=0 else 'not_present'


def verify(d,source_hash):
    """Fixed-record checks with explicit bindings; no arbitrary prose interpretation."""
    assert d['source_sha256']==source_hash
    assert d['subject']=='OPTION-CONSISTENCY-2026-10-06'
    assert d['case'] in ['complete','missing-underlying','contradictory']
    assert d['terms_provenance']=='Synthetic caller stipulations, not actual market instrument records.'
    expected=[dict(strike=k,underlying='U1',expiry='T1',time_years=1,style='European',currency='USD',notional=1,settlement='cash at T1') for k in KS]
    if d['case']=='missing-underlying':expected[3]['underlying']=None
    assert d['selected_instrument_terms']==expected
    terms={r['strike']:r for r in d['selected_instrument_terms']}
    assert d['producer_claims']==([{'id':f'C{i+1}','text':t} for i,t in enumerate(CLAIMS)] if d['case']=='contradictory' else [])
    assert d['inputs']=={'strikes':KS,'authored_call_prices':[21,14,9,8,3],'constant_stddev':.2,
                         'payoff_nodes':NODES,'half_spreads':['0','1/20','1/5']}
    assert d['calculation_assumptions']=={'forward':100,'discount':1,'time_years':1,'displacement':0,
        'option_style':'European','underlying_domain':'nonnegative terminal values',
        'unit':'USD per option, unit notional','market_data':False,
        'same_underlying_maturity_settlement':True,'fractional_positions_permitted':True,
        'simultaneous_quotes_for_quantities_assumed':True,'other_costs_or_constraints_modeled':False,
        'global_arbitrage_free_claim':False,'price_tolerance_usd':1e-8,'stddev_tolerance':1e-9}
    assert [s['id'] for s in d['slices']]==['constant_volatility','authored_quotes']
    findings=[]
    for s in d['slices']:
        assert [q['strike'] for q in s['quotes']]==KS
        for i,q in enumerate(s['quotes']):
            k=q['strike'];p=q['call_mid_usd']
            near(p,price(k,.2) if s['id']=='constant_volatility' else [21,14,9,8,3][i])
            assert float(F(q['call_mid_exact_input']))==p
            assert q['intrinsic_bound_usd']==max(100-k,0) and q['forward_bound_usd']==100
            assert max(100-k,0)<=p<=100
            assert q['native_success'] is True and q['native_error'] is None
            assert q['native_implied_stddev']>0
            near(q['native_implied_stddev'],q['reference_implied_stddev'],1e-9)
            near(price(k,q['reference_implied_stddev']),p)
            near(price(k,q['native_implied_stddev']),q['native_call_usd'])
            near(q['native_call_usd'],p)
            near(q['native_put_usd'],p-100+k)
            near(q['put_from_parity_usd'],p-100+k)
            near(q['repricing_residual_usd'],q['native_call_usd']-p,1e-12)
            near(q['parity_residual_usd'],q['native_call_usd']-q['native_put_usd']-(100-k),1e-12)
        ps=[F(q['call_mid_exact_input']) for q in s['quotes']]
        assert len(s['adjacent_slopes'])==4
        for i,r in enumerate(s['adjacent_slopes']):
            expected=(ps[i+1]-ps[i])/(KS[i+1]-KS[i])
            assert r['strikes']==KS[i:i+2] and F(r['call_slope'])==expected
            assert 'within_vertical_bounds' not in r
            assert F(-1)<=expected<=0
        assert len(s['strategies'])==6
        for index,r in enumerate(s['strategies']):
            i=index//2;k=KS[i:i+3]
            aware=index%2==0
            weights=[F(k[2]-k[1],k[2]-k[0]),F(-1),F(k[1]-k[0],k[2]-k[0])] if aware else [F(1,2),F(-1),F(1,2)]
            assert r['weighting']==('strike_aware' if aware else 'equal_wings')
            assert r['id']==r['weighting']+'_'+str(k[1]) and r['strikes']==k
            assert [F(r[key]) for key in ['lower_weight','middle_weight','upper_weight']]==weights
            assert r['payoff_nodes']==NODES
            payoffs=[sum(w*max(x-strike,0) for w,strike in zip(weights,k)) for x in NODES]
            assert [F(x) for x in r['terminal_payoff_usd']]==payoffs
            assert F(r['tail_slope'])==sum(weights)==0
            assert F(r['minimum_payoff_usd'])==min(payoffs)
            safe=min(payoffs)>=0
            assert 'payoff_nonnegative_for_all_nonnegative_underlying' not in r
            mid=sum(w*p for w,p in zip(weights,ps[i:i+3]))
            assert F(r['mid_cost_usd'])==mid and len(r['costs'])==3
            legs=[terms[j] for j in k]
            joint=joint_terms_support(legs)
            views=[]
            for cost,h in zip(r['costs'],SPREADS):
                expected=sum(w*(p+h if w>0 else p-h) for w,p in zip(weights,ps[i:i+3]))
                assert F(cost['half_spread_usd'])==h and F(cost['purchase_cost_usd'])==expected
                assert 'negative_cost' not in cost and 'nonnegative_payoff_witness' not in cost
                views.append({'half_spread_usd':str(h),'purchase_cost_usd':str(expected),
                              'witness_under_calculation_assumptions':expected<0 and safe,
                              'selected_terms_witness':witness_state(expected,min(payoffs),joint)})
            findings.append({'slice':s['id'],'strategy':r['id'],'joint_terms_support':joint,
                             'minimum_payoff_under_calculation_assumptions':str(min(payoffs)),
                             'cost_views':views})
    return {'quotes':10,'strategies':12,'cost_views':36,'individual_fit':'met','findings':findings,
            'global_arbitrage_freedom':'not_established'}


def main():
    read=lambda p:json.loads(p.read_text())
    digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    receipt=read(EXAMPLE/'receipt.json')
    source_hash=digest(EXAMPLE/receipt['source_path'])
    assert receipt['source_sha256']==source_hash
    assert receipt['plan_sha256']==digest(EXAMPLE/receipt['plan_path'])
    results={};packets={}
    for case,record in receipt['packets'].items():
        p=EXAMPLE/record['path'];assert record['sha256']==digest(p)
        packets[case]=read(p);assert packets[case]['case']==case
        results[case]=verify(packets[case],source_hash)
    assert set(packets)=={'complete','missing-underlying','contradictory'}
    assert results['contradictory']==results['complete']
    complete=results['complete']['findings'];missing=results['missing-underlying']['findings']
    assert all(r['joint_terms_support']=='met' for r in complete)
    assert [r['joint_terms_support'] for r in missing]==['met','met','unresolved','unresolved','unresolved','unresolved']*2
    present=[(r['slice'],r['strategy'],v['half_spread_usd']) for r in complete for v in r['cost_views'] if v['selected_terms_witness']=='supported']
    assert present==[('authored_quotes','strike_aware_110','0'),('authored_quotes','strike_aware_110','1/20')]
    assert not any(v['selected_terms_witness']=='supported' for r in missing for v in r['cost_views'])
    assert [v['selected_terms_witness'] for v in missing[10]['cost_views']]==['unresolved','unresolved','not_present']
    assert [v['selected_terms_witness'] for v in missing[11]['cost_views']]==['unresolved']*3
    assert all(r['cost_views']==m['cost_views'] for r,m in zip(complete,missing) if r['strategy'].endswith('_90'))
    assert witness_state(F(0),F(0),'met')=='not_present'
    assert witness_state(F(-1),F(0),'met')=='supported'
    assert witness_state(F(-1),F(-1),'met')=='not_present'
    assert witness_state(F(-1),F(-1),'unresolved')=='unresolved'
    assert witness_state(F(1),F(-1),'unresolved')=='not_present'
    near(1e-8,0,1e-8)
    try:near(1.00001e-8,0,1e-8)
    except AssertionError:pass
    else:raise AssertionError('Tolerance exceeded unnoticed')
    mutations=[
        ('omit_quote','complete',lambda x:x['slices'][0]['quotes'].pop()),
        ('wrong_strike','complete',lambda x:x['slices'][0]['quotes'][2].update(strike=100)),
        ('changed_root','complete',lambda x:x['slices'][1]['quotes'][0].update(native_implied_stddev=.2)),
        ('broken_parity','complete',lambda x:x['slices'][1]['quotes'][0].update(native_put_usd=2)),
        ('changed_quote','complete',lambda x:x['slices'][1]['quotes'][0].update(call_mid_exact_input='22')),
        ('false_native_success','complete',lambda x:x['slices'][0]['quotes'][0].update(native_success=False)),
        ('omit_strategy','complete',lambda x:x['slices'][0]['strategies'].pop()),
        ('wrong_wing','complete',lambda x:x['slices'][1]['strategies'][4].update(lower_weight='1/2')),
        ('hide_negative_payoff','complete',lambda x:x['slices'][0]['strategies'][5].update(minimum_payoff_usd='0')),
        ('wrong_tail','complete',lambda x:x['slices'][0]['strategies'][0].update(tail_slope='1')),
        ('wrong_spread_side','complete',lambda x:x['slices'][1]['strategies'][4]['costs'][1].update(purchase_cost_usd='-3/10')),
        ('omit_spread','complete',lambda x:x['slices'][1]['strategies'][4]['costs'].pop()),
        ('fill_missing_identity','missing-underlying',lambda x:x['selected_instrument_terms'][3].update(underlying='U1')),
        ('erase_known_identity','complete',lambda x:x['selected_instrument_terms'][3].update(underlying=None)),
        ('change_currency','complete',lambda x:x['selected_instrument_terms'][3].update(currency='EUR')),
        ('global_all_clear','complete',lambda x:x['calculation_assumptions'].update(global_arbitrage_free_claim=True)),
        ('actual_market_claim','complete',lambda x:x['calculation_assumptions'].update(market_data=True)),
        ('inject_answer','complete',lambda x:x['slices'][0]['strategies'][0]['costs'][0].update(nonnegative_payoff_witness=True)),
    ]
    rejected=[]
    for name,case,mutate in mutations:
        altered=copy.deepcopy(packets[case]);mutate(altered)
        try:verify(altered,source_hash)
        except (AssertionError,KeyError,ValueError,TypeError):rejected.append(name)
        else:raise AssertionError('Undetected mutation: '+name)
    print(json.dumps({'cases':3,'quotes_per_case':10,'strategies_per_case':12,'cost_views_per_case':36,
                      'mutations_rejected':rejected,'native_inversions':0,'provider_calls':0}))


if __name__=='__main__':main()
