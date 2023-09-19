from datetime import datetime
from auth import check_credentials,check_password,check_username
import functions
from flask import Flask, render_template, request, redirect, url_for, session
import re

app = Flask(__name__)
app.secret_key = '7f843d947faaf119f26c8b9307efe64f'

@app.route('/')
def hello():
    return redirect(url_for('login'))

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        login_uname = request.form['login-username']
        login_pword = request.form['login-password']
        user = check_credentials(login_uname, login_pword)
        if isinstance(user,str):
            print(user)
        else:
            session['user-data'] = user
            return redirect(url_for("home"))
    else:
        return render_template("login.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if 'register-username' not in request.form or 'register-password' not in request.form:
            SystemError("Please make sure to enter a username and password")
        else:
            username = request.form['register-username']
            password = request.form['register-password']
            match check_username(username) == "Valid", check_password(password) == "Valid":
                case True, True:
                    functions.create_user(username,password,request.form['admin-token'])
                case True, False:
                    SystemError(check_password(password))
                case False, True:
                    SystemError(check_username(username))
                case False, False:
                    SystemError("Please enter valid credentials.")
    else:
        return render_template("register.html")
    
@app.route("/home", methods=["POST","GET"])
def home():
    session_data = session.get('user-data',{})
    booladmin = bool(session_data[3])
    username = str(session_data[1])
    
    if booladmin:
        return render_template("functions-admin.html",username=username)
    else:
        return render_template("functions-user.html",username=username)
    
@app.route("/add_record",methods=["POST","GET"])
def add_record():
    if request.method == "POST":
        name = request.form['owner-name']
        location = request.form['property-location']
        value = request.form['property-value']
        user = session.get('user-data',{})
        username = str(user[1])
        outcome = functions.append(name,location,value,username)
        return render_template("outcome.html",message=outcome)
    
    return render_template("record-create.html")

@app.route("/display_record",methods=["POST","GET"])
def display_record():
    if request.method == "POST":
        if 'search-btn' in request.form:
            mortgage_id = int(request.form['mortgage-id'])
            result = functions.read(mortgage_id,False)
            return render_template("results.html",results=result)
        elif 'display-all-btn' in request.form:
            result = functions.read(None,True)
            return render_template("results.html",results=result)
        else:
            SystemError("Unrecognised button clicked")
    else:
        return render_template("record-display.html")
        
@app.route("/update_record",methods=["POST","GET"])
def update_record():
    columns = {'name':'','location':'','value':''}
    update_details = {}
    if request.method == "POST":
        if 'mortgage-id' in request.form:
            mortgage = int(request.form['mortgage-id'])
            if len(functions.read(mortgage,False)) > 0:
                for form_field in request.form:
                    update_details[form_field] = request.form[form_field]
                for x in columns.keys():
                    for key,value in update_details.items():
                        if x in key:
                            columns[x] = value
                        else:
                            pass
                if any(value for value in columns):
                    update_outcome = functions.update(mortgage=mortgage,name=columns['name'],location=columns['location'],value=columns['value'])
                    if "success" in update_outcome:
                        return render_template("outcome.html",update_outcome)
                    else:
                        SystemError(update_outcome)
                else:
                    SystemError("You didn't provide any values to update a user with.") 
            else:
                SystemError("Your mortgage ID provided no results")
        else:
            SystemError("You must specify a mortgage ID to update")
                    
    else:
        return render_template("record-update.html")
    
@app.route("/delete_record",methods=["POST","GET"])
def delete_record():
    if request.method == "POST":
        if 'mortgage-id' in request.form:
            mortgage_id = int(request.form['mortgage-id'])
            result = functions.read(mortgage_id,False)
            if result is not None:
                outcome = functions.delete(mortgage_id)
                return render_template("outcome.html",message=outcome)
            else:
                SystemError("The mortgage value you provided was not found.")

        else:
            SystemError("You must provide a mortgage ID for deletion")
    else:
        return render_template("record-delete.html")