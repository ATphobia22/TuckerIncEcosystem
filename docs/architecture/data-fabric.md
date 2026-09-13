# TuckerInc.82 Data Fabric

## Pipeline

`source -> bounded fetch -> raw evidence -> validation -> canonical record -> provenance -> freshness -> current state -> API/consumers`

## Source classes

- `realtime`: source itself publishes continuously or event-driven.
- `near_realtime`: source publishes frequently enough for operational monitoring but not continuously.
- `daily`: expected daily refresh.
- `periodic`: publisher-controlled update cadence.
- `rolling`: continuously available application/program state.
- `static_reference`: reference material; not a live feed.

Polling frequency never changes the underlying source class.

## Integrity

Every canonical record can carry:

- source identifier and registered origin;
- retrieval and observation timestamps in UTC;
- schema version;
- geographic scope;
- horizontal CRS and vertical datum when applicable;
- freshness state;
- SHA-256 content hash;
- provenance chain.

## Security

External payloads are untrusted. The current ingestion adapter requires HTTPS, a registered source origin, bounded payload size, bounded timeout, JSON object shape, and schema validation before accepting a record.

## Engineering separation

Visualization may consume canonical engineering data but does not become the engineering authority. Safety-critical control decisions are outside the generic data-fabric API.
