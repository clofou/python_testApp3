from tabnanny import check
import mysql.connector
import re

class MyBdd:
    def __init__(self) -> None:
        self.bdd = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "user_crud"
        )

    def check(self, email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(regex, email)):
            return True
        else:
            return False
    
    def recuperation(self):
        myDbWriter = self.bdd.cursor()
        myDbWriter.execute("SELECT * FROM user")
        userList = myDbWriter.fetchall()
        return userList
    def recupOne(self, email):
        myDbWriter = self.bdd.cursor()
        myDbWriter.execute("SELECT * FROM user")
        userList = myDbWriter.fetchall()
        aUser = []
        for user in userList:
            if (user[5] == email):
                aUser.append(user[0])
                aUser.append(user[1])
                aUser.append(user[2])
                aUser.append(user[3])
                aUser.append(user[4])
                aUser.append(user[5])
                break
        self.bdd.close()
        return aUser

    
    
    def register(self, email, password, name, surname, note, age):
        myDbWriter = self.bdd.cursor()
        myDbWriter.execute("SELECT * FROM user")
        userList = myDbWriter.fetchall()
        isResgister = False
        if (email!="" and name!="" and surname!="" and note!="" and password!=""):
            for user in userList:
                if (user[5] == email):
                    isResgister = True
                    break
                
            if isResgister or self.check(email)==False:
                return False
            else:
                sql = "INSERT INTO user(nom, prenom, age, note, email, password) VALUES (%s, %s, %s, %s, %s, %s)"
                newUser = (name, surname, age, note, email, password)
                myDbWriter.execute(sql, newUser)
                self.bdd.commit()
                self.bdd.close()
                self.bdd.close()
                return True

    
    def login(self, email, password):
        myDbWriter = self.bdd.cursor()
        myDbWriter.execute("SELECT * FROM user")
        userList = myDbWriter.fetchall()
        isLogin = False
        for user in userList:
            if (user[5] == email and user[6] == password and self.check(email)):
                isLogin = True
                break
        self.bdd.close()
        return isLogin

    
    def delete(self, email):
        myDbWriter = self.bdd.cursor()
        myDbWriter.execute("SELECT * FROM user")
        userList = myDbWriter.fetchall()
        isDelete = False
        for user in userList:
            if (user[5] == email):
                myDbWriter.execute(f"DELETE FROM user WHERE email = '{email}'")
                isDelete = True
                break
        self.bdd.close()
        return isDelete

    
    def update(self, email, name, surname, note, age):
        myDbWriter = self.bdd.cursor()
        myDbWriter.execute("SELECT * FROM user")
        userList = myDbWriter.fetchall()
        isUpdate = False
        if (email!="" and name!="" and surname!="" and note!=""):
            for user in userList:
                if (user[5] == email):
                    myDbWriter.execute(f"UPDATE user SET nom='{name}',prenom='{surname}',age='{age}',note='{note}' WHERE email='{email}'")
                    isUpdate = True
                    break
        self.bdd.close()
        return isUpdate

    
    def research(self, nom):
        myDbWriter = self.bdd.cursor()
        myDbWriter.execute("SELECT * FROM user")
        userList = myDbWriter.fetchall()
        allUser = []
        for user in userList:
            if (user[1] == nom):
                allUser.append(user[1])
                break
        self.bdd.close()
        return allUser

