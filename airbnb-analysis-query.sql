-- 1. Find the average listing price for each room type.

SELECT 
	room_type,
	ROUND(AVG(price::numeric), 2)
from listings
GROUP BY room_type;

-- Find all listings that have zero total reviews.

SELECT 
	host_id,
	host_name
from listings
WHERE number_of_reviews = 0;

-- Find all listings that are available for 365 days a year.

SELECT 
	host_id,
	host_name,
	availability_365
from listings
WHERE availability_365 = 365;
