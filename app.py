from datetime import datetime
from auth import check_credentials,check_password,check_username
import functions
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = '7f843d947faaf119f26c8b9307efe64f'         #for assigning and obtaining session data

def display_template(filename, **context):              #function which standardizes rendering templates and their arguments
    if 'user-data' in session:                                          #checking if user is logged into session for displaying log off button
        return render_template(filename,logged_in = True,**context)
    elif request.endpoint not in ['login', 'register','outcome']:       #redirect to login page if user isn't logged in, with endpoint exceptions
        return redirect(url_for('login'))                                      
    else:                                                               #if the user is logged in, render template with arguments
        return render_template(filename, **context)
        
@app.route('/')
def hello():                                        #route which redirects to login when app is first launched
    return redirect(url_for('login'))


@app.errorhandler(Exception)                                #error handling function supplied by Flask, modified to return all exceptions caught within the application
def handle_exception(exception):
    error_message = "Error encountered: " + str(exception)          #outcome page can be any sort of message, so the contents are parameterized
    error_outcome = "Error"
    return redirect(url_for('outcome',message=error_message,outcome=error_outcome))     #redirect to outcome page, which returns the content

@app.route('/outcome')
def outcome():
    message = request.args.get('message')
    outcome = request.args.get('outcome')
    if 'user-data' in session:                      #checks if the user is logged in, if not, the button displayed once the message has been displayed is to return to login, otherwise, it allows the user to return to the homepage.
        destination = 'home'
    else:
        destination = 'login'
    arguments = {'message':message,'outcome':outcome,'destination':destination}
    return display_template("outcome.html",**arguments)             #passes all the arguments to display_template

@app.route("/login", methods=["POST", "GET"])
def login():
    session.clear()                                     #everytime the login page is accessed, the session is cleared so that it can be updated if a different user needs to log in
    if request.method == "POST":
        login_uname = request.form['login-username']            #if a POST request is triggered, retrieve the fields from the form and validate their values in auth.py
        login_pword = request.form['login-password']
        user = check_credentials(login_uname, login_pword)
        session['user-data'] = user                 #if this line is reached, there weren't any errors logging in, so the user found is assigned to the session 
        return redirect(url_for("home"))            #redirect to the home route
    else:
        return display_template("login.html")       #when the login page is routed to by the hello() function, there is no POST request, so the login page just needs to be rendered

@app.route("/register", methods=["POST", "GET"]) #the register page is triggered by an <a> tag in the login page html
def register():     #function for registering a new user
    if request.method == "POST":
            username = request.form['register-username']
            password = request.form['register-password']
            match check_username(username) == "Valid", check_password(password) == "Valid":
                case True, True:
                    functions.create_user(username,password,request.form['admin-token'])
                    return redirect(url_for("login"))
                case True, False:
                    raise SystemError(check_password(password))
                case False, True:
                    raise SystemError(check_username(username))
                case False, False:
                    raise SystemError("Please enter valid credentials.")
    else:
        return display_template("register.html")
    
@app.route("/home", methods=["POST","GET"])
def home():
    session_data = session.get('user-data',{})
    booladmin = bool(session_data[3])
    username = str(session_data[1])
    if booladmin:
        return display_template("functions-admin.html",username=username)
    else:
        return display_template("functions-user.html",username=username)
    
@app.route("/add_record",methods=["POST","GET"])
def add_record():
    if request.method == "POST":
        name = request.form['owner-name']
        location = request.form['property-location']
        value = request.form['property-value']
        user = session.get('user-data',{})
        username = str(user[1])
        outcome_message = functions.append(name,location,value,username)
        return redirect(url_for('outcome',message=outcome_message,outcome="Record Added"))
    else:
        return display_template("record-create.html")

@app.route("/display_record",methods=["POST","GET"])
def display_record():
    if request.method == "POST":
        if 'search-btn' in request.form:
            mortgage_id = request.form['mortgage-id']
            result = functions.read(mortgage_id,False)
            return display_template("results.html",results=result)
        elif 'display-all-btn' in request.form:
            result = functions.read(None,True)
            return display_template("results.html",results=result)
        else:
            raise SystemError("Unrecognised button clicked")
    else:
        return display_template("record-display.html")
        
@app.route("/update_record",methods=["POST","GET"])
def update_record():
    columns = {'name':'','location':'','value':''}
    update_details = {}
    if request.method == "POST":
        mortgage = request.form['mortgage-id']
        if mortgage is not None and len(mortgage) > 0:
            functions.read(mortgage,False)
            for form_field in request.form:
                update_details[form_field] = str(request.form[form_field])
            for x in columns.keys():
                for key,value in update_details.items():
                    if x in key:
                        columns[x] = value
                    else:
                        pass
            if any(len(value) > 0 for value in columns.values()):
                update_outcome = functions.update(mortgage=mortgage,name=columns['name'],location=columns['location'],value=columns['value'])
                if "success" in update_outcome:
                    return redirect(url_for('outcome',message=update_outcome,outcome="Updated Record"))
                else:
                    raise SystemError(update_outcome)
            else:
                raise SystemError("You didn't provide any values to update a user with.") 
        else:
            raise SystemError("You must specify a mortgage ID to update")
                    
    else:
        return display_template("record-update.html")
    
@app.route("/delete_record",methods=["POST","GET"])
def delete_record():
    if request.method == "POST":
        mortgage = request.form['mortgage-id']
        if mortgage is not None and len(mortgage) > 0:
            functions.read(mortgage,False)
            delete_outcome = functions.delete(mortgage)
            return redirect(url_for('outcome',message=delete_outcome,outcome="Deleted Record"))
        else:
            raise SystemError("You must provide a mortgage ID for deletion")
    else:
        return display_template("record-delete.html")