import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os
import plotly.express as px
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.utils import get_column_letter

plt.style.use('seaborn-v0_8-poster')
from config import DB_CONFIG

db_connection_str = (
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)
db_engine = create_engine(db_connection_str)

def load_query(filename):
    """Загружает SQL-запрос из файла в папке /sql."""
    filepath = os.path.join('sql', filename)
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

bar_chart_query = load_query('bar_chart.sql')
pie_chart_query = load_query('pie_chart.sql')
hbar_chart_query = load_query('hbar_chart.sql')
line_chart_query = load_query('line_chart.sql')
histogram_query = load_query('histogram.sql')
scatter_plot_query = load_query('scatter_plot.sql')
interactive_plot_query = load_query('interactive_plot.sql')

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

    print("Открывается интерактивный график в браузере...")
    fig.show(renderer="browser")

def export_to_excel(dataframes_dict, filename="olist_analytics_report.xlsx"):

    if not os.path.exists('exports'):
        os.makedirs('exports')
    filepath = os.path.join('exports', filename)

    print(f"\n--- Создание отчета в Excel: '{filepath}' ---")
    
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        total_rows = 0
        for sheet_name, df in dataframes_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            total_rows += len(df)
        workbook = writer.book

        for sheet_name, df in dataframes_dict.items():
            worksheet = workbook[sheet_name]

            worksheet.freeze_panes = "A2"
            worksheet.auto_filter.ref = worksheet.dimensions

            for col_idx, column in enumerate(df.columns, 1):
                col_letter = get_column_letter(col_idx)
                
                max_length = max(df[column].astype(str).map(len).max(), len(column)) + 2
                worksheet.column_dimensions[col_letter].width = max_length

                if pd.api.types.is_numeric_dtype(df[column]):
                    cell_range = f"{col_letter}2:{col_letter}{len(df) + 1}"
                    
                    color_scale_rule = ColorScaleRule(
                        start_type='min', start_color='FFEE5858', # Светло-красный
                        end_type='max', end_color='FF63BE7B'     # Светло-зеленый
                    )
                    worksheet.conditional_formatting.add(cell_range, color_scale_rule)
    print(f"✓ Отчет успешно создан.")
    print(f"  - Количество листов: {len(dataframes_dict)}")
    print(f"  - Всего строк экспортировано: {total_rows}")

if __name__ == "__main__":
    try:
        # # 1. Столбчатая диаграмма (уже была)
        # df_bar = pd.read_sql(bar_chart_query, db_engine)
        # create_bar_chart(df_bar)
        
        # # 2. Круговая диаграмма
        # df_pie = pd.read_sql(pie_chart_query, db_engine)
        # create_pie_chart(df_pie)
        
        # # 3. Горизонтальная столбчатая диаграмма ПРИМЕР
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

        # 8.1. Определяем, какие данные мы хотим экспортировать
        # reports_to_export = {
        #     "top_10_sellers": load_query('top_sellers_by_items.sql'),
        #     "sales_by_month": load_query('orders_by_month.sql'),
        #     "avg_freight_by_state": load_query('avg_freight_by_state.sql')
        # }
        
        # # 8.2. Создаем словарь для хранения DataFrame'ов
        # dataframes_for_excel = {}
        
        # print("\n--- Подготовка данных для Excel-отчета ---")
        # for report_name, query in reports_to_export.items():
        #     print(f"Выполняется запрос для отчета: '{report_name}'...")
        #     dataframes_for_excel[report_name] = pd.read_sql(query, db_engine)
        # export_to_excel(dataframes_for_excel)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
