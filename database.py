#!/usr/bin/python
import psycopg2
from psycopg2 import sql


class Database:
    def __init__(self, schema, username, database, pg_password):
        self.conn = psycopg2.connect(database=database,
                                     user=username,
                                     password=pg_password)

        self.cursor = self.conn.cursor()
        self.schema = schema

    def __del__(self):
        # make sure to commit transactions or else wont save in DB
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def checkRefInt(self):
        for table in self.schema:
            try:
                print("\n*********************************\
                       \n DB REF INT CHECKING TABLE:", table,
                      "\n*********************************")


                # if table has no fk nothing to check
                if(len(self.schema[table]['Fks']) == 0):
                    print('\nDB Ref Int CHECK, Table: ',
                          table, ' -> No fK to check')
                    self.schema[table]['dbRefInt'] = True
                    continue

                # skip DB check if table has no PK
                if(len(self.schema[table]['Pk']) == 0):
                    raise Exception('Skipping table: ',
                                    table, ' -> No PK')

                # skip DB if FK references invalid column or table
                if(len(self.schema[table]['invalidFks']) > 0):
                    raise Exception('Skipping table: ', table, ' -> invalid FK: ',
                                    self.schema[table]['invalidFks'])

                # check ref Int for remaining tables that have PK and Valid Fk's
                for ttc in self.schema[table]['validFks']:
                    # get table and attr from foreignKey
                    fKTableName = ttc.split('.')[0]
                    fKTableAttr = ttc.split('.')[1]
                    refKey = self.schema[table]['validFks'][ttc]
                    # get table and attr to check in referenced table
                    refTableName = self.schema[table]['validFks'][ttc].split('.')[
                        0]
                    refTableAttr = self.schema[table]['validFks'][ttc].split('.')[
                        1]

                    print('-----> checking refInt for fk: ',
                          ttc, ' -> ', refKey, '\n')

                    # check if any foreign Key row is NULL
                    self.cursor.execute(
                        sql.SQL(
                            """
    SELECT * FROM {} WHERE {} IS NULL
    """
                        ).format(sql.Identifier(fKTableName),
                                 sql.Identifier(fKTableAttr))
                    )

                    totalNullForKeys = self.cursor.rowcount
                    self.schema[table]['dbCommands'].append(
                        self.cursor.query.strip())

                    # check if all rows in referencing table
                    # exist in referenced table
                    self.cursor.execute(
                        sql.SQL(
                            """
    SELECT * FROM {}
    """
                        ).format(sql.Identifier(fKTableName))
                    )

                    totalRows = self.cursor.rowcount
                    self.schema[table]['dbCommands'].append(
                        self.cursor.query.strip())

                    self.cursor.execute(
                        sql.SQL(
                            """
    SELECT t.{}, b.{} FROM {} t JOIN {} b ON t.{} = b.{}
    """
                        ).format(
                            sql.Identifier(fKTableAttr),
                            sql.Identifier(refTableAttr),
                            sql.Identifier(fKTableName),
                            sql.Identifier(refTableName),
                            sql.Identifier(fKTableAttr),
                            sql.Identifier(refTableAttr)
                        ),
                    )
                    totalReferencedKeys = self.cursor.rowcount
                    self.schema[table]['dbCommands'].append(
                        self.cursor.query.strip())

                    print('Total Nulls FOR FK in table ',
                          fKTableName, ' : ',   totalNullForKeys)
                    print('Total Rows in table ',
                          fKTableName, ' : ',   totalRows)
                    print('Total JOIN Referenced Keys in table ',
                          refTableName, ' : ',   totalReferencedKeys)

                    # failed if we have nulls for foreign keys
                    if (totalNullForKeys != 0):
                        raise Exception(' Failed!!! NULLS : ', totalNullForKeys,
                                        ' For:', fKTableName + '.' + fKTableAttr,
                                        ' -> ' + refTableName + "." + refTableAttr)

                    # if all rows for referencing table
                    # are not in referenced table, dbRefInt failed
                    if(totalRows != totalReferencedKeys):
                        raise Exception('Failed!!!', totalRows, ' total rows in table ',
                                        fKTableName,
                                        ' Doesnt Match', totalReferencedKeys, 'totalReferencedKeys in',
                                        refTableName,
                                        ' For:', fKTableName + '.' + fKTableAttr,
                                        ' -> ' + refTableName + "." + refTableAttr)

                    # if no nulls and row count is equal to referenced keys
                    if(totalRows == totalReferencedKeys):
                        print('\nPASSED DB REF INT: ', fKTableName + '.' + fKTableAttr,
                              ' -> ' + refTableName + "." + refTableAttr)
                        self.schema[ttc.split('.')[0]]['dbRefInt'] = True

            except Exception as e:
                # if any DB errors for that table print error
                # commit db commands and fail refInt for table
                # and skip checking rest of table
                self.conn.commit()
                print('DB REFINT CHECK FAILED SKIPPING TABLE: ', table, '\n', e)
                self.schema[table]['dbRefInt'] = False
                continue

    def checkNormal(self):
        for table in self.schema:
            try:
                print("\n*****************************************\
                       \n DB NORMALIZATION CHECKING TABLE:", table,
                      "\n*****************************************")

                # skip DB normalization check if table has no PK
                if(len(self.schema[table]['Pk']) == 0):
                    raise Exception('Skipping table: ',
                                    table, ' -> No PK')

                # skip DB normalization if any FK references invalid column or table
                if(len(self.schema[table]['invalidFks']) > 0):
                    raise Exception('Skipping table: ', table, ' -> invalid FK: ',
                                    self.schema[table]['invalidFks'])

                # if only one NonPrime attribute than table is in 3NF
                if(len(self.schema[table]['nonPrimaryAttributes']) == 1):
                    print('Only one NonPrimeAttr by default in 3NF',)
                    self.schema[table]['normalized'] = True
                    continue

                # check npa -> npa for 3NF
                print('\nALL NPA: ', self.schema[table]['nonPrimaryAttributes'])
                for npa in self.schema[table]['nonPrimaryAttributes']:
                    # if column has no duplicates than skip it, it passes by default
                    self.cursor.execute(
                        sql.SQL(
                            """
    SELECT {} FROM {} GROUP BY({}) HAVING count({}) > 1
    """
                        ).format(
                            sql.Identifier(npa),
                            sql.Identifier(table),
                            sql.Identifier(npa),
                            sql.Identifier(npa)
                        ),
                    )

                    self.schema[table]['dbCommands'].append(
                        self.cursor.query.strip())

                    if self.cursor.rowcount == 0:
                        print("\nNPA: ", npa, " -> has no duplicates passed 3NF",
                              "checking rest of table")
                        self.schema[table]['normalized'] = True
                        continue

                    # check all other npa attributes except this one
                    for checkNpa in self.schema[table]['nonPrimaryAttributes']:
                        if checkNpa == npa:
                            continue

                        print('\n--> checking npa: ', npa)
                        print('-----> with attr: ', checkNpa)

                        self.cursor.execute(
                            sql.SQL(
                                """
    DROP TABLE IF EXISTS temp
    """
                            )
                        )

                        self.schema[table]['dbCommands'].append(
                            self.cursor.query.strip())
                        self.cursor.execute(
                            sql.SQL(
                                """
    DROP TABLE IF EXISTS pairs
    """
                            )
                        )

                        self.schema[table]['dbCommands'].append(
                            self.cursor.query.strip())
                        self.cursor.execute(
                            sql.SQL(
                                """
    CREATE TABLE IF NOT EXISTS pairs AS (SELECT {} FROM {} GROUP BY {} HAVING COUNT({}) > 1)
    """
                            ).format(
                                sql.Identifier(npa),
                                sql.Identifier(table),
                                sql.Identifier(npa),
                                sql.Identifier(npa)
                            ),
                        )

                        self.schema[table]['dbCommands'].append(
                            self.cursor.query.strip())

                        self.cursor.execute(
                            sql.SQL(
                                """
    CREATE TABLE IF NOT EXISTS temp AS (SELECT {}, {} FROM {} WHERE {} IN (SELECT {} FROM pairs) GROUP BY {}, {})
    """
                            ).format(
                                sql.Identifier(npa),
                                sql.Identifier(checkNpa),
                                sql.Identifier(table),
                                sql.Identifier(npa),
                                sql.Identifier(npa),
                                sql.Identifier(npa),
                                sql.Identifier(checkNpa)
                            ),
                        )
                        self.schema[table]['dbCommands'].append(
                            self.cursor.query.strip())

                        self.cursor.execute(
                            sql.SQL(
                                """
    SELECT EXISTS (SELECT {} FROM temp GROUP BY {} HAVING COUNT({}) > 1)
    """
                            ).format(
                                sql.Identifier(npa),
                                sql.Identifier(npa),
                                sql.Identifier(npa)
                            ),
                        )
                        finalResult = self.cursor.fetchall()[0][0]

                        self.schema[table]['dbCommands'].append(
                            self.cursor.query.strip())

                        if(finalResult == False):
                            # if not normalized column break out of loop, whole table fails
                            raise Exception('Column: ', npa, ' -> ', checkNpa,
                                            ' failed 3NF')
                        if(finalResult == True):
                            print('Column: ', npa, ' -> ', checkNpa,
                                  ' passed 3NF checking rest of table')
                            self.schema[table]['normalized'] = True

            except Exception as e:
                self.conn.commit()
                self.schema[table]['normalized'] = False
                print('DB NORMAL COMMANDS FAILED SKIPPING TABLE: ', table, '\n', e)
                continue
