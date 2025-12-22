-- Number of thanks sent
SELECT COUNT(DISTINCT log_id) AS TOTAL_THANKS_ON_PROJECT
FROM logging
WHERE log_type = 'thanks'