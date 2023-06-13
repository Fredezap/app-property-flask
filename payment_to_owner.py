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

#INSERTS A NEW PAYMENT TASK TO AN OWNER (PERSON + PROPERTY) IN PAYMENT_TO_OWNER TABLE
def insert_new_payment_task(Id_is_owner,Cbu="-",Payment_date="-",Amount=0,Detail="-"):
	mycursor = mydb.cursor(dictionary=True)
	sql = '''INSERT INTO payment_to_owner (id_is_owner,cbu,payment_date,amount,detail)
	VALUES ({},'{}','{}',{},'{}')'''.format(Id_is_owner,Cbu,Payment_date,Amount,Detail)
	mycursor.execute(sql)
	mydb.commit()
	success = mycursor.rowcount
	mycursor.close()
	return success

def select_all_pending_payment_owner():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM payment_to_owner WHERE payment_date = "-"'''
	mycursor.execute(sql)
	everything = mycursor.fetchall()
	mycursor.close()
	return everything

#SELECT ALL FROM PAYMENT_TO_OWNER TABLE
def select_all():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM payment_to_owner'''
	mycursor.execute(sql)
	everything = mycursor.fetchall()
	mycursor.close()
	return everything

def end_task_insert_amount_detail_cbu(payment_date,cbu,amount,detail,id_payment_to_owner_task):
	mycursor = mydb.cursor(dictionary=True)
	sql = '''UPDATE payment_to_owner SET cbu='{}', payment_date='{}', amount={}, detail='{}'
	WHERE id_payment_to_owner={}'''.format(cbu,payment_date,amount,detail,id_payment_to_owner_task)
	mycursor.execute(sql)
	mydb.commit()
	success = mycursor.rowcount
	mycursor.close()
	return success

def select_all_plus_info():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM payment_to_owner p INNER JOIN is_owner i ON p.id_is_owner = i.id_is_owner
	INNER JOIN person pe ON i.id_person = pe.id_person
	INNER JOIN property pr ON i.id_property = pr.id_property ORDER BY payment_date'''
	mycursor.execute(sql)
	everything = mycursor.fetchall()
	mycursor.close()
	return everything