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
    "top_10_states_by_orders": """
        -- 1. Какое количество заказов приходится на каждый штат? (топ-10 штатов)
        SELECT c.customer_state, COUNT(o.order_id) AS order_count
        FROM orders AS o JOIN customers AS c ON o.customer_id = c.customer_id
        GROUP BY c.customer_state ORDER BY order_count DESC LIMIT 10;
    """,
    "average_delivery_time": """
        -- 2. Какое среднее время доставки заказов?
        SELECT AVG(order_delivered_customer_date - order_purchase_timestamp) AS average_delivery_time
        FROM orders WHERE order_status = 'delivered';
    """,
    "popular_payment_methods": """
        -- 3. Какие способы оплаты самые популярные?
        SELECT payment_type, COUNT(order_id) AS total_payments
        FROM order_payments GROUP BY payment_type ORDER BY total_payments DESC;
    """,
    "avg_score_by_category": """
        -- 4. Какая средняя оценка (review score) у товаров в разных категориях? (топ-10)
        SELECT t.product_category_name_english, AVG(r.review_score) AS average_score
        FROM order_reviews AS r
        JOIN order_items AS oi ON r.order_id = oi.order_id
        JOIN products AS p ON oi.product_id = p.product_id
        JOIN product_category_name_translation AS t ON p.product_category_name = t.product_category_name
        GROUP BY t.product_category_name_english ORDER BY average_score DESC LIMIT 10;
    """,
    "orders_by_month": """
        -- 5. Сколько заказов было сделано в каждом месяце?
        SELECT DATE_TRUNC('month', order_purchase_timestamp)::DATE AS month, COUNT(order_id) AS number_of_orders
        FROM orders GROUP BY month ORDER BY month;
    """,
    "top_10_expensive_products": """
        -- 6. Топ-10 самых дорогих товаров, которые были проданы?
        SELECT p.product_id, t.product_category_name_english, oi.price
        FROM order_items AS oi
        JOIN products AS p ON oi.product_id = p.product_id
        JOIN product_category_name_translation AS t ON p.product_category_name = t.product_category_name
        ORDER BY oi.price DESC LIMIT 10;
    """,
    "review_score_distribution": """
        -- 7. Каково распределение оценок (от 1 до 5) среди всех отзывов?
        SELECT review_score, COUNT(review_id) AS score_count
        FROM order_reviews GROUP BY review_score ORDER BY review_score;
    """,
    "top_10_sellers_by_items": """
        -- 8. Топ-10 продавцов по количеству проданных товаров.
        SELECT seller_id, COUNT(order_item_id) AS items_sold
        FROM order_items GROUP BY seller_id ORDER BY items_sold DESC LIMIT 10;
    """,
    "top_10_avg_freight_by_state": """
        -- 9. Какая средняя стоимость доставки (freight_value) в разные штаты? (топ-10 самых дорогих)
        SELECT c.customer_state, AVG(oi.freight_value) AS average_freight
        FROM order_items AS oi
        JOIN orders AS o ON oi.order_id = o.order_id
        JOIN customers AS c ON o.customer_id = c.customer_id
        GROUP BY c.customer_state ORDER BY average_freight DESC LIMIT 10;
    """,
    "loyal_customers_count": """
        -- 10. Сколько клиентов являются "постоянными" (делали больше одного заказа)?
        SELECT COUNT(*) AS loyal_customers FROM (
            SELECT c.customer_unique_id, COUNT(o.order_id)
            FROM orders AS o JOIN customers AS c ON o.customer_id = c.customer_id
            GROUP BY c.customer_unique_id HAVING COUNT(o.order_id) > 1
        ) AS loyal_customer_counts;
    """
}

def run_analytics():
    """
    Основная функция для подключения к БД, выполнения всех запросов
    и сохранения результатов.
    """
    conn = None
    try:
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**DB_CONFIG)
        print("Connection successful!")

        for query_name, sql_query in QUERIES.items():
            try:
                print(f"\n--- Выполняется запрос: '{query_name}' ---")
                
                df = pd.read_sql_query(sql_query, conn)
                
                print(df)
                
                filename = f"{query_name}.csv"
                df.to_csv(filename, index=False)
                print(f"Результат сохранен в файл '{filename}'")

            except (Exception, psycopg2.Error) as query_error:
                print(f"    !!! Ошибка при выполнении запроса '{query_name}': {query_error}")

    except (Exception, psycopg2.Error) as error:
        print(f"Ошибка при подключении к PostgreSQL: {error}")
    finally:
        if conn:
            conn.close()
            print("\nDatabase connection closed.")

if __name__ == "__main__":
    run_analytics()
