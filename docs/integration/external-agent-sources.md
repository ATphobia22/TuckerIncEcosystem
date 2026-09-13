# External agent-skill and context-source assessment

## Tech Leads Club Agent Skills

The registry currently exposes curated skills across architecture, security, development, quality, tooling, and other categories. The useful integration principle for Tucker AI is **skill-as-policy**, not uncontrolled prompt ingestion: skills should be versioned, security-reviewed, and triggered by explicit task boundaries.

Tucker AI therefore treats external skills as optional development-time inputs. Production runtime behavior remains encoded in typed contracts, tests, provenance, and governance modules.

## OpenResearch

OpenResearch's `orx` workflow provides a strong research reproducibility pattern: fixed run contracts, experiment branches, immutable answered nodes, evidence capture, and explicit experiment-tree progression. Tucker AI's benchmark and evidence layers adopt the compatible principles without copying the OpenResearch implementation.

## OpenViking

OpenViking is an AGPLv3 context database organized around `viking://` resources, memories, skills, directory summaries, and layered retrieval. Tucker AI does not copy OpenViking code into the repository. A future deployment can integrate it behind an external-service boundary where its license and operational requirements are preserved.

## system_prompts_leaks

The repository is treated as a research corpus only. Leaked or purported hidden prompts are not accepted as authoritative runtime policy, and no hidden prompt is copied into Tucker AI's governance layer. The useful engineering signal is comparative analysis of agent-tool conventions, not treating leaked instructions as trusted specifications.
