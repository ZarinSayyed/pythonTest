import re
import sqlite3
from sqlite3.dbapi2 import Cursor, Error
from flask import Flask, json,request,jsonify
import markdown
import os

#Create an instance of Flask
app=Flask(__name__)

@app.route('/')
def index():
    '''Present some documentation'''
    #open the readme file
    with open('README.md', 'r') as markdown_file:
        #read the content of the file 
        content=markdown_file.read()

        #Convert to HTML
        return markdown.markdown(content)

def deb_connection():
    conn=None
    try:
        conn=sqlite3.connect("resource.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn


@app.route('/resources',methods=['GET','POST'])
def device():
    conn=deb_connection()
    cursor=conn.cursor()

    if request.method=='GET':
        cursor=conn.execute("SELECT * FROM resource")
        device_list=[
            dict(Service=row[0],Port=row[1],Maintainer=row[2],Labels=row[3])
            for row in cursor.fetchall()
        ]
        if device_list is not None:
            return jsonify (device_list),200
        else:
            'nothing found',404

    if request.method=='POST':
        new_service=request.form['Service']
        new_Port=request.form['Port']
        new_Maintainer=request.form['Maintainer']
        new_Labels=request.form['Labels']
        

        reg = r"\b[a-zA-Z]+\b"
        if len(new_service) < 4 or len(new_service)>30 or new_service is None or not re.match(reg,new_service):
            return "Please enter valid Service name between 4 to 30 characters."
        
        regp= r"\b[0-9]+\b"
        if int(new_Port )< 0 or int(new_Port) > 65536  or new_Port is None or not re.match(regp,new_Port):
            return "Please enter valid Port Number range between 0 to 65536." 

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match (regex, new_Maintainer):
            return "Enter valid email for Maintainer."  
        
        if  new_Labels == "":
            return "Enter valid key value pair for  groups: or team values: for Labels."
             

        sql='''INSERT INTO resource(Service,Port,Maintainer,Labels) values(?,?,?,?)'''
        cursor=cursor.execute(sql,(new_service,new_Port,new_Maintainer,new_Labels))
        conn.commit()

        return f"Service : {new_service} created successfully.",201
    


@app.route('/resource/<string:Service>',methods=['GET','PUT','DELETE'])
def single_resource(Service):
    conn=deb_connection()
    cursor=conn.cursor()
    resource=None
    if request.method=='GET':
        cursor=conn.execute("SELECT * FROM resource WHERE Service=?",(Service,))
        device=[
            dict(Service=row[0],Port=row[1],Maintainer=row[2],Labels=row[3])
            for row in cursor.fetchall()
        ]
        if device is not None:
            return jsonify (device),200
        else:
            'Not Found',404
        
    if request.method=='PUT':
        sql=""" UPDATE resource
                SET Port =?,
                    Maintainer=?,
                    Labels=?
                WHERE Service=? """
       
        Port=request.form['Port']
        Maintainer=request.form['Maintainer']
        Labels=request.form['Labels']
        
        updated_resouce={
                'Service':Service,
                'Port':Port,
                'Maintainer':Maintainer,
                'Labels':Labels
        }
        conn.execute(sql,(Port,Maintainer,Labels,Service,)) 
        conn.commit()
        return jsonify(updated_resouce),200
    
    
    if request.method=='DELETE':
        sql='''DELETE FROM resource WHERE Service=?'''
        conn.execute(sql,(Service,))
        conn.commit()
        return f"The Service with name {Service} has been deleted.",200
   


if __name__=='__main__':
    app.run(debug=True)
