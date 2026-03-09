# End-to-End OLTP → RAW → Analytics Data Pipeline

A data engineering pipeline that ingests transactional data from an OLTP database,
loads it into a RAW ingestion layer, and transforms it into analytics-ready tables.

The OLTP data is generated using synthetic ecommerce data generators to simulate
real-world transactional workloads.

Pipeline architecture:

OLTP → RAW → Transform → Analytics

