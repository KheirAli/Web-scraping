import requests
from bs4 import BeautifulSoup
import mysql.connector
import re

def englishmaker (a):
    b = []
    for letter in a :
        if letter == '۰':
            b.append('0')
        elif letter == '۱':
            b.append('1')
        elif letter == '۲':
            b.append('2')
        elif letter == '۳':
            b.append('3')
        elif letter == '۴':
            b.append('4')
        elif letter == '۵':
            b.append('5')
        elif letter == '۶':
            b.append('6')
        elif letter == '۷':
            b.append('7')
        elif letter == '۸':
            b.append('8')
        elif letter == '۹':
            b.append('9')
    if str(b) != '':
        c = ''.join(b)
    else :
        c = ' '
    return c

def ML(cursor,cnx,voroodi):
    from sklearn import tree
    from sklearn import preprocessing
    le = preprocessing.LabelEncoder()
    clf = tree.DecisionTreeRegressor()
    x = []
    y = []
    a = []
    b = []
    cursor.execute('SELECT * FROM ihome;')
    for row in cursor:
        x.append([row[0],row[2],row[3],row[4]])
        y.append(row[1])
    for i in range (0,len(x)):
        a.append(str(x[i][0]))
    le.fit(a)
    for i in range (0,len(x)):
        b.append([int(le.transform([x[i][0]])),x[i][1],x[i][2],x[i][3]])
    clf = clf.fit(b,y)
    c = le.transform([str(voroodi[0])])
    print ('gheymat ehtemali :')
    print (clf.predict([[int(c),int(voroodi[1]),int(voroodi[2]),int(voroodi[3])]])[0])

def milion_maker (a):
    return a/1000000

def main (cursor,cnx):
    cursor.execute('CREATE TABLE ihome (mahalleh varchar(120) ,gheymat_be_milion int ,otaghe_khab int ,metraj int ,sal int)')
    cursor.execute("ALTER DATABASE `%s` CHARACTER SET 'utf8' COLLATE 'utf8_persian_ci'" %'test')
    sql = "SELECT DISTINCT(table_name) FROM information_schema.columns WHERE table_schema = '%s'" % 'test'
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        sql = "ALTER TABLE `%s` convert to character set DEFAULT COLLATE DEFAULT" % (row[0])
        cursor.execute(sql)
    count_page = 1
    count = 0 
    while count != 200 :
        b = 'https://www.ihome.ir/خرید-فروش/املاک/ایران/'
        if count_page == 1 :
            r = requests.get(b,verify = False)
            count_page += 1
        else :
            b = b + str(count_page) + '/'
            r = requests.get(b,verify = False)
            count_page += 1
        soup = BeautifulSoup(r.text,'html.parser')
        all_page = soup.find_all('div',attrs = {'class':'sh-content left'})
        for lists in all_page:
            l = []
            for line in str(lists).splitlines():
                l.append(englishmaker(str(line)))
            c = re.sub(r'\s+','',str(l)).split(',')
            l = []
            test = 0
            l.append(''.join(re.findall(r'\<span\>(.+)\<\/span\>',str(lists))))
            for letter in c :
                letter = letter.replace("'",'')
                if letter != '' and letter != "[" and letter != "]":
                    test += 1
                    if test == 1 :
                        l.append(milion_maker(int(letter)))
                    else:
                        l.append(letter)
            if int(l[2]) > 20 :
                if len(l)>3:
                    if int(l[3])<20 :
                        del(l[2])
            if int (l[2]) >20 :
                if len(l) == 3 :
                    l.append(0)
                    l[2],l[3] = l[3],l[2]
                    l.append(0)
                elif len(l) == 4 :
                    l.append(0)
                    l[3],l[4] = l[4],l[3]
                    l[2],l[3] = l[3],l[2]
            while len(l) != 5 and len(l) <= 5 :
                l.append(0)
            val =  (str(l[0]),l[1],l[2],l[3],l[4])
            sq = "INSERT INTO ihome VALUES (%s, %s, %s, %s, %s);"
            cursor.execute(sq, val)
            cnx.commit()
            #print (l)
            count += 1
            #print (count)
            if count == 200:
                break

def main_1 (cursor,cnx):
    count_page = 1
    count = 0 
    count_break = 0
    while count != 200 :
        if count_break == 1 :
            return
        b = 'https://www.ihome.ir/خرید-فروش/املاک/ایران/'
        if count_page == 1 :
            r = requests.get(b,verify = False)
            count_page += 1
        else :
            b = b + str(count_page) + '/'
            r = requests.get(b,verify = False)
            count_page += 1
        soup = BeautifulSoup(r.text,'html.parser')
        all_page = soup.find_all('div',attrs = {'class':'sh-content left'})
        for lists in all_page:
            l = []
            for line in str(lists).splitlines():
                l.append(englishmaker(str(line)))
            c = re.sub(r'\s+','',str(l)).split(',')
            l = []
            test = 0
            l.append(''.join(re.findall(r'\<span\>(.+)\<\/span\>',str(lists))))
            for letter in c :
                letter = letter.replace("'",'')
                if letter != '' and letter != "[" and letter != "]":
                    test += 1
                    if test == 1 :
                        l.append(milion_maker(int(letter)))
                    else:
                        l.append(letter)
            if int(l[2]) > 20 :
                if len(l)>3:
                    if int(l[3])<20 :
                        del(l[2])
            if int (l[2]) >20 :
                if len(l) == 3 :
                    l.append(0)
                    l[2],l[3] = l[3],l[2]
                    l.append(0)
                elif len(l) == 4 :
                    l.append(0)
                    l[3],l[4] = l[4],l[3]
                    l[2],l[3] = l[3],l[2]
            while len(l) != 5 :
                l.append(0)
            cursor.execute("SELECT 1 from ihome WHERE metraj = %s and gheymat_be_milion = %s and otaghe_khab = %s and sal = %s and mahalleh = %s",(str(l[3]),str(l[1]),str(l[2]),str(l[4]),str(l[0])))
            for i in cursor :
                if i == 'none' :
                    pass
                else :
                    return
            val =  (str(l[0]),l[1],l[2],l[3],l[4])
            sq = "INSERT INTO ihome VALUES (%s, %s, %s, %s, %s);"
            cursor.execute(sq, val)
            cnx.commit()
            #print (l)
            count += 1
            #print (count)
            if count == 200 :
                break

cnx = mysql.connector.connect(
    user = 'root' , password = '' , host = '127.0.0.1' , database = 'test'
)
cursor = cnx.cursor()
cursor.execute('SHOW TABLES;')
temp = 0
show = []
for i in cursor:
    if i == ('ihome',):
        temp += 1
if temp == 1 :
    main_1(cursor,cnx)
elif temp == 0:
    main(cursor,cnx)
cursor.execute('SELECT * FROM ihome;')
for row in cursor:
    show.append(row[0])
show = list(dict.fromkeys(show))
print (show)
vorood = input ('''
mahallehaye bala dar mysql shoma vojood darad
The input form must be like this : location , bedroom , meter , age
khaneye mored anzar khod ra vared konid :
''')
voroodi = vorood.split(',')
for i in range (0,len(voroodi)):
    voroodi[i] = voroodi[i].strip()
ML(cursor,cnx,voroodi)

cursor.close()
cnx.close()