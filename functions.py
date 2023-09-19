import sqlite3
import random

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

        conn.commit()
        conn.close()
        return statement
    except sqlite3.Error as e:
        return "SQLite error: "  + e  
    
def append(owner,location,value,user):
    for x in owner,location,value,user:
        if isinstance(x,str):
            pass
        else:
            TypeError(x)
    values = (owner,location,value,user)
    insert_query = "INSERT INTO mortgage (owner,location,value,inserted_by) VALUES (?,?,?,?)"
    outcome = executor(insert_query,values,'add')
    return outcome

def read(mortgage,searchall):
    query = None
    args = None
    if searchall:
        query = "SELECT mortgage_id,owner,location,value FROM mortgage"
    else:
        query = "SELECT mortgage_id,owner,location,value FROM mortgage WHERE mortgage_id = ?"
        args = str(mortgage)
    return executor(query,args,'read')
    

def update(mortgage,name,location,value):
    values = {'owner':name, 'location':location, 'value':value}
    query = "UPDATE mortgage SET "
    updates = []
    args = []
    for key,value in values.items():
        if len(value) != 0:
            updates.append(f"{key} = ?")
            args.append(value)
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
            SystemError("Invalid admin token provided.")
    else:
        args = (random.randint(0,9999999),username,password,0)
    
    executor(query,args,'add')


