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