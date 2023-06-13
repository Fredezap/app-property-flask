import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Fede1234",
  database="appproperty"
)
mycursor = mydb.cursor(dictionary=True)

#INSERTS A NEW PERSON IN PERSON TABLE
def insert_person(Name,Surname,DNI,Cellphone="-",Mail="-",Address="-",Already_exist=1):
	mycursor = mydb.cursor(dictionary=True)
	Name = Name.capitalize()
	Surname = Surname.capitalize()
	sql = '''INSERT INTO person (name,surname,cellphone,mail,address,dni,already_exist)
	VALUES ('{}','{}','{}','{}','{}','{}',{})'''.format(Name,Surname,Cellphone,Mail,Address,DNI,Already_exist)
	mycursor.execute(sql)
	mydb.commit()
	success = mycursor.rowcount
	mycursor.close()
	return success

#DELETE O RECOVER A PERSON, UPDATING ALREADY EXIST VALUE IN PERSON TABLE
def delete_or_recover_person_by_dni(already_exist,dni):
	mycursor = mydb.cursor(dictionary=True)
	sql = '''UPDATE person SET already_exist={}
	WHERE dni="{}"'''.format(already_exist,dni)
	mycursor.execute(sql)
	mydb.commit()
	success = mycursor.rowcount
	mycursor.close()
	return success

def delete_or_recover_person_by_id(already_exist,id_person):
	mycursor = mydb.cursor(dictionary=True)
	sql = '''UPDATE person SET already_exist={}
	WHERE id_person={}'''.format(already_exist,id_person)
	mycursor.execute(sql)
	mydb.commit()
	success = mycursor.rowcount
	mycursor.close()
	return success

def update_person_exist_by_id(name,surname,dni,id_person,cellphone="-",mail="-",address="-"):
	mycursor = mydb.cursor(dictionary=True)
	name = name.capitalize()
	surname = surname.capitalize()
	sql = '''UPDATE person SET name='{}', surname='{}', cellphone='{}', mail='{}', address='{}', dni='{}'
	WHERE id_person={}'''.format(name,surname,cellphone,mail,address,dni,id_person)
	mycursor.execute(sql)
	mydb.commit()
	success = mycursor.rowcount
	mycursor.close()
	return success

#SELECT ALL FROM PERSON TABLE
def select_all():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM person'''
	mycursor.execute(sql)
	everyone = mycursor.fetchall()
	mycursor.close()
	return everyone

def select_all_existing_people():
	mycursor = mydb.cursor(dictionary=True)
	all = select_all()
	everyone = [data for data in all if data['already_exist'] == 1]
	return everyone

def select_all_existing_owners():
		mycursor = mydb.cursor(dictionary=True)
		sql = '''SELECT * FROM person p INNER JOIN is_owner i ON p.id_person = i.id_person WHERE already_exist = 1'''
		mycursor.execute(sql)
		everyone = mycursor.fetchall()
		mycursor.close()
		return everyone

def select_all_owners():
		mycursor = mydb.cursor(dictionary=True)
		sql = '''SELECT * FROM person p WHERE id_person IN (SELECT DISTINCT id_person FROM is_owner)'''
		mycursor.execute(sql)
		everyone = mycursor.fetchall()
		mycursor.close()
		return everyone

def select_all_existing_tenants():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM person p INNER JOIN tenant_permanency t ON p.id_person = t.id_person WHERE already_exist = 1'''
	mycursor.execute(sql)
	everyone = mycursor.fetchall()
	mycursor.close()
	return everyone

def select_all_tenants():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM person WHERE person.id_person IN (SELECT DISTINCT id_person FROM
	tenant_permanency)'''
	mycursor.execute(sql)
	everyone = mycursor.fetchall()
	mycursor.close()
	return everyone

def select_all_existing_service_providers():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM person p INNER JOIN is_service_provider i t ON p.id_person = i.id_person WHERE already_exist = 1'''
	mycursor.execute(sql)
	everyone = mycursor.fetchall()
	mycursor.close()
	return everyone

def select_all_service_providers():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM person WHERE person.id_person IN (SELECT DISTINCT id_person FROM
	is_service_provider)'''
	mycursor.execute(sql)
	everyone = mycursor.fetchall()
	mycursor.close()
	return everyone

def select_all_existing_people_not_in_other_table():
	mycursor = mydb.cursor(dictionary=True)
	sql =	'''SELECT * FROM person WHERE person.id_person NOT IN (SELECT DISTINCT id_person FROM
	is_owner UNION ALL SELECT DISTINCT id_person FROM tenant_permanency UNION ALL SELECT DISTINCT id_person
	FROM is_service_provider)'''
	mycursor.execute(sql)
	everyone = mycursor.fetchall()
	mycursor.close()
	return everyone

#SELECT ONE FROM PERSON TABLE BY ID
def select_one_by_id(ID):
	mycursor = mydb.cursor(dictionary=True)
	sql = "SELECT * FROM person WHERE ID={}".format(ID)
	mycursor.execute(sql)
	person = mycursor.fetchone()
	return person

#SELECT ONE FROM PERSON TABLE BY NAME AND SURNAME
def select_one_by_dni(dni):
	mycursor = mydb.cursor(dictionary=True)
	sql = "SELECT * FROM person WHERE dni='{}'".format(dni)
	mycursor.execute(sql)
	person = mycursor.fetchone()
	return person

#CHECKING IF PERSON EXIST IN DATABASE AND CHECK IF ALREADY_EXIST
def check_existing_person(dni):
	mycursor = mydb.cursor(dictionary=True)
	person = select_one_by_dni(dni)
	if person == None:
		return False
	if person['already_exist'] == 1:
		return True
	if person['already_exist'] == 0:
		return "inactive"
