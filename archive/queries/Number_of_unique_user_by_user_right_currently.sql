-- Number of unique user by user right currently
SELECT ug_group, 
       COUNT(DISTINCT ug_user) AS unique_users  -- Count distinct users in each group
FROM user_groups  -- From the 'user_groups' table
WHERE ug_group IN ('autoconfirmed', 'rollback', 'sysop', 'bureaucrat', 'checkuser', 'bot')  
-- Filter only for specific user groups
GROUP BY ug_group  -- Group by user group to count users per group
ORDER BY unique_users DESC;  -- Sort results in descending order based on unique user count