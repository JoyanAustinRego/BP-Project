import MySQLdb
import os
import webbrowser


def dbinit():
    global db
    db = MySQLdb.connect(host="localhost", user="root", passwd="", db="daqtest")


def createTable():
    global cur
    cur = db.cursor()
    cur.execute('''Create table if not exists project(ID int not null auto_increment,CDate varchar(20),CTime varchar(20),Name varchar(45),Age int,Blood_Pressure decimal(12,8),
    primary key(id));''')


def entries(cdate, ctime, name, age, bpval):
    cur.execute('insert into project(cdate,ctime,name,age,blood_pressure) values (%s,%s,%s,%s,%s)', (cdate, ctime, name, age, bpval))


def viewxl():
    os.chdir('C:\python')
    os.startfile('alpha.csv')


def viewdb():
    webbrowser.open('http://localhost/phpmyadmin/')


def fwrite(cdate, ctime, name, age, bpval):
    filename = open('C:\\python\\alpha.csv','a')
    filename.write('%s,%s,%s,%s,%s\n' % (cdate, ctime, name, age, bpval))
    filename.close()


if __name__ == '__main__':
    viewxl()
