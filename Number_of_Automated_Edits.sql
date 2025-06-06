/* Retrieving Number of Automated edits done i.e ( Edits done by the bots) , 
For that we need Revision , actor , user_group tables to get the data . 
Revision table stores the edits done in database and 
Actor table shows the edit done by whom (user or bot)  and 
to conform edit done by bot we use user_group table in which 
ug_group contains values like : 'bot', 'bureaucrat', 'sysop... */

SELECT COUNT(*) AS Automated_Edits                   -- Count the number of automated edits
FROM revision                                        -- Refer to the revision table
JOIN actor 
    ON revision.rev_actor = actor.actor_id           -- Join actor and revision tables
JOIN user_groups 
    ON actor.actor_user = user_groups.ug_user        -- Join user_groups and actor tables
WHERE user_groups.ug_group = 'bot'                   -- Filter for bot user group
  AND revision.rev_timestamp BETWEEN '20230101' AND '20240301';  -- Filter by specific date range
