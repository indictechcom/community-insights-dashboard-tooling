SELECT COUNT(*)  AS no_of_unedited_pages
FROM page 
WHERE
page_id NOT IN (
  SELECT (rev_page) FROM
  revision 
  GROUP BY rev_page
  HAVING COUNT(rev_id)>1);