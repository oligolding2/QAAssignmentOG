import sqlite3,random,re

def executor(query,args,query_type):
    try:
        conn = sqlite3.connect('static/database.db')
        curs = conn.cursor()
        match query_type:
            case 'read':
                if args==None:
                    return curs.execute(query).fetchall()
                else:
                    return curs.execute(query,(args,)).fetchall()
                
            case 'add' | 'update':
                curs.execute(query,args)
                statement = 'Statement successfully executed'

            case 'delete':
                curs.execute(query,(args,))
                statement = 'Record successfully deleted'
            
            case 'login':
                return curs.execute(query,args).fetchone()

        conn.commit()
        conn.close()
        return statement
    except sqlite3.Error as e:
        return "Error encountered"
    
def append(owner,location,value,user):
    items = {'owner':owner,'location':location,'value':value,'user':user}
    for k,v in items.items():
        if v is None or len(v) == 0:
            raise SystemError(f"You must provide a value for {k.capitalize()}")
        elif k!='value' and bool(re.match(r'^\d+$', v)):
            raise SystemError(f"The value for {k} must be a string")
        else:
            pass
    values = (owner,location,value,user)
    insert_query = "INSERT INTO mortgage (owner,location,value,inserted_by) VALUES (?,?,?,?)"
    outcome = executor(insert_query,values,'add')
    if "error" in outcome.lower():
        raise SystemError("Failed adding record to database")
    else:
        return outcome

def read(mortgage,searchall):
    if searchall:
        query = "SELECT mortgage_id,owner,location,value FROM mortgage"
        args = None
    else:
        query = "SELECT mortgage_id,owner,location,value FROM mortgage WHERE mortgage_id = ?"
        if mortgage is None or len(mortgage) == 0:
            raise SystemError("You must specify a mortgage ID to search.")
        else:
            args = str(mortgage)
    
    result = executor(query,args,'read')
    if result is not None and len(result) != 0:
        return result
    else:
        raise SystemError(f"There was no record for mortgage ID {mortgage}.")
    

def update(mortgage,name,location,value):
    values = {'owner':name, 'location':location, 'value':value}
    query = "UPDATE mortgage SET "
    updates = []
    args = []
    for k,v in values.items():
        if len(v) > 0 and k!='value' and bool(re.match(r'^\d+$', v)):
            raise SystemError(f"The value for {k} must be a string")
        elif len(v) != 0:
            updates.append(f"{k} = ?")
            args.append(v)
        else:
            pass
    query += ", ".join(updates) + " WHERE mortgage_id = ?"
    args.append(mortgage)
    outcome = executor(query,args,'update')
    return outcome

def delete(mortgage_id):
    query = "DELETE FROM mortgage WHERE mortgage_id = ?"
    args = mortgage_id
    outcome = executor(query,args,'delete')
    return outcome

def create_user(username,password,admin_token):
    query = "INSERT INTO users (user_id,username,password,admin) VALUES (?,?,?,?)"
    if admin_token is not None:
        if str(admin_token) == "HiQA99999999":
            args = (random.randint(0,9999999),username,password,1)
        else:
            raise SystemError("Invalid admin token provided.")
    else:
        args = (random.randint(0,9999999),username,password,0)
    
    executor(query,args,'add')

def login(username,password):
    query = "SELECT * FROM users where username = ? AND password = ?"
    args = username,password
    result = executor(query,args,'login')
    return result
