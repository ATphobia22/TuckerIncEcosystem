# Project-file integration record

The following project files were reviewed and converted into structured implementation inputs. The original files remain available in the project workspace; this repository stores implementation-safe summaries rather than blindly copying binary documents into the runtime.

## 47620 grant intelligence

`47620_Grant_Master_Matrix.pdf` and `47620_Grant_link Matrix .pdf` define the Mount Vernon / Point Township funding framework and official-source directory. The repository stores the resulting planning baseline in `data/grants/47620_baseline.json` and authoritative source seeds in `data/sources/source_registry.json`.

The source material explicitly states that active federal/state notices must be directly validated before action.

## Tri-State Systems Manager / PTDT

`Tri-State Systems Manager Full Production Engine.pdf` supplies digital-twin, flood comparison, histogram, geospatial, evidence-ledger, and visualization concepts. These are treated as application-layer inputs; calculation authority remains separate from visualization.

## Tucker Power

`Tucker Power Implementation Specification.pdf` supplies power-system architecture, open-source grid tooling, AI governance, cybersecurity, and hydro-development staging concepts. AI governance is represented as a safety boundary: AI can assist forecasting, anomaly detection, inspection prioritization, and scheduling, but cannot independently execute safety-critical grid controls or fabricate evidence.

## Municipal website seed

`Mount Vernon website.txt` supplies the municipal website seed used by the source registry.

## Copied utilities

Selected source-code utilities are copied into `legacy/` with source repository and revision metadata. They are isolated from production runtime until individually validated and adapted.
