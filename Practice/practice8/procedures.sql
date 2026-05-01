-- Процедура добавления или обновления одного пользователя
CREATE OR REPLACE PROCEDURE insert_or_update_user(
    p_name VARCHAR(100),
    p_phone VARCHAR(20)
)
AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM phonebook
        WHERE name = p_name
    ) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE name = p_name;
    ELSE
        INSERT INTO phonebook(name, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$ LANGUAGE plpgsql;


-- Процедура удаления по имени или телефону
CREATE OR REPLACE PROCEDURE delete_by_name_or_phone(
    p_value VARCHAR(100)
)
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE name = p_value
       OR phone = p_value;
END;
$$ LANGUAGE plpgsql;