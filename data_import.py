import pandas as pd
from sqlalchemy import create_engine
from config import DB_CONFIG
import os

IMPORT_ORDER = {
    "product_category_name_translation": "product_category_name_translation.csv",
    "customers": "olist_customers_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "products": "olist_products_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv"
}

def import_data():
    try:
        db_connection_str = (
            f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
            f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        )
        engine = create_engine(db_connection_str)
        datasets_path = 'datasets' # Убедитесь, что ваши CSV лежат в папке 'datasets'
        
        print("Starting data import process...")
        
        for table_name, csv_file in IMPORT_ORDER.items():
            file_path = os.path.join(datasets_path, csv_file)
            
            if os.path.exists(file_path):
                print(f"  > Loading '{csv_file}' into '{table_name}' table...")
                
                df = pd.read_csv(file_path)
                df.to_sql(table_name, engine, if_exists='append', index=False)
                
                print(f"  > Successfully loaded {len(df)} rows.")
            else:
                print(f"  ! Warning: File '{csv_file}' not found at '{file_path}'. Skipping.")
        
        print("\nData import process finished successfully.")

    except Exception as e:
        print(f"An error occurred during data import: {e}")

if __name__ == '__main__':
    import_data()