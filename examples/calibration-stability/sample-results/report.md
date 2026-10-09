# Calibration stability report

Authored illustration for complete; not an agent-generated result or institutional approval.

## Scope and available support

The selected packet retains all twenty-one requested cases, each solved in physical and integrated coordinates: forty-two native solutions. Eight matrix condition numbers cover both coordinates at four interval spacings. The supplied model is synthetic. Baseline a=0.04 and b=0.09 are variance rates per year; q1 and q2 are dimensionless total variances. There are no empirical observations or institutional acceptance limits. [Brief; complete.native_cases; complete.spacings]

At any positive epsilon, a=q1 and b=(q2-q1)/epsilon uniquely solve the two equations. That exact-input uniqueness does not determine how uncertain b is when the inputs vary. Under the stipulated independent box of ±0.00004 in each total variance, b varies by ±0.00008/epsilon. Opposing input shifts attain those extrema. Common shifts leave b unchanged because their difference is unchanged. Neither finding specifies a probability distribution. [Brief; complete.native_cases, common-up/common-down/steepen/flatten]

## Physical uncertainty and coordinates

| Epsilon (years) | Physical condition number | Integrated condition number | Raw b interval (variance/year) | Admissible b interval |
|---|---:|---:|---|---|
| 1 | 4 | 4 | [0.08992, 0.09008] | [0.08992, 0.09008] |
| 1/12 | 26 | 4 | [0.08904, 0.09096] | [0.08904, 0.09096] |
| 1/365 | 732 | 4 | [0.0608, 0.1192] | [0.0608, 0.1192] |
| 1/3650 | 7302 | 4 | [-0.202, 0.382] | [0, 0.382] |

The intervals follow analytically from the brief's exact inputs. Native steepen and flatten records corroborate the endpoints within the parameter tolerance. The admissible interval requires b≥0; a remains positive throughout the box. At the shortest spacing, q1=q2=0.04 lies within the allowed box because its q2 change has magnitude 0.09/3650, below 0.00004. This gives b=0; continuity and the upper-corner witness establish every value in the admissible interval. The additional native boundary case corroborates that endpoint. These are sharp bounds under the stipulated model and input set, not statistical confidence intervals. [Brief; complete.native_cases; complete.spacings]

The physical matrix's infinity-norm condition number is 2(1+epsilon)/epsilon, while the integrated matrix's is 4. The recorded 1/365 physical value is 732.0000000000001, displayed as 732. These meet the stated relative tolerance. In integrated coordinates the second parameter is u=epsilon*b; recovering b divides by epsilon. The better condition number describes that coordinate representation, not a reduction in uncertainty about b. [Brief matrix definitions; complete.spacings.native_conditions]

The marginal interval for a is [0.03996, 0.04004], but arbitrary combinations with b's interval need not satisfy the joint input box. At the shortest spacing, a=0.04004 and b=0.382 each attain a marginal maximum, yet together imply q2≈0.0401446575342466, exceeding its upper bound ≈0.0400646575342466 by 0.00008. In general, this pair gives q2_baseline+3*eta instead of at most q2_baseline+eta. Native common-up supplies the high a and steepen supplies the high b in different cases; combining them is a derivation, not an observation of one supported native state. [Brief; complete.native_cases: common-up and steepen]

## Native accuracy and admissibility

All forty-two solves return normally. All retained native repricing residuals are zero against the binary64 inputs. Mapping integrated solutions to physical rates agrees with direct physical solutions within 1e-10 variance/year; comparison with the exact rational design has maximum absolute parameter difference about 1.35e-14. Residual and condition criteria pass at their stated numerical scope. A recorded zero is a floating-point calculation result, not a guarantee of exact real arithmetic or exact input observations. [Requirements; complete.native_cases.solves; brief]

The shortest-spacing flatten solution has b approximately -0.202 and is inadmissible as a variance rate, despite native success and an exact numerical fit. Both coordinate systems return the same adverse finding. It is retained without clipping. All other supplied cases have nonnegative physical rates. Thus accurate solving, unique exact-input identification, variance admissibility and stability under input uncertainty are separate findings. [complete.native_cases: 1/3650/flatten and other cases]

## Reporting conclusion

The supplied complete packet supports the requested numerical and analytical review. No producer claims are included in this selection. The assumed input box controls the uncertainty conclusion; its real-world appropriateness is unestablished. No fresh model execution, empirical validation, institutional acceptance or savings is claimed. The receipt attributes the source and original calculation; native execution beyond the retained records remains outside this report's evidence. [Receipt; complete.producer_claims]
