# 2. Data Analysis and Experiment Management

Date: 2022-11-22

## Status

Accepted

## Context

This project development is performed in a MLOps-compliant environment.
Experiments cant be satisfactorily mantained over Jupyter notebooks.
Not using notebooks (or using them only in a very sketchy phase) means experimentation
pipeline (data recovering, preparation, model training and evaluation) have
to be managed in some other way.
To comply with MLOps good practices, experiments should be easily triggered and shared,
and reproducible.

## Decision

We are going to use DVC for experiment management, with GIT for version control.

## Consequences

Experiment pipeline is configured in [dvc.yaml](../../dvc.yaml).
Experiment execution info is stored in [dvc.lock](../../dvc.lock) (non human readable).
Dvc data remote storage is GCS.
`dvc repro` executes pipeline steps that have changed.
`dvc exp` manages experiments (see [DVC exp documentation](https://dvc.org/doc/command-reference/exp)).
New experiment executions are persisted and shown as GIT commits.
New experiment configurations and thought paths are persisted and shown as GIT branches.
Branching strategy is needed (see [0003-branch-strategy.md](0003-branch-strategy.md))
