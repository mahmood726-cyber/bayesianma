# BayesianMA: A Browser-Based Bayesian Random-Effects Meta-Analysis Engine

Mahmood Ahmad^1 | ^1 Royal Free Hospital, London, UK | mahmood.ahmad2@nhs.net | ORCID: 0009-0003-7781-4478

## Abstract

BayesianMA is a single-file browser application (1,723 lines) that performs Bayesian random-effects meta-analysis entirely client-side. Users specify prior distributions for the pooled effect and between-study variance, and the engine computes posterior distributions via numerical integration. Features include interactive prior specification with visual feedback, posterior density plots, forest plots with credible intervals, posterior predictive distributions, Bayes factors for the null hypothesis, and sensitivity analysis across prior choices. The tool requires no installation, runs offline, and supports dark/light themes. Available at https://github.com/mahmood726-cyber/bayesian-ma.

## Introduction

Frequentist meta-analysis dominates practice, but Bayesian approaches offer advantages: natural incorporation of prior information, direct probability statements about parameters, and coherent handling of small-sample uncertainty. Existing Bayesian MA software requires R (bayesmeta, brms) or BUGS/Stan, creating barriers for clinicians. BayesianMA brings Bayesian inference to the browser with zero dependencies.

## Implementation

The engine implements conjugate and semi-conjugate models for normal-normal hierarchical meta-analysis. Prior specification supports informative, weakly informative, and vague options for both the pooled effect (normal) and heterogeneity (half-normal, inverse-gamma, uniform). Posterior computation uses adaptive Gauss-Hermite quadrature for the marginal posterior of tau, with closed-form conditional posteriors for theta given tau. All computation runs in JavaScript with no external libraries beyond Plotly for visualization.

## Availability

Single HTML file, MIT license. Source: https://github.com/mahmood726-cyber/bayesian-ma

## Funding
None.

## References
1. Rover C, Friede T. Bayesian random-effects meta-analysis using the bayesmeta R package. J Stat Softw. 2017;93(6):1-51.
2. Higgins JPT, et al. Cochrane Handbook. Version 6.4, 2023.
3. Spiegelhalter DJ, et al. Bayesian approaches to clinical trials and health-care evaluation. Wiley; 2004.
