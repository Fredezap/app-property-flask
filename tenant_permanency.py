import mysql.connector
import person
import property
import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Fede1234",
  database="appproperty"
)

mycursor = mydb.cursor(dictionary=True)

#INSERTS A NEW RENT (PERSON + PROPERTY + DATE) IN TENANT_PERMANENCY TABLE
def insert_rent(Id_person,Id_property,Entry_date=datetime.date.today(),Exit_date="-"):
	mycursor = mydb.cursor(dictionary=True)
	sql = '''INSERT INTO tenant_permanency (id_person,id_property,entry_date,exit_date)
	VALUES ({},{},'{}','{}')'''.format(Id_person,Id_property,Entry_date,Exit_date)
	mycursor.execute(sql)
	mydb.commit()
	success = mycursor.rowcount
	mycursor.close()
	return success

#UPDATE A EXIT DATE (TO STOP RENTING) IN TENANT_PERMANENCY TABLE
def stop_renting(id_tenant_permanency):
	mycursor = mydb.cursor(dictionary=True)
	exit_date = datetime.date.today()
	sql = '''UPDATE tenant_permanency SET exit_date='{}'
	WHERE id_tenant_permanency={}'''.format(exit_date,id_tenant_permanency)
	mycursor.execute(sql)
	mydb.commit()
	success = mycursor.rowcount
	mycursor.close()
	return success

def start_renting_again(id_tenant_permanency):
	mycursor = mydb.cursor(dictionary=True)
	exit_date = "-"
	sql = '''UPDATE tenant_permanency SET exit_date='{}'
	WHERE id_tenant_permanency={}'''.format(exit_date,id_tenant_permanency)
	mycursor.execute(sql)
	mydb.commit()
	success = mycursor.rowcount
	mycursor.close()
	return success

#SELECT ALL FROM TENANT_PERMANENCY TABLE
def select_all():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM tenant_permanency'''
	mycursor.execute(sql)
	everything = mycursor.fetchall()
	mycursor.close()
	if everything == []:
		everything = None
	print(type(everything))
	print(everything)
	return everything

def select_all_plus_info():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM tenant_permanency t INNER JOIN property pr ON t.id_property = pr.id_property
	INNER JOIN person pe ON t.id_person = pe.id_person'''
	mycursor.execute(sql)
	everything = mycursor.fetchall()
	mycursor.close()
	return everything

#GET ALL RENTED PROPERTYS FROM TENANT_PERMANENCY TABLE
def get_all_tenants_currenrly_not_renting():
		mycursor = mydb.cursor(dictionary=True)
		sql = '''SELECT * FROM tenant_permanency t INNER JOIN person p ON t.id_person = p.id_person
		WHERE t.id_person NOT IN (SELECT DISTINCT id_person FROM tenant_permanency WHERE exit_date = "-")'''
		mycursor.execute(sql)
		everyone = mycursor.fetchall()
		return everyone

def check_if_person_currenrly_renting(Id_person):
		Id_person = int(Id_person)
		mycursor = mydb.cursor(dictionary=True)
		sql = '''SELECT * FROM tenant_permanency WHERE exit_date = "-"'''
		mycursor.execute(sql)
		everyone = mycursor.fetchall()
		for person in everyone:
			if Id_person == person['id_person']:
				return True
		return False

#SELECT ONE FROM TENANT_PERMANENCY TABLE
def select_one(Id_property):
	mycursor = mydb.cursor()
	sql = "SELECT * FROM tenant_permanency WHERE id_property={}".format(Id_property)
	mycursor.execute(sql)
	ROW = mycursor.fetchone()
	return ROW

def check_if_rent_already_exist(Id_property,Id_person):
	mycursor = mydb.cursor()
	sql = "SELECT * FROM tenant_permanency WHERE id_property={} and id_person={} and exit_date='-'".format(Id_property,Id_person)
	mycursor.execute(sql)
	ROW = mycursor.fetchone()
	return ROW