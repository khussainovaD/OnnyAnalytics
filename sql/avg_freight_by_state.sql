-- Средняя стоимость доставки по штатам (топ-10 самых дорогих)
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
