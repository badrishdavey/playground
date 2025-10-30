## Sales Data Generator and Processor

A lightweight, memory-efficient toolkit to generate large synthetic sales datasets and process them in streaming batches. The processor filters for active records, transforms prices (adds 20% tax), and writes results incrementally to avoid high memory usage.

---

### Features
- **Generator**: Create realistic CSV sales data at scale (dates, product categories, stores, prices, statuses)
- **Processor (streaming)**: Read → filter active → transform → batch-write without loading the entire file into memory
- **Two processing modes**:
  - Modular pipeline with composable generators
  - Single-pass optimized loop
- **Progress and summaries**: Periodic progress updates and end-of-run metrics

---

### Repository Contents
- `generator.py`: Utilities to generate sample CSV files (full, small, and with anomalies)
- `main.py`: Processing pipeline(s) for large CSVs using batch writes
- `sales_data.csv`: Example generated dataset (can be recreated)
- `sales_data_small.csv`: Small test dataset
- `sales_data_anomalies.csv`: Dataset containing intentional anomalies for testing
- `processed_sales.csv`: Example output produced by the processor

---

### Data Schema
Input schema produced by the generator (`generator.py`):
- `YYYYMMDD` (string): Calendar date, e.g., `20240131`
- `ProductID` (string): Category-prefixed product identifier (e.g., `ELEC1234`)
- `StoreId` (string): Store code formatted as `ST###` (e.g., `ST042`)
- `SalePrice(USD)` (number or string in anomalies): Sale price in USD
- `Status` (string): One of `active`, `inactive`, `pending`, `cancelled` (mixed case and blanks possible in anomaly set)

Output schema produced by the processor (`main.py`):
- `Date` (string): Copied from `YYYYMMDD`
- `ProductID` (string)
- `StoreId` (string)
- `OriginalPrice` (float)
- `PriceWithTax` (float): `OriginalPrice * 1.20` rounded to 2 decimals
- `Status` (string)

---

### Requirements
- Python 3.9+

No external dependencies beyond the Python standard library (`csv`, `datetime`, `random`).

---

### Quick Start
1) Optionally (re)generate sample data:
```bash
python generator.py
```
This will create or refresh:
- `sales_data.csv`
- `sales_data_small.csv`
- `sales_data_anomalies.csv`

2) Process a dataset (default example):
```bash
python main.py
```
This reads `sales_data.csv` and writes `processed_sales.csv` in batches of 1,000.

---

### Usage
#### Generate Data
- Full-sized dataset (adjust `num_records` as needed):
```bash
python -c "from generator import generate_sample_csv; generate_sample_csv('sales_data.csv', num_records=1_000_000)"
```
- Small quick test dataset:
```bash
python -c "from generator import generate_smaller_sample; generate_smaller_sample('sales_data_small.csv', num_records=10_000)"
```
- Dataset with anomalies (for error handling tests):
```bash
python -c "from generator import generate_data_with_anomalies; generate_data_with_anomalies('sales_data_anomalies.csv', num_records=100_000)"
```

#### Process Data (Modular Pipeline)
From `main.py`, the modular pipeline is exposed via `process_large_csv`:
```python
from main import process_large_csv
process_large_csv('sales_data.csv', 'processed_sales.csv', batch_size=1000)
```
Key stages:
- `read_csv_generator` → stream rows from CSV
- `filter_active_records` → keep only rows where `Status == 'active'` (case-insensitive)
- `transform_records` → parse price, compute `PriceWithTax`, map schema
- `batch_generator` → yield batches of `batch_size` for streaming writes

#### Process Data (Single-Pass Optimized)
```python
from main import process_csv_optimized
process_csv_optimized('sales_data.csv', 'processed_sales.csv', batch_size=1000)
```
This performs filtering, transforming, and batching inline for fewer function calls.

---

### CLI Examples
- Process a small dataset quickly:
```bash
python -c "from main import process_large_csv; process_large_csv('sales_data_small.csv', 'processed_sales.csv', batch_size=500)"
```
- Process anomalies dataset (skips invalid rows and logs issues):
```bash
python -c "from main import process_large_csv; process_large_csv('sales_data_anomalies.csv', 'processed_sales.csv', batch_size=2000)"
```

---

### Performance Notes
- Tune `batch_size` to your environment. Larger batches reduce I/O overhead but increase memory per batch.
- The pipeline is streaming; memory usage is proportional to `batch_size`, not total rows.
- Periodic progress logs are emitted every 100 batches (modular) or 100 batches (optimized path).

---

### Error Handling
- Non-numeric or missing `SalePrice(USD)` and missing fields are caught; such rows are skipped with a log message.
- Status filtering is case-insensitive in the modular pipeline. The anomalies dataset intentionally includes mixed casing and blanks to validate robustness.

---

### Troubleshooting
- "File not found": Ensure the input file path exists. Generate data with `generator.py` or set the correct path.
- "Permission denied" on write: Close the output file if open in another program and check directory permissions.
- Empty `processed_sales.csv`: Confirm the input file contains rows with `Status` set to `active`.
- Slow I/O on very large files: Increase `batch_size` moderately (e.g., 5,000–20,000) and ensure you are writing to fast storage.

---

### Extending
- Add new transformations in `transform_record` (e.g., currency conversion, additional computed fields).
- Adjust category distributions and price ranges in `generator.py` to simulate your domain.
- Replace the sink in `write_batch_to_file` to stream into databases or object storage.

---

### License
Provide your preferred license here (e.g., MIT). If omitted, usage is governed by your organization’s policies.
