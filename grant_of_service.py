import mysql.connector
import is_service_provider
import property
import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Fede1234",
  database="appproperty"
)
mycursor = mydb.cursor(dictionary=True)

#INSERTS A NEW PAYMENT TASK TO AN SERVICE PROVIDER (PERSON/SERVICE + PROPERTY) IN GRANT_OF_SERVICE TABLE
def insert_new_payment_task(Id_service,Id_property,Cbu="-",Payment_date="-",Amount=0,Detail="-"):
	mycursor = mydb.cursor(dictionary=True)
	sql = '''INSERT INTO grant_of_service (id_service,id_property,cbu,payment_date,amount,detail)
	VALUES ({},{},'{}','{}',{},'{}')'''.format(Id_service,Id_property,Cbu,Payment_date,Amount,Detail)
	mycursor.execute(sql)
	mydb.commit()
	success = mycursor.rowcount
	mycursor.close()
	return success

#UPDATE ID_PERSON_AND_SERVICE, ADDING IT WHICH MEANS THAT THE TASK HAS BEEN GIVEN TO A PERSON (THE USER CONTACTED THE PROFESIONAL)
def already_contacted_service_provider(id_grant_of_service_task,id_is_service_provider):
	mycursor = mydb.cursor(dictionary=True)
	if id_is_service_provider == "None":
		sql = '''UPDATE grant_of_service set id_is_service_provider = NULL WHERE id_grant_of_service={}'''.format(id_grant_of_service_task)
		mycursor.execute(sql)
		mydb.commit()
		success = mycursor.rowcount
		mycursor.close()
		return success
	else:
		sql = '''UPDATE grant_of_service SET id_is_service_provider={} WHERE id_grant_of_service={}'''.format(id_is_service_provider,id_grant_of_service_task)
		mycursor.execute(sql)
		mydb.commit()
		success = mycursor.rowcount
		mycursor.close()
		return success

#UPDATE AMOUNT AND/OR DETAIL IN TENANT_PAYMENT TABLE
def end_task_insert_amount_detail_cbu(payment_date,cbu,amount,detail,id_grant_of_service_task):
	mycursor = mydb.cursor(dictionary=True)
	sql = '''UPDATE grant_of_service SET cbu='{}', payment_date='{}', amount={}, detail='{}'
	WHERE id_grant_of_service={}'''.format(cbu,payment_date,amount,detail,id_grant_of_service_task)
	mycursor.execute(sql)
	mydb.commit()
	success = mycursor.rowcount
	mycursor.close()
	return success

#SELECT ALL FROM PAYMENT_TO_OWNER TABLE
def select_all():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM grant_of_service'''
	mycursor.execute(sql)
	everything = mycursor.fetchall()
	mycursor.close()
	if everything == []:
		everything = None
	return everything

def select_all_plus_info():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM grant_of_service g	LEFT JOIN is_service_provider i ON g.id_is_service_provider = i.id_is_service_provider
	LEFT JOIN person pe ON i.id_person = pe.id_person
	INNER JOIN service s ON g.id_service = s.id_service
	INNER JOIN property pr ON g.id_property = pr.id_property ORDER BY payment_date'''
	mycursor.execute(sql)
	everything = mycursor.fetchall()
	mycursor.close()
	return everything

def select_all_pending_payment_service_provider():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM grant_of_service WHERE payment_date = "-"'''
	mycursor.execute(sql)
	everything = mycursor.fetchall()
	mycursor.close()
	return everything

def check_if_has_service_provider(id_grant_of_service):
	mycursor = mydb.cursor(dictionary=True)
	id_grant_of_service = int(id_grant_of_service)
	sql = '''SELECT * FROM grant_of_service WHERE id_is_service_provider IS NULL'''
	mycursor.execute(sql)
	everything = mycursor.fetchall()
	mycursor.close()
	for data in everything:
		check = [data for data in everything if data['id_grant_of_service'] == id_grant_of_service]
		if check:
			return False
		else:
			return True