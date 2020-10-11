class Schema:
    def __init__(self, schema):
        self.schema = schema

    def checkRefInt(self):
        # check referential Integrity of schema
        for table in self.schema:
            try:
                print("\n**************************\
                    \n Schema checking table:", table,
                      "\n**************************")

                # if table has no fk nothing to check
                if(len(self.schema[table]['Fks']) == 0):
                    print('\nTable: ', table, ' -> No fK to check')
                    continue

                # if table has no Pk, skip it
                if(len(self.schema[table]['Pk']) == 0):
                    raise Exception('Skipping tables: ', table, ' -> No PK')

                # check all Fks if they hold ref integrity
                for ttc in self.schema[table]['FullFks']:

                    # get table and attr from foreignKey
                    fKTableName = ttc.split('.')[0]
                    fKTableAttr = ttc.split('.')[1]

                    # get table and attr to check in referenced table
                    refKey = self.schema[table]['FullFks'][ttc]
                    refTableName = self.schema[table]['FullFks'][ttc].split('.')[
                        0]
                    refTableAttr = self.schema[table]['FullFks'][ttc].split('.')[
                        1]

                    print('\n -----> checking refInt for fk: ',
                          ttc, ' -> ', refKey, '\n')

                    # if referenced table doesn't exist display
                    # invalid foreign key, skip checking rest of table
                    if(refTableName not in self.schema.keys()):
                        self.schema[table]['invalidFks'].update({
                            ttc: refKey
                        })
                        raise Exception(
                            'INVALID FOREIGN KEY !!'
                            'Table doesnt exist: ', refTableName, ' !!! FOR:',
                            ttc, ' -> ', refKey)

                    # if refFk attribute doesn not exist in referenced table
                    # skip checking rest of table
                    if refTableAttr not in self.schema[refTableName]['filterAttributes']:
                        self.schema[table]['invalidFks'].update({
                            ttc:  refKey
                        })
                        raise Exception(
                            'INVALID FOREIGN KEY !!'
                            ' ATTRIBUTE: ',
                            refTableAttr,
                            'doesnt exist  in table: ',
                            refTableName,
                            ' !!! FOR:',
                            ttc, '->', refKey)

                    # if attribute found in table referenced, fk ref Int passed
                    if refTableAttr in self.schema[refTableName]['filterAttributes']:
                        self.schema[table]['validFks'].update({
                            ttc: refKey
                        })
                        print('PASSED SCHEMA REF INT: ', ttc, '->', refKey)
                        self.schema[table]['schemaRefInt'] = True

            except Exception as e:
                print('SCHEMA REF INT CHECK ERROR SKIPPING TABLE: ', e)
                self.schema[table]['schemaRefInt'] = False
                continue
