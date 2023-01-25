# 12. Model Versioning Strategy

Date: 2022-12-02

## Status

In progress

## Context

In order to make it possible to mantain models in production, they have to be versioned following some kind of strategy.

## Decision

A variation of semantic versioning will be used.

Versions will be structured by three numbers: `MAJOR.MINOR.PATCH`
- `MAJOR` represents a significant change or improvement to the model, such as a change in model type for a better one.
- `MINOR` represents a change in model tuning, features selection or generation. It's usually what changes in a standard
development cycle.
- `PATCH` represents the training, and gets upgraded on retraining.

## Consequences

`releases` tagging - see [0003-branch-strategy.md](0003-branch-strategy.md) - must be compliant with versioning strategy.
VertexAI's Model Versioning has to be studied to check how to merge it with this versioning strategy.
