-- "Каково распределение цен на товары в категории 'Компьютеры и аксессуары'?"
SELECT
    oi.price
FROM
    order_items AS oi
JOIN
    products AS p ON oi.product_id = p.product_id
JOIN
    product_category_name_translation AS t ON p.product_category_name = t.product_category_name
WHERE
    t.product_category_name_english = 'computers_accessories' AND oi.price < 500; -- Ограничим цену для наглядности