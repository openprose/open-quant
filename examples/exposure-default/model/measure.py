"""Fixed joint exposure/default expectations and two bounded native LP solves."""
import hashlib
import json
import platform
import sys
import time
from datetime import datetime, timezone
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import linprog


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main(output):
    start = time.perf_counter()
    x = list(map(F, [10, 50, 100])); p = [F(1, 2), F(3, 10), F(1, 5)]
    pd, lgd, discount = F(1, 10), F(3, 5), F(20, 21)
    mean = sum(a*b for a,b in zip(x,p)); marginal_product = discount*lgd*mean*pd
    X, P = np.array(x, dtype=float), np.array(p, dtype=float)
    proposals = {
        "independent": [F(1,20), F(3,100), F(1,50)],
        "low-exposure-default": [F(1,10), F(0), F(0)],
        "middle-exposure-default": [F(0), F(1,10), F(0)],
        "high-exposure-default": [F(0), F(0), F(1,10)],
        "dependent-zero-covariance": [F(3,50), F(3,250), F(7,250)],
        "invalid-negative-cell": [F(-1,100), F(11,100), F(0)]}
    controls = []
    def check(name, value, expected, unit="dimensionless"):
        error = abs(float(value)-float(expected))
        controls.append(dict(id=name,value=float(value),reference=float(expected),unit=unit,absolute_error=error,passed=error<=1e-10))
    records=[]
    for name, d in proposals.items():
        n = [a-b for a,b in zip(p,d)]; weighted=sum(a*b for a,b in zip(x,d))
        exact = dict(default_cells=list(map(str,d)), nondefault_cells=list(map(str,n)),
            admissible=all(0<=a<=b for a,b in zip(d,p)) and sum(d)==pd,
            independent=all(a==b*pd for a,b in zip(d,p)),
            mean_exposure_million_usd=str(mean),default_weighted_exposure_million_usd=str(weighted),
            exposure_ratio_on_default_million_usd=str(weighted/pd),
            conditional_default_given_exposure=list(map(str,[a/b for a,b in zip(d,p)])),
            covariance_exposure_default_million_usd=str(weighted-mean*pd),
            discounted_loss_million_usd=str(discount*lgd*weighted),
            marginal_product_million_usd=str(marginal_product))
        D=np.array(d,dtype=float); N=P-D; W=float(X@D)
        native=dict(default_cells=D.tolist(),nondefault_cells=N.tolist(),
            exposure_marginal=(D+N).tolist(),default_probability=float(sum(D)),
            total_probability=float(sum(D)+sum(N)),mean_exposure_million_usd=float(X@(D+N)),
            default_weighted_exposure_million_usd=W,exposure_ratio_on_default_million_usd=W/float(pd),
            conditional_default_given_exposure=(D/P).tolist(),
            covariance_exposure_default_million_usd=W-float(X@P)*float(pd),
            discounted_loss_million_usd=float(discount*lgd)*W,
            marginal_product_million_usd=float(discount*lgd)*float(X@P)*float(pd))
        for i in range(3):
            check(f"{name}:default-cell-{i}",D[i],d[i]);check(f"{name}:nondefault-cell-{i}",N[i],n[i])
            check(f"{name}:exposure-marginal-{i}",native['exposure_marginal'][i],p[i])
            check(f"{name}:conditional-default-{i}",native['conditional_default_given_exposure'][i],d[i]/p[i])
        check(f"{name}:pd",native['default_probability'],pd)
        check(f"{name}:total",native['total_probability'],1)
        for key in ['mean_exposure_million_usd','default_weighted_exposure_million_usd','exposure_ratio_on_default_million_usd','covariance_exposure_default_million_usd','discounted_loss_million_usd','marginal_product_million_usd']:
            check(name+':'+key,native[key],F(exact[key]),"USD million")
        records.append(dict(id=name,native=native,exact=exact))
    solves=[]
    for name, sign, witness in [('minimum',1,proposals['low-exposure-default']),('maximum',-1,proposals['high-exposure-default'])]:
        result=linprog(sign*X,A_eq=[[1.,1.,1.]],b_eq=[float(pd)],bounds=[(0,float(v)) for v in p],method='highs',options={'maxiter':100,'time_limit':10.0})
        candidate=None if result.x is None else result.x.tolist()
        native=dict(success=bool(result.success),status=int(result.status),message=str(result.message),
            candidate_default_cells=candidate,objective=None if result.fun is None else float(result.fun),iterations=int(result.nit))
        for key in ['eqlin','lower','upper']:
            field=getattr(result,key,None)
            native[key]=None if field is None else {k:None if field.get(k) is None else np.asarray(field[k]).tolist() for k in ['residual','marginals']}
        exact_objective=sum(a*b for a,b in zip(x,witness))
        if candidate is not None:
            check(name+':candidate-sum',sum(candidate),pd)
            check(name+':native-objective',result.fun,sign*(X@result.x),"USD million")
            if result.success:
                check(name+':sharp-bound',sign*result.fun,exact_objective,"USD million")
        solves.append(dict(id=name,native=native,reference=dict(default_cells=list(map(str,witness)),
            default_weighted_exposure_million_usd=str(exact_objective),discounted_loss_million_usd=str(discount*lgd*exact_objective))))
    result=dict(schema='exposure-default-study-v1',recorded_at=datetime.now(timezone.utc).isoformat(),
        source_sha256=sha(Path(__file__)),plan_sha256=sha(Path(__file__).with_name('README.md')),
        environment=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,platform=platform.platform()),
        specification=dict(exposure_million_usd=list(map(str,x)),exposure_probabilities=list(map(str,p)),
            default_probability=str(pd),loss_fraction=str(lgd),discount_factor=str(discount),horizon_years=1,
            probability_basis='One stipulated measure; no empirical or market estimate',loss_timing='All loss paid at T=1 year',
            numeric_absolute_tolerance='1e-10'),proposals=records,optimizations=solves,controls=controls,calculation_seconds=time.perf_counter()-start)
    with Path(output).open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(proposals=len(records),optimizations=len(solves),controls=len(controls),passed=sum(c['passed'] for c in controls))))
    if not all(c['passed'] for c in controls):raise SystemExit(1)


if __name__=='__main__':main(sys.argv[1])
