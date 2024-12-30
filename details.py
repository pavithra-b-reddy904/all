from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk
import random
from time import strptime
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
class detailsroom:
    def __init__ (self,root):
        self.root=root
        self.root.title("hotel management system")
        self.root.geometry("1100x500+190+180")

        #=========== title =================
        lbl_title=Label(self.root,text="ROOM BOOKING DETAILS",font=("times new roman",18,"bold"),bg="grey",fg="gold",bd=4,relief=RIDGE)
        lbl_title.place(x=0,y=0,width=1295,height=50)

         #================ logo===============
        img2=Image.open(r"C:\Users\INDIRA S\OneDrive\Desktop\pro\images\logo1.jpg")
        img2=img2.resize((100,40),Image.LANCZOS)
        self.photoimg2=ImageTk.PhotoImage(img2)

        lblimg=Label(self.root,image=self.photoimg2,bd=0,relief=RIDGE)
        lblimg.place(x=5,y=2,width=100,height=40)

        #====== label frame ==================
        labelframeleft=LabelFrame(self.root,bd=2,relief=RIDGE,text="NEW ROOM ADD",font=("times new roman",12,"bold"),padx=2,)
        labelframeleft.place(x=5,y=50,width=540,height=350)

        #floor
        lbl_floor=Label(labelframeleft,text="Floor",font=("times new roman",12,"bold"),padx=2,pady=6)
        lbl_floor.grid(row=0,column=0,sticky=W,padx=20)

        self.var_floor=StringVar()
        enty_floor=ttk.Entry(labelframeleft,textvariable=self.var_floor,font=("times new roman",13,"bold"),width=20)
        enty_floor.grid(row=0,column=1,sticky=W)

        #ROON NO
        lbl_roomno=Label(labelframeleft,text="Room_No",font=("times new roman",12,"bold"),padx=2,pady=6)
        lbl_roomno.grid(row=1,column=0,sticky=W,padx=20)

        self.var_roomno=StringVar()
        enty_roomno=ttk.Entry(labelframeleft,font=("times new roman",13,"bold"),width=20)
        enty_roomno.grid(row=1,column=1,sticky=W)

        #ROOM TYPE
        lbl_roomtype=Label(labelframeleft,text="Room_Type",font=("times new roman",12,"bold"),padx=2,pady=6)
        lbl_roomtype.grid(row=2,column=0,sticky=W,padx=20)

        self.var_roomtype=StringVar()
        enty_roomtype=ttk.Entry(labelframeleft,font=("times new roman",13,"bold"),width=20)
        enty_roomtype.grid(row=2,column=1,sticky=W)

        
        #================= btns ============
        btn_frame=Frame(labelframeleft,bd=2,relief=RIDGE)
        btn_frame.place(x=0,y=200,width=412,height=40)

        btnAdd=Button(btn_frame,text="ADD",command=self.add_data,font=("times new roman",11,"bold"),bg="grey",fg="gold",width=10)
        btnAdd.grid(row=0,column=0,padx=1)

        btnUpdate=Button(btn_frame,text="Update",command=self.update,font=("times new roman",11,"bold"),bg="grey",fg="gold",width=10)
        btnUpdate.grid(row=0,column=1,padx=1)

        btnDelete=Button(btn_frame,text="Delete",command=self.mdelete,font=("times new roman",11,"bold"),bg="grey",fg="gold",width=10)
        btnDelete.grid(row=0,column=2,padx=1)

        btnReset=Button(btn_frame,text="Reset",command=self.reset_data,font=("times new roman",11,"bold"),bg="grey",fg="gold",width=10)
        btnReset.grid(row=0,column=3,padx=1)


        #===================table frame=============
        table_frame=LabelFrame(self.root,bd=2,relief=RIDGE,text="SHOW ROOM DETAILS",font=("times new roman",12,"bold"),padx=2,)
        table_frame.place(x=600,y=55,width=600,height=350)

        scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL)

        self.room_table=ttk.Treeview(table_frame,columns=("floor","roomno","roomtype"),xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set)
        scroll_x.pack(side=RIGHT,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)


        scroll_x.config(command=self.room_table.xview)
        scroll_y.config(command=self.room_table.yview)

        self.room_table.heading("floor",text="floor")
        self.room_table.heading("roomno",text="roomno")
        self.room_table.heading("roomtype",text="roomtype")

        self.room_table["show"]="headings"

        self.room_table.column("floor",width=100)
        self.room_table.column("roomno",width=100)
        self.room_table.column("roomtype",width=100)

        self.room_table.pack(fill=BOTH,expand=1)
        self.room_table.bind("<ButtonRelease-1>",self.get_cursor)
        self.fetch_data()

    
     # add data
    def add_data(self):
        if self.var_floor.get()=="" or self.var_roomtype.get()=="":
            messagebox.showerror("Error","All feilds are required",parent=self.root)
        else:
            try:
                conn=mysql.connector.connect(host="localhost",username="root",password="rujusmitha@99",database="management")
                my_cursor=conn.cursor()
                my_cursor.execute("insert into detailsroom values(%s,%s,%s,)",(
                                                                                     self.var_floor.get(),
                                                                                     self.var_roomno.get(),
                                                                                     self.var_roomtype.get()
                                                                                     ))
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success","Room added successfully",parent=self.root)
            except Exception as es:
                messagebox.showwarning("warning",f"something went wrong:{str(es)}",parent=self.root)
    #fetch data
    def fetch_data(self):
        conn=mysql.connector.connect(host="localhost",username="root",password="rujusmitha@99",database="management")
        my_cursor=conn.cursor()
        my_cursor.execute("select*from detailsroom")
        rows=my_cursor.fetchall()
        if len(rows)!=0:
            self.room_table.delete(*self.room_table.get_children())
            for i in rows:
                self.room_table.insert("",END,values=i)
            conn.commit()
        conn.close()
    # get cursor
    def get_cursor(self,event=" "):
        cursor_row=self.room_table.focus()
        content=self.room_table.item(cursor_row)
        row=content["values"]
        
        self.var_floor.set(row[0]),
        self.var_roomno.set(row[1]),
        self.var_roomtype.set(row[2])


    #update
    def update(self):
        if self.var_floor.get()=="":
            messagebox.showerror("error please enter room number",parent=self.root)
        else:
            conn=mysql.connector.connect(host="localhost",username="root",password="rujusmitha@99",database="management")
            my_cursor=conn.cursor()
            my_cursor.execute("Update detailsroom set floor=%s,roomtype=%s where roomno=%s",(
                                                                                                self.var_floor.get(),
                                                                                                self.var_roomtype.get(),
                                                                                                self.var_roomno.get(),
                                                                                                                        
            ))
        conn.commit()
        self.fetch_data()
        conn.close()
        messagebox.showinfo("Update","Room detail has been updated successfully",parent=self.root)
    #delete
    def mdelete(self):
        mdelete=messagebox.askyesno("Hotel Management System","Do you want to delete this room",parent=self.root)
        if mdelete>0:
            conn=mysql.connector.connect(host="localhost",username="root",password="rujusmitha@99",database="management")
            my_cursor=conn.cursor()
            query="delete from detailsroom where roomno=%s"
            value=(self.var_roomno.get())
            my_cursor.execute(query,value)
        else:
            if not mdelete:
                return
        conn.commit()
        self.fetch_data()
        conn.close()

    def reset_data(self):
        self.var_floor.set(""),
        self.var_roomno.set(""),
        self.var_roomtype.set("")








    





    

    

        












if __name__=="__main__":
    root=Tk()
    obj= detailsroom(root)
    root.mainloop()
