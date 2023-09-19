import sqlite3

def check_credentials(username, password):
    match check_username(username) == "Valid", check_password(password) == "Valid":
        case True,True:
            if login(username,password) is not None:
                output = login(username,password)
            else:
                output = "Your username and password are incorrect and returned no results."
        case True, False:
            output = "Your password is invalid. Please try again or register below."
        case False, True:
            output = "Your username is invalid. Please ensure you have at least 6 characters, no special characters are inserted."
        case False, False:
            output = "Neither your password nor your username satisfy the requirements. Please try again or register below."
    
    return output



def check_username(username):
    if len(username) > 12:
        return "Your username cannot exceed 12 characters. Please try again or register below."
    elif len(username) > 0 and len(username) < 6:
        return "Your username needs to be at least 6 characters in length. Please try again or register below."
    else:
        return "Valid"
            
def check_password(password):
    if len(password) <= 6:
        return "Your password is too short, it must be at least 7 characters long."
    elif len(password) > 30:
        return "Your password is too long, it cannot exceed 30 characters."
    else:
        return "Valid"

def login(username, password):
    conn = sqlite3.connect('static/database.db')
    curs = conn.cursor()
    result = curs.execute('''SELECT * FROM users WHERE username = ? AND password = ?''',(username,password)).fetchone()
    return result






    