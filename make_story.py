import sys
sys.dont_write_bytecode = True

from dataclasses import dataclass
from faker import Faker
from faker_vehicle import VehicleProvider

import random
# random.seed(0) # test seed code
from datetime import date,datetime,timedelta
import sqlite3

import util.data_gen as data_gen
import util.csv_to_db as csv_to_db

data_gen 
csv_to_db

fake = Faker()
# Faker.seed(0) # test seed code

# make crime_day 
crime_date_row = fake.date_between_dates(date_start=datetime(2017,1,1),date_end=datetime(2018,5,1))
td = timedelta(days=-7)
crime_date = crime_date_row.strftime("%Y%m%d")                                                                      
workout_date_row = date(crime_date_row.year,crime_date_row.month,crime_date_row.day) + td
workout_date = workout_date_row.strftime("%b,%d,%Y")
workout_date_db = (date(crime_date_row.year,crime_date_row.month,crime_date_row.day) + td).strftime("%Y%m%d") 
# make persons init
# 0:criminal,1:Witness 1,2:Witness 2,3:true criminal,4:fake_member1,
# 5:fake_member2,6:fake_driver1,7:fake_driver2,8:fake_driver3,9:fake_driver4
charctors = 10
persons = [] 
db_filepath = './mystery.db'
conn = sqlite3.connect(db_filepath)
cur = conn.cursor()
cur.execute('SELECT * from person order by random() limit (?)',[charctors])
persons = cur.fetchall()

# make crime_scene_report add クライムレポートは1件のみ重複書き込みするので要再考
db_filepath = './mystery.db'
conn = sqlite3.connect(db_filepath)
cur = conn.cursor() 
new_line = [crime_date,'murder','Security footage shows that there were 2 witnesses. \
The first witness lives at the last house on "Northwestern Dr". \
The second witness, named Annabel, lives somewhere on "Franklin Ave".','SQL City']
cur.execute('INSERT INTO crime_scene_report VALUES (?,?,?,?);', new_line)
conn.commit()
conn.close()

# make witnenss 1 DBからwitness1を決定し、personsに入れておく
db_filepath = './mystery.db'
conn = sqlite3.connect(db_filepath)
cur = conn.cursor()
# witness_1_id is max_address number in person_table and change person(1)
cur.execute('SELECT * from person WHERE address_street_name = "Northwestern Dr" order by address_number Desc limit 1')
persons[1]  = list(cur.fetchone())

# make witnenss 2 address create add 
city2 = 'Franklin Ave'
name2 = 'Annabel Miller'
cur.execute('UPDATE person SET address_street_name = (?) WHERE id = (?)',[city2,persons[2][0]]) # address
cur.execute('UPDATE person SET name = (?) WHERE id = (?)',[name2,persons[2][0]]) # name
conn.commit()
cur.execute('SELECT * from person WHERE name = (?) and address_street_name = (?)',[name2,city2])
persons[2]  = list(cur.fetchone())

# make interviews
witness1_intervew = 'I heard a gunshot and then saw a man run out. He had a "Get Fit Now Gym" bag.\
The membership number on the bag started with "48Z". Only gold members have those bags. \
The man got into a car with a plate that included "H42W".'
witness2_intervew = 'I saw the murder happen, and I recognized the killer from my gym when \
I was working out last week on ' + workout_date + '.'
criminal_interview = '''I was hired by a woman with a lot of money. \
I don't know her name but I know she's around 5'5" (65") or 5'7" (67"). \
She has red hair and she drives a Tesla Model S. \
I know that she attended the SQL Symphony Concert 3 times in December 2017.'''

db_filepath = './mystery.db'
conn = sqlite3.connect(db_filepath)
cur = conn.cursor()

# make witness 1 interview
cur.execute('INSERT INTO interview VALUES (?,?)',[persons[1][0],witness1_intervew])
# make witness 2 interview
cur.execute('INSERT INTO interview VALUES (?,?)',[persons[2][0],witness2_intervew])
# make criminal interview
cur.execute('INSERT INTO interview VALUES (?,?)',[persons[0][0],criminal_interview])
conn.commit()
conn.close()

    
# get people data
criminal = persons[0]
witness1 = persons[1]
witness2 = persons[2]
true_criminal = persons[3]
fake_member1 = persons[4]
fake_member2 = persons[5]
fake_driver1 = persons[6]
fake_driver2 = persons[7]
fake_driver3 = persons[8]
fake_driver4 = persons[9]

# criminal in get_fit_members
db_filepath = './mystery.db'
conn = sqlite3.connect(db_filepath)
cur = conn.cursor()
# cur.execute('SELECT * from get_fit_now_member WHERE person_id = (?)',criminal[0])
# memberdata = cur.fetchone()

# old make fit_members maker
cur.execute('DELETE FROM get_fit_now_member WHERE id = (?) or id = (?) or id = (?) or id = (?);',['48Z38','48Z7A','48Z55','90081'])
conn.commit()
cur.execute('INSERT INTO get_fit_now_member VALUES (?,?,?,?,?)',['48Z38',fake_member1[0],fake_member1[1],'20170203','silver'])
cur.execute('INSERT INTO get_fit_now_member VALUES (?,?,?,?,?)',['48Z7A',fake_member2[0],fake_member2[1],'20160305','gold'])
cur.execute('INSERT INTO get_fit_now_member VALUES (?,?,?,?,?)',['48Z55',criminal[0],criminal[1],'20160101','gold'])
cur.execute('INSERT INTO get_fit_now_member VALUES (?,?,?,?,?)',['90081',witness2[0],witness2[1],'20160208','gold'])
conn.commit()
# change checkin data 
cur.execute('INSERT INTO get_fit_now_check_in VALUES (?,?,?,?)',['48Z55',workout_date_db,'1530','1700'])
conn.commit()
conn.close()

# make drivers_license
db_filepath = './mystery.db'
conn = sqlite3.connect(db_filepath)
cur = conn.cursor()
# clean up people's license
license_list = [criminal[2],witness1[2],witness2[2],fake_member1[2],fake_driver1[2],fake_driver2[2],fake_driver3[2],fake_driver4[2]]
for j in license_list:
    cur.execute('DELETE FROM drivers_license WHERE id = (?);',[j])
conn.commit()

# 1 criminal + 1fake_member + 2 fake drivers + 2 witness
drivers_data = list()
drivers_data.append([witness1[2],'35','65','green','brown','female','23AM98','Toyota','Yaris'])
drivers_data.append([witness2[2],'64','84','blue','white','male','00NU00','Mercedes-Benz','E-Class'])
drivers_data.append([fake_member1[2],'88','67','amber','grey','male','7REGF3','Chevrolet','Express 1500'])
drivers_data.append([fake_driver1[2],'21','65','blue','blonde','female','H42W0X','Toyota','Prius'])
drivers_data.append([fake_driver2[2],'30','70','brown','brown','male','0H42W2','Chevrolet','Spark LS'])
drivers_data.append([fake_driver3[2],'65','66','blue','red','female','08CM64','Tesla','Model S'])
drivers_data.append([fake_driver4[2],'48','65','black','red','female','917UU3','Tesla','Model S'])
drivers_data.append([criminal[2],'21','71','black','black','male','4H42WR','Nissan','Altima'])
drivers_data.append([true_criminal[2],'68','66','green','red','female','500123','Tesla','Model S'])
for driver_data in drivers_data:
    cur.execute('INSERT INTO drivers_license VALUES (?,?,?,?,?,?,?,?,?)',driver_data)
conn.commit()
conn.close()

# show persons list  TEST Code
# db_filepath = './story.db'
# conn = sqlite3.connect(db_filepath)
# print("persons:")
# cur = conn.cursor()
# for p in persons:
#     cur.execute('SELECT * from person WHERE id = (?)',[p[0]])
#     print(cur.fetchone())
# conn.close()

# 2nd story
# true criminal info update female name,SQL Symphony Concert event ID : 1143 , income

true_criminal = persons[3]
true_criminal_rename = fake.name_female()
true_criminal_income = 310000
db_filepath = './mystery.db'
conn = sqlite3.connect(db_filepath)
cur = conn.cursor()
rename_sql = "UPDATE person SET name = (?) WHERE id = (?)"
income_sql = "INSERT INTO income VALUES (?,?);"
cur.execute(rename_sql,[true_criminal_rename,true_criminal[0]])
cur.execute(income_sql,[true_criminal[5],true_criminal_income])
conn.commit()

# make 3 times events
cur.execute('SELECT * from facebook_event_checkin WHERE event_name  like "SQL%" and date like "2017%" order by random() limit 3')
events = cur.fetchall()
for i in  events:
    event = true_criminal[0],i[1],i[2],i[3]
    cur.execute("INSERT INTO facebook_event_checkin VALUES (?,?,?,?)",event)
    conn.commit()
conn.close()

# trigger make 
hex_criminal_name = (persons[0][1].encode('utf-8')).hex().upper()
hex_true_criminal_name = (true_criminal_rename.encode('utf-8')).hex().upper()
create_solution_table = """CREATE TABLE solution (
        user integer,
        value text
    )
"""
trigger = """
CREATE TRIGGER check_solution AFTER INSERT ON solution
    WHEN new.user==1
    BEGIN
        DELETE FROM solution;
        INSERT INTO solution VALUES (0,
        CASE WHEN hex(new.value)=='{0}' THEN "Congrats, you found the murderer! But wait, there's more... \
If you think you're up for a challenge, try querying the interview transcript of the murderer to find the real villain behind this crime. \
If you feel especially confident in your SQL skills, try to complete this final step with no more than 2 queries. \
Use this same INSERT statement with your new suspect to check your answer."
             WHEN hex(new.value)=='{1}' THEN "Congrats, you found the brains behind the murder! \
Everyone in SQL City hails you as the greatest SQL detective of all time. Time to break out the champagne!"
             ELSE "That's not the right person. Try again!"
        END
        );
    END
"""
trigger_sql = trigger.format(hex_criminal_name,hex_true_criminal_name)
# print("hex_criminal_name:",hex_criminal_name)
# print("hex_true_criminal_name:",hex_true_criminal_name)
db_filepath = './mystery.db'
conn = sqlite3.connect(db_filepath)
cur = conn.cursor()
cur.execute(create_solution_table)
conn.commit()
cur.execute(trigger_sql)
conn.commit()

# introduction
introduction = '''\n\n ***Generate SQL Mystery*** \n 
There's been a Murder in SQL City  on {} ! \
Check out Crime scene report.\n\n'''
print(introduction.format(crime_date_row.strftime("%b,%d,%Y")))