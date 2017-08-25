import urllib.request, urllib.parse, urllib.error
import pdfkit
from bs4 import BeautifulSoup
import re
import sqlite3

conn = sqlite3.connect('knit_result_2017.sqlite')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS result_2017 (Rollno INTEGER, Name varchar, father_name varchar, Branch varchar, year varchar, semIII INTEGER, semIV INTEGER, Total INTEGER)''')
serviceurl = 'http://knit.ac.in/coe/ODD_2016/btreg16xcdaz.asp?rollno='

roll_list = open('roll_list.txt','r')
roll_list = roll_list.read()
roll_list = roll_list.split(",")


for rollno in roll_list:
    cur.execute('SELECT * FROM result_2017 WHERE Rollno= ? ', (int(rollno), ))
    row = cur.fetchone()
    if row is None:
        url = serviceurl + str(rollno)
        print('Retrieving', url)
        uh = urllib.request.urlopen(url)
        data = uh.read().decode()

        mark = re.findall('<td.+?>(.+?)/2000</td>', data)
        try:
            Total = int(mark[0])
            pdf = "pdf/"+str(rollno)+".pdf"
            print (pdf)
            pdfkit.from_url(url, pdf)
        except:
            print ("Result not found !!!!!!")
            continue
        En = re.findall('<td.*?>(.+?)</td>', data)
# computing the personal details of student

        name = En[1]
        fname = En[3]
        branch = En[7]
        year = En[170]

# calculating the marks of III semester        
        semIII = [En[103], En[110], En[117], En[124], En[131], En[138], En[145], En[152], En[159], En[166]]
        marks=0
        for mark in semIII:
            try:
                mark = int(mark)
            except:
                string = ""
                for a in mark:
                    if a == '*':
                        continue
                    string += a
                mark = int(string)
            marks += mark
        semIII=marks



# calculating the marks of IV semester        
        semIV = [En[24], En[38], En[45], En[52], En[59], En[66], En[73], En[80], En[87], En[94]]
        marks=0
        for mark in semIV:
            try:
                mark = int(mark)
            except:
                string = ""
                for a in mark:
                    if a == '*':
                        continue
                    string += a
                mark = int(string)
            marks += mark
        semIV=marks
        

        print (rollno,name,Total)

        cur.execute('''INSERT INTO result_2017 (Rollno, Name, father_name, Branch, year, semIII, semIV, Total) VALUES ( ?, ?, ?, ?, ?, ?, ?, ? )''', (rollno,name,fname,branch,year,semIII,semIV,Total))
        conn.commit()
    else:
        print (row[0], row[1], row[6])
sqlstr = 'SELECT * FROM result_2017 ORDER BY Total DESC'

count = 1
for row in cur.execute(sqlstr) :
    print (count, row[6], row[0], row[1])
    count += 1

