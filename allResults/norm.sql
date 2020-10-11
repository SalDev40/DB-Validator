
DROP TABLE IF EXISTS temp;
DROP TABLE IF EXISTS pairs;
CREATE TABLE temp AS (SELECT b, c
                      FROM t2 LIMIT 0);
CREATE TABLE pairs AS (SELECT b
                       FROM t2 LIMIT 0);

select * from temp;

INSERT INTO pairs
SELECT b
FROM t2
GROUP BY b
HAVING count(b) > 1;

INSERT INTO temp(
    SELECT b, c
    FROM t2
    WHERE b IN (
        SELECT b
        FROM pairs
    )
    GROUP BY b, c);

SELECT EXISTS
           (SELECT
            FROM temp
            GROUP BY b
            HAVING count(b) > 1);
