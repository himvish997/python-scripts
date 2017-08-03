import urllib.request, urllib.parse, urllib.error
#import json
#import pdfkit
#from bs4 import BeautifulSoup
import re
import sqlite3

conn = sqlite3.connect('result_IT.sqlite')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS Result (Roll_No INTEGER, Name TEXT, Marks INTEGER)''')
# Note that Google is increasingly requiring keys
# for this API
serviceurl = 'http://knit.ac.in/coe/ODD_2016/btreg16xcdaz.asp?rollno='
roll_list = []
for rollno in range(15601, 15661):
    roll_list.append(rollno)
for rollno in range(168601, 168613):
    roll_list.append(rollno)


for rollno in roll_list:
    cur.execute('SELECT * FROM Result WHERE Roll_No = ? ', (rollno, ))
    row = cur.fetchone()
    if row is None:
        url = serviceurl + str(rollno)
        print('Retrieving', url)
        uh = urllib.request.urlopen(url)
        data = uh.read().decode()

        mark = re.findall('<td.+?>(.+?)/2000</td>', data)
        try:
            mark = int(mark[0])
        except:
            continue
        rollNo = re.findall('<td>([0-9]+?)</td>', data)
        rollNo = int(rollNo[0])
        
        En = re.findall('<td.*?>(.+?)</td>', data)
        En = [En[1], En[3], En[5]]
        print(mark,En[2],En[0])
        '''for en in En:
            print(count, en)
            count += 1'''
        cur.execute('''INSERT INTO Result (Roll_No, Name, Marks) VALUES ( ?, ?, ? )''', ( En[2], En[0], mark ) )
        conn.commit()
    else:
        print (row[2], row[0], row[1])
sqlstr = 'SELECT * FROM Result ORDER BY Marks DESC'

count = 1
for row in cur.execute(sqlstr) :
    print (count, row[2], row[0], row[1])
    count += 1

