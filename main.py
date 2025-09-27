import psycopg2
import pandas as pd

DB_CONFIG = {
    "host": "localhost",
    "user": "postgres",       
    "password": "123456",  
    "database": "olist_db",     
    "port": 5432
}

QUERIES = {
    "top_states_by_orders": """
        -- 1. Топ-5 штатов по количеству заказов.
        SELECT
            c.customer_state,
            COUNT(o.order_id) AS order_count
        FROM
            orders AS o
        JOIN
            customers AS c ON o.customer_id = c.customer_id
        GROUP BY
            c.customer_state
        ORDER BY
            order_count DESC
        LIMIT 5;
    """,
    "popular_payment_methods": """
        -- 2. Самые популярные способы оплаты.
        SELECT
            payment_type,
            COUNT(order_id) AS total_payments
        FROM
            order_payments
        GROUP BY
            payment_type
        ORDER BY
            total_payments DESC;
    """
}

def run_analytics():
    conn = None
    try:
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**DB_CONFIG)
        print("Connection successful!")

        print("\n--- 1: Топ-5 штатов по количеству заказов ---")
        df1 = pd.read_sql_query(QUERIES["top_states_by_orders"], conn)
        print(df1)
        
        df1.to_csv("top_states_by_orders.csv", index=False)
        print("файл 'top_states_by_orders.csv'")

        print("\n--- 2: Самые популярные способы оплаты ---")
        df2 = pd.read_sql_query(QUERIES["popular_payment_methods"], conn)
        print(df2)

        # РЕЗУЛЬТАТЫ
        df2.to_csv("popular_payment_methods.csv", index=False)
        print("файл 'popular_payment_methods.csv'")

    except (Exception, psycopg2.Error) as error:
        print(f"Ошибка при работе с PostgreSQL: {error}")
    finally:
        if conn:
            conn.close()
            print("\nDatabase connection closed.")

if __name__ == "__main__":
    run_analytics()
