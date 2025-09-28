-- "Каково распределение способов оплаты для топ-3 самых продаваемых категорий товаров?"
SELECT
    t.product_category_name_english AS category,
    op.payment_type
FROM
    order_payments AS op
JOIN
    order_items AS oi ON op.order_id = oi.order_id
JOIN
    products AS p ON oi.product_id = p.product_id
JOIN
    product_category_name_translation AS t ON p.product_category_name = t.product_category_name
WHERE
    t.product_category_name_english IN (
        SELECT
            t2.product_category_name_english
        FROM
            order_items oi2
        JOIN
            products p2 ON oi2.product_id = p2.product_id
        JOIN
            product_category_name_translation t2 ON p2.product_category_name = t2.product_category_name
        GROUP BY
            t2.product_category_name_english
        ORDER BY
            COUNT(oi2.order_item_id) DESC
        LIMIT 3
    );