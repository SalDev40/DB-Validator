- DESCRIPTION:

    A program that generates SQL statements (SELECT + temp tables) to check referential integrity and normalization (simplified).The input is a database consisting of a set of SQL tables (relations) and a primary key (PK) for eachtable, as well as foreign keys. We assume all keys are simple keys (one column). The schema of the tables will be specified as a text file,  and the actual tables will be already stored in the database.   While your program must generate the output as text files, all the processing will be done with SQL queries.The output is a single text file showing if each table has referential integrity and if it is normalized or not. More details below.



- ASSUMPTIONS:

1.  Referential integrity: For each table the program must state if referential integrity is correct: Y/N. Since the key is simpleand we assume PKs are clean you can check only 3NF.

2.  Normalization: For each table the program must state if it is normalized Y/N. Since the key is simple and we assumePKs are clean you can check only 3NF with simple keys.





- EXAMPLE:

    dbxyz.txt

    --------------------------------------
    T1(K(pk),K2(fk:T2.K2),A,B)
    T2(K2(pk),C)
    T3(K3(pk),D,E)
    T4(K4(pk),K3(fk:T3.K3),F)

    --------------------------------------
    Sample output file:refintnorm.txt
    -----------------------------------------
    referential integrity     normalized
    T1              Y                  Y
    T2              N                  Y
    T3              N                  Y
    T4              Y                  Y
    DB referential integrity: N
    DB normalized: Y