CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone BIGINT)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO phonebook(name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE insert_many_contacts(
    p_names VARCHAR[],
    p_phones BIGINT[],
    OUT invalid_data TEXT
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
    phone_text TEXT;
BEGIN
    invalid_data := '';
    FOR i IN 1..array_length(p_names, 1) LOOP
        phone_text := CAST(p_phones[i] AS TEXT);
        IF length(phone_text) != 11 THEN
            invalid_data := invalid_data || p_names[i] || ' - ' || phone_text || '; ';
        ELSE
            INSERT INTO phonebook(name, phone)
            VALUES(p_names[i], p_phones[i])
            ON CONFLICT (phone) DO NOTHING;
        END IF;
    END LOOP;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_contact(p_name VARCHAR, p_phone BIGINT)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook
    WHERE name = p_name OR phone = p_phone;
END;
$$;