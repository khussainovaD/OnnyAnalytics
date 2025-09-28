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