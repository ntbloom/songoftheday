SELECT 
  song_name,
  song_lexemes
FROM entries
WHERE song_lexemes @@ to_tsquery('english', regexp_replace('home welcome','\s',' | '))
;
