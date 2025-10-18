-- Количество доставленных заказов по месяцам
SELECT
    DATE_TRUNC('month', order_purchase_timestamp)::DATE AS month,
    COUNT(order_id) AS number_of_orders
FROM
    orders
WHERE
    order_status = 'delivered'
GROUP BY
    month
ORDER BY
    month;
