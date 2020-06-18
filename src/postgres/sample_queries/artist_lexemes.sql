SELECT 
  artist,
  artist_lexemes 
FROM entries
WHERE artist @@ to_tsquery('english', regexp_replace('princ','\s',' | '))
;
