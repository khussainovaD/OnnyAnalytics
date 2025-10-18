import time
import random
import uuid
from datetime import datetime
from sqlalchemy import create_engine, text

from config import DB_CONFIG

REFRESH_INTERVAL = 10
orders = 'orders' 
order_reviews = 'order_reviews'
# --------------------------------------------------


DB_CONNECTION_STRING = (
    f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

COMMENTS = [
    (None, None), ("Отлично", "Все супер!"), ("Хорошо", "Неплохо."),
    ("Нормально", "Обычный товар."), ("Плохо", "Не понравилось."),
]

def add_new_review(engine):
    try:
        with engine.connect() as connection:
            print(f"✅ Успешное подключение к базе данных '{DB_CONFIG['database']}'.")

            # 1. Получаем ID доставленных заказов
            query_orders = text(f"SELECT order_id FROM {orders} WHERE order_status = 'delivered'")
            result = connection.execute(query_orders)
            delivered_order_ids = [row[0] for row in result]
            
            if not delivered_order_ids:
                print(f"⚠️ В таблице '{orders}' не найдено доставленных заказов.")
                return

            print(f"Загружено {len(delivered_order_ids)} ID доставленных заказов.")

            # 2. Бесконечный цикл для добавления новых записей
            while True:
                random_order_id = random.choice(delivered_order_ids)
                comment = random.choice(COMMENTS)
                
                # Создаем SQL-запрос с параметрами для безопасности
                insert_query = text(
                    f"""
                    INSERT INTO {order_reviews} (
                        review_id, order_id, review_score, review_comment_title, 
                        review_comment_message, review_creation_date, review_answer_timestamp
                    ) VALUES (
                        :review_id, :order_id, :review_score, :review_comment_title, 
                        :review_comment_message, :review_creation_date, :review_answer_timestamp
                    )
                    """
                )

                # Параметры для вставки
                params = {
                    "review_id": uuid.uuid4().hex,
                    "order_id": random_order_id,
                    "review_score": random.randint(1, 5),
                    "review_comment_title": comment[0],
                    "review_comment_message": comment[1],
                    "review_creation_date": datetime.now(),
                    "review_answer_timestamp": datetime.now()
                }

                # Выполняем запрос
                connection.execute(insert_query, params)
                
                # --- ЭТО САМЫЙ ВАЖНЫЙ ШАГ ---
                # Явно сохраняем изменения в базе данных
                connection.commit()
                # ---------------------------
                
                print(f"🚀 Данные успешно вставлены и сохранены! Оценка: {params['review_score']}.")
                print(f"--- Следующее обновление через {REFRESH_INTERVAL} секунд ---")
                time.sleep(REFRESH_INTERVAL)

    except Exception as e:
        print(f"❌ Произошла критическая ошибка: {e}")

if __name__ == "__main__":
    try:
        db_engine = create_engine(DB_CONNECTION_STRING)
        add_new_review(db_engine)
    except KeyboardInterrupt:
        print("\nСкрипт остановлен.")