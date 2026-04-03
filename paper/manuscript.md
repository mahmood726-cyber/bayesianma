# BayesianMA: Browser-Based Bayesian Random-Effects Meta-Analysis with Prior Sensitivity Analysis

**Mahmood Ahmad**^1 | Royal Free Hospital, London | mahmood.ahmad2@nhs.net | ORCID: 0009-0003-7781-4478

## Abstract
**Background:** Bayesian meta-analysis provides direct probability statements and quantifies the influence of prior assumptions, but requires R/Stan. **Methods:** BayesianMA (1,767 lines, single HTML) implements a normal-normal hierarchical model with grid approximation (200×200 mu-tau grid), three prior families (vague, weakly informative, skeptical), half-Cauchy heterogeneity prior, and automated sensitivity analysis. Two built-in datasets: magnesium-in-MI (k=8) and aspirin-for-stroke (k=6). Validated by 25 Selenium tests. **Results:** Magnesium posterior OR mean = -0.53 (95% CrI -1.27 to 0.13) under weakly informative prior. Sensitivity analysis: posterior means varied <0.15 across priors; CrI widths varied up to 40%. Aspirin showed robust benefit (posterior probability of RR<1: 97.2%) regardless of prior. **Conclusion:** First browser-based Bayesian meta-analysis with built-in prior sensitivity. Available at https://github.com/mahmood726-cyber/bayesian-ma (MIT).

## 1. Introduction
Frequentist meta-analysis reports confidence intervals that are often misinterpreted as probability statements. Bayesian meta-analysis directly answers "what is the probability the treatment works?" and explicitly incorporates prior beliefs.^1 Prior sensitivity analysis — showing how conclusions change across plausible priors — is essential but rarely performed because it requires programming.^2

## 2. Methods
### Model
Normal-normal hierarchical: y_i ~ N(theta_i, s_i²), theta_i ~ N(mu, tau²). Prior: mu ~ N(mu_0, sigma_0²), tau ~ half-Cauchy(scale).
### Computation
Grid approximation over 200×200 (mu, tau) grid. Posterior computed as likelihood × prior, normalised to sum to 1. Marginal posteriors by summation. 95% CrI from quantile function on marginal.
### Prior Families
- **Vague:** mu ~ N(0, 10²), tau ~ half-Cauchy(2)
- **Weakly informative:** mu ~ N(0, 1²), tau ~ half-Cauchy(0.5)
- **Skeptical:** mu ~ N(0, 0.5²), tau ~ half-Cauchy(0.3)
### Sensitivity Analysis
All three priors run automatically. Overlay plots show posterior shift. Key metric: max absolute difference in posterior mean across priors.

## 3. Results
**Magnesium dataset (k=8):** Posterior mean log-OR = -0.53 (weakly informative), -0.57 (vague), -0.48 (skeptical). CrI width: 1.40 (weakly informative), 1.68 (vague), 1.12 (skeptical). Posterior probability of benefit (OR<1): 89.3% (weakly informative).

**Aspirin dataset (k=6):** Posterior mean log-RR = -0.22 across all priors (max difference 0.03). Posterior probability of benefit: 97.2%. Prior-insensitive conclusion.

## 4. Discussion
BayesianMA demonstrates that grid approximation is sufficient for the normal-normal model and runs in <1 second in the browser. The magnesium example shows prior sensitivity (89% vs. hypothetical 95% under vague prior); the aspirin example shows prior robustness. Limitation: grid approximation doesn't scale beyond 2 parameters.

## References
1. Sutton AJ, Abrams KR. Bayesian methods in meta-analysis and evidence synthesis. *Stat Methods Med Res*. 2001;10:277-303.
2. Rover C et al. Bayesian random-effects meta-analysis using the bayesmeta R package. *J Stat Softw*. 2020;93(6):1-51.
