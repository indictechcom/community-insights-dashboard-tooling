-- This query looks at the ipblocks table from the MediaWiki Permissions database
-- The ipblocks table stores all blocked IP addresses in a hashed format
-- ipb_range_start and ipb_range_end are TINYBLOB fields that store the blocked IP range
-- ipb_expiry is a DATETIME field that indicates when the block expires

SELECT ipb_range_start, ipb_range_end, ipb_expiry  
FROM ipblocks  
WHERE ipb_range_start IS NOT NULL  -- Only get entries that have a range start
  AND ipb_range_end IS NOT NULL    -- Only get entries that have a range end
  AND (ipb_expiry IS NULL OR ipb_expiry > NOW());  -- Only get active blocks - ipb_expiry is often set to "infinity" (NULL) by default
