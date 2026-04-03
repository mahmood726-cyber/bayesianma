Mahmood Ahmad
Tahir Heart Institute
author@example.com

BayesianMA: Browser-Based Bayesian Random-Effects Meta-Analysis with Prior Sensitivity Analysis

Can Bayesian random-effects meta-analysis with prior sensitivity analysis be performed entirely in a browser without requiring R, Stan, or specialized installation? The tool implements a normal-normal hierarchical model and was validated on two canonical datasets: eight magnesium-for-MI trials and six aspirin-for-stroke-prevention trials. Posterior computation uses grid approximation over a 200-by-200 mu-tau grid with a normal prior for the grand mean and half-Cauchy prior for heterogeneity. For the magnesium dataset the posterior OR mean was -0.53 (95% credible interval -1.27 to 0.13) under a weakly informative prior with half-Cauchy 0.5. Sensitivity analysis across vague, weakly informative, and skeptical priors showed that posterior means varied by less than 0.15 while credible interval widths changed by up to 40%. The tool enables clinicians to quantify the influence of prior assumptions on pooled conclusions through direct probability statements rather than p-values. Grid approximation is limited to two-parameter models and may not scale to complex hierarchical structures with additional random-effect layers.

Outside Notes

Type: methods
Primary estimand: Posterior mean and 95% credible interval
App: BayesianMA v1.0
Data: Magnesium-for-MI (8 trials) and Aspirin-for-stroke (6 trials) datasets
Code: https://github.com/mahmood726-cyber/bayesianma
Version: 1.0
Certainty: moderate
Validation: DRAFT

References

1. Roever C. Bayesian random-effects meta-analysis using the bayesmeta R package. J Stat Softw. 2020;93(6):1-51.
2. Higgins JPT, Thompson SG, Spiegelhalter DJ. A re-evaluation of random-effects meta-analysis. J R Stat Soc Ser A. 2009;172(1):137-159.
3. Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.

AI Disclosure

This work represents a compiler-generated evidence micro-publication (i.e., a structured, pipeline-based synthesis output). AI (Claude, Anthropic) was used as a constrained synthesis engine operating on structured inputs and predefined rules for infrastructure generation, not as an autonomous author. The 156-word body was written and verified by the author, who takes full responsibility for the content. This disclosure follows ICMJE recommendations (2023) that AI tools do not meet authorship criteria, COPE guidance on transparency in AI-assisted research, and WAME recommendations requiring disclosure of AI use. All analysis code, data, and versioned evidence capsules (TruthCert) are archived for independent verification.
