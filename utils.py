import re


def readFile(fileName):
    inputSchema = {}
    with open(fileName, 'r') as f:
        for line in f:
            line = line.lower()

            # skip new lines  error in input
            if(line == '\n'):
                continue

            # split up  line information properly
            splitInput = line.split('(', 1)
            tableName = splitInput[0]
            tableAllAttributes = splitInput[1].split(',')
            tableAllAttributes[-1] = tableAllAttributes[-1].split(')')[0]
            tableFilterAttributes = []
            tableKeys = []
            tableFks = []
            tableFullFks = {}
            tablePks = []
            nonPrimaryAttributes = []

            print(line)

            # pull out all keys, fks, pk, and attributes to seperate lists
            for attr in tableAllAttributes:
                attr = attr.strip()  # remove accidental spaces in begin/end
                if 'fk' in attr:
                    # print(attr)
                    tableKeys.append(attr)
                    tableFks.append(attr)
                    # get attr name that is doing referencing
                    attrForKey = attr.split('(')[0]
                    # get foreign key attribute is referencing to
                    forKey = attr.split(':', 1)[1].split(')')[0]
                    tableFullFks.update({tableName + '.' + attrForKey: forKey})
                elif 'pk' in attr:
                    tableKeys.append(attr)
                    tablePks.append(attr)

                # pull out only attr name
                filtAttr = attr
                if '(' in attr:
                    filtAttr = attr.split('(')[0]
                    tableFilterAttributes.append(filtAttr)
                else:
                    tableFilterAttributes.append(filtAttr)

                # filter out all non-prime attributes
                if 'pk' not in attr:
                    if '(' in attr:
                        filtAttr = attr.split('(')[0]
                        nonPrimaryAttributes.append(filtAttr)
                    else:
                        nonPrimaryAttributes.append(filtAttr)

            # if table has no pk display error
            if(len(tablePks) == 0):
                print('\nERROR: NO PRIMARY KEY !!! FOR table: ', tableName)

            # if no fk in table it passes ref integrity
            schemaReInt = False
            dbRefInt = False
            if(len(tableFks) == 0):
                schemaReInt = True
                dbRefInt = True

            inputSchema.update({
                tableName: {
                    'allAttributes': tableAllAttributes,
                    'filterAttributes': tableFilterAttributes,
                    'nonPrimaryAttributes': nonPrimaryAttributes,
                    'allKeys': tableKeys,
                    'Fks': tableFks,
                    'FullFks': tableFullFks,
                    'Pk': tablePks,
                    'invalidFks': {},
                    'validFks': {},
                    'schemaRefInt': schemaReInt,
                    'dbRefInt': dbRefInt,
                    'normalized': False,
                    'dbCommands': []
                }
            })

    return inputSchema


def printResult(schema={}):
    for key in schema:
        print("Table: ", key)
        print('\tschemaRefInt: ', schema[key]['schemaRefInt'])
        print('\tdbRefInt: ', schema[key]['dbRefInt'])
        print('\tnormalized: ', schema[key]['normalized'])
        print()


def printFormat(schema={}):
    for key in schema:
        print("Table: ", key)
        for value in schema[key]:
            print('-', value, ':', end=" ")
            print(schema[key][value])
        print('\n')


#save all test case results to one file

def saveAllResultsToOneFile(fileName, schema={}):
    file = open('./allResults/allToOne.txt', 'a')
    file.write(fileName + "\n" +
               "-----------------------------------------\n")
    file.write("\treferential integrity" + " normalized\n")

    dbRefInt = 'Y'
    dbNormal = 'Y'

    for table in schema:
        # check if table held ref integrity
        refIntTable = 'Y'
        if(schema[table]['schemaRefInt'] == False
           or schema[table]['dbRefInt'] == False):
            refIntTable = 'N'
            dbRefInt = 'N'

        # check if table is normalized
        normalized = 'Y'
        if(schema[table]['normalized'] == False):
            normalized = 'N'
            dbNormal = 'N'

        file.write(table.upper() + "\t\t\t\t\t" +
                   refIntTable + "\t\t\t" + normalized + "\n")

    file.write("DB referential integrity: " + dbRefInt + "\n"
               "DB normalized: " + dbNormal + "\n\n\n")

    file.close()
    


def saveAllSqlToOneFile(fileName, schema={}):

    file = open('./allResults/allToOne.sql', 'a')
    file.write('-- *********************************\n')
    file.write('-- Test Case: ' + fileName + '\n')
    file.write('-- *********************************\n\n')

    for table in schema:
        file.write('-- table: ' + table + '\n\n')

        if len(schema[table]['Fks']) == 0:
            file.write('-- table has no foreign tables\n\n')

        for q in schema[table]['dbCommands']:

            query = str(q)
            saveQuery = query.split('b', 1)[1]
            saveQuery = saveQuery[1:-1]  # remove end quotations

            # format sql statements
            if 'SELECT' in saveQuery:
                indices = re.finditer('SELECT', saveQuery)
                startIndex = [ind.start() for ind in indices]
                for i in startIndex:
                    saveQuery = saveQuery[:i] + '\n' + saveQuery[i:]
            if 'JOIN' in saveQuery:
                index = saveQuery.find('JOIN')
                saveQuery = saveQuery[:index] + '\n\t' + saveQuery[index:]
            if 'WHERE' in saveQuery:
                index = saveQuery.find('WHERE')
                saveQuery = saveQuery[:index] + '\n' + saveQuery[index:]
            if 'GROUP' in saveQuery:
                index = saveQuery.find('GROUP')
                saveQuery = saveQuery[:index] + '\n\t' + saveQuery[index:]
            if 'HAVING' in saveQuery:
                index = saveQuery.find('HAVING')
                saveQuery = saveQuery[:index] + '\n\t' + saveQuery[index:]

            saveQuery = saveQuery + ';\n\n'
            file.write(saveQuery)

        file.write('\n')
    file.close()
    


# Overwrite same file with different testcases

def saveOverwriteResultsToOneFile(schema={}):
    dbRefInt = 'Y'
    dbNormal = 'Y'

    file = open('refintnorm.txt', 'w')
    file.write("    referential integrity normalized")

    for table in schema:
        # check if table held ref integrity
        refIntTable = 'Y'
        if(schema[table]['schemaRefInt'] == False
           or schema[table]['dbRefInt'] == False):
            refIntTable = 'N'
            dbRefInt = 'N'

        # check if table is normalized
        normalized = 'Y'
        if(schema[table]['normalized'] == False):
            normalized = 'N'
            dbNormal = 'N'

        file.write(table.upper() + "                " +
                   refIntTable + "           " + normalized + "\n")

    file.write("DB referential integrity: " + dbRefInt + "\n"
               "DB normalized: " + dbNormal)
    file.close()
    





def saveOverwriteSqlToOneFile(schema={}):

    file = open('./checkdb.sql', 'w')
    for table in schema:
        file.write('-- table: ' + table + '\n\n')

        if len(schema[table]['Fks']) == 0:
            file.write('-- table has no foreign tables\n\n')

        for q in schema[table]['dbCommands']:

            query = str(q)
            saveQuery = query.split('b', 1)[1]
            saveQuery = saveQuery[1:-1]  # remove end quotations

            # format sql statements
            if 'SELECT' in saveQuery:
                indices = re.finditer('SELECT', saveQuery)
                startIndex = [ind.start() for ind in indices]
                for i in startIndex:
                    saveQuery = saveQuery[:i] + '\n' + saveQuery[i:]
            if 'JOIN' in saveQuery:
                index = saveQuery.find('JOIN')
                saveQuery = saveQuery[:index] + '\n\t' + saveQuery[index:]
            if 'WHERE' in saveQuery:
                index = saveQuery.find('WHERE')
                saveQuery = saveQuery[:index] + '\n' + saveQuery[index:]
            if 'GROUP' in saveQuery:
                index = saveQuery.find('GROUP')
                saveQuery = saveQuery[:index] + '\n\t' + saveQuery[index:]
            if 'HAVING' in saveQuery:
                index = saveQuery.find('HAVING')
                saveQuery = saveQuery[:index] + '\n\t' + saveQuery[index:]

            saveQuery = saveQuery + ';\n\n'
            file.write(saveQuery)

        file.write('\n')
    file.close()
