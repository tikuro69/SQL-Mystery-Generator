import sys
sys.dont_write_bytecode = True

from collections import OrderedDict
from faker import Faker
from faker_vehicle import VehicleProvider

# random.seed(0) # test code
fake = Faker()

# fake.add_provider(VehicleProvider)
from datetime import datetime
import os
import csv

csv_path = "./CSV/"
if not os.path.exists(csv_path):
    os.makedirs(csv_path)
# person_table_data
def get_person():
    id = fake.unique.random_int(min=10000,max=99990)
    name = fake.unique.name()
    licence_id = fake.unique.random_int(min=100000,max=999999)
    address_number = fake.random_int(min=1,max=5000)
    address_street_name = fake.street_name()
    SSN = fake.unique.random_int(min=100000000,max=999999999)
    return [id,name,licence_id,address_number,address_street_name,SSN]

with open(csv_path+'person.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'name', 'licence_id', 'address_number', 'address_street_name', 'SSN'])
    for n in range(1, 10011):
        writer.writerow(get_person())
        
# person_table_data(set witness address on person_table)
num = 50
witness_1_id = 0
cnt = 0
persons_list = []
file = open(csv_path+"person.csv","r")
csv_reader = csv.reader(file)
header = next(csv_reader)

for row in csv_reader:
    persons_list.append(row)
    
n = len(persons_list)
while num >= cnt:
    r1 = fake.unique.random_int(min=0,max=n)
    r2 = fake.unique.random_int(min=0,max=n)
    persons_list[r1][4]='Northwestern Dr'
    persons_list[r2][4]='Franklin Ave'   
    cnt += 1
# person_csv rewrite
with open(csv_path+'person.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'name', 'licence_id', 'address_number', 'address_street_name', 'SSN'])
    for row in persons_list:
        writer.writerow(row)

# crime_scene_report       
def get_crime_scene_report():
    data = fake.date_between_dates(date_start=datetime(2017,1,1),date_end=datetime(2018,5,1)).strftime("%Y%m%d")
    type = fake.random_element(elements=('robbery','murder','theft','fraud','arson','bribery','assault','smuggling','blackmail'))
    description = fake.text(max_nb_chars=80)
    city = fake.city()
    return [data,type,description,city]

def get_crime_scene_sql_report():
    data = fake.date_between_dates(date_start=datetime(2017,1,1),date_end=datetime(2018,5,1)).strftime("%Y%m%d")
    type = fake.random_element(elements=('robbery','murder','theft','fraud','arson','bribery','assault','smuggling','blackmail'))
    description = fake.text(max_nb_chars=80)
    city = 'SQL City'
    return [data,type,description,city]

with open(csv_path+'crime_scene_report.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['data', 'type', 'description', 'city'])
    for n in range(1, 1228):
        r = fake.random_element(elements=OrderedDict([("a", 0.99), ("b", 0.01), ]))
        if r == "a":
            p = get_crime_scene_report()
            writer.writerow(p)
        elif r == "b":
            p = get_crime_scene_sql_report()
            writer.writerow(p)

# interview
def get_interview():
    person_id = fake.unique.random_int(min=10000,max=99990)
    transcript = fake.text(max_nb_chars=80)
    return [person_id,transcript]

    
with open(csv_path+'interview.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['person_id', 'transcript'])
    for n in range(1, 5000):
        writer.writerow(get_interview())

# get_fit_now_member
def get_now_member():
    id = fake.password(length=5,special_chars=False,upper_case=True,lower_case=False)
    person_id = fake.unique.random_int(min=10000,max=99990)
    name = fake.unique.name()
    membership_start_date = fake.date_between_dates(date_start=datetime(2016,1,1),date_end=datetime(2018,5,1)).strftime("%Y%m%d")
    membership_status = fake.random_element(elements=('gold','regular','silver'))
    return [id,person_id,name,membership_start_date,membership_status]
    
with open(csv_path+'get_fit_now_member.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id','person_id','name','membership_start_date','membership_status'])
    for n in range(1, 180):
        writer.writerow(get_now_member())

# drivers_license
def get_drivers_license():
    fake.add_provider(VehicleProvider)
    id = fake.unique.random_int(min=100000,max=999999)
    age = fake.random_int(min=18,max=99)
    height = fake.random_int(min=18,max=99)
    eye_color = fake.random_element(elements=('brown','green','amber','blue','black'))
    hair_color = fake.random_element(elements=('red','brown','green','grey','blue','white','black','blonde'))
    gender = fake.random_element(elements=('male','female'))
    plate_number = fake.unique.password(length=6,special_chars=False,upper_case=True,lower_case=False)
    car = fake.vehicle_object()
    car_make = car['Make']
    car_model = car['Model']
    return [id,age,height,eye_color,hair_color,gender,plate_number,car_make,car_model]
    
with open(csv_path+'drivers_license.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id','person_id','name','membership_start_date','membership_status'])
    for n in range(1, 10000):
        writer.writerow(get_drivers_license())

# get_now_check
def get_now_check():
    # membership_id = fake.password(length=5,special_chars=False,upper_case=True,lower_case=False)
    check_in_date = fake.date_between_dates(date_start=datetime(2017,1,1),date_end=datetime(2018,5,1)).strftime("%Y%m%d")
    check_in_time = fake.random_int(min=1,max=1600)
    check_out_time = fake.random_int(min=check_in_time,max=1730)
    return [check_in_date,check_in_time,check_out_time]
    
with open(csv_path+'get_fit_now_check_in.csv', 'w') as csvfile:
    file = open(csv_path+"get_fit_now_member.csv","r")
    csv_reader = csv.reader(file)
    header = next(csv_reader)
    writer = csv.writer(csvfile)
    writer.writerow(['membership_id','check_in_date','check_in_time','check_out_time'])
    for r in csv_reader:
        line = get_now_check()
        line.insert(0,r[0])
        writer.writerow(line)
    file.close()

# facebook_event_checkin
def get_facebook_event_checkin():
    person_id = fake.unique.random_int(min=10000,max=99990)
    event_id = fake.random_int(min=3,max=9974)
    event_name = fake.text(max_nb_chars=80)
    date = fake.date_between_dates(date_start=datetime(2017,1,1),date_end=datetime(2018,5,1)).strftime("%Y%m%d")
    return [person_id,event_id,event_name,date]

def get_SQL_Symphony_Concert():
    person_id = fake.unique.random_int(min=10000,max=99990)
    event_id = 1143
    event_name = "SQL Symphony Concert"
    date = fake.date_between_dates(date_start=datetime(2017,1,1),date_end=datetime(2018,5,1)).strftime("%Y%m%d")
    return [person_id,event_id,event_name,date]


with open(csv_path+'facebook_event_checkin.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['person_id','event_id','event_name','date'])
    fake = Faker()
    for _ in range(10000):
        r = fake.random_element(elements=OrderedDict([("a", 0.99), ("b", 0.01), ]))
        if r == "a":
            p = get_facebook_event_checkin()
            writer.writerow(p)
        elif r == "b":
            p = get_SQL_Symphony_Concert()
            writer.writerow(p)


# income
def get_income():
    ssn = fake.unique.random_int(min=100000000,max=999999999)
    annual_income = fake.random_int(min=10000,max=498500,step=100)
    return [ssn,annual_income]

with open(csv_path+'income.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['ssn','annual_income'])
    for n in range(1, 7514):
        writer.writerow(get_income())

     