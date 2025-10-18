-- Топ-10 продавцов по количеству проданных товаров (с их местоположением)
SELECT
    oi.seller_id,
    s.seller_city,
    s.seller_state,
    COUNT(oi.order_item_id) AS items_sold
FROM
    order_items AS oi
JOIN
    sellers AS s ON oi.seller_id = s.seller_id
GROUP BY
    oi.seller_id, s.seller_city, s.seller_state
ORDER BY
    items_sold DESC
LIMIT 10;