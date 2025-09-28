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