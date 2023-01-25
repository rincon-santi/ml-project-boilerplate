# 3. Branch Strategy

Date: 2022-11-22

## Status

Accepted

## Context

As decided in [0002-data-analysis-and-experiment-management.md], all deployment issues are persisted as git/dvc commits.
In consequence, a strategy to order those commits is extremely necessary.
Aditionally, that strategy must ensure test stage is only performed once.

## Decision

Productionalized code will live in `main` branch.
When an experiment round starts, a `series/...` is branched from `main`. This branch is where experimentation "chaos"
is contained.
`experiment/...` branches is where analysis and development is done. They branch from `series/...` or from other
`experiment/...` branches.
One and only one of the `experiment/...` branches in `series/...` offspring can be merged into `series/...`. This merge is
performed using a Squash strategy. Once it happens, `series/...` can only be either merged into `main` (if test stage
results are satisfying) or abandoned (if not). 
To train or retrain a model in production environment, a release from `main`'s head is open. In this release, training
is performed and committed, getting afterwards merged into `main` with a 'release's tag' resembling model's version,
which politic can be found in [0012-model-versioning-strategy.md](0012-model-versioning-strategy.md)

## Consequences

GC collector over GIT tree could be good.
