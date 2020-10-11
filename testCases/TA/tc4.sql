DROP TABLE IF EXISTS T1;
DROP TABLE IF EXISTS T2;
DROP TABLE IF EXISTS T3;


CREATE TABLE T1 (k1 int, k2 int, A int);
INSERT INTO T1 VALUES (1,10,2);
INSERT INTO T1 VALUES (2,20,2);
INSERT INTO T1 VALUES (3,30,3);
INSERT INTO T1 VALUES (4,30,3);
INSERT INTO T1 VALUES (5,20,4);


CREATE TABLE T2 (k2 int, B int, C int);
INSERT INTO T2 VALUES (10,12,3);
INSERT INTO T2 VALUES (20,33,3);
INSERT INTO T2 VALUES (30,33,3);



CREATE TABLE T3 (k3 int, k2 int, D int);
INSERT INTO T3 VALUES (100,10,1);
INSERT INTO T3 VALUES (200,30,1);
INSERT INTO T3 VALUES (300,30,1);