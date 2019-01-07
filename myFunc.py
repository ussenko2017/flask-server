from JSONdb.DBHelper import DBHelper
import datetime,json,random

DBName = 'database'

STUDENT_TABLE = 'students'
PREDMET_TABLE = 'predmets'
BALL_TABLE = 'balls'
OTDEL_TABLE = 'otdels'
USER_TABLE = 'users'


NAME_FIELD = 'name'
FIRSTNAME_FIELD = 'firstname'
LASTNAME_FIELD = 'lastname'
PATR_FIELD = 'patr'
NUMBER_FIELD = 'number'
OTDEL_ID_FIELD = 'otdel_id'
KOLVO_CHASOV_FIELD = 'kolvo_chasov'
BALL_FIELD = 'ball'
PREDMET_ID_FIELD = 'predmet_id'
STUDENT_ID_FIELD = 'student_id'
DATE_FIELD = 'date'
ID_FIELD = 'id'
EMAIL_FIELD = 'email'
PASSWORD_FIELD = 'password'

def getDate():
    now = datetime.datetime.now()
    return '{0}.{1}.{2} {3}:{4}'.format(now.day,now.month,now.year,now.hour,now.minute)

def createTables(DBName):
    try:
        with open(DBName + ".json", "r", encoding="utf-8") as file:
            json.load(file)
            db = DBHelper(DBName)
    except FileNotFoundError:
        db = DBHelper(DBName)
        db.newTable(STUDENT_TABLE,[FIRSTNAME_FIELD,LASTNAME_FIELD,PATR_FIELD,NUMBER_FIELD,OTDEL_ID_FIELD,DATE_FIELD])
        db.newTable(PREDMET_TABLE,[NAME_FIELD,KOLVO_CHASOV_FIELD,DATE_FIELD])
        db.newTable(OTDEL_TABLE,[NAME_FIELD,DATE_FIELD])
        db.newTable(BALL_TABLE,[BALL_FIELD,PREDMET_ID_FIELD,STUDENT_ID_FIELD,DATE_FIELD])
        db.newTable(USER_TABLE,[EMAIL_FIELD,PASSWORD_FIELD,DATE_FIELD])
    return db



def getStatByPredmet():
    db = createTables(DBName)
    balls = db.select(db.SELECT_TYPE_STANDARD, BALL_TABLE, 0)
    predmets = db.select(db.SELECT_TYPE_STANDARD, PREDMET_TABLE, 0)

    predmet_list = []
    for predmet in predmets:
        count = 0
        summ = 0
        string = ' '
        for ball in balls:
            if predmet != db.IDS and predmet != db.COLUMN_LIST and ball != db.IDS and ball != db.COLUMN_LIST:
                if predmet == balls[ball][PREDMET_ID_FIELD]:
                    count+=1
                    summ+=int(balls[ball][BALL_FIELD])
        try:
            string = '{:.4}'.format(str(summ/count))

            predmet_list.append([string,predmets[predmet][NAME_FIELD]])
        except:pass
    return predmet_list

def getStatByStudent():
    db = createTables(DBName)
    balls = db.select(db.SELECT_TYPE_STANDARD, BALL_TABLE, 0)
    students = db.select(db.SELECT_TYPE_STANDARD, STUDENT_TABLE, 0)


    student_list = []
    for student in students:
        count = 0
        summ = 0
        string = ' '

        for ball in balls:
            if student != db.IDS and students != db.COLUMN_LIST and ball != db.IDS and ball != db.COLUMN_LIST:
                if student == balls[ball][STUDENT_ID_FIELD]:
                    count+=1
                    summ+=int(balls[ball][BALL_FIELD])
        try:
            string = '{:.4}'.format(str(summ/count))

            student_list.append([string,students[student][LASTNAME_FIELD] + ' ' +
                        students[student][FIRSTNAME_FIELD]+ ' ' +
                        students[student][PATR_FIELD]])
        except:
            pass
    return student_list

def autoadd():
    db = DBHelper(DBName)
    for j in range(10):
        num = j + 1
        db.addRow(OTDEL_TABLE, ['Отделение' + str(num), getDate()])
        db.addRow(PREDMET_TABLE, ['Предмет' + str(num), str(random.randint(24, 89)), getDate()])
        db.addRow(STUDENT_TABLE,
                  ['Имя' + str(num),
                   'Фамилия' + str(num),
                   'Отчество' + str(num),
                   str(random.randint(87270000000, 87970000000)),
                   str(random.randint(1, 10)),
                   getDate()])
    for i in range(300):
        db.addRow(BALL_TABLE,[str(random.randint(2, 5)),
                              str(random.randint(1, 10)),
                              str(random.randint(1, 10)),
                              getDate()])
def addInTable(*args):
    db = createTables(DBName)
    db.addRow(args)



def addUser(ColumnListVariables,email):
    db = createTables(DBName)
    #ColumnListVariables.append(getDate())
    id = db.base[USER_TABLE][db.IDS] + 1
    db.base[USER_TABLE][db.IDS] = id
    list = db.base[USER_TABLE][db.COLUMN_LIST]
    column_dict = {}
    for i in range(len(list)):
        column_dict.update(dict([(list[i], ColumnListVariables[i])]))
    column_dict.update([('id', id)])
    di = dict([(email, column_dict)])
    db.base[USER_TABLE].update(di)

    # Update base
    db.CreateOrUpdateBase(db.DBName)