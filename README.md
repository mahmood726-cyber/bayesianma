# Bayesian MA

Browser-based Bayesian random-effects meta-analysis with grid approximation and prior sensitivity analysis.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Overview

Bayesian MA implements a Normal-Normal hierarchical model for random-effects meta-analysis using numerical grid approximation, entirely in the browser. Users specify priors for the grand mean (Normal) and between-study heterogeneity (Half-Cauchy), then obtain full posterior distributions, shrinkage estimates, and credible intervals. A built-in prior sensitivity analysis runs the model under three prior specifications (Vague, Weakly Informative, Skeptical) to assess robustness of conclusions to prior choice.

## Features

- Normal-Normal hierarchical model: y_i | mu, tau ~ N(mu, sigma_i^2 + tau^2)
- Configurable Normal prior for grand mean mu with user-specified mean and SD
- Half-Cauchy prior for heterogeneity tau (Polson and Scott 2012)
- Numerical grid approximation over a fine (mu, tau) grid for exact posterior computation
- Posterior density plots for both mu and tau
- Bayesian forest plot with study-specific shrinkage estimates and 95% credible intervals
- Shrinkage table showing how each study's estimate is pulled toward the grand mean
- Prior sensitivity analysis across three scenarios (Vague, Weakly Informative, Skeptical)
- Support for multiple effect types: log-OR, log-RR, log-HR, SMD, MD, Fisher's z
- CSV data import with flexible parsing
- Auto-generated methods text for manuscripts
- MAIF (Meta-Analysis Interchange Format) import/export for cross-tool data flow
- Dark mode toggle
- Print-optimized layout

## Quick Start

1. Download `bayesian-ma.html`
2. Open in any modern browser
3. No installation, no dependencies, works offline

## Built-in Examples

- **Magnesium for MI**: 8 trials, log-OR (including ISIS-4, the large-sample outlier)
- **Aspirin for Stroke Prevention**: 6 trials, log-RR

## Methods

- Hierarchical model: y_i ~ N(theta_i, sigma_i^2), theta_i ~ N(mu, tau^2)
- Prior: mu ~ N(m_0, s_0^2), tau ~ Half-Cauchy(scale)
- Grid approximation: joint posterior p(mu, tau | y) evaluated on a 200 x 200 grid
- Marginal posteriors obtained by numerical integration
- Study-specific posteriors (shrinkage): theta_i | y, mu, tau
- Sensitivity analysis: Vague (s_0=10, scale=1), Weakly Informative (s_0=1, scale=0.5), Skeptical (s_0=0.5, scale=0.25)
- Based on: Rover C, Friede T. Bayesian random-effects meta-analysis using the bayesmeta R package. JSS. 2017;93(6).

## Screenshots

> Screenshots can be added by opening the tool and using browser screenshot.

## Validation

- 25/25 Selenium tests pass
- Posterior summaries cross-validated against the R bayesmeta package (Rover and Friede 2017)

## Export

- CSV (posterior summaries, shrinkage estimates)
- JSON (full results)
- MAIF (Meta-Analysis Interchange Format) for cross-tool data flow

## Citation

If you use this tool, please cite:

> Ahmad M. Bayesian MA: A browser-based Bayesian random-effects meta-analysis tool with prior sensitivity analysis. 2026. Available at: https://github.com/mahmood726-cyber/bayesian-ma

## Author

**Mahmood Ahmad**
Royal Free Hospital, London, United Kingdom
ORCID: [0009-0003-7781-4478](https://orcid.org/0009-0003-7781-4478)

## License

MIT
