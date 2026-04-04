CREATE OR REPLACE FUNCTION filtr(a TEXT)
RETURNS TABLE(
    id INT,
    name VARCHAR,
    phone VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.name, p.phone
    FROM phonebook p
    WHERE p.name ILIKE '%' || a || '%'
       OR p.phone ILIKE '%' || a || '%';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_phonebook_page(p_limit INT, p_offset INT)
RETURNS TABLE(
    id INT,
    name VARCHAR,
    phone VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.name, p.phone
    FROM phonebook p
    ORDER BY p.id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;