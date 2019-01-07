import json
import datetime



class DBHelper:
    DBName = 'StandartName'
    base = {}

    #Постоянные базы данных
    CONFIG = 'config'
    BASE_NAME = 'name'
    CREATE_DATE  = 'createDate'
    COLUMN_LIST = 'ColumnList'
    IDS = 'ids'
    #

    SELECT_TYPE_STANDARD = 'standard'
    SELECT_TYPE_DISTINCT = 'distinct'
    SELECT_TYPE_LIMIT = 'limit'


    def __init__(self, DBName):
        self.openBase(DBName)

    def openBase(self, DBName):
        self.DBName = DBName
        try:
            with open(DBName+".json", "r", encoding="utf-8") as file:
                base = json.load(file)
                self.base = base
        except FileNotFoundError:
            now = datetime.datetime.now()
            self.base = {"config":{"name":DBName,"createDate":
                str(now.day)+'.'+str(now.month)+'.'+str(now.year) + ' '+ str(now.hour)+':'+str(now.minute)}}
            self.CreateOrUpdateBase(DBName)

    def CreateOrUpdateBase(self, DBName):
        if self.DBName == DBName:
            with open(DBName+".json", "w", encoding="utf-8") as file:
                file.write(json.dumps(self.base, ensure_ascii=False))
            self.openBase(DBName)

    def dropTable(self,TableName):
        self.base[TableName].clear()

        # Update base
        self.CreateOrUpdateBase(self.DBName)

    def newTable(self,TableName,ColumnList):
        ids = 0
        dict_column = dict([(self.COLUMN_LIST,ColumnList)])
        dict_ids = dict([(self.IDS,ids)])
        dict_table = dict([(TableName,dict_column)])
        self.base.update(dict_table)
        self.base[TableName].update(dict_ids)

        #Update base
        self.CreateOrUpdateBase(self.DBName)

    def addRow(self,TableName,ColumnListVariables):
        id = self.base[TableName][self.IDS] + 1
        self.base[TableName][self.IDS] = id
        list = self.base[TableName][self.COLUMN_LIST]
        column_dict = {}
        for i in range(len(list)):
            column_dict.update(dict([(list[i],ColumnListVariables[i])]))
        column_dict.update([('id',id)])
        di = dict([(id,column_dict)])
        self.base[TableName].update(di)


        # Update base
        self.CreateOrUpdateBase(self.DBName)

    def select(self, type , table_name,res_arg):
            if type == self.SELECT_TYPE_STANDARD:
                return self.base[table_name]
            elif type == self.SELECT_TYPE_DISTINCT:
                return None
            elif type == self.SELECT_TYPE_LIMIT:
                list = []
                count = 0
                res_arg+=2
                for i in self.base[table_name].values():
                    if count < res_arg and count > 1:
                        list.append(i)
                    count += 1
                return list




    def getObjByIdAndTableName(self,TableName,id):
        return self.base[TableName][id]







