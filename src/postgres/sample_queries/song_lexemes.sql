SELECT 
  song_name,
  song_lexemes
FROM entries
WHERE song_lexemes @@ to_tsquery('english', 'come | home')
;
