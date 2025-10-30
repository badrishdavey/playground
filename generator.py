import csv
import random
from datetime import datetime, timedelta

def generate_sample_csv(filename: str, num_records: int = 1000000):
    """
    Generate a sample CSV file with realistic sales data.
    Format: YYYYMMDD, ProductID, StoreId, SalePrice(USD), Status
    """
    print(f"Generating {num_records:,} sample records...")
    print(f"Output file: {filename}")
    print("-" * 60)
    
    start_time = datetime.now()
    
    # Define realistic data ranges
    statuses = ['active', 'inactive', 'pending', 'cancelled']
    status_weights = [0.6, 0.2, 0.15, 0.05]  # 60% active, 20% inactive, etc.
    
    # Product categories with different price ranges
    product_categories = {
        'Electronics': (50.0, 2000.0),
        'Clothing': (15.0, 200.0),
        'Food': (5.0, 50.0),
        'Furniture': (100.0, 1500.0),
        'Books': (10.0, 60.0),
        'Toys': (8.0, 100.0)
    }
    
    # Generate dates for the past year
    end_date = datetime(2024, 12, 31)
    start_date = datetime(2024, 1, 1)
    
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write header
        writer.writerow(['YYYYMMDD', 'ProductID', 'StoreId', 'SalePrice(USD)', 'Status'])
        
        # Generate records
        for i in range(num_records):
            # Generate random date
            days_between = (end_date - start_date).days
            random_days = random.randint(0, days_between)
            random_date = start_date + timedelta(days=random_days)
            date_str = random_date.strftime('%Y%m%d')
            
            # Generate product ID with category prefix
            category = random.choice(list(product_categories.keys()))
            category_prefix = category[:3].upper()
            product_id = f"{category_prefix}{random.randint(1000, 9999)}"
            
            # Generate store ID (100 stores)
            store_id = f"ST{random.randint(1, 100):03d}"
            
            # Generate price based on product category
            price_range = product_categories[category]
            price = round(random.uniform(price_range[0], price_range[1]), 2)
            
            # Generate status with weighted distribution
            status = random.choices(statuses, weights=status_weights)[0]
            
            # Write row
            writer.writerow([date_str, product_id, store_id, price, status])
            
            # Progress update every 100,000 records
            if (i + 1) % 100000 == 0:
                elapsed = (datetime.now() - start_time).total_seconds()
                rate = (i + 1) / elapsed
                remaining = (num_records - i - 1) / rate
                print(f"Progress: {i + 1:,}/{num_records:,} records "
                      f"({(i + 1)/num_records*100:.1f}%) - "
                      f"Rate: {rate:,.0f} records/sec - "
                      f"ETA: {remaining:.0f}s")
    
    # Final summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n" + "=" * 60)
    print("Sample Data Generation Complete!")
    print("=" * 60)
    print(f"Total records: {num_records:,}")
    print(f"Output file: {filename}")
    print(f"File size: {get_file_size(filename)}")
    print(f"Generation time: {duration:.2f} seconds")
    print(f"Records per second: {num_records/duration:,.0f}")
    print("=" * 60)
    
    # Show sample of data
    print("\nFirst 10 rows preview:")
    print("-" * 60)
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            if i < 11:  # Header + 10 rows
                print(line.strip())
            else:
                break


def get_file_size(filename: str) -> str:
    """Get human-readable file size."""
    import os
    size_bytes = os.path.getsize(filename)
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def generate_smaller_sample(filename: str, num_records: int = 1000):
    """
    Generate a smaller sample for quick testing.
    """
    print(f"Generating small sample with {num_records:,} records...")
    
    statuses = ['active', 'inactive', 'pending']
    
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['YYYYMMDD', 'ProductID', 'StoreId', 'SalePrice(USD)', 'Status'])
        
        for i in range(num_records):
            date = f"2024{random.randint(1,12):02d}{random.randint(1,28):02d}"
            product_id = f"P{random.randint(1000, 9999)}"
            store_id = f"ST{random.randint(1, 20):03d}"
            price = round(random.uniform(10.0, 500.0), 2)
            status = random.choice(statuses)
            
            writer.writerow([date, product_id, store_id, price, status])
    
    print(f"Small sample created: {filename} ({get_file_size(filename)})")


def generate_data_with_anomalies(filename: str, num_records: int = 100000):
    """
    Generate sample data that includes some anomalies for testing error handling.
    """
    print(f"Generating {num_records:,} records with intentional anomalies...")
    
    statuses = ['active', 'inactive', 'pending', 'Active', 'ACTIVE', '']  # Mixed case and empty
    
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['YYYYMMDD', 'ProductID', 'StoreId', 'SalePrice(USD)', 'Status'])
        
        for i in range(num_records):
            date = f"2024{random.randint(1,12):02d}{random.randint(1,28):02d}"
            product_id = f"P{random.randint(1000, 9999)}"
            store_id = f"ST{random.randint(1, 50):03d}"
            
            # Introduce some anomalies
            if i % 10000 == 0:
                # Bad price (non-numeric)
                price = "INVALID"
            elif i % 7500 == 0:
                # Negative price
                price = round(random.uniform(-50.0, -10.0), 2)
            else:
                # Normal price
                price = round(random.uniform(10.0, 500.0), 2)
            
            status = random.choice(statuses)
            
            writer.writerow([date, product_id, store_id, price, status])
    
    print(f"Data with anomalies created: {filename}")


if __name__ == "__main__":
    # Option 1: Generate full 1 million records (takes ~30-60 seconds)
    print("Generating FULL dataset (1 million records)...")
    generate_sample_csv("sales_data.csv", num_records=10)
    
    print("\n" + "="*60 + "\n")
    
    # Option 2: Generate smaller sample for quick testing
    print("Generating SMALL test dataset (10,000 records)...")
    generate_smaller_sample("sales_data_small.csv", num_records=10)
    
    print("\n" + "="*60 + "\n")
    
    # Option 3: Generate data with anomalies for testing error handling
    print("Generating dataset with ANOMALIES (100,000 records)...")
    generate_data_with_anomalies("sales_data_anomalies.csv", num_records=10)
    
    print("\n" + "="*60)
    print("All sample files generated successfully!")
    print("="*60)
    print("\nGenerated files:")
    print("1. sales_data.csv - Full dataset (1 million records)")
    print("2. sales_data_small.csv - Small test dataset (10,000 records)")
    print("3. sales_data_anomalies.csv - Dataset with errors (100,000 records)")
    print("\nYou can now run the processing script on these files.")