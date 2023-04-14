import sqlite3
import tkinter
from datetime import date
##-------------------------create shop database--------------------------
cnt=sqlite3.connect("shop.db")
##print("database created successfully")
##--------------------create users table-----------------------
##query='''create table users
##(id integer primary key,
##username char(15) not null,
##password char(15) not null,
##addr char(50) not null)'''
##cnt.execute(query)
##cnt.close()
##--------------------create products table-----------------------
##query='''create table products
##(id integer primary key,
##pname char(30) not null,
##price real not null,
##qnt int not null)'''
##cnt.execute(query)
##cnt.close()
##------------------------create final_shop table-----------------
##query='''create table final_shop
##(id integer primary key,
##pid int not null,
##uid int not null,
##qnt int not null,
##date char(15) not null)'''
##cnt.execute(query)
##cnt.close()
##------------------------create activities table-----------------------
##query='''create table activities
##(id integer primary key,
##activity char(15) not null,
##uid int nul null,
##date char(15) not null)'''
##cnt.execute(query)
##cnt.close()
##------------------------create total-p table-----------------------------
##query='''create table totalp
##(id integer primary key,
##pid int not null,
##totalqnt int not null)'''
##cnt.execute(query)
##cnt.close()
##------------------------insert initial record into table-----------------
##query='''insert into final_shop(pid,uid,qnt,date) values(1,1,5,"2022-02-21")'''
##cnt.execute(query)
##cnt.commit()
##cnt.close()
##--------------------------Functions--------------------
def insert_into_activities(a,b,c):
    query='''insert into activities(activity,uid,date) values(?,?,?)'''
    cnt.execute(query,(a,b,c))
    cnt.commit()
def login():
    global user_id
    t2=date.today()
    user=txt_user.get()
    pas=txt_pass.get()
    if user=="" or pas=="":
        lbl_msg.configure(text="Please fill user and password",fg="red")
        return
    query='''select * from users where username=? and password=? '''
    result=cnt.execute(query,(user,pas))
    rows=result.fetchall()
    if len(rows)==0:
        lbl_msg.configure(text="Wrong username or password",fg="red")
        return
    user_id=rows[0][0]
    lbl_msg.configure(text="Logged in successfully!",fg="green")
    btn_login.configure(state="disabled")
    btn_logout.configure(state="active")
    btn_submit.configure(state="disabled")
    btn_shop.configure(state="active")
    btn_my_shop.configure(state="active")
    txt_user.delete("0","end")
    txt_pass.delete("0","end")
    if user=="admin" and pas=="123456789":
        btn_admin.configure(state="active")
    insert_into_activities("login",user_id,str(t2))
def logout():
    t3=date.today()
    btn_logout.configure(state="disabled")
    btn_login.configure(state="active")
    lbl_msg.configure(text="You have beed logged out of your account",fg="green")
    btn_submit.configure(state="active")
    btn_shop.configure(state="disabled")
    btn_my_shop.configure(state="disabled")
    btn_admin.configure(state="disabled")
    insert_into_activities("logout",user_id,str(t3))
def submit():
    global txt_user2,txt_pass2,txt_cpas,txt_addr,lbl_msg2
    win_submit=tkinter.Toplevel(win)
    win_submit.title("Submit Panel")
    win_submit.geometry("350x300")
    win_submit.resizable(False,False)
##--------------------widgets--------------------    
    lbl_user2=tkinter.Label(win_submit,text="Username")
    lbl_user2.pack()
    txt_user2=tkinter.Entry(win_submit,width="15")
    txt_user2.pack()
    
    lbl_pass2=tkinter.Label(win_submit,text="Pasword")
    lbl_pass2.pack()
    txt_pass2=tkinter.Entry(win_submit,width="15")
    txt_pass2.pack()
    
    lbl_cpas=tkinter.Label(win_submit,text="Password Confirmation")
    lbl_cpas.pack()
    txt_cpas=tkinter.Entry(win_submit,width="15")
    txt_cpas.pack()
    
    lbl_addr=tkinter.Label(win_submit,text="Address")
    lbl_addr.pack()
    txt_addr=tkinter.Entry(win_submit,width="50")
    txt_addr.pack()

    lbl_msg2=tkinter.Label(win_submit,text="")
    lbl_msg2.pack()
    
    btn_submit2=tkinter.Button(win_submit,text="Submit",command=final_submit)
    btn_submit2.pack()
    
    win_submit.mainloop()
def get_submit_values():
    user=txt_user2.get()
    pas=txt_pass2.get()
    cpas=txt_cpas.get()
    addr=txt_addr.get()
    return (user,pas,cpas,addr)
def submit_validation():
    user,pas,cpas,addr=get_submit_values()
    if user=="" or pas=="" or cpas=="" or addr=="":
        lbl_msg2.configure(text="Please fill in required information",fg="red")
        return False
    query='''select * from users where username=?'''
    result=cnt.execute(query,(user,))
    rows=result.fetchall()
    if len(rows)>0:
        lbl_msg2.configure(text="Username already exists!",fg="red")
        return False
    if len(pas)<8:
        lbl_msg2.configure(text="Password must have at least 8 characters!",fg="red")
        return False
    if cpas!=pas:
        lbl_msg2.configure(text="Password and its confirmation are not the same!",fg="red")
        return False
    return True
    
def final_submit():
    t4=date.today()
    user,pas,cpas,addr=get_submit_values()
    result=submit_validation()
    if not(result):
        return
    query='''insert into users(username,password,addr) values(?,?,?)'''
    cnt.execute(query,(user,pas,addr))
    cnt.commit()
    query2='''select id from users where username=?'''
    result=cnt.execute(query2,(user,))
    rows=result.fetchall()
    idd=rows[0][0]
    lbl_msg2.configure(text="Submit done!",fg="green")
    txt_user2.delete("0","end")
    txt_pass2.delete("0","end")
    txt_cpas.delete("0","end")
    txt_addr.delete("0","end")
    insert_into_activities("submit",idd,str(t4))
def shop():
    global txt_pid,txt_qnt,lbl_msg3,lstbox
    win_shop=tkinter.Toplevel(win)
    win_shop.title("Shop")
    win_shop.geometry("400x400")
    win_shop.resizable(False,False)
    lbl_msg6=tkinter.Label(win_shop,text="Products")
    lbl_msg6.pack()
##---------listbox------------
    lstbox=tkinter.Listbox(win_shop,width="60")
    lstbox.pack(pady="10")
##-----------------------------
    update_shop_list()
    lbl_pid=tkinter.Label(win_shop,text="Product id")
    lbl_pid.pack()
    txt_pid=tkinter.Entry(win_shop,width="15")
    txt_pid.pack()
    lbl_qnt=tkinter.Label(win_shop,text="Quantity")
    lbl_qnt.pack()
    txt_qnt=tkinter.Entry(win_shop,width="15")
    txt_qnt.pack()
    lbl_msg3=tkinter.Label(win_shop,text="")
    lbl_msg3.pack()
    btn_final_shop=tkinter.Button(win_shop,text="Add to cart",command=add_to_cart)
    btn_final_shop.pack()

    win_shop.mainloop()
def update_shop_list():
    query='''select * from products'''
    result=cnt.execute(query)
    rows=result.fetchall()
    lstbox.delete(0,"end")
    for item in rows:
##      s=str(item[0])+"  "+"Pname: "+item[1]+"  "+"Price: "+str(item[2])+"  "+"Quantity: "+str(item[3])
        lstbox.insert("end",f"{item[0]}  Product: {item[1]}  Price: {item[2]}  Quantity: {item[3]}")
def add_to_cart():
    global t1
    a=(ValueError,sqlite3.ProgrammingError)
    try:
        pid=txt_pid.get()
        qnt=txt_qnt.get()
        uid=user_id
        if pid=="" or qnt=="":
            lbl_msg3.configure(text="Please fill the blanks",fg="red")
            return
        if int(pid)<0 or int(qnt)<0:
            lbl_msg3.configure(text="?!!!",fg="red")
            return
        query='''select * from products where id=?'''
        result=cnt.execute(query,(pid))
        rows=result.fetchall()
        if len(rows)==0:
            lbl_msg3.configure(text="The Product id does not exist!!!",fg="red")
            return
        row=rows[0]
        real_qnt=row[3]
        if int(qnt)>real_qnt:
            lbl_msg3.configure(text="The quantity you entered is higher than the quantity of the product",fg="red")
            return
##----------------------insert into final_shop----------------------
        t1=date.today()
        query='''insert into final_shop(pid,uid,qnt,date) values(?,?,?,?)'''
        cnt.execute(query,(pid,user_id,qnt,str(t1)))
        cnt.commit()
##------------------------update shop---------------------------
        new_qnt=real_qnt-int(qnt)
        query='''update products set qnt=? where id=?'''
        cnt.execute(query,(new_qnt,pid))
        cnt.commit()
##------------------------
        txt_pid.delete("0","end")
        txt_qnt.delete("0","end")
        lbl_msg3.configure(text="Product added to your cart successfully",fg="green")
        update_shop_list()
        insert_into_activities("add to cart",user_id,str(t1))
    except a:
        lbl_msg3.configure(text="Please enter a number in the fields",fg="red")
        return
def my_shop():
    global lstbox2,lbl_msg5
    win_my_shop=tkinter.Toplevel(win)
    win_my_shop.title("My Shop")
    win_my_shop.geometry("500x400")
    win_my_shop.resizable(False,False)

    lbl_msg7=tkinter.Label(win_my_shop,text="Add to cart History")
    lbl_msg7.pack()
    
    lstbox2=tkinter.Listbox(win_my_shop,width="75")
    lstbox2.pack(pady="10")

    btn_delete_history=tkinter.Button(win_my_shop,text="Delete History",command=delete_history)
    btn_delete_history.pack()

    lbl_msg5=tkinter.Label(win_my_shop,text="")
    lbl_msg5.pack()

    query='''select products.pname,products.price,final_shop.qnt,final_shop.date
    from final_shop
    join products
    on products.id=final_shop.pid
    where final_shop.uid=?'''
    result=cnt.execute(query,(user_id,))
    rows=result.fetchall()
    for item in rows:
        lstbox2.insert("end",f"Product:{item[0]}  Price:{item[1]}  Quantity:{item[2]}  Full price:{int(item[1]*int(item[2]))}  Date added:{item[3]}")
    
    win_my_shop.mainloop()
def admin_panel():
    global txt_pname2,txt_price,txt_qnt2,lbl_msg4,win_admin_panel
    win_admin_panel=tkinter.Toplevel(win)
    win_admin_panel.title("Admin Panel")
    win_admin_panel.geometry("400x400")
    win_admin_panel.resizable(False,False)
    lbl_pname2=tkinter.Label(win_admin_panel,text="Product name")
    lbl_pname2.pack()
    txt_pname2=tkinter.Entry(win_admin_panel,width="15")
    txt_pname2.pack()
    lbl_price=tkinter.Label(win_admin_panel,text="Price")
    lbl_price.pack()
    txt_price=tkinter.Entry(win_admin_panel,width="15")
    txt_price.pack()
    lbl_qnt2=tkinter.Label(win_admin_panel,text="Quantity")
    lbl_qnt2.pack()
    txt_qnt2=tkinter.Entry(win_admin_panel,width="15")
    txt_qnt2.pack()
    lbl_msg4=tkinter.Label(win_admin_panel,text="")
    lbl_msg4.pack()
    btn_add=tkinter.Button(win_admin_panel,text="Add Products",command=add_products)
    btn_add.pack()
    btn_update=tkinter.Button(win_admin_panel,text="Update",command=update_products)
    btn_update.pack()
    btn_delete=tkinter.Button(win_admin_panel,text="Delete Product",command=delete_product)
    btn_delete.pack()
    btn_activities=tkinter.Button(win_admin_panel,text="Activities",command=activities)
    btn_activities.pack()
    btn_reports=tkinter.Button(win_admin_panel,text="Reports",command=reports)
    btn_reports.pack()
    btn_delete_user=tkinter.Button(win_admin_panel,text="Delete user",command=delete_user)
    btn_delete_user.pack()
    
    win_admin_panel.mainloop()
def add_products():
    try:
        t6=date.today()
        pname=txt_pname2.get()
        price=txt_price.get()
        qnt=txt_qnt2.get()
        if pname=="" or price=="" or qnt=="":
            lbl_msg4.configure(text="Please leave no empty spaces!!",fg="red")
            return
        if int(price)<0 or int(qnt)<0:
            lbl_msg.configure(text="??!!",fg="red")
            return
        query='''select * from products where pname=?'''
        result=cnt.execute(query,(pname,))
        rows=result.fetchall()
        if len(rows)>0:
            lbl_msg4.configure(text="This Product already exists!",fg="red")
            return
        query2='''insert into products(pname,price,qnt)
    values(?,?,?)'''
        cnt.execute(query2,(pname,price,qnt))
        cnt.commit()
        lbl_msg4.configure(text="Product successfully added!",fg="green")
        txt_pname2.delete("0","end")
        txt_price.delete("0","end")
        txt_qnt2.delete("0","end")
        insert_into_activities("product addition",user_id,str(t6))
    except ValueError:
        lbl_msg4.configure(text="Please enter number for price and quantity fields!",fg="red")
        return
def update_products():
    try:
        t7=date.today()
        pname=txt_pname2.get()
        price=txt_price.get()
        qnt=txt_qnt2.get()
        if pname=="" or price=="" or qnt=="":
            lbl_msg4.configure(text="Please leave no empty spaces!!",fg="red")
            return
        if int(price)<0 or int(qnt)<0:
            lbl_msg.configure(text="??!!",fg="red")
            return
        query='''select * from products where pname=?'''
        result=cnt.execute(query,(pname,))
        rows=result.fetchall()
        if len(rows)==0:
            lbl_msg4.configure(text="This Product doesn't exist!",fg="red")
            return
        query2='''update products set price=?,qnt=? where pname=?'''
        cnt.execute(query2,(price,qnt,pname))
        cnt.commit()
        lbl_msg4.configure(text="Product successfully updated!",fg="green")
        txt_pname2.delete("0","end")
        txt_price.delete("0","end")
        txt_qnt2.delete("0","end")
        insert_into_activities("product update",user_id,str(t7))
    except ValueError:
        lbl_msg4.configure(text="Please enter number for price and quantity fields!",fg="red")
        return
def delete_product():
    try:
        pname=txt_pname2.get()
        price=txt_price.get()
        qnt=txt_qnt2.get()
        if pname=="" or price=="" or qnt=="":
            lbl_msg4.configure(text="Please leave no empty spaces!!",fg="red")
            return
        if int(price)<0 or int(qnt)<0:
            lbl_msg.configure(text="??!!",fg="red")
            return
        query='''select * from products where pname=? and price=? and qnt=?'''
        result=cnt.execute(query,(pname,price,qnt))
        rows=result.fetchall()
        if len(rows)==0:
            lbl_msg4.configure(text="This Product doesn't exist!(price or quantity might be incorrect)",fg="red")
            return
        query2='''delete from products where pname=? and price=? and qnt=?'''
        cnt.execute(query2,(pname,price,qnt))
        cnt.commit()
        lbl_msg4.configure(text="Product deleted successfully",fg="green")
        txt_pname2.delete("0","end")
        txt_price.delete("0","end")
        txt_qnt2.delete("0","end")
    except ValueError:
        lbl_msg4.configure(text="Please enter number for price and quantity fields!",fg="red")
        return
    
def delete_history():
    t5=date.today()
    lstbox2.delete("0","end")
    query='''delete from final_shop where uid=?'''
    cnt.execute(query,(user_id,))
    cnt.commit()
    lbl_msg5.configure(text="History was wiped successfully!",fg="green")
    insert_into_activities("delete history",user_id,str(t5))
def activities():
    win_activities=tkinter.Toplevel(win_admin_panel)
    win_activities.title("Activities")
    win_activities.geometry("450x400")
    win_activities.resizable(False,False)
    lstbox3=tkinter.Listbox(win_activities,width="70",height="20")
    lstbox3.pack()
    query='''select users.username,activities.activity,activities.date
    from activities
    join users
    on users.id=activities.uid'''
    result=cnt.execute(query)
    rows=result.fetchall()
    for item in rows:
        lstbox3.insert("end",f"Username:{item[0]}  Activity:{item[1]}  Date:{item[2]}")
        
    win_activities.mainloop()
def reports():
    global lstbox4
    win_reports=tkinter.Toplevel(win_admin_panel)
    win_reports.title("Reports")
    win_reports.geometry("450x400")
    win_reports.resizable(False,False)
    lstbox4=tkinter.Listbox(win_reports,width="70")
    lstbox4.pack()
    btn_need=tkinter.Button(win_reports,text="Most needed item",command=need)
    btn_need.pack()

    win_reports.mainloop()
def need_calculation():
    query='''select id from products'''
    result=cnt.execute(query)
    rows=result.fetchall()
    i=0
    for item in rows:
        i+=1
    for j in range(1,i+1):
        query='''select qnt from final_shop where pid=?'''
        result=cnt.execute(query,(j,))
        rows=result.fetchall()
        s=0
        for item in rows:
            s+=item[0]
        query2='''insert into totalp(pid,totalqnt) values(?,?)'''
        cnt.execute(query2,(j,s))
        cnt.commit()
    query3='''select pid,totalqnt from totalp'''
    result=cnt.execute(query3)
    rows=result.fetchall()
    ttlp=0
    for item in rows:
        if item[1]>ttlp:
            ttlp=item[1]
            z=item[0]
    return (ttlp,z)
def need():
    a,b=need_calculation()
    query='''select products.pname,products.price
             from totalp
             join products
             on products.id=totalp.pid
             where pid=?'''
    result=cnt.execute(query,(b,))
    rows=result.fetchall()
    for item in rows:
        lstbox4.insert("end",f"Product name:{item[0]}    Price:{item[1]}    total amount sold:{a}")
    query2='''delete from totalp'''
    cnt.execute(query2)
    cnt.commit()
def delete_user():
    global txt_user1,lbl_msg5
    win_delete_user=tkinter.Toplevel(win_admin_panel)
    win_delete_user.title("Delete user")
    win_delete_user.geometry("400x400")
    win_delete_user.resizable(False,False)
    lbl_user1=tkinter.Label(win_delete_user,text="Username")
    lbl_user1.pack()
    txt_user1=tkinter.Entry(win_delete_user,width="15")
    txt_user1.pack()
    lbl_msg5=tkinter.Label(win_delete_user,text="")
    lbl_msg5.pack()
    btn_delete_account=tkinter.Button(win_delete_user,text="Delete Account",command=final_delete)
    btn_delete_account.pack()
def final_delete():
    user=txt_user1.get()
    if user=="":
        lbl_msg5.configure(text="Please input the user",fg="red")
        return
    query='''delete from users where username=?'''
    cnt.execute(query,(user,))
    cnt.commit()
    lbl_msg5.configure(text="Account successfully deleted",fg="green")
    txt_user1.delete("0","end")
##------------------------------main-----------------------
win=tkinter.Tk()
win.title("Shop")
win.geometry("400x400")
win.resizable(False,False)
lbl_user=tkinter.Label(win,text="Username")
lbl_user.pack()
txt_user=tkinter.Entry(win,width="15")
txt_user.pack()
lbl_pass=tkinter.Label(win,text="Pasword")
lbl_pass.pack()
txt_pass=tkinter.Entry(win,width="15")
txt_pass.pack()
lbl_msg=tkinter.Label(win,text="")
lbl_msg.pack()
btn_login=tkinter.Button(win,text="Login",command=login)
btn_login.pack()
btn_logout=tkinter.Button(win,text="Logout",command=logout,state="disabled")
btn_logout.pack()
btn_submit=tkinter.Button(win,text="Submit",command=submit)
btn_submit.pack()
btn_shop=tkinter.Button(win,text="Shop",command=shop,state="disabled")
btn_shop.pack()
btn_my_shop=tkinter.Button(win,text="My Shop",command=my_shop,state="disabled")
btn_my_shop.pack()
btn_admin=tkinter.Button(win,text="Admin",state="disabled",command=admin_panel)
btn_admin.pack()
win.mainloop()
