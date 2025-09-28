-- 1. какое количество заказов приходится на каждый штат? (топ-10 штатов)
-- Помогает понять географию продаж
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
LIMIT 10;


-- 2. Какое среднее время доставки заказов?
-- Оценивает эффективность логистики
SELECT
    AVG(order_delivered_customer_date - order_purchase_timestamp) AS average_delivery_time
FROM
    orders
WHERE
    order_status = 'delivered';


-- 3. Какие способы оплаты самые популярные?
-- Показывает предпочтения клиентов
SELECT
    payment_type,
    COUNT(order_id) AS total_payments
FROM
    order_payments
GROUP BY
    payment_type
ORDER BY
    total_payments DESC;


-- 4. Какая средняя оценка (review score) у товаров в разных категориях? (топ-10)
-- Помогает выявить самые качественные и некачественные категории товаров
SELECT
    t.product_category_name_english,
    AVG(r.review_score) AS average_score
FROM
    order_reviews AS r
JOIN
    order_items AS oi ON r.order_id = oi.order_id
JOIN
    products AS p ON oi.product_id = p.product_id
JOIN
    product_category_name_translation AS t ON p.product_category_name = t.product_category_name
GROUP BY
    t.product_category_name_english
ORDER BY
    average_score DESC
LIMIT 10;


-- 5. Сколько заказов было сделано в каждом месяце?
-- Позволяет увидеть сезонность продаж
SELECT
    DATE_TRUNC('month', order_purchase_timestamp)::DATE AS month,
    COUNT(order_id) AS number_of_orders
FROM
    orders
GROUP BY
    month
ORDER BY
    month;


-- 6. Топ-10 самых дорогих товаров, которые были проданы?
-- Помогает понять, какие товары приносят максимальный доход за единицу
SELECT
    p.product_id,
    t.product_category_name_english,
    oi.price
FROM
    order_items AS oi
JOIN
    products AS p ON oi.product_id = p.product_id
JOIN
    product_category_name_translation AS t ON p.product_category_name = t.product_category_name
ORDER BY
    oi.price DESC
LIMIT 10;


-- 7. Каково распределение оценок (от 1 до 5) среди всех отзывов?
-- Показывает общий уровень удовлетворенности клиентов
SELECT
    review_score,
    COUNT(review_id) AS score_count
FROM
    order_reviews
GROUP BY
    review_score
ORDER BY
    review_score;


-- 8. Топ-10 продавцов по количеству проданных товаров
-- Помогает выявить ключевых партнеров на платформе
SELECT
    seller_id,
    COUNT(order_item_id) AS items_sold
FROM
    order_items
GROUP BY
    seller_id
ORDER BY
    items_sold DESC
LIMIT 10;


-- 9. Какая средняя стоимость доставки (freight_value) в разные штаты? (топ-10 самых дорогих)
-- Помогает в анализе логистических затрат
SELECT
    c.customer_state,
    AVG(oi.freight_value) AS average_freight
FROM
    order_items AS oi
JOIN
    orders AS o ON oi.order_id = o.order_id
JOIN
    customers AS c ON o.customer_id = c.customer_id
GROUP BY
    c.customer_state
ORDER BY
    average_freight DESC
LIMIT 10;


-- 10. Сколько клиентов являются "постоянными" (делали больше одного заказа)?
-- Помогает оценить лояльность клиентской базы
SELECT
    COUNT(*) AS loyal_customers
FROM (
    SELECT
        c.customer_unique_id,
        COUNT(o.order_id) AS order_count
    FROM
        orders AS o
    JOIN
        customers AS c ON o.customer_id = c.customer_id
    GROUP BY
        c.customer_unique_id
    HAVING
        COUNT(o.order_id) > 1
) AS loyal_customer_counts;

----------------
--Какова средняя стоимость доставки (freight_value) для топ-5 категорий товаров с самым высоким средним рейтингом? (Горизонталоно столбчатая)
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

--"Каково распределение способов оплаты для топ-3 самых продаваемых категорий товаров?"
