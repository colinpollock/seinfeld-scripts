/*
 * Find the average number of sentences in each utterance for each character.
 */


select *
from
    (
    select u.speaker, count(*) as utt_count
    from utterance u
    where u.speaker = 'KESSLER'
    group by u.speaker
UNION all
    select u.speaker, count(*) as sent_count
    from sentence s join utterance u on s.utterance_id = u.id
    where u.speaker = 'KESSLER'
    group by u.speaker
    )
;

/*
SELECT u.speaker, COUNT(s.id) / COUNT(u.id) as the_count
FROM utterance u JOIN sentence s ON u.id = s.utterance_id
where u.speaker in ('JERRY', 'ELAINE', 'GEORGE', 'KRAMER')
group by speaker
order by the_count
;
*/
