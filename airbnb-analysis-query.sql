-- Write a query to return the top 10 neighborhoods by estimated annual revenue (price × availability).

SELECT
    nb.neighbourhood,
    SUM(ls.price * ls.availability_365) AS total_estimated_revenue 
FROM listings AS ls
INNER JOIN neighbourhoods AS nb 
    ON ls.neighbourhood_id = nb.neighbourhood_id
GROUP BY nb.neighbourhood
ORDER BY total_estimated_revenue DESC
LIMIT 10;

-- Write a query to find the average price of each room type.

SELECT
	room_type,
	ROUND(AVG(price), 2)
FROM listings
GROUP BY room_type;

-- Find the top 5 hosts who have the most listings.

SELECT
	hosts.host_id,
	hosts.host_name,
	COUNT(listings.id) AS total_listings
FROM hosts 
INNER JOIN listings 
	ON hosts.host_id = listings.host_id
GROUP BY hosts.host_id, listings.host_id
ORDER BY COUNT(listings.id) DESC
LIMIT 5;

-- Find the top 5 neighborhoods with the highest average number of reviews.

SELECT
	nh.neighbourhood_id,
	nh.neighbourhood,
	ROUND(AVG(rs.number_of_reviews), 2) AS avg_reviews
FROM listings AS ls
INNER JOIN neighbourhoods AS nh 
	ON ls.neighbourhood_id = nh.neighbourhood_id
INNER JOIN reviews_summary AS rs 
	ON ls.id = rs.listing_id
GROUP BY nh.neighbourhood_id, nh.neighbourhood
ORDER BY AVG(rs.number_of_reviews) DESC
LIMIT 5;

-- Find all listings where the minimum_nights is greater than 365 (likely invalid).

SELECT
	id,
	name,
	minimum_nights
FROM listings
WHERE minimum_nights > 365;

-- For each neighborhood, determine the most common room type.

WITH room_type_count AS (SELECT
	nh.neighbourhood,
	ls.room_type,
	COUNT(ls.id) AS room_count,
	RANK() OVER (
		PARTITION BY nh.neighbourhood
		ORDER BY COUNT(ls.id) DESC
	) AS room_rank
FROM listings AS ls
INNER JOIN neighbourhoods AS nh ON ls.neighbourhood_id = nh.neighbourhood_id
GROUP BY nh.neighbourhood, ls.room_type)

SELECT
	neighbourhood,
	room_type,
	room_count
FROM room_type_count
WHERE room_rank = 1;

-- Find all listings that have zero total reviews.

SELECT
	ls.id,
	ls.name,
	ls.price,
	rs.number_of_reviews
FROM listings AS ls
INNER JOIN reviews_summary AS rs
	ON ls.id = rs.listing_id
WHERE rs.number_of_reviews = 0;

-- Find all listings that are available for 365 days a year.

SELECT
	id,
	name,
	price,
	availability_365
FROM listings 
WHERE availability_365 = 365;