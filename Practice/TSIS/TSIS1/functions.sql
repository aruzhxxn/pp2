-- Функция поиска по шаблону
CREATE OR REPLACE FUNCTION search_pattern(patt TEXT)
RETURNS TABLE(
    id INT,
    name VARCHAR(100),
    phone VARCHAR(20)
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        p.id,
        p.name,
        p.phone
    FROM phonebook p
    WHERE p.name ILIKE '%' || patt || '%'
       OR p.phone ILIKE '%' || patt || '%';
END;
$$ LANGUAGE plpgsql;


-- Функция пагинации
CREATE OR REPLACE FUNCTION get_contacts_paginated(
    p_limit INT,
    p_offset INT
)
RETURNS TABLE(
    id INT,
    name VARCHAR(100),
    phone VARCHAR(20)
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        p.id,
        p.name,
        p.phone
    FROM phonebook p
    ORDER BY p.id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;


-- Функция добавления многих пользователей
-- Возвращает все некорректные данные
DROP FUNCTION IF EXISTS insert_many_users(TEXT[], TEXT[]);
DROP PROCEDURE IF EXISTS insert_many_users(TEXT[], TEXT[]);

CREATE OR REPLACE FUNCTION insert_many_users(
    p_names TEXT[],
    p_phones TEXT[]
)
RETURNS TABLE(
    invalid_name TEXT,
    invalid_phone TEXT
)
AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(p_names, 1) LOOP
        IF p_phones[i] ~ '^[0-9]{10,15}$' THEN
            IF EXISTS (
                SELECT 1
                FROM phonebook
                WHERE name = p_names[i]
            ) THEN
                UPDATE phonebook
                SET phone = p_phones[i]
                WHERE name = p_names[i];
            ELSE
                INSERT INTO phonebook(name, phone)
                VALUES (p_names[i], p_phones[i]);
            END IF;
        ELSE
            invalid_name := p_names[i];
            invalid_phone := p_phones[i];
            RETURN NEXT;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;