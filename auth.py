from functions import login

def check_credentials(username, password):
    match check_username(username) == "Valid", check_password(password) == "Valid":
        case True,True:
            output = login(username,password)
            if output is not None:
                pass
            else:
                raise SystemError("Your username and password are incorrect and returned no results.")
        case True, False:
            raise SystemError("Your password is invalid. Please try again or register below.")
        case False, True:
            raise SystemError("Your username is invalid. Please ensure you have at least 6 characters, no special characters are inserted.")
        case False, False:
            raise SystemError("Neither your password nor your username satisfy the requirements. Please try again or register below.")
    
    return output



def check_username(username):
    if len(username) > 12:
        raise SystemError("Your username cannot exceed 12 characters. Please try again or register a new user.")
    elif len(username) <= 4:
        raise SystemError("Your username needs to be at least 6 characters in length. Please try again or register below.")
    else:
        return "Valid"
            
def check_password(password):
    if len(password) <= 6:
        raise SystemError("Your password is too short, it must be at least 7 characters long.")
    elif len(password) > 30:
        raise SystemError("Your password is too long, it cannot exceed 30 characters.")
    else:
        return "Valid"






    