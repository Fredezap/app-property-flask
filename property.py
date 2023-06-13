import mysql.connector

mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "Fede1234",
	database = "appproperty"
)

mycursor = mydb.cursor(dictionary=True)

#SELECT ALL FROM PROPERTY TABLE
def select_all():
	mycursor = mydb.cursor(dictionary=True)
	sql = "SELECT * FROM property"
	mycursor.execute(sql)
	everything = mycursor.fetchall()
	mycursor.close()
	return everything

def select_all_existing_propertys():
	mycursor = mydb.cursor(dictionary=True)
	sql = "SELECT * FROM property WHERE already_exist = 1"
	mycursor.execute(sql)
	everything = mycursor.fetchall()
	mycursor.close()
	return everything

def select_all_existing_property_not_in_tenant_permanency_table():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM property p WHERE p.id_property NOT IN (SELECT id_property FROM
	tenant_permanency) AND already_exist = 1'''
	mycursor.execute(sql)
	everyone = mycursor.fetchall()
	mycursor.close()
	return everyone

def select_all_unrented_propertys():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM property WHERE id_property IN (SELECT DISTINCT
	id_property FROM tenant_permanency t WHERE t.exit_date <> "-"
	AND t.id_property NOT IN (SELECT id_property
	FROM tenant_permanency t WHERE t.exit_date = "-"))'''
	mycursor.execute(sql)
	everything = mycursor.fetchall()
	mycursor.close()
	return everything

#DELETE O RECOVER A PROPERTY, UPDATING ALREADY EXIST VALUE IN PROPERTY TABLE
def delete_or_recover_property_by_id(id_property,already_exist):
	mycursor = mydb.cursor(dictionary=True)
	sql = '''UPDATE property SET already_exist={}
	WHERE id_property="{}"'''.format(already_exist,id_property)
	mycursor.execute(sql)
	mydb.commit()
	success = mycursor.rowcount
	mycursor.close()
	return success

def delete_or_recover_property_by_nomenclatura(nomenclatura,already_exist):
	mycursor = mydb.cursor(dictionary=True)
	sql = '''UPDATE property SET already_exist={}
	WHERE nomenclatura="{}"'''.format(already_exist,nomenclatura)
	mycursor.execute(sql)
	mydb.commit()
	success = mycursor.rowcount
	mycursor.close()
	return success

#INSERT A PROPERTY IN PROPERTY TABLE
def insert_property(Nomenclatura,State,City,Street,Number,Neighborhood="-",Floor="-",Postal_code="-",Already_exist=1):
	mycursor = mydb.cursor(dictionary=True)
	sql = '''INSERT INTO property (nomenclatura,state,city,neighborhood,street,number,floor,postal_code,already_exist)
	VALUES ('{}','{}','{}','{}','{}','{}','{}','{}',{})'''.format(Nomenclatura,State,City,Neighborhood,Street,Number,Floor,Postal_code,Already_exist)
	mycursor.execute(sql)
	mydb.commit()
	success = mycursor.rowcount
	return success

#UPDATE A PROPERTY IN PROPERTY TABLE
def update_property_exist(Id_property,Nomenclatura,State,City,Street,Number,Neighborhood="-",Floor="-",Postal_code="-"):
	mycursor = mydb.cursor(dictionary=True)
	sql = '''UPDATE property SET nomenclatura='{}', state='{}', city='{}', neighborhood='{}', street='{}', number='{}', floor='{}', postal_code='{}'
	WHERE id_property={}'''.format(Nomenclatura,State,City,Neighborhood,Street,Number,Floor,Postal_code,Id_property)
	mycursor.execute(sql)
	mydb.commit()
	success = mycursor.rowcount
	mycursor.close()
	return success

#CHECKING IF PROPERTY ALREADY EXIST IN DATABASE
def check_existing_property(nomenclatura):
	mycursor = mydb.cursor(dictionary=True)
	property = select_one_by_nomenclatura(nomenclatura)
	if property == None:
		return False
	if property['already_exist'] == 1:
		return True
	if property['already_exist'] == 0:
		return "inactive"

def select_one_by_nomenclatura(nomenclatura):
	mycursor = mydb.cursor(dictionary=True)
	sql = "SELECT * FROM property WHERE nomenclatura={}".format(nomenclatura)
	mycursor.execute(sql)
	property = mycursor.fetchone()
	return property

def select_all_propertys_without_owner():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM property p WHERE p.already_exist = 1 AND p.id_property NOT IN (SELECT DISTINCT
	id_property FROM is_owner i WHERE i.already_exist_is_owner = 1)'''
	mycursor.execute(sql)
	everything = mycursor.fetchall()
	mycursor.close()
	return everything