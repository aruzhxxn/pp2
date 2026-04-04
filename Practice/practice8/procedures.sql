DROP PROCEDURE IF EXISTS insert_or_update_user(TEXT, TEXT);
DROP PROCEDURE IF EXISTS insert_many_users(TEXT[], TEXT[]);
DROP PROCEDURE IF EXISTS delete_by_name_or_phone(TEXT);

CREATE OR REPLACE PROCEDURE insert_or_update_user(p_name TEXT, p_phone TEXT)
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE name = p_name;
    ELSE
        INSERT INTO phonebook(name, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE insert_many_users(p_names TEXT[], p_phones TEXT[])
AS $$
DECLARE
    i INT;
    invalid_data TEXT := '';
BEGIN
    IF array_length(p_names, 1) IS DISTINCT FROM array_length(p_phones, 1) THEN
        RAISE EXCEPTION 'Количество имен и телефонов не совпадает';
    END IF;

    FOR i IN 1..array_length(p_names, 1) LOOP
        IF p_phones[i] ~ '^[0-9]{11}$' THEN
            IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_names[i]) THEN
                UPDATE phonebook
                SET phone = p_phones[i]
                WHERE name = p_names[i];
            ELSE
                INSERT INTO phonebook(name, phone)
                VALUES (p_names[i], p_phones[i]);
            END IF;
        ELSE
            invalid_data := invalid_data || p_names[i] || ' - ' || p_phones[i] || E'\n';
        END IF;
    END LOOP;

    RAISE NOTICE 'Invalid data:%', E'\n' || invalid_data;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE delete_by_name_or_phone(p_value TEXT)
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE name = p_value OR phone = p_value;
END;
$$ LANGUAGE plpgsql;