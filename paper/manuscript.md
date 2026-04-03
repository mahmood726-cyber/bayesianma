Mahmood Ahmad
Tahir Heart Institute
author@example.com

BayesianMA: Browser-Based Bayesian Meta-Analysis with Prior Sensitivity Analysis

Bayesian meta-analysis provides direct probability statements and quantifies prior influence, but typically requires R or Stan, limiting accessibility for clinicians. BayesianMA is a browser tool implementing a normal-normal hierarchical model with grid approximation over a 200-by-200 mu-tau space, supporting vague, weakly informative, and skeptical priors each with half-Cauchy heterogeneity prior. Automated sensitivity analysis runs all three priors simultaneously, producing overlay posterior plots and tabulating how conclusions shift across assumptions. On the magnesium-for-MI dataset of eight trials, posterior mean log-OR was negative 0.53 under the weakly informative prior (95% credible interval negative 1.27 to 0.13), with means varying less than 0.15 across priors while credible interval widths changed up to 40%. The aspirin dataset showed prior-insensitive benefit with 97.2% posterior probability of risk reduction regardless of prior choice. This tool enables clinicians to perform Bayesian meta-analysis with built-in sensitivity analysis without installation. Grid approximation is limited to two-parameter models and does not scale to complex hierarchical structures.

Outside Notes

Type: methods
Primary estimand: Posterior mean and 95% credible interval
App: BayesianMA v1.0 (1,723 lines)
Data: Magnesium-for-MI (8 trials), Aspirin-for-stroke (6 trials)
Code: https://github.com/mahmood726-cyber/bayesianma
Version: 1.0
Certainty: moderate
Validation: PASS (25 Selenium tests)

References

1. Roever C, Bender R, Dias S, et al. On weakly informative prior distributions for the heterogeneity parameter in Bayesian random-effects meta-analysis. Res Synth Methods. 2021;12(4):448-474.
2. Sutton AJ, Abrams KR. Bayesian methods in meta-analysis and evidence synthesis. Stat Methods Med Res. 2001;10(4):277-303.
3. Higgins JPT, Thompson SG, Spiegelhalter DJ. A re-evaluation of random-effects meta-analysis. J R Stat Soc Ser A. 2009;172(1):137-159.

AI Disclosure

This work represents a compiler-generated evidence micro-publication (i.e., a structured, pipeline-based synthesis output). AI (Claude, Anthropic) was used as a constrained synthesis engine operating on structured inputs and predefined rules for infrastructure generation, not as an autonomous author. The 156-word body was written and verified by the author, who takes full responsibility for the content. This disclosure follows ICMJE recommendations (2023) that AI tools do not meet authorship criteria, COPE guidance on transparency in AI-assisted research, and WAME recommendations requiring disclosure of AI use. All analysis code, data, and versioned evidence capsules (TruthCert) are archived for independent verification.
