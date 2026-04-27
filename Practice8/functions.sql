CREATE OR REPLACE FUNCTION search_contacts(p TEXT)
RETURNS TABLE(id INT, name VARCHAR, phone BIGINT) AS $$
BEGIN
    RETURN QUERY
    SELECT pb.id, pb.name, pb.phone
    FROM phonebook pb
    WHERE pb.name ILIKE '%' || p || '%'
    OR CAST(pb.phone AS TEXT) ILIKE '%' || p || '%';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_contacts_paginated(lim INT, off INT)
RETURNS TABLE(id INT, name VARCHAR, phone BIGINT) AS $$
BEGIN
    RETURN QUERY
    SELECT pb.id, pb.name, pb.phone
    FROM phonebook pb
    ORDER BY pb.id
    LIMIT lim OFFSET off;
END;
$$ LANGUAGE plpgsql;