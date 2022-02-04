import sys
sys.dont_write_bytecode = True

import csv
import sqlite3
import os

def person():
    # query for create table
    table_sql = """CREATE TABLE person (
            id integer PRIMARY KEY,
            name text,
            license_id integer,
            address_number integer,
            address_street_name text,
            ssn integer,
            FOREIGN KEY (license_id) REFERENCES drivers_license(id));"""

    # import csv file_name
    file_name = 'person.csv'
    # query for import csv file
    row_sql = 'INSERT INTO person VALUES (?,?,?,?,?,?);'
    
    return [file_name,table_sql,row_sql]
    
def crime_scene_report():
    table_sql = """CREATE TABLE crime_scene_report (
            date integer,
            type text,
            description text,
            city text
        );"""

    # import csv file_name
    file_name = 'crime_scene_report.csv'
    # query for import csv file
    row_sql = 'INSERT INTO crime_scene_report VALUES (?,?,?,?);'
    
    return [file_name,table_sql,row_sql]

def drivers_license():
    table_sql = """CREATE TABLE drivers_license (
            id integer PRIMARY KEY,
            age integer,
            height integer,
            eye_color text,
            hair_color text,
            gender text,
            plate_number text,
            car_make text,
            car_model text
            );"""

    # import csv file_name
    file_name = 'drivers_license.csv'
    # query for import csv file
    row_sql = 'INSERT INTO drivers_license VALUES (?,?,?,?,?,?,?,?,?);'
    
    return [file_name,table_sql,row_sql]    

def face_book_event_checkin():
    table_sql = """CREATE TABLE facebook_event_checkin (
            person_id integer,
            event_id integer,
            event_name text,
            date integer,
            FOREIGN KEY (person_id) REFERENCES person(id)
            );""" 

    # import csv file_name
    file_name = 'facebook_event_checkin.csv'
    # query for import csv file
    row_sql = 'INSERT INTO facebook_event_checkin VALUES (?,?,?,?);'
    
    return [file_name,table_sql,row_sql]   

def get_fit_now_check_in_sql():
    table_sql = """CREATE TABLE get_fit_now_check_in (
            membership_id text,
            check_in_date integer,
            check_in_time integer,
            check_out_time integer,
            FOREIGN KEY (membership_id) REFERENCES get_fit_now_member(id)
            );"""

    # import csv file_name
    file_name = 'get_fit_now_check_in.csv'
    # query for import csv file
    row_sql = 'INSERT INTO get_fit_now_check_in VALUES (?,?,?,?);'
    
    return [file_name,table_sql,row_sql]

def get_fit_now_member():
    table_sql = """CREATE TABLE get_fit_now_member (
            id text PRIMARY KEY,
            person_id integer,
            name text,
            membership_start_date integer,
            membership_status text,
            FOREIGN KEY (person_id) REFERENCES person(id)
        );"""

    # import csv file_name
    file_name = 'get_fit_now_member.csv'
    # query for import csv file
    row_sql = 'INSERT INTO get_fit_now_member VALUES (?,?,?,?,?);'
    
    return [file_name,table_sql,row_sql]   
   
def income():
    table_sql = """CREATE TABLE income (
            ssn integer PRIMARY KEY,
            annual_income integer
        );"""

    # import csv file_name
    file_name = 'income.csv'
    # query for import csv file
    row_sql = 'INSERT INTO income VALUES (?,?);'
    
    return [file_name,table_sql,row_sql]  

def interview():
    table_sql = """CREATE TABLE interview (
            person_id integer,
            transcript text,
            FOREIGN KEY (person_id) REFERENCES person(id)
        );"""

    # import csv file_name
    file_name = 'interview.csv'
    # query for import csv file
    row_sql = 'INSERT INTO interview VALUES (?,?);'
    
    return [file_name,table_sql,row_sql]  

# init 
csv_path = './CSV'
db_path = 'mystery.db'
table_creators_list = ['person()','crime_scene_report()','drivers_license()','face_book_event_checkin()','get_fit_now_check_in_sql()','get_fit_now_member()','income()','interview()']
if os.path.exists(db_path):
    os.remove(db_path)
    
# # db query exec
for tc in table_creators_list:
    file_name,table_sql,row_sql = eval(tc)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(table_sql)
    conn.commit()
    with open(csv_path+'/'+file_name, 'rt') as f: 
        rows = csv.reader(f)
        header = next(rows)
        for line in rows:
            cur.execute(row_sql, line)
    conn.commit()
    conn.close()
