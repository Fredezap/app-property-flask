import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Fede1234",
  database="appproperty"
)
mycursor = mydb.cursor(dictionary=True)

#INSERTS A NEW THING IN TENANT_THINGS_TO_PAY TABLE
def insert_thing(Name_of_thing,Description="-",Still_exist=1):
	mycursor = mydb.cursor(dictionary=True)
	sql = '''INSERT INTO tenant_thing_to_pay (name_of_thing,description,still_exist)
	VALUES ('{}','{}',{})'''.format(Name_of_thing,Description,Still_exist)
	mycursor.execute(sql)
	mydb.commit()
	success = mycursor.rowcount
	mycursor.close()
	return success

#SELECT ALL FROM PERSON TABLE
def select_all_existing_tenant_things_to_pay():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM tenant_thing_to_pay WHERE still_exist=1'''
	mycursor.execute(sql)
	everything = mycursor.fetchall()
	mycursor.close()
	return everything

#SELECT ALL FROM PERSON TABLE
def select_all_tenant_things_to_pay():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM tenant_thing_to_pay'''
	mycursor.execute(sql)
	everything = mycursor.fetchall()
	mycursor.close()
	return everything

#SELECT ONE FROM PERSON TABLE
def select_one(Thing_name):
	mycursor = mydb.cursor(dictionary=True)
	sql = "SELECT * FROM tenant_thing_to_pay WHERE name_of_thing='{}'".format(Thing_name)
	mycursor.execute(sql)
	service = mycursor.fetchone()
	return service

#CHECKING IF PERSON ALREADY EXIST IN DATABASE
def check_existing_thing_get_id(Thing_name):
	mycursor = mydb.cursor(dictionary=True)
	thing = select_one(Thing_name)
	if thing == None:
		return False
	if thing['still_exist'] == 1:
		return True
	if thing['still_exist'] == 0:
		return thing

#DELETE O RECOVER A TENANT THING TO PAY, UPDATING STILL EXIST VALUE IN TENANT_THING_TO_PAY TABLE
def delete_or_recover_thing_to_pay(id_tenant_thing_to_pay,still_exist):
	mycursor = mydb.cursor(dictionary=True)
	sql = '''UPDATE tenant_thing_to_pay SET still_exist={}
	WHERE id_tenant_thing_to_pay={}'''.format(still_exist,id_tenant_thing_to_pay)
	mycursor.execute(sql)
	mydb.commit()
	success = mycursor.rowcount
	mycursor.close()
	return success

def update_tenant_thing_to_pay(Id_tenant_thing_to_pay,Name_of_thing="-",Description="-"):
	mycursor = mydb.cursor(dictionary=True)
	sql = '''UPDATE tenant_thing_to_pay SET name_of_thing='{}', description='{}'
	WHERE id_tenant_thing_to_pay={}'''.format(Name_of_thing,Description,Id_tenant_thing_to_pay)
	mycursor.execute(sql)
	mydb.commit()
	success = mycursor.rowcount
	mycursor.close()
	return success