import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Fede1234",
  database="appproperty"
)
mycursor = mydb.cursor(dictionary=True)

#INSERTS A NEW OWNER IN IS_OWNER TABLE
def insert_owner(id_person,id_property,already_exist_is_owner=1):
	mycursor = mydb.cursor(dictionary=True)
	sql = '''INSERT INTO is_owner (id_person,id_property,already_exist_is_owner)
	VALUES ({},{},{})'''.format(id_person,id_property,already_exist_is_owner)
	mycursor.execute(sql)
	mydb.commit()
	success = mycursor.rowcount
	mycursor.close()
	return success

#SELECT ALL FROM IS_OWNER TABLE
def select_all():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM is_owner'''
	mycursor.execute(sql)
	everything = mycursor.fetchall()
	mycursor.close()
	return everything

def select_all_plus_info():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM is_owner i INNER JOIN person pe ON i.id_person = pe.id_person
	INNER JOIN property pr ON i.id_property = pr.id_property'''
	mycursor.execute(sql)
	everything = mycursor.fetchall()
	mycursor.close()
	return everything

def select_all_existing_owners_plus_info():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM is_owner i INNER JOIN person pe ON i.id_person = pe.id_person
	INNER JOIN property pr ON i.id_property = pr.id_property WHERE already_exist_is_owner = 1'''
	mycursor.execute(sql)
	everything = mycursor.fetchall()
	mycursor.close()
	return everything

#SELECT ONE FROM IS_OWNER TABLE
def select_one(Id_person):
	mycursor = mydb.cursor(dictionary=True)
	sql = "SELECT * FROM is_owner WHERE Id_person={}".format(Id_person)
	mycursor.execute(sql)
	owner = mycursor.fetchone()
	return owner

def check_if_person_currenrly_owner_of_any_property(Id_person):
		Id_person = int(Id_person)
		mycursor = mydb.cursor(dictionary=True)
		sql = '''SELECT * FROM person p WHERE p.id_person IN (SELECT DISTINCT 
		id_person FROM is_owner WHERE already_exist = 1)'''
		mycursor.execute(sql)
		everyone = mycursor.fetchall()
		for person in everyone:
			if Id_person == person['id_person']:
				return True
		return False

#DELETE O RECOVER A ROW, UPDATING ALREADY EXIST VALUE IN IS_OWNER TABLE
def delete_or_recover_is_owner_row_by_id(already_exist_is_owner,id_is_owner):
	mycursor = mydb.cursor(dictionary=True)
	sql = '''UPDATE is_owner SET already_exist_is_owner={}
	WHERE id_is_owner={}'''.format(already_exist_is_owner,id_is_owner)
	mycursor.execute(sql)
	mydb.commit()
	success = mycursor.rowcount
	mycursor.close()
	return success

def check_if_record_already_exist(Id_person,Id_property):
		mycursor = mydb.cursor(dictionary=True)
		Id_person = int(Id_person)
		Id_property = int(Id_property)
		mycursor = mydb.cursor(dictionary=True)
		sql = '''SELECT * FROM is_owner'''
		mycursor.execute(sql)
		everything = mycursor.fetchall()
		checkIfExist = [data for data in everything if data['id_property'] == Id_property and data['already_exist_is_owner'] == 1]
		checkIfNotExistSameOwner = [data for data in everything if data['id_property'] == Id_property and data['already_exist_is_owner'] == 0 and data['id_person'] == Id_person]
		if checkIfNotExistSameOwner != [] and checkIfExist == []:
			for data in checkIfNotExistSameOwner:
				return data['id_is_owner']
		if checkIfExist != []:
			for data in checkIfExist:
				if data['id_person'] == Id_person:
						return "Already_exist_same_owner"
				else:
						return "Already_exist_diferent_owner"
		if checkIfExist == [] or checkIfNotExistSameOwner == []:
			return False