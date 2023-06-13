import mysql.connector
import person
import services

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Fede1234",
  database="appproperty"
)
mycursor = mydb.cursor(dictionary=True)

#INSERTS A NEW SERVICE PROVIDER (PERSON + SERVICE) IN IS SERVICE PROVIDER TABLE
def insert_new_service_provider(Id_service,Id_person,Registration_number="-",Still_working=1):
	mycursor = mydb.cursor(dictionary=True)
	sql = '''INSERT INTO is_service_provider (id_service,id_person,registration_number,still_working)
	VALUES ({},{},'{}',{})'''.format(Id_service,Id_person,Registration_number,Still_working)
	mycursor.execute(sql)
	mydb.commit()
	success = mycursor.rowcount
	mycursor.close()
	return success

#SELECT ALL FROM IS_SERVICE_PROVIDER TABLE
def select_all():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM is_service_provider'''
	mycursor.execute(sql)
	everything = mycursor.fetchall()
	mycursor.close()
	if everything == []:
		everything = None
	return everything

def select_all_plus_info():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM is_service_provider i INNER JOIN person p ON i.id_person = p.id_person
	INNER JOIN service s ON i.id_service = s.id_service'''
	mycursor.execute(sql)
	everything = mycursor.fetchall()
	mycursor.close()
	return everything

def check_if_person_still_exist_in_service_provider(Id_person):
	Id_person = int(Id_person)
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM person p WHERE p.id_person IN (SELECT DISTINCT 
	id_person FROM is_service_provider WHERE still_working = 1)'''
	mycursor.execute(sql)
	everyone = mycursor.fetchall()
	for person in everyone:
		if Id_person == person['id_person']:
			return True
	return False

def select_any_not_working_in_service_provider():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM is_service_provider i WHERE still_working = 0'''
	mycursor.execute(sql)
	everyone = mycursor.fetchall()
	mycursor.close()
	return everyone

def check_if_record_already_exist(Id_person,Id_service):
	mycursor = mydb.cursor(dictionary=True)
	Id_person = int(Id_person)
	Id_service = int(Id_service)
	sql = '''SELECT * FROM is_service_provider'''
	mycursor.execute(sql)
	everything = mycursor.fetchall()
	checkIfExist = [data for data in everything if data['id_person'] == Id_person and data['id_service'] == Id_service]
	if checkIfExist == []:
		return False
	else:
		for data in checkIfExist:
			if data['still_working'] == 1:
				return "exist_still_working"
			else:
				return data['id_is_service_provider']

#DELETE O RECOVER A ROW, UPDATING ALREADY EXIST VALUE IN IS_SERVICE_PROVIDER TABLE
def delete_or_recover_is_service_provider_row_by_id(Still_working,id_is_service_provider):
	mycursor = mydb.cursor(dictionary=True)
	sql = '''UPDATE is_service_provider SET still_working={}
	WHERE id_is_service_provider={}'''.format(Still_working,id_is_service_provider)
	mycursor.execute(sql)
	mydb.commit()
	success = mycursor.rowcount
	mycursor.close()
	return success

#UPDATE REGISTRATION NUMBER VALUE IN IS_SERVICE_PROVIDER TABLE
def update_registation_number_by_id(Registration_number,id_is_service_provider):
	mycursor = mydb.cursor(dictionary=True)
	sql = '''UPDATE is_service_provider SET registration_number='{}'
	WHERE id_is_service_provider={}'''.format(Registration_number,id_is_service_provider)
	mycursor.execute(sql)
	mydb.commit()
	success = mycursor.rowcount
	mycursor.close()
	return success