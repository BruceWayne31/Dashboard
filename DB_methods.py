# -*- coding: utf-8 -*-
class db_methods():
    def create_record(self,EmpID,EmpName,Comp,Date):
        import sqlite3
        conn=sqlite3.connect("Records.db")
        cursor=conn.cursor()
        result=cursor.execute("SELECT * FROM deadlines WHERE EmpID =? and Competency=?;",(EmpID,Comp)).fetchall()
        if len(result)==0:
            cursor.execute("INSERT INTO deadlines VALUES (?,?,?,?);",(EmpID,EmpName,Comp,Date))
            conn.commit()
            conn.close()
            return "Deadline assigned for the competency"
        else:
            cursor.execute("UPDATE deadlines SET Date=? WHERE EmpID =? and Competency =?",(Date,EmpID,Comp))
            conn.commit()
            conn.close()
            return "Deadline updated for the competency"
            
    def check_record(self,EmpID,EmpName,Comp,Date):
        import sqlite3
        conn=sqlite3.connect("Records.db")
        cursor=conn.cursor()
        result=cursor.execute("SELECT * FROM deadlines WHERE EmpID =? and Competency=?;",(EmpID,Comp)).fetchall()      
        return result

    def get_date(self,EmpID,Comp):
        import sqlite3
        conn=sqlite3.connect("Records.db")
        cursor=conn.cursor()
        c=cursor.execute("SELECT Date FROM deadlines WHERE EmpID=? and Competency=?;",(EmpID,Comp)).fetchall()
        conn.commit()
        conn.close()
        return c