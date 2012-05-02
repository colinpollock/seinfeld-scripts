SELECT speaker, count(*) as count
FROM utterance
GROUP BY speaker
ORDER BY count
;
