
import requests,myFunc
for i in range(1000):
    r = requests.get('http://127.0.0.1:5000/api/v1/add/',
                 params={'tablename':myFunc.OTDEL_TABLE,
                         myFunc.NAME_FIELD:myFunc.NAME_FIELD})
    r1 = requests.get('http://127.0.0.1:5000/api/v1/add/',
                 params={'tablename':myFunc.STUDENT_TABLE,
                         myFunc.FIRSTNAME_FIELD:myFunc.FIRSTNAME_FIELD,
                         myFunc.LASTNAME_FIELD:myFunc.LASTNAME_FIELD,
                         myFunc.PATR_FIELD:myFunc.PATR_FIELD,
                         myFunc.NUMBER_FIELD: myFunc.NUMBER_FIELD,
                         myFunc.OTDEL_ID_FIELD:1
                         })
    r2 = requests.get('http://127.0.0.1:5000/api/v1/add/',
                 params={'tablename':myFunc.PREDMET_TABLE,
                         myFunc.NAME_FIELD:myFunc.NAME_FIELD,
                         myFunc.KOLVO_CHASOV_FIELD:99,
                         })
    r3 = requests.get('http://127.0.0.1:5000/api/v1/add/',
                 params={'tablename':myFunc.BALL_TABLE,
                         myFunc.BALL_FIELD:'1',
                         myFunc.PREDMET_ID_FIELD:'1',
                         myFunc.STUDENT_ID_FIELD:'1'})
    messages = r.json()
    messages1 = r1.json()
    messages2 = r2.json()
    messages3 = r3.json()
    print(messages)
    print(messages1)
    print(messages2)
    print(messages3)
