-- ZoroLogistics Lakehouse Intelligence, Medallion Pipeline (Lakeflow / Spark
-- Declarative Pipelines, formerly Delta Live Tables).
--
-- Part of Zorost AI Lab by Zorost Intelligence · zorost.com
--
-- Produces, in catalog/schema set by the bundle (default zrl_.zorologistics):
-- bronze_shipments raw, append-only ingest from a UC volume
-- silver_shipments cleaned + deduplicated + typed, with data-quality expectations
-- gold_on_time_kpis on-time KPIs aggregated by carrier + month
--
-- BEFORE RUNNING: upload the Week-01 `shipments.csv` to a volume:
-- /Volumes/zrl_/zorologistics/raw/shipments.csv
-- (see capstone/README-run.md for the exact upload command)

-- ---------------------------------------------------------------------------
-- BRONZE, raw ingest (Auto Loader, incremental: new CSVs are picked up on update)
-- ---------------------------------------------------------------------------
CREATE OR REFRESH STREAMING TABLE bronze_shipments
AS
SELECT
  _metadata.file_path AS source_file,
  _metadata.file_modification_time AS ingested_at,
  *
FROM STREAM read_files(
  '/Volumes/zrl_/zorologistics/raw/',
  format => 'csv',
  header => true,
  inferSchema => true,
  multiLine => true
);

-- ---------------------------------------------------------------------------
-- SILVER, clean, type, deduplicate, and enforce data quality.
-- A materialized view gives "always correct" semantics over the (small) bronze
-- table: dedup by shipment_id, safe casts, and expectation-driven row dropping.
-- ---------------------------------------------------------------------------
CREATE OR REFRESH MATERIALIZED VIEW silver_shipments
(
  CONSTRAINT valid_shipment_id EXPECT (shipment_id IS NOT NULL AND length(trim(shipment_id)) > 0)
    ON VIOLATION DROP ROW,
  CONSTRAINT valid_ids EXPECT (carrier_id IS NOT NULL AND lane_id IS NOT NULL)
    ON VIOLATION DROP ROW,
  CONSTRAINT valid_weight EXPECT (weight_kg IS NOT NULL AND weight_kg > 0)
    ON VIOLATION DROP ROW,
  CONSTRAINT valid_delay EXPECT (delay_hours IS NOT NULL)
    ON VIOLATION DROP ROW
)
AS
SELECT
  shipment_id,
  carrier_id,
  lane_id,
  commodity,
  CAST(weight_kg AS DOUBLE) AS weight_kg,
  CAST(value_usd AS DOUBLE) AS value_usd,
  CAST(planned_departure AS TIMESTAMP) AS planned_departure,
  CAST(planned_arrival AS TIMESTAMP) AS planned_arrival,
  CAST(actual_arrival AS TIMESTAMP) AS actual_arrival,
  CAST(delay_hours AS DOUBLE) AS delay_hours,
  -- Recompute on-time from the delay ground truth (<= 2h grace) so the flag is
  -- robust to whatever string form the CSV serialized booleans into.
  (CAST(delay_hours AS DOUBLE) <= 2.0) AS is_on_time,
  status,
  weather_severity
FROM (
  SELECT *,
         row_number() OVER (
           PARTITION BY shipment_id
           ORDER BY planned_departure DESC
         ) AS rn
  FROM bronze_shipments
)
WHERE rn = 1;

-- ---------------------------------------------------------------------------
-- GOLD, business-aligned on-time KPIs, aggregated by carrier + month.
-- Batch read (no STREAM) over silver → incrementally refreshable aggregation.
-- ---------------------------------------------------------------------------
CREATE OR REFRESH MATERIALIZED VIEW gold_on_time_kpis
AS
SELECT
  carrier_id,
  date_trunc('MONTH', planned_departure) AS month,
  COUNT(*) AS total_shipments,
  SUM(CASE WHEN is_on_time THEN 1 ELSE 0 END) AS on_time_shipments,
  ROUND(100.0 * SUM(CASE WHEN is_on_time THEN 1 ELSE 0 END) / COUNT(*), 2) AS on_time_pct,
  ROUND(AVG(delay_hours), 2) AS avg_delay_hours,
  SUM(CASE WHEN delay_hours > 48 THEN 1 ELSE 0 END) AS late_48h_shipments
FROM silver_shipments
GROUP BY carrier_id, date_trunc('MONTH', planned_departure);
