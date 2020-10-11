#!/usr/bin/python
import sys
import database
import schema
import utils


inputSchema = {}
try:
    fileName = str(sys.argv[-1]).split("=")[1]
    inputSchema = utils.readFile(fileName)

    print('\n*******************************')
    print('*******************************')
    print('CHECKING SCHEMA')
    print('*******************************')
    print('*******************************\n')

    testSchema = schema.Schema(inputSchema)

    testSchema.checkRefInt()

except Exception as e:
    print('SOMETHING WENT WRONG IN SCHEMA CHECKS: ', e)

try:
    print('\n\n*******************************')
    print('*******************************')
    print('CHECKING DATABASE REF INT')
    print('*******************************')
    print('*******************************\n')

    with open('user.txt') as f:
        lines = [line.rstrip() for line in f]

    username = lines[0]
    pg_password = lines[1]
    database = lines[2]

    testDb = database.Database(inputSchema, username, pg_password)

    testDb.checkRefInt()
    
    print('\n\n*******************************')
    print('*******************************')
    print('CHECKING DATABASE NORMALIZATION')
    print('*******************************')
    print('*******************************\n')

    testDb.checkNormal()
except Exception as e:
    print('SOMETHING WENT WRONG IN DB CHECKS: ', e)


try:
    print('\n\n*******************************')
    print('*******************************')
    print('OUTPUT')
    print('*******************************')
    print('*******************************\n')

    utils.printFormat(inputSchema)
    utils.printResult(inputSchema)

    # save the name of the file and schema results to
    # one file for each test case
    utils.saveAllResultsToOneFile(fileName, inputSchema)
    utils.saveAllSqlToOneFile(fileName, inputSchema)

    # overwrite same file for each test case
    utils.saveOverwriteResultsToOneFile(inputSchema)
    utils.saveOverwriteSqlToOneFile(inputSchema)


except Exception as e:
    print('SOMETHING WENT WRONG IN SAVING TO FILES: ', e)
