# 10. CI/CD/CT Pipeline

Date: 2022-11-22

## Status

In progress

## Context

Continuous integration, deployment and training must be set.
CRISP-ML(Q) establishes the following automatizable training&integration stages:
- Validation stage
- Test stage
- Deployment stage
- Monitoring stage

## Decision

### Validation stage
We differenciate between temporal validations, made by the analyst while performing
experiments to check those experiment results; and persisted-validations, when the
analyst wants to share experiments with their colleagues, so the validation gets
persisted as a git commit.

Temporal validations are managed by dvc as stated in [0002-data-analysis-and-experiment-management.md](0002-data-analysis-and-experiment-management.md)
[{Decisions about how to automate validation stage}]

### Test stage
Test stage can only be performed once on each experiment round. This is ensured via branch strategy.
Test stage has an unique validation dataset.
[{Decisions about how to automate test stage}]

### Deployment stage
[{Decisions about how to automate deployment stage}]

### Monitoring stage
[{Decisions about how to automate monitoring stage}]

## Consequences

### Validation stage
[{Consequences of decisions about how to automate validation stage}]
Other consequences are covered by [0002-data-analysis-and-experiment-management.md](0002-data-analysis-and-experiment-management.md).

### Test stage
Branch strategy consequences are covered by [0003-branch-strategy.md](0003-branch-strategy.md).
[{Consequences of decisions about how to automate test stage}]

### Deployment stage
[{Consequences of decisions about how to automate deployment stage}]

### Monitoring stage
[{Consequences of decisions about how to automate monitoring stage}]