import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import DB_CONFIG

def create_database():
    temp_config = DB_CONFIG.copy()
    db_name = temp_config.pop("database") 
    temp_config["dbname"] = "postgres"
    
    conn = None
    try:
        print("Connecting to PostgreSQL server...")
        conn = psycopg2.connect(**temp_config)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        cur = conn.cursor()
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        exists = cur.fetchone()
        
        if not exists:
            print(f"Database '{db_name}' does not exist. Creating...")
            cur.execute(f"CREATE DATABASE {db_name}")
            print(f"Database '{db_name}' created successfully.")
        else:
            print(f"Database '{db_name}' already exists.")

        cur.close()

    except (Exception, psycopg2.Error) as error:
        print(f"Error while connecting to or working with PostgreSQL: {error}")
    finally:
        if conn:
            conn.close()
            print("PostgreSQL connection closed.")

if __name__ == '__main__':
    create_database()