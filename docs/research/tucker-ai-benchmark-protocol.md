# Tucker AI Benchmark Protocol

## Purpose

This protocol prevents unsupported claims of quantum advantage. A Tucker AI experiment is a research result only when its classical baseline, hybrid model, execution environment, configuration, and uncertainty are recorded together.

## Required comparisons

1. **Classical baseline:** a competitive non-quantum model with documented hyperparameters.
2. **Hybrid model:** the same task with an explicitly identified quantum component.
3. **Noisy model:** when hardware/noise is relevant, report noisy performance separately from ideal simulation.
4. **Mitigated model:** if error mitigation is used, report the unmitigated result alongside the mitigated result.

## Reproducibility

Record:

- dataset identifier and content hash;
- train/validation/test split;
- random seed(s);
- preprocessing configuration;
- model architecture and parameter count;
- quantum circuit depth, width, gates, shots, and measurement observable;
- backend/provider and version;
- simulator versus QPU status;
- optimization algorithm and stopping criteria;
- runtime and resource counts;
- failure/retry information;
- full configuration hash and provenance ID.

## Statistical reporting

Use repeated trials where stochasticity matters. Report point estimates with uncertainty intervals and avoid selecting a single favorable seed. For classification, include task-appropriate metrics rather than accuracy alone when class imbalance or asymmetric error costs exist.

## Quantum-resource accounting

Report qubit count, circuit depth, two-qubit gate count, measurement shots, number of circuit evaluations, wall-clock runtime, accelerator usage, and cloud/QPU task counts where applicable.

## Scientific claim levels

- **Level 0:** implementation verified.
- **Level 1:** reproducible benchmark result.
- **Level 2:** statistically supported improvement over the selected baseline.
- **Level 3:** improvement that survives ablations, noise analysis, and resource accounting.
- **Level 4:** evidence consistent with a meaningful quantum advantage under a clearly stated computational model.

The current Tucker AI implementation makes **no quantum-advantage claim**. The framework exists to make such claims testable rather than assumed.
