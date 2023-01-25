# 11. Repository Structure

Date: 2022-11-22

## Status

Accepted

## Context

As meant to contain a whole ML pipeline, this repository have a lot of contents.
A consequence of that is that a cristal clear structure is needed.

## Decision

Folders are defined by goals:
- ct/ contains files used to prepare and create Vertex Custom Jobs, as explained in [0010-ci-cd-ct-pipeline.md](0010-ci-cd-ct-pipeline.md)
- data/ is an empty folder to save data in workspace.
- docs/ contains documentation files.
    - adr/ contains Architecture Definition Records.
    - other files could be automatically generated and define data schemas.
- metrics/ contains experimentation metric files. General validations results can be found in [validation_results.json](../../metrics/validation_results.json).
Controlled by dvc.
- params/ contains parameters used by dvc to control experiment executions.
- serving/ contains code to configure the server for model productionalization.
- src/ contains our pipeline code. Development is performed here mostly.
- trained_model/ contains the trained model.
- utils/ contains code that could be used in different contexts.
- the repo root keeps configuration and repo definition files.
