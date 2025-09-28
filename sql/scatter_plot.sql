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