from flask import Flask,request,jsonify,render_template_string
import pymysql.cursors
import requests
from datetime import datetime
from flask import Flask,render_template,redirect,url_for,request,flash
import random
import string
from Database_schema import create_table_query_UsersData,create_table_query_employee_attendance,create_table_holiday,create_table_Announcement
from Database_schema import create_table_query_employee,create_table_leave_request,create_table_daily_status,create_table_leave_balance,create_table_leave_history
from flask_mail import Mail, Message
from datetime import datetime,timedelta,date


app = Flask(__name__)



# Configure mail server
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'suckerpunchjohnwick007@gmail.com'
app.config['MAIL_USERNAME'] = 'enerziff@gmail.com'
app.config['MAIL_PASSWORD'] = 'qjts fwqq qgtn hbjt'
# app.config['MAIL_PASSWORD'] = 'ilkv wibm olar coow'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)



#database connection with pymysql..........
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Kavitha@27'
MYSQL_DB = 'logindetails'
connection = pymysql.connect(host=MYSQL_HOST,
                             user=MYSQL_USER,
                             password=MYSQL_PASSWORD,
                             db=MYSQL_DB,
                             cursorclass=pymysql.cursors.DictCursor)




#creating table (employee_complete_details) into database
with connection.cursor() as cursor:
    cursor.execute(create_table_query_employee)
    connection.commit()

#creating table(users_Register_Data) into database
with connection.cursor() as cursor:
        cursor.execute(create_table_query_UsersData)
        connection.commit()

#creating table(Employee_Attendance_Data) into database
with connection.cursor() as cursor:
     cursor.execute(create_table_query_employee_attendance)
     connection.commit()

with connection.cursor() as cursor:
     cursor.execute(create_table_daily_status)
     connection.commit()

#creating table(Leave_Request) into database
with connection.cursor() as cursor:
     cursor.execute(create_table_leave_request)
     connection.commit()

#creating table(Leave_history) into database
with connection.cursor() as cursor:
    cursor.execute(create_table_leave_history)
    connection.commit()

#creating table for leave_balance........
with connection.cursor() as cursor:
    cursor.execute(create_table_leave_balance)
    connection.commit()


with connection.cursor() as cursor:
     cursor.execute(create_table_Announcement)
     connection.commit()

with connection.cursor() as cursor:
    cursor.execute(create_table_holiday)
    connection.commit()




#getting data from user and performing update(data) and insert(data) into main table(employee_complete_details)..
@app.route('/employee_complete_details',methods=['POST'])
def Upsert_Employee_Details():
    if request.method=='POST':
       Data=request.get_json()
       #printing data(got by user)...........
       print(Data)
       # extracting data....................
       Employee_id=Data['employee_id']
       Employee_Name=Data['employee_name']
       Employee_email=Data['employee_email']
       Gender=Data['Gender']
       Phone_Number=Data['Phone_Number']
       Date_of_birth=Data['Date_of_birth']
       Address=Data['Address']
       Department=Data['Department']
       Position=Data['Position']
       Team_Lead=Data['Team_lead']
       Team_Lead_Email=Data['Team_lead_email']
       Date=Data['Date']
       Manager_Name=Data['Manager_name']
       Manager_Email=Data['Manager_email']
       Hire_Date=Data['Hire_date']
       Work_Location=Data['Work_location']
       Skills=Data['Skills']
       Emergency_Contact=Data['Emergency_contact']
       Username=Data['Username']
       Password=Data['Password']
       Usertype=Data['userType']
       Request_type=Data['request_type']
       # performing insert/update based on the request_type......
       try:
        with connection.cursor() as cursor:
         if Request_type=='insert':
            #query to insert data into main table(employee_complete_details....)
            Insert_Query="INSERT INTO Employee_complete_Details(Employee_id,Employee_Name,Employee_email,Gender,Phone_Number,Date_of_birth,Address,Department,Position,Team_lead,Team_lead_email,Date,Manager_name,Manager_email,Hire_date,Work_location,Skills,Emergency_contact,Username,Password,usertype) VALUES (%s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
            cursor.execute( Insert_Query,(Employee_id,Employee_Name,Employee_email,Gender,Phone_Number,Date_of_birth,Address,Department,Position,Team_Lead,Team_Lead_Email,Date,Manager_Name,Manager_Email,Hire_Date,Work_Location,Skills,Emergency_Contact,Username,Password,Usertype))
            connection.commit()
            Response_Data = {'status': 'success', 'message': 'employee_details inserted into database successfully'}
            return jsonify(Response_Data)
         elif Request_type=='update':
            #query to update data into main table(employee_complete_details....)
            Update_Query="UPDATE Employee_complete_Details SET  Employee_Name=%s,Employee_email=%s,Gender=%s,Phone_Number=%s,Date_of_birth=%s,Address=%s,Department=%s,Position=%s,Team_lead=%s,Team_lead_email=%s,Date=%s,Manager_name=%s,Manager_email=%s,Hire_date=%s,Work_location=%s,Skills=%s,Emergency_contact=%s,Username=%s,Password=%s,usertype=%s WHERE Employee_id=%s"
            cursor.execute(Update_Query,(Employee_Name,Employee_email,Gender,Phone_Number,Date_of_birth,Address,Department,Position,Team_Lead,Team_Lead_Email,Date,Manager_Name,Manager_Email,Hire_Date,Work_Location,Skills,Emergency_Contact,Username,Password,Usertype,Employee_id))
            connection.commit()
            #sending response as success...
            Response_Data = {'status': 'success', 'message': 'employee_details updated into database successfully'}
            return jsonify(Response_Data)
         else:
                print("invalid_request_type")
                #sending response as invalid_request_type if request_types does'not matches...
                Response_Data = {'status': 'failed', 'message': 'invalid_request_type'}
                return jsonify(Response_Data)
       except Exception as e:
           print("exception occured in upsert_employee_details function and error is:",e)
    else:
        Response_Data = {'status': 'failed', 'message': 'invalid request_type check once and try again!!!'}
        return jsonify(Response_Data)        





#sending employee_complete details present in the main table(employee_complete_details) based on the employee_id...
@app.route('/employee_details',methods=['POST'])
def Fetch_Emp_Info():
    #getting employee_id.....
    if request.method=='POST':
       Data=request.get_json()
       Employee_Id=Data['Employee_id']
       #printing employee_id from request for clarification...
       print(Data)
       with connection.cursor() as cursor:
        #selecting employee details from main table based on employee_id.....
        Select_Query='SELECT * FROM Employee_complete_Details WHERE Employee_id=%s'
        cursor.execute(Select_Query,Employee_Id)
        Emp_Info=cursor.fetchone()
        try:
            if Emp_Info:
                #sending employee_info in response if user exists...
                Response_Data = {'status': 'success', 'employee_complete_info':Emp_Info}
                print("employee_details basedon Employee_id  data sent  successfully")
                return jsonify(Response_Data)
            else:
                Response_Data = {'status': 'failed','message':'requested emp_id doesn"t exist in table...'}
                print("employee_id not exist..")
                return jsonify(Response_Data)
        except Exception as e:
            print("exception occured in Fetch_Emp_Info function and error is",e)
            return jsonify(Response_Data)





@app.route('/admin_edit',methods=['POST'])
def emp_id_name_email():
    if request.method=='POST':
       data=request.get_json()
    #    Employee_Id=data['Employee_id']
       print(data)
       with connection.cursor() as cursor:
            sql='SELECT Employee_id, Employee_Name,Employee_email FROM Employee_complete_Details '
            cursor.execute(sql)
            emp_data=cursor.fetchall()
            response_data = {'status': 'success', 'employee_complete_info':emp_data}
            print("employees_id_email,name sent  successfully")
    return jsonify(response_data)






#receiving data from request for inserting into users_register table... 
@app.route('/data_receive',methods=['POST'])
def User_Register():
     if request.method=='POST':
       Data=request.json
       print(Data)
       #Extracting data........
       Username = Data['username']
       Password = Data['password']
       Email = Data['email']
       Usertype = Data['usertype']
       if Data:
        try:          
#inserting data into table (users_Register_Data)
         with connection.cursor() as cursor:
          Insert_Query= "INSERT INTO users_Register_Data (username, password, email, usertype) VALUES (%s, %s, %s, %s)"
          cursor.execute(Insert_Query, (Username, Password, Email, Usertype))
          connection.commit()
          Response_Data = {'status': 'success', 'message': 'registred successfully'}
          return jsonify(Response_Data)
        except Exception as e:
            print("exception occured in User_Register function and error is",e)
            Response_Data = {'status': 'failed', 'message': 'fields are not matched'}
        return jsonify(Response_Data)
 





def Specific_Info():
 with connection.cursor() as cursor:
    Current_Date = datetime.now().date()
    Current_Formate_Date= datetime.now().strftime('%Y-%m-%d')
    No_Of_Days=30
    New_Date_Str = Current_Date + timedelta(No_Of_Days)
    New_Date= New_Date_Str.strftime('%Y-%m-%d')

#selecting emp_name and dob from main table based on specific dates(1 month).........
    Emplyee_Complete_Details_Query='SELECT Employee_Name,Date_of_birth FROM Employee_complete_Details WHERE Date BETWEEN  %s AND %s'
    cursor.execute(Emplyee_Complete_Details_Query,(Current_Formate_Date, New_Date))
    Emp_Names_Dob_Info=cursor.fetchall()
    print("this is date",Emp_Names_Dob_Info)

#selecting emp_name and start & end dates from history table based on specific dates(1 month).........
    Leave_history_Query='SELECT Employee_Name,Start_date,End_date FROM Leave_history WHERE Start_date BETWEEN  %s AND %s'
    cursor.execute(Leave_history_Query,(Current_Formate_Date, New_Date))
    Leave_History_Info=cursor.fetchall()
    print("this is date",Leave_History_Info)

#selecting festname and holidaydate from holiday table based on specific dates(1 month).........
    Holiday_Query='SELECT Festival_name,Holiday_date FROM Holiday WHERE Holiday_date BETWEEN  %s AND %s'
    cursor.execute(Holiday_Query,(Current_Formate_Date, New_Date))
    Holiday_Info=cursor.fetchall()
    print("this is date",Holiday_Info)

#selecting announcement and announcement date from announcement table based on specific dates(1 month).........
    Announcement_Query='SELECT Announcement,Announcement_date FROM Announcement WHERE Announcement_date BETWEEN  %s AND %s'
    cursor.execute(Announcement_Query,(Current_Formate_Date, New_Date))
    Announcement_Info=cursor.fetchall()
    print("this is date",Announcement_Info)

#returning the specific details based on in between dates......
    return Emp_Names_Dob_Info,Leave_History_Info,Holiday_Info,Announcement_Info




        
    
# getting data and checking login ......
@app.route('/login', methods=['POST'])
def Login():
 if request.method == 'POST':
    Data = request.get_json()
    # Extract data from the request
    Email = Data['username']
    Password = Data['password']
    Usertype = Data['usertype']
    print(Email,Password,Usertype)        
    # Check if user exists in the database(users_Register_Data)
    with connection.cursor() as cursor:          
     query_To_Check = 'SELECT * FROM Employee_complete_Details WHERE Employee_email=%s AND usertype=%s  AND Password=%s'  
     cursor.execute(query_To_Check ,(Email,Usertype,Password))
     User_Info = cursor.fetchone()
     print("user data is",User_Info)
    #checking user information....
    try:
     Employee_Id=User_Info['Employee_id']
     Current_Date=datetime.now().strftime('%Y-%m-%d')
     print("currenyt_date",Current_Date)
     if User_Info['usertype']=='Employee' or User_Info['usertype']=='employee':
#check in attendance table by id and today date comparision.....
       with connection.cursor() as cursor: 
        # Current_Date=str(datetime.now().strftime('%Y-%m-%d'))
        Select_Query='select * FROM Employee_Attendance_Data WHERE Employee_id=%s AND Date=%s'
        cursor.execute(Select_Query,( Employee_Id,Current_Date))
        Exist_Data=cursor.fetchone()
        clock_in_time_str=""
        print("upto this1")
        try:
          clock_in_time_str=str(Exist_Data['clock_in_time'])
        #   clock_in_time_str = datetime.strptime(Exist_Data['clock_in_time'], "%H:%M:%S")
          print("upto this2")
        except:
            clock_in_time_str=""
        #  clock_in_time=datetime.strptime(datetime.strftime("%H:%M:%S"), "%H:%M:%S")
        # clock_in_time = datetime.strptime(clock_in_time_str, "%H:%M:%S")
        print(Exist_Data)
        #  if exist_data:
        #calling specific info function and extracting the information
        Info_From_Specific=Specific_Info()
        Employee_Names_Dob=Info_From_Specific[0]
        History_Info=Info_From_Specific[1]
        Holiday_info=Info_From_Specific[2]
        Announcement_Info=Info_From_Specific[3]
        print("complete_information",Info_From_Specific)
        print("login success")
        #sending required  info if login success................... 
        response_data = {'status': 'success', 'message': 'Login successful','username':User_Info['Employee_Name'],
                                    'user_id':User_Info['Employee_id'],'employee_email':Email,'user_type':Usertype,
                                    'clock_in_time':clock_in_time_str,
                                    "date_of_births":Employee_Names_Dob,"leaves_info":History_Info,"holiday_info":Holiday_info,
                                    "announcement_info":Announcement_Info}
        return jsonify(response_data)  
      #if request_type is employer then sending employee_count and employee_id and names             
     elif User_Info['usertype']=='Employer' or User_Info['usertype']=='employer':
        with connection.cursor() as cursor:           
           Count_Query='SELECT COUNT(Employee_id) FROM Employee_complete_Details'
           cursor.execute(Count_Query)
           Employee_Count=cursor.fetchall()
           Employee_Id_Name_Query="SELECT Employee_id,Employee_Name FROM Employee_complete_Details"
           cursor.execute(Employee_Id_Name_Query)  
           Employee_Id_Names = cursor.fetchall()
           #sending required  info if login success(employer)................... 
           Response_Data = {'status': 'success', 'message': 'Login successful','username':User_Info['Employee_Name'],
                            'user_id':User_Info['Employee_id'],'employee_email':Email,'user_type':Usertype,
                            'Total_employees':Employee_Count,'all_employee_name_id':Employee_Id_Names}
           return jsonify(Response_Data)
        #sending response as invalid if usertype not matches..........
     else:
        print("login failed")
        Response_Data = {'status': 'failed', 'message': 'invalid usertype'}
        return jsonify(Response_Data)
     #excepting occured if user enterd the wrong credentials.........
    except Exception as e:
       print("error is",e)
       Response_Data = {'status': 'failed', 'message': 'invalid user credentials'}
       return jsonify(Response_Data)





#not in use.................................................................
#getting data and validating email.....                      
@app.route('/validate_email', methods=['POST'])
def Validate_Email():
   if request.method=='POST':
    Data=request.get_json()
    Email=Data['email']
    print(Email)             
    # Execute the query to validate if email exists or not
    with connection.cursor() as cursor:
      Select_Query = 'SELECT Employee_email FROM Employee_complete_Details '
      cursor.execute(Select_Query)
      Existing_Emails = [row['email'] for row in cursor.fetchall()]
      print("exixting emails:",Existing_Emails)
# Check if the provided email exists in the list of existing emails          
      if Email in Existing_Emails:
        print("email exist")
        Response_Data = {'status': 'success', 'message': 'email exist'}
        return jsonify(Response_Data)
      else:
        print("email not exist")
        Response_Data = {'status': 'failed', 'message': 'email not exist'}
        return jsonify(Response_Data) 





#not in use.................................................................
#getting data and update password...            
@app.route('/update_password', methods=['POST'])
def Update_Password():
        if request.method == 'POST':
            Data = request.get_json()
            Email = Data['email']
            New_Password = Data['password']
            # Execute the query to update the user's password
            with connection.cursor() as cursor:
                 Select_Query = 'SELECT Employee_email FROM Employee_complete_Details '
                 cursor.execute(Select_Query)
                 Existing_Emails = [row['email'] for row in cursor.fetchall()]
                 if Email in Existing_Emails:
                   Update_Query = 'UPDATE Employee_complete_Details SET  Password = %s WHERE Employee_email = %s'
                   cursor.execute(Update_Query,(New_Password, Email))
                   print(Email,New_Password)
                   connection.commit()
                   Response_Data = {'status': 'success','message': ' email exist!!.. Password updated successfully'}
                   return jsonify(Response_Data)
                 else:
                     Response_Data={'status': 'failed and try again!', 'message': 'email not exist'}    
                     return jsonify(Response_Data)   






#checking clockin and clockout..................
@app.route('/clock_in',methods=['POST'])
def Clock_In_Out():
    if request.method=='POST':
    # Get the current date and time
        Current_Date_Formate = datetime.now().strftime('%Y-%m-%d')
        Current_Time = datetime.strptime(datetime.now().strftime("%H:%M:%S"), "%H:%M:%S")
        Clock_In_Time=Current_Time
        Data = request.get_json()
        print(Data)
    #extracting the emplyee data
    Employee_Id   = Data['employee_id']
    Employee_Name = Data['employee_name'] 
    Historic=       Data['historic']
    District=       Data['district']
    Clock_In_Location = Historic+ " "+District
    Clock_Out_Location=Clock_In_Location
    Button_Name=    Data['button_name']
    with connection.cursor() as cursor:
            Select_Query='select * FROM Employee_Attendance_Data WHERE Employee_id=%s AND Date=%s'
            cursor.execute(Select_Query,( Employee_Id,Current_Date_Formate))
            Exist_Data=cursor.fetchone()
            print("data is ",Exist_Data)
         
#checking button name................................................        
    if Button_Name =='clock_in':
    #inserting data into table Employee_Attendance_Data....       
      with connection.cursor() as cursor:
        if Exist_Data== None:
            Insert_Query= "INSERT INTO Employee_Attendance_Data (employee_id, employee_name, clock_in_time, clock_in_location, clock_out_time,Date) VALUES (%s, %s, %s, %s, %s,%s)"
            cursor.execute(Insert_Query,(Employee_Id, Employee_Name, Clock_In_Time, Clock_In_Location,None,Current_Date_Formate))
            connection.commit()
            Select_Query='SELECT Employee_Name,Employee_email from Employee_complete_Details WHERE Employee_id=%s'
            cursor.execute(Select_Query,(Employee_Id))
            Emp_Info=cursor.fetchone()
            Employee_Name=Emp_Info['Employee_Name']
            Employee_Email=Emp_Info['Employee_email']
            #sending response is clock_in success alongwith Current_Time,Employee_Email,Employee_Name
            Response_Data = {'status': 'success', 'message': 'clock_in success','current_time': Current_Time,'employee_email':Employee_Email,'empoyee_name':Employee_Name}
            Exist_Data=dict()
            #printing existing_data....
            print("another data",Exist_Data)
            return jsonify(Response_Data)  
        else:
            print("Already clockedin with this employee_id and date")
            Clock_In_Time=str(Exist_Data['clock_in_time'])  
            #if clockin fails.........
            #sending response is Already clockedin with this employee_id and date  alongwith Clock_In_Time 
            Response_Data = {'status': 'failed', 'message': 'Already clockedin with this employee_id and date','current_time':Clock_In_Time}
            return jsonify(Response_Data) 
        

#if buttonname is clockout updating the information..............................
    elif Button_Name =='clock_out':
        with connection.cursor() as cursor:
         #selecting employee_details from Employee_Attendance_Data table..
         Select_Query = "SELECT * FROM Employee_Attendance_Data WHERE employee_id = %s AND Date=%s"
         cursor.execute(Select_Query , (Employee_Id,Current_Date_Formate))  
         Employe_Row = cursor.fetchone()
        try:
            if Employe_Row:
                print("employee row value is",Employe_Row),
                Clock_In=(Employe_Row['clock_in_time'])
                Clock_Out_Time=datetime.strptime(datetime.now().strftime("%H:%M:%S"), "%H:%M:%S")
                #calculating average working hours......
                Avg_Working_Hrs=Clock_Out_Time - Clock_In
                print("clock_in and clock_out times:",Current_Date_Formate)
                print("clock out location name is",Clock_Out_Location)
                #updating the Employee_Attendance_Data when button_type is clock_out....
                with connection.cursor() as cursor:
                    Update_Query = "UPDATE Employee_Attendance_Data SET clock_out_time = %s, clock_out_location = %s ,Avg_working_hrs= %s WHERE employee_id = %s AND employee_name = %s AND Date= %s"
                    cursor.execute(Update_Query,(Clock_Out_Time, Clock_Out_Location,Avg_Working_Hrs, Employee_Id, Employee_Name,Current_Date_Formate))
                    connection.commit()
                    print("upto commit line")
                    Response_Data={'status': 'clock_out_success', 'message': 'clock out updated successfully','current_time':Avg_Working_Hrs}    
                    return jsonify(Response_Data)
            else:
                Response_Data={'status': 'failed and try again!', 'message': 'you don"t have clock_in information '}    
                return jsonify(Response_Data)
        except Exception as e:
                print("error in clock out",e)
    #sending response as invalid button name if button_name not matches
    else:
        Response_Data = {'status': 'failed', 'message': 'invalid button name'}
        return jsonify(Response_Data)






#getting request and sending employee_attendance data based on request_type(all_data/between_dates..)
@app.route('/get_attendance_data', methods=['POST'])
def Get_Specific_Attendance():
 if request.method=='POST':
    Data=request.get_json()
    print("the data from request is:..", Data)
    Employee_Id=Data['id']
    Employee_Name=Data['username']
    Start_Date=Data['start_date']
    End_Date=Data['end_date']
    try:      
      if Data['request_type'] == 'all_data':
        with connection.cursor() as cursor:
         #selecting employee information based on the employee_id and employee_name....
         Select_Query = 'SELECT * FROM Employee_Attendance_Data where employee_id=%s AND employee_name=%s'
         cursor.execute(Select_Query,(Employee_Id,Employee_Name))
         Employe_Info=cursor.fetchall()
        #converting clocks into required time formates...
         for i in range(len(Employe_Info)):
            Clock_In_Time=str(Employe_Info[i]['clock_in_time'])
            Clock_Out_Time=str(Employe_Info[0]['clock_out_time'])
            Avg_Working_Hrs=str(Employe_Info[0]['Avg_working_hrs'])
            Employe_Info[i]['clock_in_time']=Clock_In_Time
            Employe_Info[i]['clock_out_time']=Clock_Out_Time
            Employe_Info[i]['Avg_working_hrs']=Avg_Working_Hrs
         print("this is employee info",Employe_Info)
         try:
           if Employe_Info: 
              Response_Data={'status':'success','required_data':Employe_Info}
            #   response={'status':'your required data is sent successfully','clock_in_time':clock_in_time,'clock_out_time':clock_out_time,'clock_in_location':clock_in_location,'clock_out_location':clock_out_location,'Avg_working_hrs':Avg_working_hrs,'Date':Date}
              return jsonify(Response_Data)
           else:
             Response_Data={'status':'failed','message':'required data not exixt in table'}
             return jsonify(Response_Data)
         except:
             print("required data not exixt in table")
             Response_Data={'status':'failed','message':'required data not exixt in table'}
             return jsonify(Response_Data)
#sending data based on request_type(in between_dates..)
      elif Data['request_type']=='between_dates':
        try:
          with connection.cursor() as cursor:
            End_Date_Formate = datetime.strptime(End_Date, '%Y-%m-%d')
            Start_Date_Formate = datetime.strptime(Start_Date, '%Y-%m-%d')
            Select_Query = 'SELECT * FROM Employee_Attendance_Data where employee_id=%s AND employee_name=%s and Date BETWEEN %s and %s'
            cursor.execute(Select_Query,(Employee_Id,Employee_Name,Start_Date_Formate,End_Date_Formate))
            Employe_Info=cursor.fetchall()
            for i in range(len(Employe_Info)):
                Clock_In_Time=str(Employe_Info[i]['clock_in_time'])
                Clock_Out_Time=str(Employe_Info[0]['clock_out_time'])
                Avg_Working_Hrs=str(Employe_Info[0]['Avg_working_hrs'])
                Employe_Info[i]['clock_in_time']=Clock_In_Time
                Employe_Info[i]['clock_out_time']=Clock_Out_Time
                Employe_Info[i]['Avg_working_hrs']=Avg_Working_Hrs
          print("this is employee info",Employe_Info)
          Response_Data={'status':'success','message':'request_data','request_data':Employe_Info}
          return jsonify(Response_Data)  
        
        except Exception as e: 
            print("exception occured in et_Specific_Attendance function and error is",e)
            Response_Data = {'status': 'failed', 'message': 'fields are not matched'}
        return jsonify(Response_Data)                     
      else:
          Response_Data={'status':'failed','message':'exit'}
          return jsonify(Response_Data)
    except Exception as e: 
            print("exception occured in get_Specific_Attendance function and error is",e)
            Response_Data = {'status': 'failed', 'message': 'invalid_request_type'}
    return jsonify(Response_Data) 






#not in use...................................................................................
#getting request and send all employee_names and leave balance data from leave_balance table based on employee_id
@app.route('/send_all_employee', methods=['POST'])
def Fetch_All_Employee():
    if request.method == 'POST':
      Data = request.get_json()
      print(Data)
      try:
        if Data:
          with connection.cursor() as cursor:
            #selecting all employee_names from main table
            Select_Query1 = 'SELECT Employee_Name FROM Employee_complete_Details '
            #selecting specific employee_leaves_data  from leave_balance table...
            Select_Query2='SELECT Sick_Leave,Wedding_Leave ,Maternity_Leave ,Paternity_Leave ,No_of_leaves ,Taken_leaves ,Pending_leaves FROM Leave_balance WHERE Employee_id=%s'
            cursor.execute(Select_Query1)              
            Employee_Names=cursor.fetchall()
            print(Employee_Names)
            cursor.execute(Select_Query2,(Data['employee_id']))              
            Employee_Leave_Bal_Info=cursor.fetchall()
            print("employee leave balence data",Employee_Leave_Bal_Info)   
            #checking required employee_id  existance  and sending  Employee_Leave_Bal_Info and all employee_names... 
            response_data={'Employee_names': Employee_Names,'employee_leaves_data':Employee_Leave_Bal_Info}    
            return jsonify(response_data)
        else:
            print("employee not exist...")
            response_data = {'status': 'failed', 'message': 'user not exist....'}
            return jsonify(response_data)
      except Exception as e:
          print("exception occured in fetch_all_employee function and error is",e)






#request mail to teamlead and manager....
# @app.route('/accept/<request_id>/<Person_Name>',methods=['POST','GET'])
# def Accept_Request(request_id,person_name):
#   print("getting person name",request_id,person_name)
#   Request_Id=str(request_id)
#   with connection.cursor() as cursor:
#     Select_Query = 'SELECT * FROM Leave_Request WHERE Request_id=%s'
#     cursor.execute(Select_Query,(Request_Id))
#     Leave_Request_Info=cursor.fetchone()
#     print("mydata is",Leave_Request_Info)
# # Check if the provided email exists in the list of existing emails          
#     if Leave_Request_Info:  
#       try:
#     # Update the status of the request with ID request_id to 'Accepted'
#          with connection.cursor() as cursor:
#             Update_Query= "UPDATE  Leave_Request SET Status =%s WHERE Request_id =%s"
#             cursor.execute(Update_Query, ("accepted",Request_Id))
#             Selet_Query= "SELECT  Employee_complete_Details.Employee_email,Employee_complete_Details.Employee_Name FROM Employee_complete_Details JOIN Leave_Request ON Employee_complete_Details.Employee_id =Leave_Request.Employee_id WHERE Leave_Request.Request_id=%s"
#             cursor.execute(Selet_Query,(Request_Id))
#             Emp_Info = cursor.fetchone()
#             print("row is ",Emp_Info)
#             Emp_Name=Emp_Info['Employee_Name']
#             Selet_Query_Request='SELECT * FROM Leave_Request WHERE Request_id=%s'
#             cursor.execute(Selet_Query_Request,Request_Id)
#             Leave_Req_Info=cursor.fetchone()
#             print('--------------------',Leave_Req_Info)
#             Employee_Name=Leave_Req_Info['Employee_Name']
#             Start_Date=Leave_Req_Info['Start_date']
#             End_Date=Leave_Req_Info['End_date']
#             No_Of_Days=Leave_Req_Info['No_of_Days']
#             Employee_Id=Leave_Req_Info['Employee_id']
#             Leave_Type=Leave_Req_Info['Leave_Type']
#             Reason=Leave_Req_Info['Reason']
#             Team_Lead=Leave_Req_Info['Team_lead']
#             Team_Lead_Email=Leave_Req_Info['Team_lead_email']
#             Manager_Email=Leave_Req_Info['Manager_email']
#             Employee_Names=Leave_Req_Info['Add_Employees'].split(',')
#             print(Employee_Names[0])
#             print('------------',Leave_Req_Info['Add_Employees'])
#             if Emp_Info:
#              Employee_Email = Emp_Info["Employee_email"]
#              print("Employee email:", Employee_Email)
#              msg = Message(
#                         'Leave Request Status ',
#                         sender='enerziff@gmail.com',
#                         recipients=[Employee_Email]
#                         )
#              msg.body = "Your request Accepted"
#              mail.send(msg)
#              print("status mail sent")
                        
#              Request_Id=request_id
#             # Iterate over the list of employee names
#             for employee_name in Employee_Names:
#                with connection.cursor() as cursor:
#         # Query the database for the employee's email address based on the name
#                 Selet_Query = "SELECT Employee_email FROM Employee_complete_Details WHERE Employee_Name = %s"
#                 cursor.execute(Selet_Query, (employee_name))
#                 Employee_Row = cursor.fetchone()
#                 print("employee row values are",Employee_Row)
#                 if Employee_Row:
#                     Employee_Email = Employee_Row['Employee_email']
#                   # Send an email to the employee
#                     msg = Message('Leave Request Status', sender='enerziff@gmail.com', recipients=[Employee_Email])
#                     msg.body = f" {Emp_Name}, leave request has been accepted from {Start_Date} to {End_Date}and Number of Days are {No_Of_Days}."
#                     mail.send(msg)
#                 #getting data from leave balance and updating the data
#                 with connection.cursor() as cursor:
#                     print("employe_id",Employee_Id)
#                     print("Leave_type is:",Leave_Type)
#                     Selet_Query="SELECT Pending_leaves,Taken_leaves,{} FROM Leave_balance where Employee_id=%s"
#                     cursor.execute(Selet_Query.format(Leave_Type),(Employee_Id,))
#                     Leave_Info=cursor.fetchone()
#                     print("leaves value are",Leave_Info)
#                     Leave_List=list(Leave_Info.items())
#                     print("leaves balenace data",Leave_List)
#                     lastkey,lastvalue=Leave_List[-1]
#                     print("leave data:",Leave_Info,No_Of_Days)
#                     print(type(lastvalue),type(No_Of_Days))
#                     Leave_Type = lastvalue - No_Of_Days
#                     print("lastvalue value is",lastvalue,Leave_Type,Leave_Info['Taken_leaves'])
#                     Taken_Leaves=float(Leave_Info['Taken_leaves'])+No_Of_Days
#                     print("taken leaves are",Taken_Leaves,type(Leave_Info['Taken_leaves']))
#                     Pending_Leaves=Leave_Info['Pending_leaves'] - No_Of_Days
#                     print("all leaves are",Leave_Type,Taken_Leaves,Pending_Leaves)
#                  #updating leaves into leave_balance table........
#                 with connection.cursor() as cursor:
#                     print("update leave balence")
#                     Update_Query='UPDATE Leave_balance SET {}=%s,Taken_leaves=%s,Pending_leaves=%s WHERE Employee_id= %s'
#                     cursor.execute(Update_Query.format(Leave_Type),(Leave_Type,Taken_Leaves,Pending_Leaves,Employee_Id))
#                     connection.commit()
#                 #inserting data into leave_history...
#                 with connection.cursor() as cursor:
#                     Insert_Query= "INSERT INTO Leave_history (Request_id,Employee_id,Employee_Name,Start_date,End_date,No_of_Days,Leave_Type,Add_Employees,Reason,Status,Team_lead,Team_lead_email,Manager_email,Approved_By_Whom) VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#                     cursor.execute(Insert_Query, (Request_Id,Employee_Id,Emp_Name,Start_Date,End_Date,No_Of_Days,Leave_Type,'NONE',Reason,"Accepted",Team_Lead,Team_Lead_Email,Manager_Email,Person_Name))
#                     print("approved by...:",person_name)
#                     connection.commit() 
#                     #after inserting data into leave_history deleting data from Leave_request_table....
#                     print("upto delete")
#                     delete_Query= "DELETE FROM Leave_Request WHERE Request_id = %s"
#                     cursor.execute(delete_Query, (Request_Id,))
#                     connection.commit()
                    
#                     Select_Query='SELECT Applied_on,Reason,Start_date,End_date,Request_id,Employee_id,Employee_Name FROM Leave_Request WHERE Employee_id=%s'
#                     cursor.execute(Select_Query,(Employee_Id))
#                     Leave_Reuest_Data=cursor.fetchall()
#                     print('remaining_leaves :',Leave_Reuest_Data)
#                     Response_Data={'status':'status updated successfully','remaining_leaves':Leave_Reuest_Data}    
#                     return jsonify(Response_Data)
#       except Exception as e:
#         print("exception occuring",(e)) 
#       return 'Leave Request is accepted for '+Employee_Name+". Thank You!"
#     else:
#         print("Request Already Accepted by:",person_name)
#         return 'Request already accepted :'".Thank You!"
             

@app.route('/accept/<request_id>/<person_name>',methods=['POST','GET'])
def accept_request(request_id,person_name):
    print("getting person name",request_id,person_name)
    # request_id=request_id.strip()
    Request_id=str(request_id)
    with connection.cursor() as cursor:
        sql = 'SELECT * FROM Leave_Request WHERE Request_id=%s'
        cursor.execute(sql,(request_id))
        data1=cursor.fetchone()
        print("mydata is",data1)
    # Check if the provided email exists in the list of existing emails          
        if data1:  
            try:
            # Update the status of the request with ID request_id to 'Accepted'
                with connection.cursor() as cursor:
                    sql_query= "UPDATE  Leave_Request SET Status =%s WHERE Request_id =%s"
                    cursor.execute(sql_query, ("accepted",request_id))
                    sql= "SELECT  Employee_complete_Details.Employee_email,Employee_complete_Details.Employee_Name FROM Employee_complete_Details JOIN Leave_Request ON Employee_complete_Details.Employee_id =Leave_Request.Employee_id WHERE Leave_Request.Request_id=%s"
                    cursor.execute(sql,(request_id))
                    row = cursor.fetchone()
                    print("row is ",row)
                    emp_name=row['Employee_Name']
                    sql_query='SELECT * FROM Leave_Request WHERE Request_id=%s'
                    cursor.execute(sql_query,request_id)
                    add_row=cursor.fetchone()
                    print('--------------------',add_row)
                    Employee_Name=add_row['Employee_Name']
                    start_date=add_row['Start_date']
                    end_date=add_row['End_date']
                    no_of_days=add_row['No_of_Days']
                    employee_id=add_row['Employee_id']
                    Leave_Type=add_row['Leave_Type']
                    Reason=add_row['Reason']
                    Team_lead=add_row['Team_lead']
                    Team_lead_email=add_row['Team_lead_email']
                    Manager_email=add_row['Manager_email']
                    employee_names=add_row['Add_Employees'].split(',')
                    print(employee_names[0])
                    print('------------',add_row['Add_Employees'])
                    if row:
                        employee_email = row["Employee_email"]
                        print("Employee email:", employee_email)
                        msg = Message(
                                    'Leave Request Status ',
                                    sender='enerziff@gmail.com',
                                    recipients=[employee_email]
                                    )
                        msg.body = "Your request Accepted"
                        mail.send(msg)
                        print("status mail sent")
                                    
                        Request_id=request_id
                        # Iterate over the list of employee names
                        for employee_name in employee_names:
                            with connection.cursor() as cursor:
                # Query the database for the employee's email address based on the name

                                sql_query = "SELECT Employee_email FROM Employee_complete_Details WHERE Employee_Name = %s"
                                cursor.execute(sql_query, (employee_name))
                                employee_row = cursor.fetchone()
                                print("employee row values are",employee_row)

                                if employee_row:
                                    employee_email = employee_row['Employee_email']

                # Send an email to the employee
                                    msg = Message('Leave Request Status', sender='enerziff@gmail.com', recipients=[employee_email])
                                    msg.body = f" {emp_name}, leave request has been accepted from {start_date} to {end_date}and Number of Days are {no_of_days}."
                                    mail.send(msg)

                                    #getting data from leave balance and updating the data
                        with connection.cursor() as cursor:
                                    print("employe_id",employee_id)
                                    print("Leave_type is:",Leave_Type)
                                    select_query="SELECT Pending_leaves,Taken_leaves,{} FROM Leave_balance where Employee_id=%s"
                                    cursor.execute(select_query.format(Leave_Type),(employee_id,))
                                    leave=cursor.fetchone()
                                    print("leaves value are",leave)
                                    leave_list=list(leave.items())
                                    print("leaves balenace data",leave_list,leave_list)
                                    lastkey,lastvalue=leave_list[-1]
                                    print("leave data:",leave,no_of_days)
                                    print(type(lastvalue),type(no_of_days))
                                    Leave_type = lastvalue - no_of_days
                                    print("lastvalue value is",lastvalue,Leave_type,leave['Taken_leaves'])
                                    Taken_leaves=float(leave['Taken_leaves'])+no_of_days
                                    print("taken leaves are",Taken_leaves,type(leave['Taken_leaves']))
                                    Pending_leaves=leave['Pending_leaves'] - no_of_days
                                    print("all leaves are",Leave_type,Taken_leaves,Pending_leaves)
                                    #updating leaves into leave_balance table........
                        with connection.cursor() as cursor:
                                    print("update leave balence")
                                    sql='UPDATE Leave_balance SET {}=%s,Taken_leaves=%s,Pending_leaves=%s WHERE Employee_id= %s'
                                    cursor.execute(sql.format(Leave_Type),(Leave_type,Taken_leaves,Pending_leaves,employee_id))
                                    connection.commit()


                                    #inserting data into leave_history...
                        with connection.cursor() as cursor:
                                    insert_into_leave_request= "INSERT INTO Leave_history (Request_id,Employee_id,Employee_Name,Start_date,End_date,No_of_Days,Leave_Type,Add_Employees,Reason,Status,Team_lead,Team_lead_email,Manager_email,Approved_By_Whom) VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                                    cursor.execute(insert_into_leave_request, (Request_id,employee_id,emp_name,start_date,end_date,no_of_days,Leave_Type,'NONE',Reason,"Accepted",Team_lead,Team_lead_email,Manager_email,person_name))
                                    print("approved by...:",person_name)
                                    connection.commit() 
                   

                            #after inserting data into leave_history deleting data from Leave_request_table....
                                    print("upto delete")
                                    delete_leave_request_query = "DELETE FROM Leave_Request WHERE Request_id = %s"
                                    cursor.execute(delete_leave_request_query, (request_id,))
                                    connection.commit()
                                    
                                    sql='SELECT Applied_on,Reason,Start_date,End_date,Request_id,Employee_id,Employee_Name FROM Leave_Request WHERE Employee_id=%s'
                                    cursor.execute(sql,(employee_id))
                                    data_in_lr=cursor.fetchall()
                                    print('remaining_leaves :',data_in_lr)
                                    response_data={'status':'status updated successfully','remaining_leaves':data_in_lr}    
                                    return jsonify(response_data)
            except Exception as e:
                print("exception occuring",(e)) 
            return 'Leave Request is accepted for '+Employee_Name+". Thank You!"
        else:
             print("Request Already Accepted by:",person_name)
             return 'Request already accepted :'".Thank You!"
             



#rejection mail...
@app.route('/reject/<request_id>/<person_name>',methods=['POST','GET'])
def reject_request(request_id,person_name):
    print("rejected person_name:",request_id,person_name)
# Update the status of the request with ID request_id to 'Rejected'
    with connection.cursor() as cursor:
        print("up to this1")
        sql_query='SELECT * FROM Leave_Request WHERE Request_id=%s'
        cursor.execute(sql_query,request_id)
        add_row=cursor.fetchone()
        Employee_Name=add_row['Employee_Name']
        start_date=add_row['Start_date']
        end_date=add_row['End_date']
        no_of_days=add_row['No_of_Days']
        employee_id=add_row['Employee_id']
        Leave_Type=add_row['Leave_Type']
        Reason=add_row['Reason']
        Team_lead=add_row['Team_lead']
        Team_lead_email=add_row['Team_lead_email']
        Manager_email=add_row['Manager_email']
        employee_names=add_row['Add_Employees'].split(',')


        insert_into_leave_history= "INSERT INTO Leave_history (Request_id,Employee_id,Employee_Name,Start_date,End_date,No_of_Days,Leave_Type,Add_Employees,Reason,Status,Team_lead,Team_lead_email,Manager_email,Approved_By_Whom) VALUES (%s,%s,%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(insert_into_leave_history, (request_id,employee_id, Employee_Name,start_date,end_date,no_of_days,Leave_Type,employee_names,Reason,"Rejected",Team_lead,Team_lead_email,Manager_email,person_name))
        print("Rejected by...:",person_name)


        sql= "SELECT  Employee_complete_Details.Employee_email FROM Employee_complete_Details JOIN Leave_Request ON Employee_complete_Details.Employee_id=Leave_Request.Employee_id WHERE Leave_Request.Request_id=%s"
        cursor.execute(sql,(request_id))
        row = cursor.fetchone()


        if row:
            employee_email = row["Employee_email"]
            print("Employee email:", employee_email)
            msg = Message(
                        'Leave Request Status ',
                            sender='enerziff@gmail.com',
                            recipients=[employee_email]
                        )
            msg.body = "Your request Rejected"
            mail.send(msg)
            print("rejected status mail sent")
            delete_leave_request_query = "DELETE FROM Leave_Request WHERE Request_id = %s"
            cursor.execute(delete_leave_request_query, (request_id,))
            connection.commit()   
            sql='SELECT Applied_on,Reason,Start_date,End_date,Request_id,Employee_id,Employee_Name FROM Leave_Request WHERE Employee_id=%s'
            cursor.execute(sql,(employee_id))
            data_in_lr=cursor.fetchall()
            print('remaining_leaves :',data_in_lr)
            response_data={'status':'status updated successfully','remaining_leaves':data_in_lr}    
            return jsonify(response_data)                                                
    return 'You rejected the request'






#generating random request_id..
def generate_id():
    return ''.join([str(random.randint(0, 9)) for _ in range(4)]) 

#getting leave request data..........           
@app.route('/leave_request_data', methods=['POST'])
def leave():
        if request.method == 'POST':
            data = request.get_json()
            print(data)
            employee_id=data['id']
            employee_name=data['employee_name']
            Start_date=data['from_date']
            End_date=data['to_date']
            Leave_Type=data['leave_type']
            Reason=data['reason']
            # Add_employees=['Sudha',]         
            request_id=generate_id()
            Request_id=str(request_id)
            print(data)
            request_type=data['request_type']
            #extracting employee_names from add_employees...
            # employe_names=""
            # for i in range(len(Add_employees)):
            #      employe_names=Add_employees[i]+","+employe_names
            #      print(type(employe_names))
            
            with connection.cursor() as cursor:                       
                    select_employe = "SELECT Team_lead_email,Manager_email,Team_lead ,Manager_name FROM  Employee_complete_Details  WHERE Employee_id = %s AND Employee_Name = %s "
                    cursor.execute(select_employe , (employee_id, employee_name))  
                    employe_row = cursor.fetchone()
                    print("employee data",employe_row)
                    Team_lead_email=employe_row['Team_lead_email']
                    Manager_email=employe_row['Manager_email']
                    Team_lead=employe_row['Team_lead']
                    Manager_name=employe_row['Manager_name']
                    print("team lead emails",Team_lead_email,Manager_email) 
                    End_date = datetime.strptime(End_date, '%Y-%m-%d')
                    Start_date = datetime.strptime(Start_date, '%Y-%m-%d')
                    No_of_Days=(End_date - Start_date).days
                    current_date= datetime.now().strftime('%Y-%m-%d')
                    applied_on=datetime.now().strftime('%Y-%m-%d')
            if request_type=="insert":
                  print("this is insert function",Start_date,End_date)
                  print("applied_on...",applied_on)
                  with connection.cursor() as cursor:
                    print("up to this1")
                    insert_into_leave_request= "INSERT INTO Leave_Request (Request_id,Employee_id,Employee_Name,Start_date,End_date,No_of_Days,Leave_Type,Add_Employees,Reason,Status,Team_lead ,Team_lead_email,Manager_email,Applied_on) VALUES (%s,%s,%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(insert_into_leave_request, (Request_id,employee_id,employee_name,Start_date,End_date,No_of_Days,Leave_Type,'NONE',Reason,"Waiting",Team_lead,Team_lead_email,Manager_email,applied_on))
                    print("up to this2")

                    connection.commit()
                    print("upto this 3")       
                    # response={'status':"success",'message':"leave_request data inserted successfully..."}
                    # return jsonify(response)
                    html = render_template_string(
                                                  """
                                                  <p>Your request_id: <strong>{{ Request_id }}</strong></p>
                                                  <p>Team Lead: <strong>{{ person_name }}</strong></p>
                                                  
                                                  <p>
                                                  <a href="{{ url_for('accept_request', request_id=Request_id,person_name=person_name, _external=True) }}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px;">Accept</a>
                                                  <a href="{{ url_for('reject_request', request_id=Request_id,person_name=person_name,  _external=True) }}" style="background-color: #f44336; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px;">Reject</a>
                                                  </p>

                                                  """,
                                                 Request_id=str(request_id),
                                                 person_name=Team_lead,
                                                 
                                                 )
                    msg_team_lead = Message(
                                    'Leave Request',
                    sender='enerziff@gmail.com',
                    recipients=[Team_lead_email]
                    )
                    msg_team_lead.body = "You have got a leave request from " + employee_name + " Leave dates are from " +str(Start_date) + "to" +str(End_date)+ "Total_no_of_days are.." +str(No_of_Days)+ " You can accept/reject the request by using your payroll management account."
                    msg_team_lead.html = html
                    mail.send(msg_team_lead)
                    print("mail sent to team_lead")
          


                    # Send email to manager
                    html = render_template_string(
                                                  """
                                                  <p>Your request_id: <strong>{{ Request_id }}</strong></p>
                                                  <p>Manager: <strong>{{person_name}}</strong></p>
                                                  <p>
                                                  <a href="{{ url_for('accept_request', request_id=Request_id,person_name=person_name,  _external=True) }}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px;">Accept</a>
                                                  <a href="{{ url_for('reject_request', request_id=Request_id,person_name=person_name,  _external=True) }}" style="background-color: #f44336; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px;">Reject</a>
                                                  </p>

                                                  """,
                                                 Request_id=str(request_id),
                                                 person_name=Manager_name,
                                                 
                                                 )
                    msg_manager = Message(
                    'Leave Request',
                    sender='enerziff@gmail.com',
                    recipients=[Manager_email]
                    )
                    msg_manager.body = "You have got a leave request from " + employee_name + " Leave dates are from " +str(Start_date) + "to" +str(End_date)+ "Total_no_of_days are.." +str(No_of_Days)+ " You can accept/reject the request by using your payroll management account."
                    msg_manager.html = html
                    mail.send(msg_manager)
                    print("mail sent to manager")
                    current_date= datetime.now().strftime('%Y-%m-%d')
                  response={'status':"success",'From_date':Start_date,'To_date':End_date,'Applied_on':current_date}
                  return jsonify(response)


            elif request_type == "update":
                        print("this is update function", Start_date, End_date)
                        with connection.cursor() as cursor:
                          sql='SELECT Request_id FROM Leave_Request WHERE Employee_id=%s'
                          cursor.execute(sql,(employee_id))
                          query=cursor.fetchone()
                          request_id=query['Request_id']
                          update_sql = "UPDATE Leave_Request SET  Start_date=%s, End_date=%s, No_of_Days=%s, Leave_Type=%s, Add_Employees=%s, Reason=%s  WHERE Employee_id=%s"
                          cursor.execute(update_sql, ( Start_date, End_date, No_of_Days, Leave_Type,'NONE ', Reason, employee_id))
                          connection.commit()
                          print("updated the leave request data")
                        #   response = {'status': "success", 'message': "leave_request data updated successfully..."}
                        #   return jsonify(response)
                          html = render_template_string(
                                                  """
                                                  <p>Your request_id: <strong>{{ Request_id }}</strong></p>
                                                  <p>Team Lead: <strong>{{ person_name }}</strong></p>
                                                  
                                                  <p>
                                                  <a href="{{ url_for('accept_request', request_id=Request_id,person_name=person_name, _external=True) }}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px;">Accept</a>
                                                  <a href="{{ url_for('reject_request', request_id=Request_id,person_name=person_name,  _external=True) }}" style="background-color: #f44336; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px;">Reject</a>
                                                  </p>

                                                  """,
                                                 Request_id=str(request_id),
                                                 person_name=Team_lead,
                                                 
                                                 )
                          msg_team_lead = Message(
                                        'Leave Request',
                          sender='enerziff@gmail.com',
                          recipients=[Team_lead_email]
                           )
                          msg_team_lead.body = "You have got a leave request from " + employee_name + " Leave dates are from " +str(Start_date) + "to" +str(End_date)+ "Total_no_of_days are.." +str(No_of_Days)+ " You can accept/reject the request by using your payroll management account."
                          msg_team_lead.html = html
                          mail.send(msg_team_lead)
                          print("mail sent to team_lead")



                    # Send email to manager
                          html = render_template_string(
                                                  """
                                                  <p>Your request_id: <strong>{{ Request_id }}</strong></p>
                                                  <p>Manager: <strong>{{person_name}}</strong></p>
                                                  <p>
                                                  <a href="{{ url_for('accept_request', request_id=Request_id,person_name=person_name,  _external=True) }}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px;">Accept</a>
                                                  <a href="{{ url_for('reject_request', request_id=Request_id,person_name=person_name,  _external=True) }}" style="background-color: #f44336; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px;">Reject</a>
                                                  </p>

                                                  """,
                                                 Request_id=str(request_id),
                                                 person_name=Manager_name,
                                                 
                                                 )
                          msg_manager = Message(
                            'Leave Request',
                            sender='enerziff@gmail.com',
                            recipients=[Manager_email]
                            )
                          msg_manager.body = "You have got a leave request from " + employee_name + " Leave dates are from " +str(Start_date) + "to" +str(End_date)+ "Total_no_of_days are.." +str(No_of_Days)+ " You can accept/reject the request by using your payroll management account."
                          msg_manager.html = html
                          mail.send(msg_manager)
                          print("mail sent to manager")

                        response={'status':"success",'From_date':Start_date,'To_date':End_date,'Applied_on':applied_on}
                        return jsonify(response)



            else:
              print("request type is invalid.....")






#getting daily status update data and insert into daily status update table
@app.route('/status_update_data', methods=['POST'])
def Insert_Into_Status():
        if request.method == 'POST':
            Data = request.get_json()
            print(Data)
            Employee_Email=Data['email']
            Completed_Task=Data['completed']
            Issues=Data['issues']
            Feature_Targets=Data['upcoming']
            Status_Update=Data['statusUpdate']
            Employee_Name=Data['employeename']
            Employee_Id=Data['employeeid']   
            current_date_formatted = datetime.now().strftime('%Y-%m-%d')
            current_time = datetime.strptime(datetime.now().strftime("%H:%M:%S"), "%H:%M:%S")
        with connection.cursor() as cursor:
           print("employee_name and email:",Employee_Name,Employee_Email)
           #INSERT DATA INTO DAILY STATUS UPDATE DATA TABLE...
           Select_Query = "INSERT INTO Daily_Status_Update (Employee_id, Employee_Name, Employee_Email,Date,Time,Status_Update,Issues,Completed_Task,Feature_Targets) VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s)"
           cursor.execute(Select_Query, (Employee_Id, Employee_Name,  Employee_Email,current_date_formatted ,current_time,Status_Update,Issues, Completed_Task,Feature_Targets))
           connection.commit()
           #SENDING RESPONSE..........
           Response_Data = {'status': 'success', 'message': 'employee registred successfully'}
        return jsonify(Response_Data)   
    




#updating status update data table..............
@app.route('/specific_status_update', methods=['POST'])
def Update_specific_status():
        if request.method == 'POST':
            Data = request.get_json()
            print("data for updating the status_table",Data)
            # Employee_Email=data['email']
            Completed_Task=Data['completed']
            Issues=Data['issues']
            Feature_Targets=Data['targets']
            Status_Update=Data['status']
            # Employee_Name=data['employeename']
            Employee_Id=Data['id']
            Date=Data['date']    
        with connection.cursor() as cursor: 
            Current_Date = datetime.strptime(Date, '%Y-%m-%d') 
            #updating the daily _status_data table....  
            Select_Query = "UPDATE Daily_Status_Update SET Status_Update=%s,Issues=%s,Completed_Task=%s,Feature_Targets=%s WHERE Employee_id=%s AND Date=%s"
            cursor.execute(Select_Query, (Status_Update,Issues,Completed_Task,Feature_Targets,Employee_Id,Current_Date))
            connection.commit()
            #sending response......
            Response_Data = {'status': 'success', 'message': 'employee registred successfully'}
        return jsonify(Response_Data)   






# sending emmployee daily status update details based on employee_name ,employee_id and specific date...
@app.route('/get_status_update_data', methods=['POST'])
def Fetch_Specific_Status():
        if request.method == 'POST':
            Data = request.get_json()
            print(Data)
            # Employee_Name=data['employeename']
            Employee_Id=Data['employeeid']
            # date=data['date']
            Request_Type=Data['request_type']
            Start_Date=Data['start_date']
            End_Date=Data['end_date']
            print("date type:",type(Start_Date))
            print("what is start date",Start_Date)
            Start_date_Formatted = datetime.strptime(Start_Date, '%Y-%m-%d')
            if(Request_Type=='single_date'):
                #selecting specific employee_data from daily_status_update table based on  employe_name id and specific date..   
               with connection.cursor() as cursor:                       
                 Select_Query = "SELECT * FROM Daily_Status_Update WHERE Employee_id = %s  AND Date= %s "
                 cursor.execute(Select_Query , (Employee_Id,  Start_date_Formatted))  
                 Employe_Row = cursor.fetchone()
                 Time=str(Employe_Row['Time'])
                 Employe_Row['Time']=Time
                 print("employee data",Employe_Row)               
                 print(Time)
                 Response_Data={"status":"success","status_update":Employe_Row}
                 return jsonify(Response_Data)
               #checking request_type..........
            elif(Request_Type=='in_between_dates'):
                 with connection.cursor() as cursor:          
                      Start_Date = datetime.strptime(str(Start_Date),'%Y-%m-%d').date()
                      End_Date_Formatted=datetime.strptime(str(End_Date),'%Y-%m-%d').date()
                      Select_Query = 'SELECT * FROM Daily_Status_Update where Employee_id=%s  and Date BETWEEN %s and %s'
                      cursor.execute(Select_Query,(Employee_Id,Start_Date,End_Date_Formatted))
                      Daily_Status_Info=cursor.fetchall()
                      #converting time into str..................
                      for i in range(len(Daily_Status_Info)):
                            Time=str(Daily_Status_Info[i]['Time'])                         
                            Daily_Status_Info[i]['Time']=Time
                      print("Daily_status_in_between_dates:",Daily_Status_Info)
                      #sending response daily_status update information based on thwe ibn between dates..................
                      Response_Data={'status':'success','message':'Daily_status_info_in_between_dates','request_data':Daily_Status_Info}
                      print("daily status _data sent successfully:")
                      return jsonify(Response_Data) 
            else:
                 Response_Data={'status':'failed','message':'invalid request_type'}
                 return jsonify(Response_Data) 
        
        





#getting request (id and name) and sending the specific data based on the request from leave_request_table  
@app.route('/get_leave', methods=['POST'])
def Fetch_Specific_Leave():
        if request.method == 'POST':
            Data = request.get_json()
            print(Data)
            Employee_Name=Data['username']
            Employee_Id=Data['id ']          
        with connection.cursor() as cursor:  
            #selecting leave_request_data based on employee id and name...                     
            Select_Query = "SELECT * FROM Leave_Request WHERE Employee_Name = %s AND Employee_id = %s "
            cursor.execute(Select_Query , (Employee_Name, Employee_Id,))  
            Employe_Row = cursor.fetchone()
            if Employe_Row:
                print("employee data",Employe_Row)  
                Start_Date=Employe_Row['Start_date']
                Start_Date_Formatted = datetime.strptime(str(Start_Date),'%Y-%m-%d').date() 
                print(Start_Date_Formatted) 
                End_Date=Employe_Row['End_date']
                End_Date_Formatted = datetime.strptime(str(End_Date),'%Y-%m-%d').date()
                #sending response start and end dates along with leave_request_data......
                Response_Data={'status':"success",'from_date':Start_Date_Formatted,'To_date': End_Date_Formatted,'Leave_type':Employe_Row['Leave_Type'],'Add_Employees':Employe_Row['Add_Employees'],'reason':Employe_Row['Reason']}
                print("data sent successfully")
                return jsonify(Response_Data)
            else:
                 Response_Data={'status':'failed','message':'employee_id or employee_name should not matching'}
                 return jsonify(Response_Data)
            






#getting request and sending employee_name and DOB based on  between dates.... and sending data from leave_history....
@app.route('/date_of_birth', methods=['POST'])
def Fetch_Specific_Dates_Info():
    if request.method == 'POST':
        Data = request.get_json()
        print(Data)
        with connection.cursor() as cursor:   
            Date = datetime.now().date()
            Date_Formatted= datetime.now().strftime('%Y-%m-%d')
            No_Of_Days=30
            Month_Added_Date = Date + timedelta(days=No_Of_Days)
            New_Date_str = Month_Added_Date.strftime('%Y-%m-%d')
            # Date=Date+no_of_days
            print("today date is:",New_Date_str)
            #selecting specific info based on present and after one month dates....                 
            Select_Query="SELECT Date_of_birth,Employee_Name FROM Employee_complete_Details WHERE Date BETWEEN %s AND %s"
            cursor.execute(Select_Query,(Date_Formatted,New_Date_str))  
            Required_Row = cursor.fetchall()
            print("data is:",Required_Row) 
            Select_Query="SELECT Employee_Name , Start_date, End_date , No_of_Days,DATE_FORMAT(Start_date, '%Y-%m-%d') AS formatted_date FROM Leave_history WHERE Start_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 1 MONTH)"
            cursor.execute(Select_Query)
            Required_Info=cursor.fetchall()
            print("info is:",Required_Info)
            #selecting leave request information.......
            Select_Query='SELECT * FROM Leave_Request'
            cursor.execute(Select_Query)
            Leave_Request_Data=cursor.fetchall()
            #selecting all employee count..... from main table
            Select_Query='SELECT COUNT(Employee_id) FROM Employee_complete_Details'
            cursor.execute(Select_Query)
            Employee_Count=cursor.fetchall()
            #selecting all employee count..... from attendance table
            Date= datetime.now().strftime('%Y-%m-%d')
            Select_Query='SELECT COUNT(Employee_id) FROM Employee_Attendance_Data WHERE DATE=%s'
            cursor.execute(Select_Query,Date)
            Clock_In_Count=cursor.fetchall()
            #selecting all employee data..... from attendance table
            Select_Query='SELECT * FROM Employee_Attendance_Data WHERE DATE=%s'
            cursor.execute(Select_Query,Date)
            Clock_In_Info=cursor.fetchall() 
            for i in range(len(Clock_In_Info)):
                            clock_in_time=str(Clock_In_Info[i]['clock_in_time'])
                            clock_out_time=str(Clock_In_Info[0]['clock_out_time'])
                            Avg_working_hrs=str(Clock_In_Info[0]['Avg_working_hrs'])
                            Clock_In_Info[i]['clock_in_time']=clock_in_time
                            Clock_In_Info[i]['clock_out_time']=clock_out_time
                            Clock_In_Info[i]['Avg_working_hrs']=Avg_working_hrs
            #selecting all data..... from Announcement table
            Select_Query='SELECT * FROM Announcement'
            cursor.execute(Select_Query)
            Announcement_Info=cursor.fetchall()
            #selecting all data..... from Holiday table
            Select_Query='SELECT * FROM Holiday'
            cursor.execute(Select_Query)
            Holiday_Info=cursor.fetchall()
            #sending response DOB and employenames,Leave_data,leave_request_data,total_no_of_employees,tdy_clk_in_count,clock_in_info,Announcement_data,Holiday_data
            Response_Data={'status':'success','DOB and employenames':Required_Row,'Leave_data':Required_Info,'leave_request_data':Leave_Request_Data,
                           'total_no_of_employees':Employee_Count,'tdy_clk_in_count':Clock_In_Count,'clock_in_info': Clock_In_Info,
                           'Announcement_data':Announcement_Info,'Holiday_data':Holiday_Info}
            print("requested data sent successfully:")
            return jsonify(Response_Data) 
        



#INSERTING DATA INTO HOLIDAY TABLE..................
@app.route('/holiday', methods=['POST'])
def Insert_Holiday():
    if request.method == 'POST':
        Data = request.get_json()
        print(Data)
        Holiday_Date=Data['date']
        Fest_Name=Data['festival_name']
        print("data is",Data)
        Date= datetime.strptime(Holiday_Date,'%Y-%m-%d') 
        print("date is",Date)
        try:
          with connection.cursor() as cursor:
            Select_Query='INSERT INTO Holiday(Festival_name,Holiday_date) VALUES(%s,%s)'
            cursor.execute(Select_Query,(Fest_Name,Date))
            connection.commit()
            Response_Data={'status':'success',"message":'data inserted into holiday table successfully..'}
            return jsonify(Response_Data) 
        except Exception as e:
            print("exception occerd in Insert_Holiday function n error is ",e)
        



#INSERTING DATA INTO Annoouncement TABLE..................
@app.route('/announcement', methods=['POST'])
def Insert_Announcement():
     if request.method=='POST':
          Data=request.get_json()
          print("the data is..... ",Data)
          Employee_Id=Data['Employee_id']
          Employee_Name=Data['Employee_Name']
          Announcement=Data['Announcement']
        #inserting_date=data['inserting_date']
          Announcement_Date=Data['Announcement_date']
          inserting_date=datetime.now().strftime('%Y-%m-%d')
          with connection.cursor() as cursor:
            Insert_Query='INSERT INTO Announcement (Employee_id,Employee_Name,Announcement,Inserting_date, Announcement_date) VALUES(%s,%s,%s,%s,%s)'
            cursor.execute(Insert_Query,(Employee_Id,Employee_Name,Announcement,inserting_date,Announcement_Date))
            connection.commit()
            Response_Data={'status':'success',"message":'Announcement data inserted into Announcement_table successfully..'}
            return jsonify(Response_Data)






#daily_status_update_details_basedon_specific_dates...............
@app.route('/status_data', methods=['POST'])
def status_details_specific():
     if request.method=='POST':
          Data=request.get_json()
          Start_Date=Data['start_date']
          End_Date=Data['end_date']
          print(Data)
          #converting dates into formatted dates......
          Start_Date_Formatted= datetime.strptime(Start_Date, '%Y-%m-%d') 
          End_Date_Formatted= datetime.strptime(End_Date, '%Y-%m-%d')
          with connection.cursor() as cursor:
               Select_Query='SELECT * FROM Daily_Status_Update WHERE Date BETWEEN %s and %s '
               cursor.execute(Select_Query,(Start_Date_Formatted,End_Date_Formatted))
               Daily_Status_Info=cursor.fetchall()
               Response_Data={'status':'success',"daily_status_data":Daily_Status_Info}
               return jsonify(Response_Data)



#sending employee_attendance_details_basedon_specific_dates.....
@app.route('/attendance_data', methods=['POST'])
def Fetch_Attendance_Specific_Dates():
     if request.method=='POST':
          Data=request.get_json()
          Start_Date=Data['start_date']
          End_Date=Data['end_date']
          Start_Date= datetime.strptime(Start_Date, '%Y-%m-%d') 
          End_Date= datetime.strptime(End_Date, '%Y-%m-%d')
          with connection.cursor() as cursor:
               Select_Query='SELECT * FROM Employee_Attendance_Data WHERE Date BETWEEN %s and %s '
               cursor.execute(Select_Query,(Start_Date,End_Date))
               Attendance_Info=cursor.fetchall()
               for i in range(len(Attendance_Info)):
                            clock_in_time=str(Attendance_Info[i]['clock_in_time'])
                            clock_out_time=str(Attendance_Info[0]['clock_out_time'])
                            Avg_working_hrs=str(Attendance_Info[0]['Avg_working_hrs'])
                            Attendance_Info[i]['clock_in_time']=clock_in_time
                            Attendance_Info[i]['clock_out_time']=clock_out_time
                            Attendance_Info[i]['Avg_working_hrs']=Avg_working_hrs              
               Response_Data={'status':'success',"Attendance_Info":Attendance_Info}
               return jsonify(Response_Data)




#insering data into leave_balance after calculating the all leaves......
@app.route('/leave_balance', methods=['POST'])
def Insert_Leave_Balance():
     if request.method=='POST':
       try:
          Data=request.get_json()
          print("data is...",Data)
          Employee_Id=Data['employee_id']
          Employee_Name=Data['employee_name']
          Sick_Leave=Data['sick_leave']
          Wedding_Leave=Data['wedding_leave']
          Maternity_Leave=Data['maternity_leave']
          Paternity_Leave=Data['paternity_leave']
          #calculating leaves..........
          No_Of_Days=3.0
          Taken_Leaves=0.0
          Pending_Leaves=0.0
          Sick_Leave=float(Sick_Leave)
          Wedding_Leave=float(Wedding_Leave)
          Maternity_Leave=float(Maternity_Leave)
          Paternity_Leave=float(Paternity_Leave)
          print("the type...",type(Sick_Leave))
          No_of_Leaves=float(Sick_Leave)+float(Wedding_Leave)+float(Maternity_Leave)+float(Paternity_Leave)
          print("sick_leave_type",type(Sick_Leave))
          Taken_Leaves=float(Taken_Leaves) + No_Of_Days
          Pending_Leaves=float(Pending_Leaves) - No_Of_Days
          print("type is",type(Pending_Leaves))
          No_of_Leaves=str(No_of_Leaves)
          Taken_Leaves=str(Taken_Leaves)
          Pending_Leaves=str(Pending_Leaves)
          with connection.cursor() as cursor:
            Select_Query='SELECT Employee_email,Gender FROM Employee_complete_Details WHERE Employee_id =%s'
            cursor.execute(Select_Query,( Employee_Id))
            Emp_Info=cursor.fetchone()
            employee_email=Emp_Info['Employee_email']
            gender=Emp_Info['Gender']
            Insert_Query='INSERT INTO Leave_balance(Employee_id,Employee_Name,Employee_email,Gender, Sick_Leave, Wedding_Leave, Maternity_Leave,Paternity_Leave,No_of_leaves,Taken_leaves, Pending_leaves) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(Insert_Query,(Employee_Id,Employee_Name,employee_email,gender,Sick_Leave,Wedding_Leave,Maternity_Leave,Paternity_Leave,No_of_Leaves,Taken_Leaves,Pending_Leaves))
            connection.commit()
            Response_Data={'status':'success',"message":'leave data inserted into leave_balance_table successfully..'}
            return jsonify(Response_Data)
       except Exception as e :
          print("exception occerd in Insert_Leave_Balance function and error is:",e)







#getting user_id as request and sending leave_history data of a specific user......
@app.route('/accepted_leave_history', methods=['POST'])
def Fetch_Emp_History():
    if request.method == 'POST':
        Data = request.get_json()
        print(Data)       
        Employee_Id=Data['employee_id']
        Request_Type=Data['request_type']
        try:          
         if Request_Type=='accept':       
            with connection.cursor() as cursor: 
                Select_Query='SELECT * FROM Leave_history WHERE Employee_id=%s AND Status=%s'
                cursor.execute(Select_Query,(Employee_Id,'Accepted'))
                Emp_Info=cursor.fetchall()
                print("this is for accept function",Emp_Info)
                if Emp_Info:
                   Response_Data={'status':'Success','Employee_Leave_history':Emp_Info}
                   return jsonify(Response_Data)
                else:
                    Response_Data={'status':'failed','message':'requested_user_id not exist in table..'}
                    return jsonify(Response_Data)
         elif Request_Type=='pending':
             with connection.cursor() as cursor: 
                Select_Query='SELECT * FROM Leave_Request WHERE Employee_id=%s'
                cursor.execute(Select_Query,(Employee_Id))
                Emp_Info=cursor.fetchall()
                if Emp_Info:
                   Response_Data={'status':'Success','Employee_Leave_history':Emp_Info}
                   return jsonify(Response_Data)
                else:
                    Response_Data={'status':'failed','message':'requested_user_id not exist in table..'}
                    return jsonify(Response_Data)
         elif Request_Type=='reject':
             with connection.cursor() as cursor: 
                Select_Query='SELECT * FROM Leave_Request WHERE Employee_id=%s AND Status=%s'
                cursor.execute(Select_Query,(Employee_Id,'Rejected'))
                Emp_Info=cursor.fetchall()
                if Emp_Info:
                   Response_Data={'status':'Success','Employee_Leave_history':Emp_Info}
                   return jsonify(Response_Data)
                else:
                    Response_Data={'status':'failed','message':'requested_user_id not exist in table..'}
                    return jsonify(Response_Data)
        except Exception as e :
            print("exception occerd in Fetch_Emp_History function and error is:",e)




#sending leave_request data and emp count and ids& names............
@app.route('/get_leaverequest_data',methods=['POST'])
def Fetch_Leave_Request():
   if request.method == 'POST':
        Data = request.get_json()
        print("data is",Data)       
        Employee_Id=Data['employee_id']
        try:
            with connection.cursor() as cursor: 
                Select_Query='SELECT Applied_on,Reason,Start_date,End_date,Request_id,Employee_id,Employee_Name FROM Leave_Request WHERE Employee_id=%s'
                cursor.execute(Select_Query,(Employee_Id))
                Emp_Info=cursor.fetchall()
                # print("this is for accept function",emp_info)
                Count_Query='SELECT COUNT(Employee_id) FROM Employee_complete_Details'
                cursor.execute(Count_Query)
                Employee_Count=cursor.fetchall()
                Select_Query="SELECT Employee_id,Employee_Name FROM Employee_complete_Details"
                cursor.execute(Select_Query)  
                Emp_Details = cursor.fetchall()
                #sending response ...................
                print(Emp_Info)
                if Emp_Info:
                   Response_Data={'status':'Success','Employee_Leave_request_data':Emp_Info,'Total_employees':Employee_Count,'all_employee_name_id':Emp_Details}
                   return jsonify(Response_Data)
                else:
                    Response_Data={'status':'failed','message':'requested_user_id not exist in table..','Total_employees':Employee_Count,'all_employee_name_id':Emp_Details}
                    return jsonify(Response_Data)
        except Exception as e :
            print("exception occerd in Fetch_Leave_Request function and error is:",e)




#getting employee_id and sending last record data from leave_request and leave_history
@app.route('/last_record', methods=['POST'])
def Last_Record():
  if request.method == 'POST':
    Data = request.get_json()
    print(Data)       
    Employee_Id=Data['employee_id']
    try:
        with connection.cursor() as cursor: 
         Select_Query='select Start_date,End_date,Applied_on from  Leave_Request  WHERE Employee_id=%s order by applied_on desc limit 1'
         cursor.execute(Select_Query,(Employee_Id))
         Emp_Info=cursor.fetchall()
         print("employee_last_record",Emp_Info)         
         Select_Query='select Start_date,End_date ,Approved_By_Whom from Leave_history WHERE Employee_id= %s order by  End_date desc limit 1 '
         cursor.execute(Select_Query,(Employee_Id))
         Emp_History=cursor.fetchall()   
         #sending response(Employee leave_request Information and leave_history information )           
        Response_Data={'status':'Success','Employee_last_record':Emp_Info,'Employee_last_history_details':Emp_History}
        return jsonify(Response_Data) 
    except Exception as e:
        print("error occured in Last_Record")
        return "employee_id not found"
  else:
      print("method not found")
      return "method not found"
  




#getting id and sending employee_attendance_info based on id and date.......
@app.route('/get_clock_in',methods=['POST'])
def specific_attendance_details():
    if request.method=='POST':
        Data = request.get_json()
        print(Data)       
        Employee_Id=Data['employee_id']
        Current_Date= datetime.now().strftime('%Y-%m-%d')
        current_Date_Formatted= datetime.strptime(Current_Date, '%Y-%m-%d')
        with connection.cursor() as cursor: 
         Select_Query='select clock_in_time FROM  Employee_Attendance_Data  WHERE Employee_id=%s AND Date=%s'
         cursor.execute(Select_Query,(Employee_Id,current_Date_Formatted))
         Emp_Info=cursor.fetchone()        
        try:
           print("employee_info",Emp_Info)
           if Emp_Info:
             Clock_In_Time=str(Emp_Info['clock_in_time'])
             print("current_time",Emp_Info)
             print("current_clock_time:",Clock_In_Time)
             Response_Data={'status':'Success','current_time':Clock_In_Time}
             return jsonify(Response_Data)
           else:
               Response_Data={'status':'failed','message':'person not there in records'}
               return jsonify(Response_Data)
        except Exception as e:
            print("exception is",e)
            Response_Data={'status':'failed','message':'person not there in records'}
            return jsonify(Response_Data)
             
    



#sending employee count ,employee id and names......
@app.route('/get_employees_count',methods=['POST'])
def Fetch_Emp_Count_Info():
    if request.method=='POST':
        Data = request.get_json()
        print(Data)
        try:
          if Data:       
            with connection.cursor() as cursor:
        #fetching employee_count......... 
             Count_Query='SELECT COUNT(Employee_id) FROM Employee_complete_Details'
             cursor.execute(Count_Query)
             Employee_Count=cursor.fetchall()
        #selecting all employee_ids and names
             Select_Query="SELECT Employee_id,Employee_Name FROM Employee_complete_Details"
             cursor.execute(Select_Query)  
             Emp_Info = cursor.fetchall()
        #sending response (employee count and their ids and names.........)
            Response_Data={'status':'Success','Total_employees':Employee_Count,'all_employee_name_id':Emp_Info}
            return jsonify(Response_Data)
          else:
            Response_Data={'status':'failed'}
            return jsonify(Response_Data)
        except Exception as e:
            print("exception is",e)
            Response_Data={'status':'failed'}
            return jsonify(Response_Data)




#sending employee_attendance info based on id along with employee count& their id_names......
@app.route('/get_employee_attendance',methods=['POST'])
def employee_attendance_data():
    if request.method=='POST':
        Data = request.get_json()
        Employee_Id=Data['employee_id']
        print(Data)
        try:
             if Data:       
               with connection.cursor() as cursor: 
                #selecting clock info from attendance table..
                Select_Query='SELECT clock_in_time,clock_out_time,clock_in_location,Avg_working_hrs,employee_name,Employee_id FROM Employee_Attendance_Data WHERE Employee_id=%s'
                cursor.execute(Select_Query,(Employee_Id))
                Clock_Info=cursor.fetchall()
                #fetching employee count......
                Count_Query='SELECT COUNT(Employee_id) FROM Employee_complete_Details'
                cursor.execute(Count_Query)
                Employee_Count=cursor.fetchall()
                 #selecting all employee_ids and names
                Select_Query="SELECT Employee_id,Employee_Name FROM Employee_complete_Details"
                cursor.execute(Select_Query)  
                Emp_Info = cursor.fetchall()
                print(Clock_Info)
                print(Employee_Count)
                print(Emp_Info)
                for i in range(len(Clock_Info)):
                    clock_in_time=str(Clock_Info[i]['clock_in_time'])
                    clock_out_time=str(Clock_Info[0]['clock_out_time'])
                    Avg_working_hrs=str(Clock_Info[0]['Avg_working_hrs'])
                    Clock_Info[i]['clock_in_time']=clock_in_time
                    Clock_Info[i]['clock_out_time']=clock_out_time
                    Clock_Info[i]['Avg_working_hrs']=Avg_working_hrs 
                    #sending response(employee count employee_clock info and all employee_ids and names)          
                Response_Data={'status':'Success','employee_clock_info':Clock_Info,'Total_employees':Employee_Count,'all_employee_name_id':Emp_Info}
                return jsonify(Response_Data)
             else:
                  Response_Data={'status':'failed','message':'requested_employee not there in records...','Total_employees':Employee_Count,'all_employee_name_id':Emp_Info}
                  return jsonify(Response_Data)
        except Exception as e:
            print("exception is",e)
            Response_Data={'status':'failed','message':'exception occured..'}
            return jsonify(Response_Data)





#sending employee count ,employee id and names......
@app.route('/admin_get_status',methods=['POST'])
def Fetch_Fest_Info():
    if request.method == 'POST':
        Data = request.get_json()
        Request_Type=Data['Request_Type']
        print(Data)
        try:
          if Request_Type=='Last_Month':
            with connection.cursor() as cursor:   
              Date = datetime.now().date()
              Present_Formatted_Date= datetime.now().strftime('%Y-%m-%d')
              No_Of_Days=30
              Last_Month_Date = Date - timedelta(days=No_Of_Days)
              Last_Month_Date_Formatted = Last_Month_Date.strftime('%Y-%m-%d')
            # Date=Date-no_of_days
              print("last month date is:",Last_Month_Date_Formatted)
            #selecting specific info based on present and before one month dates....                 
              Select_Query="SELECT Employee_id,Employee_Name,Date,Status_Update FROM Daily_Status_Update WHERE Date BETWEEN %s AND %s"
              cursor.execute(Select_Query,(Present_Formatted_Date,Last_Month_Date_Formatted))  
              Status_Info = cursor.fetchall()
              print("data is:",Status_Info) 
              #sending response (festival information.........)
              Response_Data={'status':'Success','Status_Info':Status_Info}
              return jsonify(Response_Data)
          elif Request_Type=='Last_week':
              with connection.cursor() as cursor:   
                Date = datetime.now().date()
                Present_Formatted_Date= datetime.now().strftime('%Y-%m-%d')
                No_Of_Days=7
                Last_Week_Date = Date - timedelta(days=No_Of_Days)
                Last_Week_Date_Formatted = Last_Week_Date.strftime('%Y-%m-%d')
               # Date=Date+no_of_days
                print("last weekdate is:",Last_Week_Date_Formatted)
               #selecting specific info based on present and before one week dates....                 
                Select_Query="SELECT Employee_id,Employee_Name,Date,Status_Update FROM Daily_Status_Update WHERE Date BETWEEN %s AND %s"
                cursor.execute(Select_Query,(Present_Formatted_Date,Last_Week_Date_Formatted))  
                Status_Info = cursor.fetchall()
                print("data is:",Status_Info) 
              #sending response (festival information.........)
                Response_Data={'status':'Success','Status_Info':Status_Info}
              return jsonify(Response_Data)
          elif Request_Type=='Last_day':
              with connection.cursor() as cursor:   
                Date = datetime.now().date()
                Present_Formatted_Date= datetime.now().strftime('%Y-%m-%d')
                No_Of_Days=1
                Last_Day_Date = Date - timedelta(days=No_Of_Days)
                Last_Day_Date_Formatted = Last_Day_Date.strftime('%Y-%m-%d')
               # Date=Date-no_of_days
                print("last day is:",Last_Day_Date_Formatted)
               #selecting specific info based on present and before one day dates....                 
                Select_Query="SELECT Employee_id,Employee_Name,Date,Status_Update FROM Daily_Status_Update WHERE Date= %s"
                cursor.execute(Select_Query,(Last_Day_Date_Formatted))  
                Status_Info = cursor.fetchall()
                print("data is:",Status_Info) 
              #sending response (festival information.........)
                Response_Data={'status':'Success','Status_Info':Status_Info}
              return jsonify(Response_Data)
          else:
            Response_Data={'status':'failed','message':'invalid request_type'}
            return jsonify(Response_Data)
        except Exception as e:
            print("exception occerd in etch_Fest_Info function and error is",e)
            return "data not found for specific dates..."




#getting id and sending employee_leave balance info based on id .......
@app.route('/fest_info',methods=['POST'])
def Fetch_Status_Fest_Info():
    if request.method=='POST':
        Data = request.get_json()
        print(Data)       
        Employee_Id=Data['employee_id']
        #selecting leaves from leave balance based on the employee_id.........
        with connection.cursor() as cursor: 
         try:
           Select_Query='select Employee_Name,Sick_Leave,Wedding_Leave,Maternity_Leave,Paternity_Leave,No_of_leaves,Taken_leaves,Pending_leaves FROM  Leave_balance  WHERE Employee_id=%s'
           cursor.execute(Select_Query,(Employee_Id))
           Leave_Balance_Info=cursor.fetchall() 
           #selecting fwestival info from holiday table.... 
           Select_Query='SELECT * FROM Holiday'
           cursor.execute(Select_Query)
           Fest_Info=cursor.fetchall()
           print("Leave_Balance_Info",Leave_Balance_Info)
           print("Fest_Info",Fest_Info)
           #sending fest and balance info..........    
           Response_Data={'status':'Success','Leave_Balance_Info':Leave_Balance_Info,'Fest_Info':Fest_Info}
           return jsonify(Response_Data) 
         except Exception as e:
            print("exception is",e)
            Response_Data={'status':'failed','message':'id not found'}
            return jsonify(Response_Data)
    else:
        print("method not found")
        return "method not found"
             













if __name__ == '__main__':
    app.run(debug=True,host='192.168.0.4',port=5000)