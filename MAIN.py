from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session, logging
# from flask_wtf.csrf import CsrfProtect
from flask_login import LoginManager
from werkzeug.urls import url_parse
import forms
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import person, payment_to_owner, is_owner, services, is_service_provider, tenant_payment, tenant_things_to_pay, tenant_permanency, grant_of_service, property
import mysql.connector
import os
import datetime


app = Flask(__name__)
e = create_engine('mysql://root:Fede1234@localhost/appproperty')


ID = []
name_surname = []
logueado = False

app = Flask(__name__)
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Fede1234',
    database='appproperty'
)
cursor = mydb.cursor(dictionary=True)

@app.route('/Portada', methods=["GET","POST"])
def Portada():
    return render_template('Portada.html')

@app.route('/Home_page', methods=["GET","POST"])
def Index():
    cursor = mydb.cursor(dictionary=True)
    All_service_providers = is_service_provider.select_all_plus_info()
    All_services = services.select_all_existing_services()
    All_propertys = property.select_all_existing_propertys()
    All_owners = is_owner.select_all_existing_owners_plus_info()
    All_tenant_things_to_pay = tenant_things_to_pay.select_all_existing_tenant_things_to_pay()
    All_current_tenants = tenant_permanency.select_all_plus_info()
    All_tasks_service_providers = grant_of_service.select_all_plus_info()
    checkEmptyListServiceProviderTasks = [data for data in All_tasks_service_providers if data['payment_date'] == "-"]
    if checkEmptyListServiceProviderTasks == []:
        All_tasks_service_providers = []
    All_tasks_owners = payment_to_owner.select_all_plus_info()
    checkEmptyListOwnerTasks = [data for data in All_tasks_owners if data['payment_date'] == "-"]
    if checkEmptyListOwnerTasks == []:
        All_tasks_owners = []
    All_tenant_tasks = tenant_payment.select_all_plus_info()
    checkEmptyListTenantTasks = [data for data in All_tenant_tasks if data['payment_date'] == "-"]
    if checkEmptyListTenantTasks == []:
        All_tenant_tasks = []
    if request.method == 'POST':
        # FROM FORM ASSIGN SERVICE PROVIDER HTML (TO ASSING A SERVICE PROVIDER TO THE TASK)
        AssignServiceProvider = request.form.get("AssignServiceProvider")
        if AssignServiceProvider:
            ids = AssignServiceProvider.split(", ")
            id_grant_of_service_task = int(ids[0])
            id_is_service_provider = int(ids[1])
            result = grant_of_service.already_contacted_service_provider(id_grant_of_service_task,id_is_service_provider)
            if result == 1:
                result = "Has asignado a un proveedor de servicio a la tarea"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            All_tasks_service_providers = grant_of_service.select_all_plus_info()
            checkEmptyListServiceProviderTasks = [data for data in All_tasks_service_providers if data['payment_date'] == "-"]
            if checkEmptyListServiceProviderTasks == []:
                All_tasks_service_providers = []
            return render_template('Home_page.html',All_tasks_service_providers=All_tasks_service_providers,
                            All_service_providers=All_service_providers,result=result,All_tasks_owners=All_tasks_owners,
                            All_tenant_tasks=All_tenant_tasks,All_propertys=All_propertys,All_services=All_services,
                            All_owners=All_owners,All_tenant_things_to_pay=All_tenant_things_to_pay,
                            All_current_tenants=All_current_tenants)
        # FROM FORM END TASK SERVICE PROVIDER HTML (TO END TASK SERVICE PROVIDER)  
        id_grant_of_service_task = request.form.get("id_grant_of_service_task")
        if id_grant_of_service_task:
            id_grant_of_service_task = int(id_grant_of_service_task)
            cbu = request.form.get("cbu")
            if cbu == "":
                cbu = "-"
            amount = request.form.get("amount")
            if amount == "":
                amount = 0
            else:
                try:
                    amount = float(amount.replace(',',"."))
                except:
                    result = '''Ocurrio un error. Ingresa el numero sin puntos, solamente agregale una coma ','
                                si queres agregar decimales'''
                    return render_template('Home_page.html',All_tasks_service_providers=All_tasks_service_providers,
                            All_service_providers=All_service_providers,result=result,All_tasks_owners=All_tasks_owners,
                            All_tenant_tasks=All_tenant_tasks,All_propertys=All_propertys,All_services=All_services,
                            All_owners=All_owners,All_tenant_things_to_pay=All_tenant_things_to_pay,
                            All_current_tenants=All_current_tenants)
            detail = request.form.get("detail")
            if detail == "":
                detail = "-"
            payment_date = datetime.date.today()
            payment_date = str(payment_date)
            result = grant_of_service.end_task_insert_amount_detail_cbu(payment_date,cbu,amount,detail,id_grant_of_service_task)
            if result == 1:
                result = "Has realizado el pago exitosamente"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            All_tasks_service_providers = grant_of_service.select_all_plus_info()
            checkEmptyListServiceProviderTasks = [data for data in All_tasks_service_providers if data['payment_date'] == "-"]
            if checkEmptyListServiceProviderTasks == []:
                All_tasks_service_providers = []
            return render_template('Home_page.html',All_tasks_service_providers=All_tasks_service_providers,
                            All_service_providers=All_service_providers,result=result,All_tasks_owners=All_tasks_owners,
                            All_tenant_tasks=All_tenant_tasks,All_propertys=All_propertys,All_services=All_services,
                            All_owners=All_owners,All_tenant_things_to_pay=All_tenant_things_to_pay,
                            All_current_tenants=All_current_tenants)
        # FROM FORM MODAL INFO IN HOME PAGE HTML (TO CANCELL SERVICE PROVIDER)
        id_grant_of_service_task2 = request.form.get("id_grant_of_service_task2")
        id_is_service_provider2 = request.form.get("id_is_service_provider2")
        if id_grant_of_service_task2:
            result = grant_of_service.already_contacted_service_provider(id_grant_of_service_task2,id_is_service_provider2)
            if result == 1:
                result = "Has dejado de asignar al proveedor de servicio"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            All_tasks_service_providers = grant_of_service.select_all_plus_info()
            checkEmptyListServiceProviderTasks = [data for data in All_tasks_service_providers if data['payment_date'] == "-"]
            if checkEmptyListServiceProviderTasks == []:
                All_tasks_service_providers = []
            return render_template('Home_page.html',All_tasks_service_providers=All_tasks_service_providers,
                                    All_service_providers=All_service_providers,result=result,
                                    All_tenant_tasks=All_tenant_tasks,All_propertys=All_propertys,All_services=All_services,
                                    All_owners=All_owners,All_tenant_things_to_pay=All_tenant_things_to_pay,
                                    All_current_tenants=All_current_tenants)
        # FROM FORM END TASK OWNER HTML (TO END OWNER TASK)  
        id_payment_to_owner_task = request.form.get("id_payment_to_owner_task")
        if id_payment_to_owner_task:
            id_payment_to_owner_task = int(id_payment_to_owner_task)
            cbu = request.form.get("cbu")
            if cbu == "":
                cbu = "-"
            amount = request.form.get("amount")
            if amount == "":
                amount = 0
            else:
                try:
                    amount = float(amount.replace(',',"."))
                except:
                    result = '''Ocurrio un error. Ingresa el numero sin puntos, solamente agregale una coma ','
                                si queres agregar decimales'''
                    return render_template('Home_page.html',All_tasks_service_providers=All_tasks_service_providers,
                            All_service_providers=All_service_providers,result=result,All_tasks_owners=All_tasks_owners,
                            All_tenant_tasks=All_tenant_tasks,All_propertys=All_propertys,All_services=All_services,
                            All_owners=All_owners,All_tenant_things_to_pay=All_tenant_things_to_pay,
                            All_current_tenants=All_current_tenants)
            detail = request.form.get("detail")
            if detail == "":
                detail = "-"
            payment_date = datetime.date.today()
            payment_date = str(payment_date)
            success = payment_to_owner.end_task_insert_amount_detail_cbu(payment_date,cbu,amount,detail,id_payment_to_owner_task)
            if success == 1:
                result = "Has realizado un pago"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            All_tasks_owners = payment_to_owner.select_all_plus_info()
            checkEmptyListOwnerTasks = [data for data in All_tasks_owners if data['payment_date'] == "-"]
            if checkEmptyListOwnerTasks == []:
                All_tasks_owners = []
            return render_template('Home_page.html',All_tasks_service_providers=All_tasks_service_providers,
                            All_service_providers=All_service_providers,result=result,All_tasks_owners=All_tasks_owners,
                            All_tenant_tasks=All_tenant_tasks,All_propertys=All_propertys,All_services=All_services,
                            All_owners=All_owners,All_tenant_things_to_pay=All_tenant_things_to_pay,
                            All_current_tenants=All_current_tenants)
        # FROM FORM END TASK TENANT HTML (TO END TENANT TASK)    
        id_tenant_payment = request.form.get("id_tenant_payment")
        if id_tenant_payment:
            id_tenant_payment = int(id_tenant_payment)
            cbu = request.form.get("cbu")
            if cbu == "":
                cbu = "-"
            amount = request.form.get("amount")
            if amount == "":
                amount = 0
            else:
                try:
                    amount = float(amount.replace(',',"."))
                except:
                    result = '''Ocurrio un error. Ingresa el numero sin puntos, solamente agregale una coma ','
                                si queres agregar decimales'''
                    return render_template('Home_page.html',All_tasks_service_providers=All_tasks_service_providers,
                            All_service_providers=All_service_providers,result=result,All_tasks_owners=All_tasks_owners,
                            All_tenant_tasks=All_tenant_tasks,All_propertys=All_propertys,All_services=All_services,
                            All_owners=All_owners,All_tenant_things_to_pay=All_tenant_things_to_pay,
                            All_current_tenants=All_current_tenants)
            detail = request.form.get("detail")
            if detail == "":
                detail = "-"
            payment_date = datetime.date.today()
            payment_date = str(payment_date)
            result = tenant_payment.end_task_insert_amount_detail_cbu(payment_date,cbu,amount,detail,id_tenant_payment)
            if result == 1:
                result = "Has realizado el pago correctamente"
            else:
                result = "Ha ocurrido un error. Intenta nuevamente"
            All_tenant_tasks = tenant_payment.select_all_plus_info()
            checkEmptyListTenantTasks = [data for data in All_tenant_tasks if data['payment_date'] == "-"]
            if checkEmptyListTenantTasks == []:
                All_tenant_tasks = []
            return render_template('Home_page.html',All_tasks_service_providers=All_tasks_service_providers,
                            All_service_providers=All_service_providers,result=result,All_tasks_owners=All_tasks_owners,
                            All_tenant_tasks=All_tenant_tasks,All_propertys=All_propertys,All_services=All_services,
                            All_owners=All_owners,All_tenant_things_to_pay=All_tenant_things_to_pay,
                            All_current_tenants=All_current_tenants)
        id_service = request.form.get("AddTaskGetIdService")
        if id_service:
            id_property = request.form.get("AddTaskGetIdProperty")
            cbu = request.form.get("AddTaskServiceprovidercbu")
            amount = request.form.get("AddTaskServiceproviderAmount")
            detail = request.form.get("AddTaskServiceproviderDetail")
            if cbu == "":
                cbu = "-"
            if amount == "":
                amount = 0
            else:
                try:
                    amount = float(amount.replace(',',"."))
                except:
                    result = '''Ocurrio un error. Ingresa el numero sin puntos, solamente agregale una coma ','
                                si queres agregar decimales'''
                    return render_template('Home_page.html',All_tasks_service_providers=All_tasks_service_providers,
                            All_service_providers=All_service_providers,result=result,All_tasks_owners=All_tasks_owners,
                            All_tenant_tasks=All_tenant_tasks,All_propertys=All_propertys,All_services=All_services,
                            All_owners=All_owners,All_tenant_things_to_pay=All_tenant_things_to_pay,
                            All_current_tenants=All_current_tenants)
            if detail == "":
                detail = "-"
            payment_date = "-"   
            result = grant_of_service.insert_new_payment_task(id_service,id_property,cbu,payment_date,amount,detail)
            if result == 1:
                result = "Has agregado una tarea/pago"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            All_tasks_service_providers = grant_of_service.select_all_plus_info()
            checkEmptyListServiceProviderTasks = [data for data in All_tasks_service_providers if data['payment_date'] == "-"]
            if checkEmptyListServiceProviderTasks == []:
                All_tasks_service_providers = []
            return render_template('Home_page.html',All_tasks_service_providers=All_tasks_service_providers,
                            All_service_providers=All_service_providers,result=result,All_tasks_owners=All_tasks_owners,
                            All_tenant_tasks=All_tenant_tasks,All_propertys=All_propertys,All_services=All_services,
                            All_owners=All_owners,All_tenant_things_to_pay=All_tenant_things_to_pay,
                            All_current_tenants=All_current_tenants)
            return render_template('Home_page.html',All_tasks_service_providers=All_tasks_service_providers,
                            All_service_providers=All_service_providers,result=result,All_tasks_owners=All_tasks_owners,
                            All_tenant_tasks=All_tenant_tasks,All_propertys=All_propertys,All_services=All_services,
                            All_owners=All_owners,All_tenant_things_to_pay=All_tenant_things_to_pay,
                            All_current_tenants=All_current_tenants)
        # ADD NEW TASK OWNERS (FORM FROM HOME PAGE)
        id_is_owner = request.form.get("AddTaskOwner")
        if id_is_owner:
            cbu = request.form.get("AddTaskOwnercbu")
            amount = request.form.get("AddTaskOwnerAmount")
            detail = request.form.get("AddTaskOwnerDetail")
            if cbu == "":
                cbu = "-"
            if amount == "":
                amount = 0
            else:
                try:
                    amount = float(amount.replace(',',"."))
                except:
                    result = '''Ocurrio un error. Ingresa el numero sin puntos, solamente agregale una coma ','
                                si queres agregar decimales'''
                    return render_template('Home_page.html',All_tasks_service_providers=All_tasks_service_providers,
                            All_service_providers=All_service_providers,result=result,All_tasks_owners=All_tasks_owners,
                            All_tenant_tasks=All_tenant_tasks,All_propertys=All_propertys,All_services=All_services,
                            All_owners=All_owners,All_tenant_things_to_pay=All_tenant_things_to_pay,
                            All_current_tenants=All_current_tenants)
            if detail == "":
                detail = "-"
            payment_date = "-"   
            result = payment_to_owner.insert_new_payment_task(id_is_owner,cbu,payment_date,amount,detail)
            if result == 1:
                result = "Has agregado un pago para un propietario"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            All_tasks_owners = payment_to_owner.select_all_plus_info()
            checkEmptyListOwnerTasks = [data for data in All_tasks_owners if data['payment_date'] == "-"]
            if checkEmptyListOwnerTasks == []:
                All_tasks_owners = []
            return render_template('Home_page.html',All_tasks_service_providers=All_tasks_service_providers,
                            All_service_providers=All_service_providers,result=result,All_tasks_owners=All_tasks_owners,
                            All_tenant_tasks=All_tenant_tasks,All_propertys=All_propertys,All_services=All_services,
                            All_owners=All_owners,All_tenant_things_to_pay=All_tenant_things_to_pay,
                            All_current_tenants=All_current_tenants)
        # ADD NEW TASK TENANT (FORM FROM HOME PAGE)
        id_tenant_thing_to_pay = request.form.get("AddTaskTenantIdThingToPay")
        if id_tenant_thing_to_pay:
            id_tenant_permanency = request.form.get("AddTaskGetIdTenantPermanency")
            cbu = request.form.get("AddTaskTenantcbu")
            amount = request.form.get("AddTaskTenantAmount")
            detail = request.form.get("AddTaskTenantDetail")
            if cbu == "":
                cbu = "-"
            if amount == "":
                amount = 0
            else:
                try:
                    amount = float(amount.replace(',',"."))
                except:
                    result = '''Ocurrio un error. Ingresa el numero sin puntos, solamente agregale una coma ','
                                si queres agregar decimales'''
                    return render_template('Home_page.html',All_tasks_service_providers=All_tasks_service_providers,
                            All_service_providers=All_service_providers,result=result,All_tasks_owners=All_tasks_owners,
                            All_tenant_tasks=All_tenant_tasks,All_propertys=All_propertys,All_services=All_services,
                            All_owners=All_owners,All_tenant_things_to_pay=All_tenant_things_to_pay,
                            All_current_tenants=All_current_tenants) 
            if detail == "":
                detail = "-"
            payment_date = "-"
            result = tenant_payment.insert_new_payment_task(id_tenant_thing_to_pay,id_tenant_permanency,cbu,payment_date,amount,detail)
            if result == 1:
                result = "Has agregado un pago para un inquilino"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            All_tenant_tasks = tenant_payment.select_all_plus_info()
            checkEmptyListTenantTasks = [data for data in All_tenant_tasks if data['payment_date'] == "-"]
            if checkEmptyListTenantTasks == []:
                All_tenant_tasks = []
            return render_template('Home_page.html',All_tasks_service_providers=All_tasks_service_providers,
                            All_service_providers=All_service_providers,result=result,All_tasks_owners=All_tasks_owners,
                            All_tenant_tasks=All_tenant_tasks,All_propertys=All_propertys,All_services=All_services,
                            All_owners=All_owners,All_tenant_things_to_pay=All_tenant_things_to_pay,
                            All_current_tenants=All_current_tenants) 
    return render_template('Home_page.html',All_tasks_service_providers=All_tasks_service_providers,
                                    All_service_providers=All_service_providers,All_tasks_owners=All_tasks_owners,
                                    All_tenant_tasks=All_tenant_tasks,All_propertys=All_propertys,All_services=All_services,
                                    All_owners=All_owners,All_tenant_things_to_pay=All_tenant_things_to_pay,
                                    All_current_tenants=All_current_tenants)
    
@app.route('/asignar_proveedor_servicio', methods=["GET","POST"])
def Assign_service_provider():
    # FROM FORM TABLE IN HOME PAGE HTML
    All_service_providers = is_service_provider.select_all_plus_info()
    if request.method == 'POST':
        id_grant_of_service_task = request.form.get("id_grant_of_service_task")
        id_service_task = request.form.get("id_service_task")
        if id_service_task:
            id_service_task = int(id_service_task)
            id_grant_of_service_task = int(id_grant_of_service_task)
            All_service_providers_matching_id = [data for data in All_service_providers if data['id_service'] == id_service_task and data['still_working'] == 1]
            return render_template('Assign_service_provider.html',id_grant_of_service_task=id_grant_of_service_task,
                    All_service_providers_matching_id=All_service_providers_matching_id)
        id_grant_of_service_task2 = request.form.get("id_grant_of_service_task2")
        id_service_task2 = request.form.get("id_service_task2")
        if id_service_task2:
            id_service_task2 = int(id_service_task2)
            id_grant_of_service_task2 = int(id_grant_of_service_task2)
            All_service_providers_matching_id = [data for data in All_service_providers if data['id_service'] == id_service_task2 and data['still_working'] == 1]
            return render_template('Assign_service_provider.html',id_grant_of_service_task=id_grant_of_service_task,
                    All_service_providers_matching_id=All_service_providers_matching_id,
                    id_grant_of_service_task2=id_grant_of_service_task2)
           

@app.route('/End_task', methods=["GET","POST"])
def End_task():
    print("ACA")
    # FROM DIFERENT FORMS IN DIFERENT TABLES IN HOME PAGE HTML
    if request.method == 'POST':
        id_grant_of_service_task3 = request.form.get("id_grant_of_service_task3")
        id_grant_of_service_task4 = request.form.get("id_grant_of_service_task4")
        if id_grant_of_service_task3 or id_grant_of_service_task4:
            if id_grant_of_service_task3:
                id_grant_of_service_task3 = int(id_grant_of_service_task3)
                check_if_has_service_provider = grant_of_service.check_if_has_service_provider(id_grant_of_service_task3)
            if id_grant_of_service_task4:
                id_grant_of_service_task4 = int(id_grant_of_service_task4)
                check_if_has_service_provider = grant_of_service.check_if_has_service_provider(id_grant_of_service_task4)
            if check_if_has_service_provider == False:
                result3 = "No podes realizar el pago de esta tarea porque aun no esta asignada a ningun proveedor de servicio"
                return render_template('End_task_service_provider.html',result3=result3)
            else:
                getMoreDataServiceProviderPayment = grant_of_service.select_all_pending_payment_service_provider()
                for payment in getMoreDataServiceProviderPayment:
                    if payment['id_grant_of_service'] == id_grant_of_service_task3 or payment['id_grant_of_service'] == id_grant_of_service_task4:
                        cbu = payment['cbu']
                        amount = payment['amount']
                        detail = payment['detail']
                return render_template('End_task_service_provider.html',id_grant_of_service_task3=id_grant_of_service_task3,
                    cbu=cbu,amount=amount,detail=detail,id_grant_of_service_task4=id_grant_of_service_task4)
        id_payment_to_owner_task = request.form.get("id_payment_to_owner_task")
        id_payment_to_owner_task2 = request.form.get("id_payment_to_owner_task2")
        if id_payment_to_owner_task or id_payment_to_owner_task2:
            if id_payment_to_owner_task:
                id_payment_to_owner_task = int(id_payment_to_owner_task)
            if id_payment_to_owner_task2:
                id_payment_to_owner_task2 = int(id_payment_to_owner_task2)
            getMoreDataOwnerPayment = payment_to_owner.select_all_pending_payment_owner()
            for payment in getMoreDataOwnerPayment:
                print(type(id_payment_to_owner_task2))
                print(id_payment_to_owner_task2)
                print(type(id_payment_to_owner_task))
                print(type(payment['id_payment_to_owner']))
                print(payment['id_payment_to_owner'])
                
                if payment['id_payment_to_owner'] == id_payment_to_owner_task or payment['id_payment_to_owner'] == id_payment_to_owner_task2:
                    cbu = payment['cbu']
                    amount = payment['amount']
                    detail = payment['detail']
            return render_template('End_task_owner.html',id_payment_to_owner_task=id_payment_to_owner_task,cbu=cbu,
                        amount=amount,detail=detail,id_payment_to_owner_task2=id_payment_to_owner_task2)
        id_tenant_payment = request.form.get("id_tenant_payment")
        id_tenant_payment2 = request.form.get("id_tenant_payment2")
        if id_tenant_payment or id_tenant_payment2:
            if id_tenant_payment:
                id_tenant_payment = int(id_tenant_payment)
            if id_tenant_payment2:
                id_tenant_payment2 = int(id_tenant_payment2)
            print(id_tenant_payment)
            print(id_tenant_payment2)
            getMoreDataTenantPayment = tenant_payment.select_all_pending_payment_tenant()
            for payment in getMoreDataTenantPayment:
                if payment['id_tenant_payment'] == id_tenant_payment2 or payment['id_tenant_payment'] == id_tenant_payment:
                    cbu = payment['cbu']
                    amount = payment['amount']
                    detail = payment['detail']
            return render_template('End_task_tenant.html',id_tenant_payment=id_tenant_payment,
                    cbu=cbu,amount=amount,detail=detail,id_tenant_payment2=id_tenant_payment2)

@app.route("/Get_all_tenants", methods=["GET","POST"])
def Get_all_tenants():
    current_tenants = tenant_permanency.select_all_plus_info()
    if request.method == 'POST':
        #END OR RESTART A TENANT PERMANENCY RENT
        id_tenant_permanency_end = request.form.get("id_tenant_permanency_end")
        if id_tenant_permanency_end:
            result = tenant_permanency.stop_renting(id_tenant_permanency_end)
            if result == 1:
                resultado = "Has finalizado el contrato de alquiler correctamente"
            else:
                resultado = "Ha ocurrido un error, intenta nuevamente"
            current_tenants = tenant_permanency.select_all_plus_info()
            return render_template("Get_all_tenants.html",current_tenants=current_tenants,resultado=resultado)
        id_tenant_permanency_restart = request.form.get("id_tenant_permanency_restart")
        if id_tenant_permanency_restart:
            result = tenant_permanency.start_renting_again(id_tenant_permanency_restart)
            if result == 1:
                resultado = "Has reactivado el contrato de alquiler correctamente"
            else:
                resultado = "Ha ocurrido un error, intenta nuevamente"
            current_tenants = tenant_permanency.select_all_plus_info()
            return render_template("Get_all_tenants.html",current_tenants=current_tenants,resultado=resultado)
    return render_template("Get_all_tenants.html",current_tenants=current_tenants)

@app.route('/Add_or_delete_person', methods=["GET","POST"])
def AddOrDeletePerson():
    all_people = person.select_all_existing_people()
    # FROM FORM TABLE IN GET ALL TENANTS PAGE
    all_people_owners = person.select_all_existing_people()
    all_people_service_providers = person.select_all_existing_people()
    all_services = services.select_all_existing_services()
    all_propertys = property.select_all_propertys_without_owner()
    all_propertys_tenant = property
    all_people_tenants = person.select_all_existing_people()
    available_propertys_tenants = []
    unrented_propertys = property.select_all_unrented_propertys()
    property_not_in_other_table = property.select_all_existing_property_not_in_tenant_permanency_table()
    for property1 in property_not_in_other_table:
        available_propertys_tenants.append(property1)
    for property2 in unrented_propertys:
        available_propertys_tenants.append(property2)
    if request.method == 'POST':
        addTenant = request.form.get("addTenant")
        addOwner = request.form.get("AddOwner")
        addServiceProvider = request.form.get("addServiceProvider")
        if addTenant:
            return render_template('Add_or_delete_person.html',all_people_tenants=all_people_tenants,
                available_propertys_tenants=available_propertys_tenants)
        if addOwner:
            return render_template('Add_or_delete_person.html',all_people_owners=all_people_owners,
                all_propertys=all_propertys)
        if addServiceProvider:
            all_people_service_providers = person.select_all_existing_people()
            return render_template('Add_or_delete_person.html',all_people_service_providers=all_people_service_providers,
                all_services=all_services)
        # ADD A NEW PERSON
        dni = request.form.get("dni")              
        if dni:
            name = request.form.get("name")
            surname = request.form.get("surname")
            cellphone = request.form.get("cellphone")
            mail = request.form.get("mail")
            address = request.form.get("address")
            if name == "":
                name = "-"
            if surname == "":
                surname = "-"
            if dni == "":
                dni = "-"
            if cellphone == "":
                cellphone = "-"
            if mail == "":
                mail = "-"
            if address == "":
                address = "-"

            # ADD NEW PERSON FOR OWNER
            AddPersonOwner = request.form.get("AddPersonOwner")
            if AddPersonOwner:
                result = person.check_existing_person(dni)
                if result == False:
                    addPerson = person.insert_person(name,surname,dni,cellphone,mail,address)
                    if addPerson == 1:
                        result = "Se ha agregado una persona exitosamente"
                    else:
                        result = "Ha ocurrido un error, intenta nuevamente"
                    all_people_owners = person.select_all_existing_people()
                    return render_template("Add_or_delete_person.html",result=result,
                        all_people_owners=all_people_owners,all_propertys=all_propertys) 
                if result == True:
                    result = "La persona que estas agregando ya existe"
                    return render_template("Add_or_delete_person.html",result=result,
                        all_people_owners=all_people_owners,all_propertys=all_propertys)          
                else:
                    resultAddOwner = "La persona que estas agregando ya existia, pero fue eliminada, queres recuperarla?"
                    return render_template("Add_or_delete_person.html",resultAddOwner=resultAddOwner,dni=dni,
                        all_people_owners=all_people_owners,all_propertys=all_propertys)

            # ADD NEW PERSON FOR SERVICE PROVIDER
            AddPersonServiceProvider = request.form.get("AddPersonServiceProvider")
            if AddPersonServiceProvider:
                result = person.check_existing_person(dni)
                if result == False:
                    addPerson = person.insert_person(name,surname,dni,cellphone,mail,address)
                    if addPerson == 1:
                        result = "Se ha agregado una persona exitosamente"
                    else:
                        result = "Ha ocurrido un error, intenta nuevamente"
                    all_people_service_providers = person.select_all_existing_people()
                    return render_template("Add_or_delete_person.html",result=result,all_services=all_services,
                    all_people_service_providers=all_people_service_providers)
                if result == True:
                    result = "La persona que estas agregando ya existe"
                    return render_template("Add_or_delete_person.html",result=result,all_services=all_services,
                    all_people_service_providers=all_people_service_providers)
                else:
                    resultAddServiceProvicer = "La persona que estas agregando ya existia, pero fue eliminada, queres recuperarla?"
                    return render_template("Add_or_delete_person.html",all_services=all_services,dni=dni,
                    all_people_service_providers=all_people_service_providers,resultAddServiceProvicer=resultAddServiceProvicer)

            # ADD NEW PERSON FOR TENANT
            AddPersonTenant = request.form.get("AddPersonTenant")
            if AddPersonTenant:
                result = person.check_existing_person(dni)
                if result == False:
                    addPerson = person.insert_person(name,surname,dni,cellphone,mail,address)
                    if addPerson == 1:
                        result = "Se ha agregado una persona exitosamente"
                    else:
                        result = "Ha ocurrido un error, intenta nuevamente"
                    all_people_tenants = person.select_all_existing_people()
                    return render_template('Add_or_delete_person.html',all_people_tenants=all_people_tenants,
                    available_propertys_tenants=available_propertys_tenants,result=result)
                if result == True:
                    result = "La persona que estas agregando ya existe"
                    return render_template('Add_or_delete_person.html',all_people_tenants=all_people_tenants,
                    available_propertys_tenants=available_propertys_tenants,result=result)    
                else:
                    resultAddTenant = "La persona que estas agregando ya existia, pero fue eliminada, queres recuperarla?"
                    return render_template('Add_or_delete_person.html',all_people_tenants=all_people_tenants,
                    available_propertys_tenants=available_propertys_tenants,resultAddTenant=resultAddTenant,dni=dni)

        # UPDATE AN EXISTING PERSON BY DNI TENANT (RECOVER)      
        updatePersonRecoverByDniTenant = request.form.get("updatePersonRecoverByDniTenant")
        if updatePersonRecoverByDniTenant:
            already_exist = 1
            result = person.delete_or_recover_person_by_dni(already_exist,updatePersonRecoverByDniTenant)
            if result == 1:
                result = "Has recuperado a la persona"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            all_people_tenants = person.select_all_existing_people()
            return render_template('Add_or_delete_person.html',all_people_tenants=all_people_tenants,
                    available_propertys_tenants=available_propertys_tenants,result=result)


        # UPDATE AN EXISTING PERSON BY DNI OWNER (RECOVER)      
        updatePersonRecoverByDniOwner = request.form.get("updatePersonRecoverByDniOwner")
        if updatePersonRecoverByDniOwner:
            already_exist = 1
            result = person.delete_or_recover_person_by_dni(already_exist,updatePersonRecoverByDniOwner)
            if result == 1:
                result = "Has recuperado a la persona"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            all_people_owners = person.select_all_existing_people()
            return render_template("Add_or_delete_person.html",result=result,
                all_people_owners=all_people_owners,all_propertys=all_propertys)

        # UPDATE AN EXISTING PERSON BY DNI SERVICE PROVIDER (RECOVER)      
        updatePersonRecoverByDniServiceProvider = request.form.get("updatePersonRecoverByDniServiceProvider")
        if updatePersonRecoverByDniServiceProvider:
            already_exist = 1
            result = person.delete_or_recover_person_by_dni(already_exist,updatePersonRecoverByDniServiceProvider)
            if result == 1:
                result = "Has recuperado a la persona"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            all_people_service_providers = person.select_all_existing_people()
            return render_template("Add_or_delete_person.html",result=result,all_services=all_services,
                    all_people_service_providers=all_people_service_providers)

        # INSERT A NEW OWNER BY ID PERSON AND ID PROPERTY
        IdPersonOwner = request.form.get("IdPersonOwner")
        IdPropertyOwner = request.form.get("IdPropertyOwner")
        if IdPersonOwner and IdPropertyOwner:
            check_already_exist = is_owner.check_if_record_already_exist(IdPersonOwner,IdPropertyOwner)
            if check_already_exist == False:
                result = is_owner.insert_owner(IdPersonOwner,IdPropertyOwner)
                if result == 1:
                    result = "Has agregado un nuevo propietario"
                else:
                    result = "Ha ocurrido un error, intenta nuevamente"
                all_propertys = property.select_all_propertys_without_owner()
                return render_template("Add_or_delete_person.html",result=result,
                    all_propertys=all_propertys,all_people_owners=all_people_owners)
            elif check_already_exist == "Already_exist_same_owner":
                result = "El propietario que estas queriendo agregar ya esta registrado como dueño de esa propiedad"
                return render_template("Add_or_delete_person.html",result=result,
                    all_propertys=all_propertys,all_people_owners=all_people_owners)
            elif check_already_exist == "Already_exist_diferent_owner":
                result = "La propiedad a la que estas intentando agregar un propietario ya existe y pertenece a otro dueño"
                return render_template("Add_or_delete_person.html",result=result,
                    all_propertys=all_propertys,all_people_owners=all_people_owners)
            else:
                resultOwner = "Este propietario ya existia anteriormente, queres recuperarlo?"
                return render_template("Add_or_delete_person.html",resultOwner=resultOwner,
                    all_people_owners=all_people_owners,check_already_exist=check_already_exist,all_propertys=all_propertys)

        # RECOVER OWNER BY ID
        RecoverOwnerId = request.form.get("RecoverOwnerId")
        if RecoverOwnerId:
            already_exist_is_owner = 1
            result = is_owner.delete_or_recover_is_owner_row_by_id(already_exist_is_owner,RecoverOwnerId)
            if result == 1:
                result = "Has recuperado el registro correctamente"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            all_propertys = property.select_all_propertys_without_owner()
            return render_template("Add_or_delete_person.html",result=result,all_people_owners=all_people_owners,
                all_propertys=all_propertys)
        
        # INSERT A NEW SERVICE PROVIDER BY ID PERSON AND SERVICE
        IdPersonIsServiceProvider = request.form.get("IdPersonIsServiceProvider")
        IdServiceIsServiceProvider = request.form.get("IdServiceIsServiceProvider")
        if IdPersonIsServiceProvider and IdServiceIsServiceProvider:
            check_already_exist = is_service_provider.check_if_record_already_exist(IdPersonIsServiceProvider,IdServiceIsServiceProvider)
            if check_already_exist == False:
                Registration_number = request.form.get("registration_number")
                if Registration_number == "":
                    Registration_number = "-"
                result = is_service_provider.insert_new_service_provider(IdServiceIsServiceProvider,IdPersonIsServiceProvider,Registration_number)
                if result == 1:
                    result = "Has agregado un nuevo proveedor de servicio"
                else:
                    result = "Ha ocurrido un error, intenta nuevamente"
                return render_template("Add_or_delete_person.html",result=result,all_services=all_services,
                    all_people_service_providers=all_people_service_providers)
            elif check_already_exist == "exist_still_working":
                result = "El proveedor de servicio que estas agregando ya existe"
                return render_template("Add_or_delete_person.html",result=result,all_services=all_services,
                    all_people_service_providers=all_people_service_providers)
            else:
                resultServiceProvider = "El proveedor de servicio que estas agregando ya existe, pero esta inactivo, queres reactivarlo?"
                return render_template("Add_or_delete_person.html",resultServiceProvider=resultServiceProvider,check_already_exist=check_already_exist,
                    all_services=all_services,all_people_service_providers=all_people_service_providers)

        # RECOVER SERVICE PROVIER BY ID
        RecoverServiceProviderId = request.form.get("RecoverServiceProviderId")
        if RecoverServiceProviderId:
            still_working = 1
            RecoverServiceProviderId = int(RecoverServiceProviderId)
            result = is_service_provider.delete_or_recover_is_service_provider_row_by_id(still_working,RecoverServiceProviderId)
            if result == 1:
                result = "Has recuperado el registro correctamente"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            return render_template("Add_or_delete_person.html",result=result,all_services=all_services,
                    all_people_service_providers=all_people_service_providers)

        # INSERT A NEW TENANT PERMANENCY BY ID PERSON AND PROPERTY TENANT
        IdPropertyTenant = request.form.get("IdPropertyTenant")
        IdPersonTenant = request.form.get("IdPersonTenant")
        if IdPropertyTenant and IdPersonTenant:
            check_if_already_renting = tenant_permanency.check_if_person_currenrly_renting(IdPersonTenant)
            if check_if_already_renting == False:
                result = tenant_permanency.insert_rent(IdPersonTenant,IdPropertyTenant)
                if result == 1:
                    result = "Has agregado un nuevo alquiler/inquilino"
                else:
                    result = "Ha ocurrido un error, intenta nuevamente"
                all_people_tenants = person.select_all_existing_people()
                available_propertys_tenants = []
                unrented_propertys = property.select_all_unrented_propertys()
                property_not_in_other_table = property.select_all_existing_property_not_in_tenant_permanency_table()
                for property1 in property_not_in_other_table:
                    available_propertys_tenants.append(property1)
                for property2 in unrented_propertys:
                    available_propertys_tenants.append(property2)
                return render_template('Add_or_delete_person.html',all_people_tenants=all_people_tenants,
                    available_propertys_tenants=available_propertys_tenants,result=result)
            else:
                available_propertys_tenants = []
                unrented_propertys = property.select_all_unrented_propertys()
                property_not_in_other_table = property.select_all_existing_property_not_in_tenant_permanency_table()
                for property1 in property_not_in_other_table:
                    available_propertys_tenants.append(property1)
                for property2 in unrented_propertys:
                    available_propertys_tenants.append(property2)
                result = "El inquilino que estas eligiendo esta actualmente alquilando"
                return render_template('Add_or_delete_person.html',all_people_tenants=all_people_tenants,result=result,
                    available_propertys_tenants=available_propertys_tenants)
    return render_template("Add_or_delete_person.html",all_people=all_people)          

@app.route('/Get_all_propertys', methods=["GET","POST"])
def AddOrDeleteProperty():
    all_propertys = property.select_all()
    if request.method == 'POST':
        # ADD A NEW PROPERTY
        nomenclatura = request.form.get("nomenclatura")
        if nomenclatura:
            state = request.form.get("state")
            city = request.form.get("city")
            neighborhood = request.form.get("neighborhood")
            street = request.form.get("street")
            number = request.form.get("number")
            floor = request.form.get("floor")
            postal_code = request.form.get("postal_code")
            if nomenclatura == "":
                nomenclatura = "-"
            if state == "":
                state = "-"
            if city == "":
                city = "-"
            if neighborhood == "":
                neighborhood = "-"
            if street == "":
                street = "-"
            if number == "":
                number = "-"
            if floor == "":
                floor = "-"
            if postal_code == "":
                postal_code = "-"
            try:
                result = property.check_existing_property(nomenclatura)
            except:
                result = "Ha ocurrido un error, intenta nuevamente"
                return render_template('Get_all_propertys.html',result=result,all_propertys=all_propertys)
            if result == False:
                addPropeorty = property.insert_property(nomenclatura,state,city,street,number,neighborhood,floor,postal_code)
                if addPropeorty == 1:
                    result = "Se ha agregado una propiedad exitosamente"
                else:
                    result = "Ha ocurrido un error, intenta nuevamente"
                all_propertys = property.select_all()
                return render_template('Get_all_propertys.html',result=result,all_propertys=all_propertys)
            if result == True:
                result = "La propiedad que estas agregando ya existe"
                return render_template('Get_all_propertys.html',result=result,all_propertys=all_propertys)          
            else:
                result2 = "La propiedad que estas agregando ya existe, pero esta inactiva, queres reactivarla?"
                return render_template('Get_all_propertys.html',nomenclatura=nomenclatura,result2=result2,
                    all_propertys=all_propertys)
        updatePropertyRecoverByNomenclatura = request.form.get("nomenclatura_property_recover")
        if updatePropertyRecoverByNomenclatura:
            already_exist = 1
            result = property.delete_or_recover_property_by_nomenclatura(updatePropertyRecoverByNomenclatura,already_exist)
            if result == 1:
                result = "La propiedad ha sido recuperada"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            all_propertys = property.select_all()
            return render_template('Get_all_propertys.html',result=result,
                all_propertys=all_propertys)
        updatePropertyDeleteById = request.form.get("id_property_delete")
        if updatePropertyDeleteById:
            already_exist = 0
            result = property.delete_or_recover_property_by_id(updatePropertyDeleteById,already_exist)
            if result == 1:
                result = "La propiedad ha sido eliminada"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            all_propertys = property.select_all()
            return render_template('Get_all_propertys.html',result=result,
                all_propertys=all_propertys)
        updatePropertyRecoverById = request.form.get("id_property_recover")
        if updatePropertyRecoverById:
            already_exist = 1
            result = property.delete_or_recover_property_by_id(updatePropertyRecoverById,already_exist)
            if result == 1:
                result = "La propiedad ha sido recuperada"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            all_propertys = property.select_all()
            return render_template('Get_all_propertys.html',result=result,
                all_propertys=all_propertys)
        id_property_edit = request.form.get("id_property_edit")                  
        if id_property_edit:
            id_property_edit = int(id_property_edit)
            nomenclatura = request.form.get("nomenclatura2")
            state = request.form.get("state2")
            city = request.form.get("city2")
            neighborhood = request.form.get("neighborhood2")
            street = request.form.get("street2")
            number = request.form.get("number2")
            floor = request.form.get("floor2")
            postal_code = request.form.get("postal_code2")
            if neighborhood == "":
                neighborhood = "-"
            if floor == "":
                floor = "-"
            if postal_code == "":
                postal_code = "-"
            result = property.update_property_exist(id_property_edit,nomenclatura,state,city,street,number,neighborhood,floor,postal_code)
            if result == 1:
                result = "Has modificado la propiedad correctamente"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            all_propertys = property.select_all()
            return render_template("Get_all_propertys.html",result=result,all_propertys=all_propertys)
    return render_template('Get_all_propertys.html',all_propertys=all_propertys)

@app.route('/Get_all_tenant_things_to_pay', methods=["GET","POST"])
def AddOrDeleteTenantThingToPay():
    things_to_pay = tenant_things_to_pay.select_all_tenant_things_to_pay()
    if request.method == 'POST':
        id_tenant_thing_to_pay_delete = request.form.get("id_tenant_thing_to_pay_delete")
        id_tenant_thing_to_pay_recover = request.form.get("id_tenant_thing_to_pay_recover")
        editServiceTenantId = request.form.get("editServiceTenantId")
        if editServiceTenantId:
            editServiceTenantId = int(editServiceTenantId)
            serviceNameTenant = request.form.get("serviceNameTenant")
            serviceDescriptionTenant = request.form.get("serviceDescriptionTenant")
            if serviceNameTenant == "":
                serviceNameTenant = "-"
            if serviceDescriptionTenant == "":
                serviceDescriptionTenant = ""
            result = tenant_things_to_pay.update_tenant_thing_to_pay(editServiceTenantId,serviceNameTenant,serviceDescriptionTenant)
            if result == 1:
                result = "Has editado correctamente el servicio"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            things_to_pay = tenant_things_to_pay.select_all_tenant_things_to_pay()
            return render_template('Get_all_tenant_things_to_pay.html',result=result,things_to_pay=things_to_pay)  
        new_thing_to_pay_name = request.form.get("name_of_thing")
        if id_tenant_thing_to_pay_delete:
            still_exist = 0
            result = tenant_things_to_pay.delete_or_recover_thing_to_pay(id_tenant_thing_to_pay_delete,still_exist)
            if result == 1:
                result = "Has eliminado el servicio"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            things_to_pay = tenant_things_to_pay.select_all_tenant_things_to_pay()
            return render_template('Get_all_tenant_things_to_pay.html',result=result,things_to_pay=things_to_pay)
        if id_tenant_thing_to_pay_recover:
            still_exist = 1
            result = tenant_things_to_pay.delete_or_recover_thing_to_pay(id_tenant_thing_to_pay_recover,still_exist)
            if result == 1:
                result = "Has recuperado el servicio"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            things_to_pay = tenant_things_to_pay.select_all_tenant_things_to_pay()
            return render_template('Get_all_tenant_things_to_pay.html',result=result,things_to_pay=things_to_pay)
        if new_thing_to_pay_name:
            check = tenant_things_to_pay.check_existing_thing_get_id(new_thing_to_pay_name)
            if check == False:
                description = request.form.get("description")
                if description == "":
                    description = "-"
                result = tenant_things_to_pay.insert_thing(new_thing_to_pay_name,description)
                if result == 1:
                    result = "Has agregado un nuevo servicio"
                elif resultado == 0:
                    result = "Ha ocurrido un error, intenta nuevamente"
                things_to_pay = tenant_things_to_pay.select_all_tenant_things_to_pay()
                return render_template('Get_all_tenant_things_to_pay.html',result=result,
                    things_to_pay=things_to_pay)
            elif check == True:
                result = "El servicio que estas agregando ya existe"
                return render_template('Get_all_tenant_things_to_pay.html',result=result,
                    things_to_pay=things_to_pay)
            else:
                result2 = "Inactivo"
                alert = "El servicio que estas agregando ya existe pero esta inactivo, queres recuperarlo?"
                things_to_pay = tenant_things_to_pay.select_all_tenant_things_to_pay()
                return render_template('Get_all_tenant_things_to_pay.html',result2=result2,check=check,
                                        alert=alert,things_to_pay=things_to_pay)
    return render_template('Get_all_tenant_things_to_pay.html',things_to_pay=things_to_pay)

@app.route("/Get_all_service_providers", methods=["GET","POST"])
def Get_all_service_providers():
    current_service_providers = is_service_provider.select_all_plus_info()
    if request.method == 'POST':
        IdServiceIsServiceProvider = request.form.get("IdServiceIsServiceProvider")
        if IdServiceIsServiceProvider:
            IdServiceIsServiceProvider = int(IdServiceIsServiceProvider)
            registration_number = request.form.get("registration_number")
            if registration_number == "":
                registration_number = "-"
            return render_template()
            # ESTO VA DESPUES. CUANDO YA AGREGO
            # resultado = is_service_provider.check_if_record_already_exist(IdPersonIsServiceProvider,IdServiceIsServiceProvider)
            # if resultado == False:  
            #     result = is_service_provider.insert_new_service_provider(IdServiceIsServiceProvider,IdPersonIsServiceProvider,registration_number)
            #     if result == 1:
            #         result = "Has agregado un nuevo prestador de servicio"
            #     else:
            #         result = "Ha ocurrido un error, intenta nuevamente"
            #     return render_template("Get_all_service_providers.html",current_service_providers=current_service_providers,
            #             all_services=all_services,service_providers_and_more=service_providers_and_more,result=result)
            # elif resultado == "exist_still_working":
            #     result = "El prestador de servicio que estas queriendo agregar ya esta registrado con ese servicio"
            #     return render_template("Get_all_service_providers.html",current_service_providers=current_service_providers,
            #             all_services=all_services,service_providers_and_more=service_providers_and_more,result=result)
            # else:
            #     result2 = "El prestador de servicio que estas intentando agregar ya existe, pero esta inactivo, queres reactivarlo?"
            #     return render_template("Get_all_service_providers.html",current_service_providers=current_service_providers,
            #             all_services=all_services,service_providers_and_more=service_providers_and_more,result2=result2,resultado=resultado)
        IdPersonIsServiceProviderRegistrationNumber = request.form.get("IdPersonIsServiceProviderRegistrationNumber")
        if IdPersonIsServiceProviderRegistrationNumber:
            registration_number = request.form.get("registration_number")
            if registration_number == "":
                registration_number = "-"
            result = is_service_provider.update_registation_number_by_id(registration_number,IdPersonIsServiceProviderRegistrationNumber)
            if result == 1:
                result = "Has modificado la matricula correctamente"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            current_service_providers = is_service_provider.select_all_plus_info()
            return render_template("Get_all_service_providers.html",current_service_providers=current_service_providers,
                        result=result)
        id_is_service_provider_delete = request.form.get("id_is_service_provider_delete")
        if id_is_service_provider_delete:
            still_working = 0
            result = is_service_provider.delete_or_recover_is_service_provider_row_by_id(still_working,id_is_service_provider_delete)
            if result == 1:
                result = "Has eliminado el registro correctamente"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            current_service_providers = is_service_provider.select_all_plus_info()
            return render_template("Get_all_service_providers.html",current_service_providers=current_service_providers,
                        result=result)
    return render_template("Get_all_service_providers.html",current_service_providers=current_service_providers)

@app.route("/Get_all_tenant_tasks", methods=["GET","POST"])
def Get_all_tenant_tasks():
    All_tenant_tasks = tenant_payment.select_all_plus_info()
    All_tenant_things_to_pay = tenant_things_to_pay.select_all_existing_tenant_things_to_pay()
    All_current_tenants = tenant_permanency.select_all_plus_info()
    if request.method == 'POST':
        id_tenant_thing_to_pay = request.form.get("AddTaskTenantIdThingToPay")
        if id_tenant_thing_to_pay:
            id_tenant_permanency = request.form.get("AddTaskGetIdTenantPermanency")
            cbu = request.form.get("AddTaskTenantcbu")
            amount = request.form.get("AddTaskTenantAmount")
            detail = request.form.get("AddTaskTenantDetail")
            if cbu == "":
                cbu = "-"
            if amount == "":
                amount = 0
            else:
                try:
                    amount = float(amount.replace(',',"."))
                except:
                    result = '''Ocurrio un error. Ingresa el numero sin puntos, solamente agregale una coma ','
                                si queres agregar decimales'''
                    return render_template("Get_all_tenant_tasks.html",All_tenant_tasks=All_tenant_tasks,result=result,
                        All_tenant_things_to_pay=All_tenant_things_to_pay,All_current_tenants=All_current_tenants)
            if detail == "":
                detail = "-"
            payment_date = "-"
            result = tenant_payment.insert_new_payment_task(id_tenant_thing_to_pay,id_tenant_permanency,cbu,payment_date,amount,detail)
            if result == 1:
                result = "Has agregado un pago para un inquilino"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            All_tenant_tasks = tenant_payment.select_all_plus_info()
            All_tenant_things_to_pay = tenant_things_to_pay.select_all_existing_tenant_things_to_pay()
            All_current_tenants = tenant_permanency.select_all_plus_info()
            return render_template("Get_all_tenant_tasks.html",All_tenant_tasks=All_tenant_tasks,result=result,
                        All_tenant_things_to_pay=All_tenant_things_to_pay,All_current_tenants=All_current_tenants)
        id_tenant_payment2 = request.form.get("id_tenant_payment2")
        print(id_tenant_payment2)
        if id_tenant_payment2:
            id_tenant_payment2 = int(id_tenant_payment2)
            cbu = request.form.get("cbu")
            if cbu == "":
                cbu = "-"
            amount = request.form.get("amount")
            if amount == "":
                amount = 0
            else:
                try:
                    amount = float(amount.replace(',',"."))
                except:
                    result = '''Ocurrio un error. Ingresa el numero sin puntos, solamente agregale una coma ','
                                si queres agregar decimales'''
                    return render_template("Get_all_tenant_tasks.html",All_tenant_tasks=All_tenant_tasks,result=result,
                        All_tenant_things_to_pay=All_tenant_things_to_pay,All_current_tenants=All_current_tenants)
            detail = request.form.get("detail")
            if detail == "":
                detail = "-"
            payment_date = datetime.date.today()
            payment_date = str(payment_date)
            result = tenant_payment.end_task_insert_amount_detail_cbu(payment_date,cbu,amount,detail,id_tenant_payment2)
            if result == 1:
                result = "Has realizado el pago correctamente"
            else:
                result = "Ha ocurrido un error. Intenta nuevamente"
            All_tenant_tasks = tenant_payment.select_all_plus_info()
            All_tenant_things_to_pay = tenant_things_to_pay.select_all_existing_tenant_things_to_pay()
            All_current_tenants = tenant_permanency.select_all_plus_info()
            return render_template("Get_all_tenant_tasks.html",All_tenant_tasks=All_tenant_tasks,result=result,
                        All_tenant_things_to_pay=All_tenant_things_to_pay,All_current_tenants=All_current_tenants)
    return render_template("Get_all_tenant_tasks.html",All_tenant_tasks=All_tenant_tasks,
        All_tenant_things_to_pay=All_tenant_things_to_pay,All_current_tenants=All_current_tenants)

@app.route("/Get_all_owners", methods=["GET","POST"])
def Get_all_owners():
    current_owners = is_owner.select_all_plus_info()
    if request.method == 'POST':
        id_is_owner_delete = request.form.get("id_is_owner_delete")
        if id_is_owner_delete:
            already_exist_is_owner = 0
            result = is_owner.delete_or_recover_is_owner_row_by_id(already_exist_is_owner,id_is_owner_delete)
            if result == 1:
                result = "Has eliminado el registro correctamente"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            current_owners = is_owner.select_all_plus_info()
            return render_template('Get_all_owners.html',current_owners=current_owners,result=result)            
    return render_template("Get_all_owners.html",current_owners=current_owners)

@app.route("/Get_all_owner_tasks", methods=["GET","POST"])
def Get_all_owner_tasks():
    print("1")
    All_tasks_owners = payment_to_owner.select_all_plus_info()
    All_owners = is_owner.select_all_existing_owners_plus_info()
    if request.method == 'POST':
        print("2")
        id_is_owner = request.form.get("AddTaskOwner")
        print(id_is_owner)
        if id_is_owner:
            print("ID IS OWNER")
            cbu = request.form.get("AddTaskOwnercbu")
            amount = request.form.get("AddTaskOwnerAmount")
            detail = request.form.get("AddTaskOwnerDetail")
            if cbu == "":
                cbu = "-"
            if amount == "":
                amount = 0
            else:
                try:
                    amount = float(amount.replace(',',"."))
                except:
                    result = '''Ocurrio un error. Ingresa el numero sin puntos, solamente agregale una coma ','
                                si queres agregar decimales'''
                    return render_template("Get_all_owner_tasks.html",All_tasks_owners=All_tasks_owners,
                        All_owners=All_owners,result=result)
            if detail == "":
                detail = "-"
            payment_date = "-"   
            result = payment_to_owner.insert_new_payment_task(id_is_owner,cbu,payment_date,amount,detail)
            print(result)
            if result == 1:
                result = "Has agregado un pago para un propietario"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            All_tasks_owners = payment_to_owner.select_all_plus_info()
            print(All_tasks_owners)
            All_owners = is_owner.select_all_existing_owners_plus_info()
            print("DEBERIA ENTRAR AL RETURN")
            return render_template("Get_all_owner_tasks.html",All_tasks_owners=All_tasks_owners,
                        All_owners=All_owners,result=result)
        id_payment_to_owner_task2 = request.form.get("id_payment_to_owner_task2")
        if id_payment_to_owner_task2:
            id_payment_to_owner_task2 = int(id_payment_to_owner_task2)
            cbu = request.form.get("cbu")
            if cbu == "":
                cbu = "-"
            amount = request.form.get("amount")
            if amount == "":
                amount = 0
            else:
                try:
                    amount = float(amount.replace(',',"."))
                except:
                    result = '''Ocurrio un error. Ingresa el numero sin puntos, solamente agregale una coma ','
                                si queres agregar decimales'''
                    return render_template("Get_all_owner_tasks.html",All_tasks_owners=All_tasks_owners,
                        All_owners=All_owners,result=result)
            detail = request.form.get("detail")
            if detail == "":
                detail = "-"
            payment_date = datetime.date.today()
            payment_date = str(payment_date)
            result = payment_to_owner.end_task_insert_amount_detail_cbu(payment_date,cbu,amount,detail,id_payment_to_owner_task2)
            if result == 1:
                result = "Has realizado el pago correctamente"
            else:
                result = "Ha ocurrido un error. Intenta nuevamente"
            All_tasks_owners = payment_to_owner.select_all_plus_info()
            All_owners = is_owner.select_all_existing_owners_plus_info()
            return render_template("Get_all_owner_tasks.html",All_tasks_owners=All_tasks_owners,
                        All_owners=All_owners,result=result)
    print("3")
    return render_template("Get_all_owner_tasks.html",All_tasks_owners=All_tasks_owners,All_owners=All_owners)

@app.route("/Get_all_service_provider_tasks", methods=["GET","POST"])
def Get_all_service_providers_tasks():
    All_tasks_service_providers = grant_of_service.select_all_plus_info()
    All_services = services.select_all_existing_services()
    All_propertys = property.select_all_existing_propertys()
    print("1")
    if request.method == 'POST':
        print("2")
        id_service = request.form.get("AddTaskGetIdService")
        if id_service:
            id_property = request.form.get("AddTaskGetIdProperty")
            cbu = request.form.get("AddTaskServiceprovidercbu")
            amount = request.form.get("AddTaskServiceproviderAmount")
            detail = request.form.get("AddTaskServiceproviderDetail")
            if cbu == "":
                cbu = "-"
            if amount == "":
                amount = 0
            else:
                try:
                    amount = float(amount.replace(',',"."))
                except:
                    result = '''Ocurrio un error. Ingresa el numero sin puntos, solamente agregale una coma ','
                                si queres agregar decimales'''
                    return render_template("Get_all_service_providers_tasks.html",All_services=All_services,All_propertys=All_propertys,
                    All_tasks_service_providers=All_tasks_service_providers,result=result)
            if detail == "":
                detail = "-"
            payment_date = "-"   
            result = grant_of_service.insert_new_payment_task(id_service,id_property,cbu,payment_date,amount,detail)
            if result == 1:
                result = "Has agregado una tarea/pago"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            All_tasks_service_providers = grant_of_service.select_all_plus_info()
            All_services = services.select_all_existing_services()
            All_propertys = property.select_all_existing_propertys()
            return render_template("Get_all_service_providers_tasks.html",All_services=All_services,All_propertys=All_propertys,
                All_tasks_service_providers=All_tasks_service_providers,result=result)
        id_grant_of_service_task = request.form.get("id_grant_of_service_task")
        if id_grant_of_service_task:
            id_grant_of_service_task = int(id_grant_of_service_task)
            cbu = request.form.get("cbu")
            if cbu == "":
                cbu = "-"
            amount = request.form.get("amount")
            if amount == "":
                amount = 0
            else:
                try:
                    amount = float(amount.replace(',',"."))
                except:
                    result = '''Ocurrio un error. Ingresa el numero sin puntos, solamente agregale una coma ','
                                si queres agregar decimales'''
                    return render_template("Get_all_service_providers_tasks.html",All_services=All_services,All_propertys=All_propertys,
                        All_tasks_service_providers=All_tasks_service_providers,result=result)
            detail = request.form.get("detail")
            if detail == "":
                detail = "-"
            payment_date = datetime.date.today()
            payment_date = str(payment_date)
            result = grant_of_service.end_task_insert_amount_detail_cbu(payment_date,cbu,amount,detail,id_grant_of_service_task)
            if result == 1:
                result = "Has realizado el pago exitosamente"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            All_tasks_service_providers = grant_of_service.select_all_plus_info()
            All_services = services.select_all_existing_services()
            All_propertys = property.select_all_existing_propertys()
            return render_template("Get_all_service_providers_tasks.html",All_services=All_services,All_propertys=All_propertys,
                All_tasks_service_providers=All_tasks_service_providers,result=result)
        AssignServiceProvider = request.form.get("AssignServiceProvider")
        if AssignServiceProvider:
            ids = AssignServiceProvider.split(", ")
            id_grant_of_service_task = int(ids[0])
            id_is_service_provider = int(ids[1])
            result = grant_of_service.already_contacted_service_provider(id_grant_of_service_task,id_is_service_provider)
            if result == 1:
                result = "Has asignado a un proveedor de servicio a la tarea"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            All_tasks_service_providers = grant_of_service.select_all_plus_info()
            All_services = services.select_all_existing_services()
            All_propertys = property.select_all_existing_propertys()
            return render_template("Get_all_service_providers_tasks.html",All_services=All_services,All_propertys=All_propertys,
                All_tasks_service_providers=All_tasks_service_providers,result=result)
        id_grant_of_service_task2 = request.form.get("id_grant_of_service_task2")
        id_is_service_provider2 = request.form.get("id_is_service_provider2")
        if id_grant_of_service_task2:
            result = grant_of_service.already_contacted_service_provider(id_grant_of_service_task2,id_is_service_provider2)
            if result == 1:
                result = "Has dejado de asignar al proveedor de servicio"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            All_tasks_service_providers = grant_of_service.select_all_plus_info()
            All_services = services.select_all_existing_services()
            All_propertys = property.select_all_existing_propertys()
            return render_template("Get_all_service_providers_tasks.html",All_services=All_services,All_propertys=All_propertys,
                All_tasks_service_providers=All_tasks_service_providers,result=result)
    return render_template("Get_all_service_providers_tasks.html",All_services=All_services,All_propertys=All_propertys,
        All_tasks_service_providers=All_tasks_service_providers)

@app.route("/Get_all_is_owner_deleted", methods=["GET","POST"])
def Get_all_is_owner_deleted():
    All_owners = is_owner.select_all_plus_info()
    if request.method == 'POST':
        id_is_owner_recover = request.form.get("id_is_owner_recover")
        if id_is_owner_recover:
            id_person_recover = request.form.get("id_person_recover")
            id_property_recover = request.form.get("id_property_recover")
            resultado = is_owner.check_if_record_already_exist(id_person_recover,id_property_recover)
            if resultado == "Already_exist_diferent_owner":
                result = "El registro que estas intentando recuperar contiene una propiedad que actualmente pertenece a otro dueño"
                return render_template("Get_all_is_owner_deleted.html",All_owners=All_owners,result=result)
            else:
                already_exist_is_owner = 1
                result = is_owner.delete_or_recover_is_owner_row_by_id(already_exist_is_owner,id_is_owner_recover)
                if result == 1:
                    result = "Recuperaste el registro exitosamente"
                    return render_template("Get_all_is_owner_deleted.html",All_owners=All_owners,result=result)
                else:
                    result = "Ha ocurrido un error. Intenta nuevamente"
                    return render_template("Get_all_is_owner_deleted.html",All_owners=All_owners,result=result)
    return render_template("Get_all_is_owner_deleted.html",All_owners=All_owners)

@app.route("/Get_all_service_providers_deleted", methods=["GET","POST"])
def Get_all_service_providers_deleted():
    current_service_providers = is_service_provider.select_all_plus_info()
    select_any_not_working_in_service_provider = is_service_provider.select_any_not_working_in_service_provider()
    if request.method == 'POST':
        id_is_service_provider_recover = request.form.get("id_is_service_provider_recover")
        if id_is_service_provider_recover:
            id_is_service_provider_recover = int(id_is_service_provider_recover)
            still_working = 1
            result = is_service_provider.delete_or_recover_is_service_provider_row_by_id(still_working,id_is_service_provider_recover)
            if result == 1:
                result = "Has recuperado el registro correctamente"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            current_service_providers = is_service_provider.select_all_plus_info()
            select_any_not_working_in_service_provider = is_service_provider.select_any_not_working_in_service_provider()
            return render_template("Get_all_service_providers_deleted.html",current_service_providers=current_service_providers,
                result=result,select_any_not_working_in_service_provider=select_any_not_working_in_service_provider)
    return render_template("Get_all_service_providers_deleted.html",current_service_providers=current_service_providers,
        select_any_not_working_in_service_provider=select_any_not_working_in_service_provider)

@app.route('/Get_all_services', methods=["GET","POST"])
def AddOrDeleteService():
    all_services = services.select_all()
    if request.method == 'POST':
        id_service_delete = request.form.get("id_service_delete")
        if id_service_delete:
            still_exist = 0
            result = services.delete_or_recover_service(id_service_delete,still_exist)
            if result == 1:
                result = "Has eliminado el servicio"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            all_services = services.select_all()
            return render_template("Get_all_services.html",all_services=all_services,result=result)
        id_service_recover = request.form.get("id_service_recover")
        if id_service_recover:
            still_exist = 1
            result = services.delete_or_recover_service(id_service_recover,still_exist)
            if result == 1:
                result = "Has recuperado el servicio"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            all_services = services.select_all()
            return render_template("Get_all_services.html",all_services=all_services,result=result)
        new_service_name = request.form.get("new_service_name")
        if new_service_name:
            if new_service_name == "":
                new_service_name = "-"
            check = services.check_existing_service_get_id(new_service_name)
            if check == False:
                description = request.form.get("description")
                if description == "":
                    description = "-"
                result = services.insert_service(new_service_name,description)
                if result == 1:
                    result = "Has agregado un nuevo servicio"
                elif resultado == 0:
                    result = "Ha ocurrido un error, intenta nuevamente"
                all_services = services.select_all()
                return render_template('Get_all_services.html',result=result,
                    all_services=all_services)
            elif check == True:
                result = "El servicio que estas agregando ya existe"
                return render_template('Get_all_services.html',result=result,
                    all_services=all_services)
            else:
                result2 = "Inactivo"
                alert = "El servicio que estas agregando ya existe pero esta inactivo, queres recuperarlo?"
                return render_template('Get_all_services.html',result2=result2,check=check,
                                        alert=alert,all_services=all_services)
        editServiceId = request.form.get("editServiceId")
        if editServiceId:
            editServiceId = int(editServiceId)
            serviceName = request.form.get("serviceName")
            if serviceName == "":
                serviceName = "-"
            description = request.form.get("serviceDescription")
            if description == "":
                description = "-" 
            result = services.update_service(serviceName,description,editServiceId)
            if result == 1:
                result = "Has modificado el servicio"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            all_services = services.select_all()
            return render_template('Get_all_services.html',result=result,all_services=all_services)
    return render_template("Get_all_services.html",all_services=all_services)

@app.route('/Get_all_people', methods=["GET", "POST"])
def Get_all_people():
    all_people = person.select_all()
    if request.method == 'POST':

        # ADD NEW PERSON 
        dni = request.form.get("dni")            
        if dni:
            name = request.form.get("name")
            surname = request.form.get("surname")
            cellphone = request.form.get("cellphone")
            mail = request.form.get("mail")
            address = request.form.get("address")
            if name == "":
                name = "-"
            if surname == "":
                surname = "-"
            if dni == "":
                dni = "-"
            if cellphone == "":
                cellphone = "-"
            if mail == "":
                mail = "-"
            if address == "":
                address = "-"
            result = person.check_existing_person(dni)
            if result == False:
                addPerson = person.insert_person(name,surname,dni,cellphone,mail,address)
                if addPerson == 1:
                    result = "Se ha agregado una persona exitosamente"
                else:
                    result = "Ha ocurrido un error, intenta nuevamente"
                all_people = person.select_all()
                return render_template('Get_all_people.html',all_people=all_people,result=result)
            if result == True:
                result = "La persona que estas agregando ya existe"
                return render_template('Get_all_people.html',all_people=all_people,result=result) 
            else:
                result2 = "La persona que estas agregando ya existia, pero fue eliminada, queres recuperarla?"
                return render_template('Get_all_people.html',all_people=all_people,result2=result2,dni=dni)

        # DELETE PERSON BY ID        
        DeletePersonById = request.form.get("DeletePersonById")
        if DeletePersonById:
            checkTenantRenting = tenant_permanency.check_if_person_currenrly_renting(DeletePersonById)
            checkOwnerOwningProperty = is_owner.check_if_person_currenrly_owner_of_any_property(DeletePersonById)
            checkServiceProviderStillWorking = is_service_provider.check_if_person_still_exist_in_service_provider(DeletePersonById)
            if checkTenantRenting == True or checkOwnerOwningProperty == True or checkServiceProviderStillWorking == True:
                result3 = '''Esta persona esta asociada a algun servicio, propiedad o alquiler actualmente en uso.
                    Para poder eliminarla revise los siguientes puntos:
                    - Si es inquilino: Finalice el contrato de alquiler
                    - Si es propietario: Desvinculelo de la/las propiedad/es a los que este asociado
                    - Si es prestador de servicio: Desvinculelo de el/los servicio/s a los que este asociado'''
                return render_template('Get_all_people.html',all_people=all_people,result3=result3)
            else:
                already_exist = 0
                result = person.delete_or_recover_person_by_id(already_exist,DeletePersonById)
                if result == 1:
                    result = "Has eliminado a la persona"
                else:
                    result = "Ha ocurrido un error, intenta nuevamente"
                all_people = person.select_all()
                return render_template('Get_all_people.html',all_people=all_people,result=result)

        # RECOVER PERSON BY ID
        RecoverPersonById = request.form.get("RecoverPersonById")
        if RecoverPersonById:
            already_exist = 1
            result = person.delete_or_recover_person_by_id(already_exist,RecoverPersonById)
            if result == 1:
                result = "Has recuperado el registro correctamente"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            all_people = person.select_all()
            return render_template('Get_all_people.html',all_people=all_people,result=result)

        # RECOVER PERSON BY DNI
        RecoverPersonByDni = request.form.get("RecoverPersonByDni")
        if RecoverPersonByDni:
            already_exist = 1
            result = person.delete_or_recover_person_by_dni(already_exist,RecoverPersonByDni)
            if result == 1:
                result = "Has recuperado a la persona"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            all_people = person.select_all()
            return render_template('Get_all_people.html',all_people=all_people,result=result)
                
        # UPDATE PERSON INFO
        id2 = request.form.get("id2")                  
        if id2:
            dni2 = request.form.get("dni2") 
            name2 = request.form.get("name2")
            surname2 = request.form.get("surname2")
            cellphone2 = request.form.get("cellphone2")
            address2 = request.form.get("address2")
            mail2 = request.form.get("mail2")
            if name2 == "":
                name = "-"
            if surname2 == "":
                surname = "-"
            if dni2 == "":
                dni = "-"
            if cellphone2 == "":
                cellphone = "-"
            if mail2 == "":
                mail = "-"
            if address2 == "":
                address = "-"
            result = person.update_person_exist_by_id(name2,surname2,dni2,id2,cellphone2,mail2,address2)
            if result == 1:
                result = "Has modificado la persona correctamente"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            all_people = person.select_all()
            return render_template('Get_all_people.html',all_people=all_people,result=result)
    return render_template('Get_all_people.html',all_people=all_people)

@app.route('/Add_property', methods=["GET", "POST"])
def Add_property():
    all_propertys = property.select_all()
    if request.method == 'POST':
        # ADD A NEW PROPERTY
        nomenclatura = request.form.get("nomenclatura")
        if nomenclatura:
            state = request.form.get("state")
            city = request.form.get("city")
            neighborhood = request.form.get("neighborhood")
            street = request.form.get("street")
            number = request.form.get("number")
            floor = request.form.get("floor")
            postal_code = request.form.get("postal_code")
            if nomenclatura == "":
                nomenclatura = "-"
            if state == "":
                state = "-"
            if city == "":
                city = "-"
            if neighborhood == "":
                neighborhood = "-"
            if street == "":
                street = "-"
            if number == "":
                number = "-"
            if floor == "":
                floor = "-"
            if postal_code == "":
                postal_code = "-"
            try:
                result = property.check_existing_property(nomenclatura)
            except:
                result = "Ha ocurrido un error, intenta nuevamente"
                return render_template('Add_or_delete_property.html',result=result,all_propertys=all_propertys)
            if result == False:
                addPropeorty = property.insert_property(nomenclatura,state,city,street,number,neighborhood,floor,postal_code)
                if addPropeorty == 1:
                    result = "Se ha agregado una propiedad exitosamente"
                else:
                    result = "Ha ocurrido un error, intenta nuevamente"
                all_propertys = property.select_all()
                return render_template('Add_or_delete_property.html',result=result,all_propertys=all_propertys)
            if result == True:
                result = "La propiedad que estas agregando ya existe"
                return render_template('Add_or_delete_property.html',result=result,all_propertys=all_propertys)          
            else:
                result2 = "La propiedad que estas agregando ya existia pero fue eliminada, queres recuperarla?"
                all_propertys = property.select_all()
                return render_template('Add_or_delete_property.html',nomenclatura=nomenclatura,result2=result2,
                    all_propertys=all_propertys)
        updatePropertyRecoverByNomenclatura = request.form.get("nomenclatura_property_recover")
        if updatePropertyRecoverByNomenclatura:
            already_exist = 1
            result = property.delete_or_recover_property_by_nomenclatura(updatePropertyRecoverByNomenclatura,already_exist)
            if result == 1:
                result = "La propiedad ha sido recuperada"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            all_propertys = property.select_all()
            return render_template('Add_or_delete_property.html',result=result,all_propertys=all_propertys)
    return render_template('Add_or_delete_property.html',all_propertys=all_propertys)

@app.route('/Add_or_delete_service', methods=["GET","POST"])
def Add_Service():
    all_services = services.select_all()
    if request.method == 'POST':
        id_service_recover = request.form.get("id_service_recover")
        if id_service_recover:
            still_exist = 1
            result = services.delete_or_recover_service(id_service_recover,still_exist)
            if result == 1:
                result = "Has recuperado el servicio"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            all_services = services.select_all()
            return render_template("Add_or_delete_service.html",all_services=all_services,result=result)
        new_service_name = request.form.get("new_service_name")
        if new_service_name:
            if new_service_name == "":
                new_service_name = "-"
            check = services.check_existing_service_get_id(new_service_name)
            if check == False:
                description = request.form.get("description")
                if description == "":
                    description = "-"
                result = services.insert_service(new_service_name,description)
                if result == 1:
                    result = "Has agregado un nuevo servicio"
                elif resultado == 0:
                    result = "Ha ocurrido un error, intenta nuevamente"
                all_services = services.select_all()
                return render_template('Add_or_delete_service.html',result=result,
                    all_services=all_services)
            elif check == True:
                result = "El servicio que estas agregando ya existe"
                return render_template('Add_or_delete_service.html',result=result,
                    all_services=all_services)
            else:
                result2 = "Inactivo"
                alert = "El servicio que estas agregando ya existia pero fue eliminado, queres recuperarlo?"
                return render_template('Add_or_delete_service.html',result2=result2,check=check,
                                        alert=alert,all_services=all_services)
    return render_template("Add_or_delete_service.html",all_services=all_services)

@app.route('/Add_or_delete_tenant_thing_to_pay', methods=["GET","POST"])
def Add_or_delete_tenant_thing_to_pay():
    print("ENTRO")
    all_tenant_things_to_pay = tenant_things_to_pay.select_all_tenant_things_to_pay()
    if request.method == 'POST':
        id_tenant_thing_to_pay_recover = request.form.get("id_tenant_thing_to_pay_recover")
        if id_tenant_thing_to_pay_recover:
            still_exist = 1
            result = tenant_things_to_pay.delete_or_recover_thing_to_pay(id_tenant_thing_to_pay_recover,still_exist)
            if result == 1:
                result = "Has recuperado el servicio"
            else:
                result = "Ha ocurrido un error, intenta nuevamente"
            all_tenant_things_to_pay = tenant_things_to_pay.select_all_tenant_things_to_pay()
            return render_template("Add_or_delete_tenant_thing_to_pay.html",all_tenant_things_to_pay=all_tenant_things_to_pay
                ,result=result)
        new_service_name = request.form.get("new_service_name")
        if new_service_name:
            if new_service_name == "":
                new_service_name = "-"
            check = tenant_things_to_pay.check_existing_thing_get_id(new_service_name)
            if check == False:
                description = request.form.get("description")
                if description == "":
                    description = "-"
                result = tenant_things_to_pay.insert_thing(new_service_name,description)
                if result == 1:
                    result = "Has agregado un nuevo servicio"
                elif resultado == 0:
                    result = "Ha ocurrido un error, intenta nuevamente"
                all_tenant_things_to_pay = tenant_things_to_pay.select_all_tenant_things_to_pay()
                return render_template("Add_or_delete_tenant_thing_to_pay.html",all_tenant_things_to_pay=all_tenant_things_to_pay
                    ,result=result)
            elif check == True:
                result = "El servicio que estas agregando ya existe"
                return render_template("Add_or_delete_tenant_thing_to_pay.html",all_tenant_things_to_pay=all_tenant_things_to_pay
                    ,result=result)
            else:
                result2 = "El servicio que estas agregando ya existia pero fue eliminado, queres recuperarlo?"
                all_tenant_things_to_pay = tenant_things_to_pay.select_all_tenant_things_to_pay()
                return render_template("Add_or_delete_tenant_thing_to_pay.html",all_tenant_things_to_pay=all_tenant_things_to_pay
                ,result2=result2,check=check)
    return render_template("Add_or_delete_tenant_thing_to_pay.html",all_tenant_things_to_pay=all_tenant_things_to_pay)

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(debug=True)
