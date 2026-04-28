CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    contact_id INT;
BEGIN
    SELECT id INTO contact_id FROM phonebook WHERE name = p_contact_name;
    IF contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact not found';
    END IF;
    INSERT INTO phones (contact_id, phone, type) VALUES (contact_id, p_phone, p_type);
END;
$$;


CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    gid INT;
BEGIN
    SELECT id INTO gid FROM groups WHERE name = p_group_name;
    IF gid IS NULL THEN
        INSERT INTO groups (name) VALUES (p_group_name) RETURNING id INTO gid;
    END IF;
    UPDATE phonebook SET group_id = gid WHERE name = p_contact_name;
END;
$$;


CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(id INT, name VARCHAR, email VARCHAR, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT p.id, p.name, p.email, ph.phone
    FROM phonebook p
    LEFT JOIN phones ph ON ph.contact_id = p.id
    WHERE p.name  ILIKE '%' || p_query || '%'
    OR    p.email ILIKE '%' || p_query || '%'
    OR    ph.phone ILIKE '%' || p_query || '%';
END;
$$ LANGUAGE plpgsql;