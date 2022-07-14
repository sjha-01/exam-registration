import psycopg2 as connector
import psycopg2.extras


class Database:
    def __init__(self):
        self.con = connector.connect(
            host='ec2-52-204-157-26.compute-1.amazonaws.com', port='5432', user='xhpgiuarbzkoup', password='0e3149f1ee98a2ecb45a948ada55c1af027bf6044d3e724c4634aecb4bf611f5', database='dberlnocf4u3fk')
        self.con.autocommit = True
        self.cur = self.con.cursor(cursor_factory= psycopg2.extras.DictCursor)
        
        # user is a reserved keyword in postgresql
        tables = ['''create table if not exists user1 (
                       username varchar(20),
                       password varchar(20),
                       fullname varchar(30),
                       primary key (username)
                    )
                   ''',

                  '''create table if not exists student_details (
                        username varchar(20),
                        gender varchar(6),
                        dob date,
                        guardian_name varchar(30),
                        category varchar(10),
                        email varchar(30),
                        mobile varchar(15),
                        addr varchar(150),
                        pin int,
                        xth decimal(5,2),
                        xiith decimal(5,2),
                        ugscheme varchar(11),
                        ugmarks decimal(5,2),
                        primary key (username),
                        constraint fk_student_details_to_user
                            foreign key (username)
                            references user1 (username)
                            on delete cascade
                        )                  
                    ''',

                  '''create table if not exists registered_students (
                        id serial,
                        username varchar(20) not null,
                        registration_no varchar(20),
                        primary key (id),
                        constraint fk_registered_to_users
                            foreign key (username)
                            references user1 (username)
                            on delete cascade
                        )'''
                  ]
        for table in tables:
            self.cur.execute(table)
        print('Created tables')

    def create_user(self, username, password, fullname):
        query = "insert into user1 values ('{}', '{}', '{}')".format(
            username, password, fullname)
        self.cur.execute(query)
        print('Row Inserted successfully')

    def isUnique(self, username):
        query = "select * from user1 where username = '{}'".format(username)
        self.cur.execute(query)
        result = self.cur.fetchall()
        if len(result) == 0:
            return True
        return False

    def userExists(self, username, password):
        query = "select * from user1 where username = '{}' and password='{}'".format(
            username, password)
        self.cur.execute(query)
        result = self.cur.fetchall()
        if len(result) == 1:
            return True
        return False

    def getFullName(self, username):
        query = "select fullname from user1 where username = '{}'".format(
            username)
        self.cur.execute(query)
        result = self.cur.fetchone()
        return result['fullname']

    def registrationExists(self, username):
        query = "select * from student_details where username = '{}'".format(
            username)
        self.cur.execute(query)
        result = self.cur.fetchall()
        if len(result) == 1:
            return True
        return False

    def create_registration(self, username, gender, dob, guardianname, category, email, mobile, address, pin, xth, xiith, ugscheme, ugmarks):
        query = "insert into student_details(username, gender, dob, guardian_name, category, email, mobile, addr, pin, xth, xiith, ugscheme, ugmarks) values ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})".format(
            username, gender, dob, guardianname, category, email, mobile, address, pin, xth, xiith, ugscheme, ugmarks)
        print('query', query)
        self.cur.execute(query)
        print('Reg Inserted successfully')

    def update_registration(self, username, gender, dob, guardianname, category, email, mobile, address, pin, xth, xiith, ugscheme, ugmarks):
        query = "update student_details set gender={}, dob={}, guardian_name={}, category={}, email={}, mobile={}, addr={}, pin={}, xth={}, xiith={}, ugscheme={}, ugmarks={} where username={}".format(
            gender, dob, guardianname, category, email, mobile, address, pin, xth, xiith, ugscheme, ugmarks, username)
        print(query)
        self.cur.execute(query)
        # print('Reg updated successfully')

    def getRegistrationProgress(self, username):
        query = "select * from student_details where username = '{}'".format(
            username)
        self.cur.execute(query)
        result = self.cur.fetchone()
        return result

    def isRegistrationPending(self, username):
        result = self.getRegistrationProgress(username)
        for k, v in result.items():
            if k == 'submitted':
                continue
            if not v:
                return True
        return False

    def submitRegistration(self, username):
        query = "insert into registered_students(username) values('{}')".format(
            username)
        self.cur.execute(query)
        query = "select id from registered_students where username='{}'".format(
            username)
        self.cur.execute(query)
        id = self.cur.fetchone()['id']
        registration_no = '202204' + '{0:04}'.format(id)
        query = "update registered_students set registration_no='{}' where username='{}'".format(
            registration_no, username)
        self.cur.execute(query)

    def isRegSubmitted(self, username):
        query = "select * from registered_students where username = '{}'".format(
            username)
        self.cur.execute(query)
        result = self.cur.fetchall()
        if len(result) == 0:
            return False
        return True

    def getRegistrationNo(self, username):
        query = "select registration_no from registered_students where username='{}'".format(
            username)
        self.cur.execute(query)
        return self.cur.fetchone()['registration_no']


db1 = Database()
# print(db1.isRegSubmitted('sjha'))

# '{0:04}'.format(id)
# a1='a'
# s='subham {}'.format('Jh'+a1)
# print(s)
