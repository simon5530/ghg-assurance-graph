# Historical source and wheel reproduction

The earlier v0.3.0a1 source/wheel reproduction completed on a fresh hosted
runner: [run 36382755169](https://github.com/simon5530/ghg-assurance-graph/actions/runs/36382755169).
It is historical software-environment evidence, not current dataset validation.

The superseded company-comparison execution harness and its scheduled workflow
are removed from the current tree. Do not use historical outputs as current
acceptance evidence. Current reproduction uses the [MOENV synthetic training case](../examples/moenv_training/README.md)
and the existing synthetic regression workflow. Historical Git tags and release
assets have not been rewritten or deleted. Fresh-host verification of the new
MOENV case is separate and must be evidenced by current CI.
