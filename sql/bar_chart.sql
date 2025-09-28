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