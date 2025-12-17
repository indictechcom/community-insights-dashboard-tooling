-- This query finds redirects to Wikistats pages
-- I'm using the 'redirect' table to find these

SELECT rd_from, rd_title, rd_namespace   -- these are the columns i need
FROM redirect   -- looking in the redirect table
WHERE
  -- find anything with Wikistats in the name
  rd_title LIKE '%Wikistats%'
;  -- don't forget the semicolon!

-- The rd_from is the page ID where the redirect comes from
-- rd_title is where it goes to
-- rd_namespace tells what type of page it is
