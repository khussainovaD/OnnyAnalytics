import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os
import plotly.express as px

plt.style.use('seaborn-v0_8-poster')
from config import DB_CONFIG

db_connection_str = (
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)
db_engine = create_engine(db_connection_str)

bar_chart_query = """
--
SELECT
    t.product_category_name_english AS category,
    AVG(r.review_score) AS average_score,
    AVG(oi.freight_value) AS average_freight_value
FROM
    order_items AS oi
JOIN
    products AS p ON oi.product_id = p.product_id
JOIN
    order_reviews AS r ON oi.order_id = r.order_id
JOIN
    product_category_name_translation AS t ON p.product_category_name = t.product_category_name
GROUP BY
    t.product_category_name_english
HAVING
    COUNT(oi.product_id) > 50
ORDER BY
    average_score DESC
LIMIT 5;
"""

pie_chart_query = """
-- "Каково распределение способов оплаты для топ-3 самых продаваемых категорий товаров?"
SELECT
    t.product_category_name_english AS category,
    op.payment_type
FROM
    order_payments AS op
JOIN
    order_items AS oi ON op.order_id = oi.order_id
JOIN
    products AS p ON oi.product_id = p.product_id
JOIN
    product_category_name_translation AS t ON p.product_category_name = t.product_category_name
WHERE
    t.product_category_name_english IN (
        SELECT
            t2.product_category_name_english
        FROM
            order_items oi2
        JOIN
            products p2 ON oi2.product_id = p2.product_id
        JOIN
            product_category_name_translation t2 ON p2.product_category_name = t2.product_category_name
        GROUP BY
            t2.product_category_name_english
        ORDER BY
            COUNT(oi2.order_item_id) DESC
        LIMIT 3
    );
"""

hbar_chart_query= """
-- "Топ-10 городов по средней сумме чека"
SELECT
    c.customer_city,
    AVG(op.payment_value) as average_payment
FROM
    order_payments AS op
JOIN
    orders AS o ON op.order_id = o.order_id
JOIN
    customers AS c ON o.customer_id = c.customer_id
GROUP BY
    c.customer_city
ORDER BY
    average_payment DESC
LIMIT 10;
"""

line_chart_query = """
-- "Как менялось общее количество проданных товаров по месяцам?"
SELECT
    DATE_TRUNC('month', o.order_purchase_timestamp)::DATE AS month,
    COUNT(oi.order_item_id) AS items_sold
FROM
    orders AS o
JOIN
    order_items AS oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY
    month
ORDER BY
    month;
"""

histogram_query = """
-- "Каково распределение цен на товары в категории 'Компьютеры и аксессуары'?"
SELECT
    oi.price
FROM
    order_items AS oi
JOIN
    products AS p ON oi.product_id = p.product_id
JOIN
    product_category_name_translation AS t ON p.product_category_name = t.product_category_name
WHERE
    t.product_category_name_english = 'computers_accessories' AND oi.price < 500; -- Ограничим цену для наглядности
"""

scatter_plot_query = """
-- Собираем данные о количестве фото и среднем рейтинге для каждого товара
SELECT
    p.product_id,
    p.product_photos_qty,
    AVG(r.review_score) AS avg_review_score
FROM
    products AS p
JOIN
    order_items AS oi ON p.product_id = oi.product_id
JOIN
    order_reviews AS r ON oi.order_id = r.order_id
WHERE
    p.product_photos_qty IS NOT NULL
GROUP BY
    p.product_id, p.product_photos_qty
HAVING
    COUNT(r.review_id) > 5
LIMIT 1000;
"""

interactive_plot_query = """
-- Собираем агрегированные данные по месяцам для интерактивного графика
SELECT
    TO_CHAR(o.order_purchase_timestamp, 'YYYY-MM') AS year_month,
    t.product_category_name_english AS category,
    AVG(oi.price) AS average_price,
    AVG(r.review_score) AS average_review_score,
    COUNT(o.order_id) AS order_count
FROM
    orders AS o
JOIN
    order_items AS oi ON o.order_id = oi.order_id
JOIN
    order_reviews AS r ON o.order_id = r.order_id
JOIN
    products AS p ON oi.product_id = p.product_id
JOIN
    product_category_name_translation AS t ON p.product_category_name = t.product_category_name
WHERE
    o.order_status = 'delivered' AND
    p.product_category_name IS NOT NULL
GROUP BY
    year_month, category
HAVING
    COUNT(o.order_id) > 20 -- Убираем категории со слишком малым числом заказов в месяц
ORDER BY
    year_month, category;
"""

def create_bar_chart(df, filename="bar_chart_avg_freight.png"):
    print(f"\n--- столбчатая диаграмма ---")
    print(f"Получено {len(df)} строк данных.")

    plt.figure(figsize=(12, 7)) 
    
    plt.bar(df['category'], df['average_freight_value'], color='skyblue')

    plt.title('Средняя стоимость доставки для топ-5 категорий по рейтингу', fontsize=16)
    plt.xlabel('Категория товаров', fontsize=12)
    plt.ylabel('Средняя стоимость доставки (R$)', fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    if not os.path.exists('charts'):
        os.makedirs('charts')
    filepath = os.path.join('charts', filename)
    plt.savefig(filepath)
    
    print(f"График сохранен в '{filepath}'")
    plt.show()

def create_pie_chart(df, filename="pie_chart_payment_types.png"):
    print(f"\n--- Создание круговой диаграммы ---")
    payment_counts = df['payment_type'].value_counts()
    print(f"Получено {len(df)} строк данных о платежах.")

    fig, ax = plt.subplots(figsize=(10, 10))
    
    ax.pie(payment_counts, labels=payment_counts.index, autopct='%1.1f%%',
           startangle=140, pctdistance=0.85, colors=plt.cm.Pastel1.colors)
    
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig.gca().add_artist(centre_circle)
    
    ax.set_title('Способы оплаты в топ-3 категориях товаров', fontsize=18, fontweight='bold', pad=20)
    ax.axis('equal')
    
    plt.tight_layout()
    
    filepath = os.path.join('charts', filename)
    plt.savefig(filepath)
    print(f"График сохранен в '{filepath}'")
    plt.show()

def create_hbar_chart(df, filename="hbar_chart_avg_payment_city.png"):
    print(f"\n--- Создание горизонтальной столбчатой диаграммы ---")
    print(f"Получено {len(df)} строк данных.")

    df_sorted = df.sort_values(by='average_payment', ascending=True)

    fig, ax = plt.subplots(figsize=(12, 8))
    
    bars = ax.barh(df_sorted['customer_city'], df_sorted['average_payment'], color='#8FBC8F')

    ax.set_title('Топ-10 городов по средней сумме чека', fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel('Средняя сумма чека (R$)', fontsize=14, labelpad=15)
    ax.set_ylabel('Город', fontsize=14, labelpad=15)

    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.25)

    plt.tight_layout()
    
    filepath = os.path.join('charts', filename)
    plt.savefig(filepath)
    print(f"График сохранен в '{filepath}'")
    plt.show()

def create_line_chart(df, filename="line_chart_items_sold.png"):
    print(f"\n--- Создание линейного графика ---")
    print(f"Получено {len(df)} строк данных.")
    
    df['month'] = pd.to_datetime(df['month'])

    fig, ax = plt.subplots(figsize=(14, 7))
    
    ax.plot(df['month'], df['items_sold'], marker='o', linestyle='-', color='indigo')

    ax.set_title('Динамика количества проданных товаров по месяцам', fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel('Месяц', fontsize=14, labelpad=15)
    ax.set_ylabel('Количество проданных товаров', fontsize=14, labelpad=15)

    ax.tick_params(axis='x', labelsize=12, rotation=45)
    ax.tick_params(axis='y', labelsize=12)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, linestyle='--', which='major', color='grey', alpha=.25)

    plt.tight_layout()
    
    filepath = os.path.join('charts', filename)
    plt.savefig(filepath)
    print(f"График сохранен в '{filepath}'")
    plt.show()

def create_histogram(df, filename="histogram_prices_computers.png"):
    print(f"\n--- Создание гистограммы ---")
    print(f"Получено {len(df)} строк данных.")

    fig, ax = plt.subplots(figsize=(12, 7))
    
    ax.hist(df['price'], bins=30, color='crimson', edgecolor='black')

    ax.set_title("Распределение цен на товары в категории 'Компьютеры и аксессуары'", fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel('Цена (R$)', fontsize=14, labelpad=15)
    ax.set_ylabel('Частота (количество товаров)', fontsize=14, labelpad=15)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    
    filepath = os.path.join('charts', filename)
    plt.savefig(filepath)
    print(f"График сохранен в '{filepath}'")
    plt.show()

def create_scatter_plot(df, filename="scatter_plot_photos_vs_rating.png"):
    print(f"\n--- Создание диаграммы рассеяния ---")
    print(f"Получено {len(df)} строк данных.")

    fig, ax = plt.subplots(figsize=(12, 7))
    
    ax.scatter(df['product_photos_qty'], df['avg_review_score'], alpha=0.5, color='darkorange')

    ax.set_title('Связь между количеством фото и средним рейтингом товара', fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel('Количество фотографий у товара', fontsize=14, labelpad=15)
    ax.set_ylabel('Средний рейтинг', fontsize=14, labelpad=15)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, linestyle='--', which='major', color='grey', alpha=.25)

    plt.tight_layout()
    
    filepath = os.path.join('charts', filename)
    plt.savefig(filepath)
    print(f"График сохранен в '{filepath}'")
    plt.show()

def create_interactive_plot(df):
    print(f"\n--- Создание интерактивного графика ---")
    print(f"Получено {len(df)} строк данных для анимации.")

    df = df.sort_values(by="year_month")

    fig = px.scatter(
        df,
        x="average_price",
        y="average_review_score",
        size="order_count",                              # Размер пузырька зависит от количества заказов
        color="category",                                # Цвет зависит от категории
        hover_name="category",       
        animation_frame="year_month",                    # Ключевой параметр: создает ползунок по этой колонке
        animation_group="category", 
        log_x=True,                                     
        range_x=[10, 500],                               
        range_y=[1, 5],
        labels={
             "average_price": "Средняя цена (R$)",
             "average_review_score": "Средний рейтинг",
             "order_count": "Количество заказов",
             "category": "Категория"
        }
    )
    fig.update_layout(
        title_text='Эволюция категорий товаров: Цена vs Рейтинг',
        xaxis_title='Средняя цена (Логарифмическая шкала)',
        yaxis_title='Средний рейтинг (1-5)',
        legend_title_text='Категории'
    )

    print("Открывается интерактивный график в вашем браузере...")
    fig.show(renderer="browser")

if __name__ == "__main__":
    try:
        # # 1. Столбчатая диаграмма (уже была)
        # df_bar = pd.read_sql(bar_chart_query, db_engine)
        # create_bar_chart(df_bar)
        
        # # 2. Круговая диаграмма
        # df_pie = pd.read_sql(pie_chart_query, db_engine)
        # create_pie_chart(df_pie)
        
        # # 3. Горизонтальная столбчатая диаграмма
        # df_hbar = pd.read_sql(hbar_chart_query, db_engine)
        # create_hbar_chart(df_hbar)
        
        # # 4. Линейный график
        # df_line = pd.read_sql(line_chart_query, db_engine)
        # create_line_chart(df_line)
        
        # # 5. Гистограмма
        # df_hist = pd.read_sql(histogram_query, db_engine)
        # create_histogram(df_hist)
        
        # # 6. Диаграмма рассеяния
        # df_scatter = pd.read_sql(scatter_plot_query, db_engine)
        # create_scatter_plot(df_scatter)

        # 7. Интерактивный график
        df_interactive = pd.read_sql(interactive_plot_query, db_engine)
        create_interactive_plot(df_interactive)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
