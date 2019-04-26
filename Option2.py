from pymongo import MongoClient 
import sqlite3 as sq 
from Modules_Packages.aadhar_project import otpcheck as otpt,smsau as smau,emailau as emau
def func():
    aadhari=input("ENTER YOUR AADHAR NUMBER: ")
    if aadhari =='':
        print("NO AADHAR NUMBER ENTERED. TRY AGAIN LATER")
        return
    else:
        aadhar=int(aadhari)
        conn=MongoClient('localhost',27017)
        db=conn['AADHAR']
        AADHARINFO=db.AADHARINFO
        cursor=AADHARINFO.find_one({'AADHARNUM':aadhar})
        if cursor is None:
            print("NO AADHAR IN AADHAR DATABASE.REGISTER FOR AADHAR USING OPTION 1")
            return
        else:
            print("YOU CAN UPDATE ONLY NAME/CITY/STATE/PHONENUM")
            name1=int(input("DO YOU WANT TO UPDATE NAME? PRESS 1 TO UPDATE ELSE 0 FOR NO CHANGE: " ))
            if name1 ==1:
                name2=input("Enter your new name: ")
                new_name=name2
            else:
                new_name=cursor['NAME']
            city1=int(input("DO YOU WANT TO UPDATE CITY? PRESS 1 TO UPDATE ELSE 0 FOR NO CHANGE: " ))
            if city1==1:
                city2=input("Enter your new city: ")
                new_city=city2
            else:
                new_city=cursor['CITY']
            state1=int(input("DO YOU WANT TO UPDATE STATE? PRESS 1 TO UPDATE ELSE 0 FOR NO CHANGE: " ))
            if state1==1:
                state2=input("Enter your new state: ")
                new_state=state2
            else:
                new_state=cursor['STATE']
            phonenum1=int(input("DO YOU WANT TO UPDATE PHONENUM? PRESS 1 TO UPDATE ELSE 0 FOR NO CHANGE: " ))
            if phonenum1==1:
                phonenum2=int(input("Enter your new phone number: "))
                for i in str(phonenum2):
                    if i not in ['0','1','2','3','4','5','6','7','8','9'] or len(str(phonenum2))!=10:
                        s='Invalid mobile number'
                        s1=s+ " " + str(phonenum2)
                        return s1
                new_phonenum=phonenum2
            else:
                new_phonenum=cursor['PHONENUM']
            rt=otpt.otpcheck()
            if rt==1:
                updateaadhar(AADHARINFO,aadhar,new_name,new_city,new_state,new_phonenum)
                updatepan(cursor['PANNUM'],new_name,new_city,new_state,new_phonenum)
                smau.sendsms(aadhar)
                email1=input("enter your email :")
                emau.emailfunc(email1,aadhar)                
            else:
                print("invalid OTP or time out")
                return
            return

def updateaadhar(AADHARINFO,aadhar,new_name,new_city,new_state,new_phonenum):
    cursor=AADHARINFO.update_one({'AADHARNUM':aadhar},{'$set':{'NAME':new_name,'CITY':new_city,'STATE':new_state,'PHONENUM':new_phonenum}})
    print("AADHAR DETAILS UPDATED SUCCESSFULLY")
    return
def updatepan(pannum,new_name,new_city,new_state,new_phonenum):
    conn=sq.connect('pancard.db')
    query="UPDATE PANCARD SET NAME='{0}',CITY='{1}',STATE='{2}',PHONENUM={3} WHERE PANNUM='{4}'"
    query1=query.format(new_name,new_city,new_state,new_phonenum,pannum)
    result=conn.execute(query1)
    conn.commit()
    conn.close()
    return