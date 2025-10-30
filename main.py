import csv
from typing import Generator, List, Dict
from datetime import datetime


def read_csv_generator(filename: str) -> Generator[Dict[str, str], None, None]:
    """
    Generator to read CSV file line by line.
    Yields each row as a dictionary.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield row


def filter_active_records(records: Generator) -> Generator[Dict[str, str], None, None]:
    """
    Filter generator that only yields records with status == 'active'.
    """
    for record in records:
        if record.get('Status', '').lower() == 'active':
            yield record


def transform_record(record: Dict[str, str]) -> Dict[str, any]:
    """
    Transform a single record:
    - Convert price string to float
    - Add 20% tax
    - Parse date
    """
    try:
        price = float(record['SalePrice(USD)'])
        price_with_tax = round(price * 1.20, 2)
        
        return {
            'Date': record['YYYYMMDD'],
            'ProductID': record['ProductID'],
            'StoreId': record['StoreId'],
            'OriginalPrice': price,
            'PriceWithTax': price_with_tax,
            'Status': record['Status']
        }
    except (ValueError, KeyError) as e:
        print(f"Error transforming record: {record}. Error: {e}")
        return None


def transform_records(records: Generator) -> Generator[Dict[str, any], None, None]:
    """
    Transform generator that processes each record.
    """
    for record in records:
        transformed = transform_record(record)
        if transformed:
            yield transformed


def batch_generator(records: Generator, batch_size: int = 1000) -> Generator[List[Dict], None, None]:
    """
    Batch generator that yields groups of records.
    """
    batch = []
    for record in records:
        batch.append(record)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    
    # Yield remaining records
    if batch:
        yield batch


def write_batch_to_file(filename: str, batch: List[Dict], mode: str = 'a', write_header: bool = False):
    """
    Write a batch of records to output file.
    """
    if not batch:
        return
    
    with open(filename, mode, newline='', encoding='utf-8') as file:
        fieldnames = batch[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        if write_header:
            writer.writeheader()
        
        writer.writerows(batch)


def process_large_csv(input_file: str, output_file: str, batch_size: int = 1000):
    """
    Main function to process large CSV file with memory optimization.
    """
    print(f"Starting processing of {input_file}...")
    start_time = datetime.now()
    
    # Initialize counters
    total_read = 0
    total_filtered = 0
    total_written = 0
    batch_count = 0
    
    # Create processing pipeline using generators
    records = read_csv_generator(input_file)
    filtered = filter_active_records(records)
    transformed = transform_records(filtered)
    batches = batch_generator(transformed, batch_size)
    
    # Process batches
    for i, batch in enumerate(batches):
        # Write first batch with header
        write_header = (i == 0)
        mode = 'w' if i == 0 else 'a'
        
        write_batch_to_file(output_file, batch, mode=mode, write_header=write_header)
        
        batch_count += 1
        total_written += len(batch)
        
        # Progress update
        if batch_count % 100 == 0:
            print(f"Processed {batch_count} batches ({total_written:,} records written)")
    
    # Final summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n" + "="*60)
    print("Processing Complete!")
    print("="*60)
    print(f"Total records written: {total_written:,}")
    print(f"Total batches: {batch_count}")
    print(f"Processing time: {duration:.2f} seconds")
    print(f"Records per second: {total_written/duration:,.0f}")
    print(f"Output file: {output_file}")
    print("="*60)


# Alternative: Single pipeline function with inline transformations
def process_csv_optimized(input_file: str, output_file: str, batch_size: int = 1000):
    """
    More compact version with inline processing.
    """
    print(f"Processing {input_file}...")
    
    batch = []
    batch_count = 0
    total_written = 0
    first_batch = True
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        
        for row in reader:
            # Filter: only active status
            if row.get('Status', '').lower() != 'active':
                continue
            
            # Transform: convert price and add tax
            try:
                price = float(row['SalePrice(USD)'])
                price_with_tax = round(price * 1.20, 2)
                
                transformed = {
                    'Date': row['YYYYMMDD'],
                    'ProductID': row['ProductID'],
                    'StoreId': row['StoreId'],
                    'OriginalPrice': price,
                    'PriceWithTax': price_with_tax,
                    'Status': row['Status']
                }
                
                batch.append(transformed)
                
                # Write batch when it reaches batch_size
                if len(batch) >= batch_size:
                    mode = 'w' if first_batch else 'a'
                    write_batch_to_file(output_file, batch, mode=mode, write_header=first_batch)
                    
                    batch_count += 1
                    total_written += len(batch)
                    
                    if batch_count % 100 == 0:
                        print(f"Processed {batch_count} batches ({total_written:,} records)")
                    
                    batch = []
                    first_batch = False
                    
            except (ValueError, KeyError) as e:
                print(f"Skipping invalid row: {e}")
                continue
    
    # Write remaining records
    if batch:
        mode = 'w' if first_batch else 'a'
        write_batch_to_file(output_file, batch, mode=mode, write_header=first_batch)
        total_written += len(batch)
    
    print(f"\nComplete! {total_written:,} records written to {output_file}")


# Example usage
if __name__ == "__main__":
    input_filename = "sales_data.csv"
    output_filename = "processed_sales.csv"
    
    # Method 1: Modular approach with separate generators
    process_large_csv(input_filename, output_filename, batch_size=1000)
    
    # Method 2: Optimized single-pass approach
    # process_csv_optimized(input_filename, output_filename, batch_size=1000)