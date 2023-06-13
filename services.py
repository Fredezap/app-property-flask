import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Fede1234",
  database="appproperty"
)
mycursor = mydb.cursor(dictionary=True)

#INSERTS A NEW SERVICE IN SERVICE TABLE
def insert_service(Service_name,Description="-",Still_exist=1):
		mycursor = mydb.cursor(dictionary=True)
		sql = '''INSERT INTO service (service_name,description,still_exist)
		VALUES ('{}','{}',{})'''.format(Service_name,Description,Still_exist)
		mycursor.execute(sql)
		mydb.commit()
		success = mycursor.rowcount
		mycursor.close()
		return success

#UPDATE A SERVICE IN SERVICE TABLE
def update_service(Service_name,Description,Id_service):
	mycursor = mydb.cursor(dictionary=True)
	sql = '''UPDATE service SET service_name='{}', description='{}' WHERE id_service={}'''.format(Service_name,Description,Id_service)
	mycursor.execute(sql)
	mydb.commit()
	success = mycursor.rowcount
	mycursor.close()
	return success

#SELECT ALL FROM SERVICE TABLE
def select_all():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM service'''
	mycursor.execute(sql)
	everything = mycursor.fetchall()
	mycursor.close()
	return everything

def select_all_existing_services():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM service WHERE still_exist = 1'''
	mycursor.execute(sql)
	everything = mycursor.fetchall()
	mycursor.close()
	return everything

#SELECT ONE FROM SERVICE TABLE
def select_one(Service_name):
	mycursor = mydb.cursor(dictionary=True)
	sql = "SELECT * FROM service WHERE service_name='{}'".format(Service_name)
	mycursor.execute(sql)
	service = mycursor.fetchone()
	return service

#CHECKING IF SERVICE ALREADY EXIST IN DATABASE
def check_existing_service_get_id(Service_name):
	mycursor = mydb.cursor(dictionary=True)
	service = select_one(Service_name)
	if service == None:
		return False
	if service['still_exist'] == 1:
		return True
	if service['still_exist'] == 0:
		return service

#DELETE O RECOVER A SERVICE, UPDATING STILL EXIST VALUE IN SERVICE TABLE
def delete_or_recover_service(id_service,still_exist):
	mycursor = mydb.cursor(dictionary=True)
	sql = '''UPDATE service SET still_exist={}
	WHERE id_service={}'''.format(still_exist,id_service)
	mycursor.execute(sql)
	mydb.commit()
	success = mycursor.rowcount
	mycursor.close()
	return success