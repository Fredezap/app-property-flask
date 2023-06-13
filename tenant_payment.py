import mysql.connector
import person
import tenant_things_to_pay
import property
import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Fede1234",
  database="appproperty"
)
mycursor = mydb.cursor(dictionary=True)

#INSERTS A NEW PAYMENT (PERSON + PROPERTY + DATE) IN TENANT_PAYMENT TABLE
def insert_new_payment_task(Id_tenant_thing_to_pay,Id_tenant_permanency,Cbu="-",Payment_date="-",Amount=0,Detail="-"):
		mycursor = mydb.cursor(dictionary=True)
		sql = '''INSERT INTO tenant_payment (id_tenant_thing_to_pay,id_tenant_permanency,cbu,payment_date,Amount,Detail)
		VALUES ({},{},'{}','{}',{},'{}')'''.format(Id_tenant_thing_to_pay,Id_tenant_permanency,Cbu,Payment_date,Amount,Detail)
		mycursor.execute(sql)
		mydb.commit()
		success = mycursor.rowcount
		mycursor.close()
		return success

#END TASK, UPDATE AMOUNT, DATE, CBU AND DETAIL IN TENANT_PAYMENT TABLE
def end_task_insert_amount_detail_cbu(payment_date,cbu,amount,detail,id_tenant_payment):
	mycursor = mydb.cursor(dictionary=True)
	sql = '''UPDATE tenant_payment SET cbu='{}', payment_date='{}', amount={}, detail='{}'
	WHERE id_tenant_payment={}'''.format(cbu,payment_date,amount,detail,id_tenant_payment)
	mycursor.execute(sql)
	mydb.commit()
	success = mycursor.rowcount
	mycursor.close()
	return success

#SELECT ALL FROM TENANT_PATMENT TABLE
def select_all():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM tenant_payment'''
	mycursor.execute(sql)
	everything = mycursor.fetchall()
	mycursor.close()
	if everything == []:
		everything = None
	return everything

def select_all_pending_payment_tenant():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM tenant_payment WHERE payment_date = "-"'''
	mycursor.execute(sql)
	everything = mycursor.fetchall()
	mycursor.close()
	return everything

def select_all_payments_already_done():
	everything = select_all()
	pending_payments = []
	if everything == None:
		return everything
	for data in everything:
		if data[5] != str(None):
			pending_payments.append(data)
	if pending_payments == []:
		pending_payments = None
	return pending_payments

#SELECT ALL FROM TENANT_PATMENT TABLE
def select_all_plus_info():
	mycursor = mydb.cursor(dictionary=True)
	sql = '''SELECT * FROM tenant_payment tpa INNER JOIN tenant_thing_to_pay tth
	ON tpa.id_tenant_thing_to_pay = tth.id_tenant_thing_to_pay
	INNER JOIN tenant_permanency tpe ON tpa.id_tenant_permanency = tpe.id_tenant_permanency
	INNER JOIN property pr ON tpe.id_property = pr.id_property
	INNER	JOIN person pe ON tpe.id_person = pe.id_person ORDER BY payment_date'''
	mycursor.execute(sql)
	everything = mycursor.fetchall()
	mycursor.close()
	return everything