-- *********************************
-- Test Case: testCases/TA/tc6.txt
-- *********************************

-- table: t1

-- table has no foreign tables


SELECT "a" FROM "t1" 
	GROUP BY("a") 
	HAVING count("a") > 1;

DROP TABLE IF EXISTS temp;

DROP TABLE IF EXISTS pairs;

CREATE TABLE IF NOT EXISTS pairs AS (
SELECT "a" FROM "t1" 
	GROUP BY "a" 
	HAVING COUNT("a") > 1);

CREATE TABLE IF NOT EXISTS temp AS (
SELECT "a", "b" FROM "t1" 
WHERE "a" IN 
(SELECT "a" FROM pairs) 
	GROUP BY "a", "b");


SELECT EXISTS 
(SELECT "a" FROM temp 
	GROUP BY "a" 
	HAVING COUNT("a") > 1);


-- table: t2


SELECT * FROM "t2" 
WHERE "l2" IS NULL;


SELECT * FROM "t2";


SELECT t."l2", b."k1" FROM "t2" t 
	JOIN "t1" b ON t."l2" = b."k1";


SELECT "l2" FROM "t2" 
	GROUP BY("l2") 
	HAVING count("l2") > 1;

DROP TABLE IF EXISTS temp;

DROP TABLE IF EXISTS pairs;

CREATE TABLE IF NOT EXISTS pairs AS (
SELECT "l2" FROM "t2" 
	GROUP BY "l2" 
	HAVING COUNT("l2") > 1);

CREATE TABLE IF NOT EXISTS temp AS (
SELECT "l2", "c" FROM "t2" 
WHERE "l2" IN 
(SELECT "l2" FROM pairs) 
	GROUP BY "l2", "c");


SELECT EXISTS 
(SELECT "l2" FROM temp 
	GROUP BY "l2" 
	HAVING COUNT("l2") > 1);


SELECT "c" FROM "t2" 
	GROUP BY("c") 
	HAVING count("c") > 1;

DROP TABLE IF EXISTS temp;

DROP TABLE IF EXISTS pairs;

CREATE TABLE IF NOT EXISTS pairs AS (
SELECT "c" FROM "t2" 
	GROUP BY "c" 
	HAVING COUNT("c") > 1);

CREATE TABLE IF NOT EXISTS temp AS (
SELECT "c", "l2" FROM "t2" 
WHERE "c" IN 
(SELECT "c" FROM pairs) 
	GROUP BY "c", "l2");


SELECT EXISTS 
(SELECT "c" FROM temp 
	GROUP BY "c" 
	HAVING COUNT("c") > 1);


-- table: t3

-- table has no foreign tables


-- table: t4


SELECT * FROM "t4" 
WHERE "l4" IS NULL;


SELECT * FROM "t4";


SELECT t."l4", b."k2" FROM "t4" t 
	JOIN "t2" b ON t."l4" = b."k2";


SELECT "l4" FROM "t4" 
	GROUP BY("l4") 
	HAVING count("l4") > 1;

DROP TABLE IF EXISTS temp;

DROP TABLE IF EXISTS pairs;

CREATE TABLE IF NOT EXISTS pairs AS (
SELECT "l4" FROM "t4" 
	GROUP BY "l4" 
	HAVING COUNT("l4") > 1);

CREATE TABLE IF NOT EXISTS temp AS (
SELECT "l4", "l5" FROM "t4" 
WHERE "l4" IN 
(SELECT "l4" FROM pairs) 
	GROUP BY "l4", "l5");


SELECT EXISTS 
(SELECT "l4" FROM temp 
	GROUP BY "l4" 
	HAVING COUNT("l4") > 1);

DROP TABLE IF EXISTS temp;

DROP TABLE IF EXISTS pairs;

CREATE TABLE IF NOT EXISTS pairs AS (
SELECT "l4" FROM "t4" 
	GROUP BY "l4" 
	HAVING COUNT("l4") > 1);

CREATE TABLE IF NOT EXISTS temp AS (
SELECT "l4", "e" FROM "t4" 
WHERE "l4" IN 
(SELECT "l4" FROM pairs) 
	GROUP BY "l4", "e");


SELECT EXISTS 
(SELECT "l4" FROM temp 
	GROUP BY "l4" 
	HAVING COUNT("l4") > 1);


SELECT "l5" FROM "t4" 
	GROUP BY("l5") 
	HAVING count("l5") > 1;

DROP TABLE IF EXISTS temp;

DROP TABLE IF EXISTS pairs;

CREATE TABLE IF NOT EXISTS pairs AS (
SELECT "l5" FROM "t4" 
	GROUP BY "l5" 
	HAVING COUNT("l5") > 1);

CREATE TABLE IF NOT EXISTS temp AS (
SELECT "l5", "l4" FROM "t4" 
WHERE "l5" IN 
(SELECT "l5" FROM pairs) 
	GROUP BY "l5", "l4");


SELECT EXISTS 
(SELECT "l5" FROM temp 
	GROUP BY "l5" 
	HAVING COUNT("l5") > 1);

DROP TABLE IF EXISTS temp;

DROP TABLE IF EXISTS pairs;

CREATE TABLE IF NOT EXISTS pairs AS (
SELECT "l5" FROM "t4" 
	GROUP BY "l5" 
	HAVING COUNT("l5") > 1);

CREATE TABLE IF NOT EXISTS temp AS (
SELECT "l5", "e" FROM "t4" 
WHERE "l5" IN 
(SELECT "l5" FROM pairs) 
	GROUP BY "l5", "e");


SELECT EXISTS 
(SELECT "l5" FROM temp 
	GROUP BY "l5" 
	HAVING COUNT("l5") > 1);


