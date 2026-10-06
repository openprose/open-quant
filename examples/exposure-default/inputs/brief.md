# Synthetic joint exposure/default review

Review TOY-EXPOSURE-DEFAULT r1 at t=0 for T=1 year. Potential positive exposure X takes USD-million values 10, 50 and 100 with marginal probabilities 1/2, 3/10 and 1/5. Default by T is indicator I with probability 1/10. All probabilities belong to one stipulated measure, with no empirical or market-implied estimation. Loss is (3/5)XI, paid at T and discounted by 20/21. This deliberately simplified timing excludes closeout, collateral, netting, earlier settlement, own default and recovery dynamics.

Six proposed joint tables have neutral identifiers J1–J6. For exposure state i, the default cell d_i is its joint probability with I=1; its nondefault cell is p_i−d_i. A probability law requires nonnegative cells and the specified marginals. Treat record identifiers and any producer statements as labels or claims, not proof of a property. Native aggregate quantities are reported observations whose input support must be examined; a reported total does not supply unavailable cells.

The packet also contains two native LP records, exact reference witnesses and the common marginal specification. For any nonnegative default allocation of total mass PD, exposure bounds imply 10*PD <= sum(x_i*d_i) <= 100*PD. An endpoint is attainable here when the corresponding exposure state has sufficient mass. Identify the scope of any bound and what the native candidate actually supports.

The question concerns mathematical validity and interpretation of the supplied evidence. No actual institution, approved policy, calibrated CVA model, regulatory EAD, accounting allowance or financial action is supplied or requested.
