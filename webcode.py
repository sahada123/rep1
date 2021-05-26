import os
from  flask import *
import  pymysql
from werkzeug.utils import secure_filename

obj=Flask(__name__)
con=pymysql.connect(host='localhost',port=3306,user='root',password='',db='arts management system')
cmd=con.cursor()
obj.secret_key='aaaaa'


@obj.route('/')
def main():
    # return render_template('indexnew.html')
    return render_template('login.html')


@obj.route('/login',methods=['post'])
def login():
    uname=request.form['textfield2']
    print(uname)
    pwd=request.form['textfield']
    print(pwd)
    cmd.execute("select * from login where username='"+uname+"' and password='"+pwd+"'")
    s=cmd.fetchone()
    if s is None:
        return '''<script>alert("invalid username or password");window.location='/'</script>'''
    elif s[3]=='admin':
        return '''<script>alert("Login Successfully");window.location='/home'</script>'''
    elif s[3]=='choreographer':
        session['lid'] = s[0]
        return '''<script>alert("Login Successfully");window.location='/chorehome'</script>'''
    elif s[3] == 'college':
        print(s)
        session['lid']=s[0]
        return '''<script>alert("Login Successfully");window.location='/collegehome'</script>'''
    elif s[3] == 'public':
        session['lid'] = s[0]
        return '''<script>alert("Login Successfully");window.location='/publichome'</script>'''
    elif s[3] == 'candidate':
        session['lid'] = s[0]
        return '''<script>alert("Login Successfully");window.location='/candyhome'</script>'''
    else:
        return '''<script>alert("invalid");window.location='/'</script>'''

@obj.route('/publichome')
def publichome():
    return render_template('publichome.html')

@obj.route('/publichome1')
def publichome1():
    return render_template('pub registration.html')
@obj.route('/publichome2',methods=['get','post'])
def publichome2():
    name=request.form['textfield']
    Place = request.form['textfield2']
    gender = request.form['radiobutton']
    Pin = request.form['textfield4']
    Phone = request.form['textfield3']
    Email = request.form['textfield6']
    Username = request.form['textfield7']
    Password = request.form['textfield8']
    Confirm = request.form['textfield9']
    if Password == Confirm:
        cmd.execute("insert into login values(null,'"+Username+"','"+Password+"','public')")
        lid=con.insert_id()
        cmd.execute("insert into public values (null,'"+str(lid)+"','"+name+"','"+Place+"','"+Phone+"','"+Pin+"','"+gender+"','"+Email+"')")
        con.commit()
        return '''<script>alert("Registered");window.location='/'</script>'''
    else:
        return '''<script>alert("Not match");window.location='/'</script>'''


@obj.route('/candyhome')
def candyhome():
        return render_template('candyhome.html')

@obj.route('/collegereg')
def collegereg():
    return render_template('college reg.html')

@obj.route('/collegereg1',methods=['get','post'])
def collegereg1():
    name=request.form['textfield']
    Place = request.form['textfield2']
    Post = request.form['textfield3']
    Pin = request.form['textfield4']
    Phone = request.form['textfield5']
    Email = request.form['textfield6']
    Username = request.form['textfield7']
    Password = request.form['textfield8']
    Confirm = request.form['textfield9']
    if Password == Confirm:
        cmd.execute("insert into login values(null,'"+Username+"','"+Password+"','pending')")
        lid=con.insert_id()
        cmd.execute("insert into college values (null,'"+str(lid)+"','"+name+"','"+Place+"','"+Post+"','"+Pin+"','"+Phone+"','"+Email+"')")
        con.commit()
        return '''<script>alert("Registered");window.location='/'</script>'''
    else:
        return '''<script>alert("Not match");window.location='/'</script>'''


@obj.route('/choreo')
def choreo():
    cmd.execute("select * from category")
    s=cmd.fetchall()
    return render_template('chore registration.html',val=s)

@obj.route('/choreo1',methods=['get','post'])
def choreo1():
    fname = request.form['textfield']
    lname = request.form['textfield54']
    Place = request.form['textfield2']
    Post = request.form['textfield3']
    Pin = request.form['textfield4']
    Phone = request.form['textfield5']
    Email = request.form['textfield6']
    Category = request.form['select']
    Username = request.form['textfield8']
    Password = request.form['textfield9']
    Confirm = request.form['textfield7']
    if Password==Confirm:
        cmd.execute("insert into login values(null,'" + Username + "','" + Password + "','pending')")
        lid = con.insert_id()
        cmd.execute("insert into choreographer values (null,'" + Category + "','" + str(lid) + "','" + fname + "','" + lname + "','" + Place + "','" + Post + "','" + Pin + "','" + Phone + "','" + Email + "')")
        con.commit()
        return '''<script>alert("Registered");window.location='/'</script>'''
    else:
        return '''<script>alert("Password Doesn't Match");window.location='/choreo'</script>'''


@obj.route('/candy')
def candy():
    cmd.execute("select * from candidate")
    s=cmd.fetchall()
    cmd.execute("select * from category")
    s1 = cmd.fetchall()
    return render_template('add candy.html',val=s, val1=s1)


@obj.route('/candy1',methods=['get','post'])
def candy1():
    Fname = request.form['textfield']
    Lname = request.form['textfield2']
    Place = request.form['textfield3']
    Post = request.form['textfield4']
    Pin = request.form['textfield5']
    Phone = request.form['textfield6']
    Email = request.form['textfield7']
    category = request.form['select']
    # Username = request.form['textfield8']
    # Password = request.form['textfield9']
    cmd.execute("insert into login values(null,'" + Email + "','" + Phone + "','candidate')")
    lid = con.insert_id()
    cmd.execute("insert into candidate values (null,'" + str(lid) + "','" + str(session['lid']) + "','" + Fname + "','" + Lname + "','" + Place + "','" + Post + "','" + Pin + "','" + Phone + "','" + Email + "','" + category + "')")
    con.commit()
    return '''<script>alert("Registered");window.location='/collegehome'</script>'''

@obj.route('/view_candy')
def view_candy():
    cmd.execute("select * from candidate where loginid='"+str(session['lid'])+"'")
    s = cmd.fetchone()
    return render_template('update candy.html',val=s)

@obj.route('/update_candy' ,methods=['post','get'])
def update_candy():
    Fname = request.form['textfield']
    Lname = request.form['textfield2']
    Place = request.form['textfield3']
    Post = request.form['textfield4']
    Pin = request.form['textfield5']
    Phone = request.form['textfield6']
    Email = request.form['textfield7']
    cmd.execute("update candidate set fname='" + Fname + "',Lname='" + Lname + "',Place='" + Place + "',Post='" + Post + "',Pin='" + Pin + "',Phone='" + Phone + "',Email='" + Email + "' where loginid='"+str(session['lid'])+"'")
    con.commit()
    return '''<script> alert("success"); window.location="/candyhome"</script>'''


@obj.route('/change_pass')
def change_pass():
    # cmd.execute("SELECT `login`.`password`FROM `login`JOIN`candidate`ON`login`.`loginid`=`candidate`.`loginid`WHERE`candidate`.`loginid`='" + str(session['lid']) + "'")
    # s = cmd.fetchone()
    return render_template('change password.html')
#

@obj.route('/change_pass1',methods=['post','get'])
def change_pass1():
    # New_username = request.form['textfield']
    current_password = request.form['textfield2']
    new_password = request.form['textfield3']
    confirm_password = request.form['textfield4']

    cmd.execute("SELECT * FROM `login` where loginid='"+str(session['lid'])+"'")
    s = cmd.fetchone()
    if s[2]==current_password:
        if  new_password==confirm_password:
            cmd.execute(" UPDATE `login` SET `password`='"+confirm_password+"' where login.loginid='"+str(session['lid'])+"' ")
            con.commit()
            return '''<script> alert("success"); window.location="/candyhome"</script>'''
        else:
            return '''<script> alert("Failed"); window.location="/candyhome"</script>'''
    else:
        return '''<script> alert("Changing Failed"); window.location="/candyhome"</script>'''





@obj.route('/view category')
def view_category():
    cmd.execute("select * from category")
    s = cmd.fetchall()
    return render_template('view category.html',val=s)


# @obj.route('/search_choreo')
# def search_choreo():
#     cid=request.args.get('id')
#     # cmd.execute("SELECT * FROM `choreographer` WHERE `loginid` NOT IN(SELECT `chorid` FROM `schedule` WHERE '" + str(session['date']) + "'>15) AND `categoryid`='" + str(id) + "'")
#     # s = cmd.fetchall()
#     # cmd.execute("SELECT `choreographer`.*,`category`.* FROM `category` JOIN `choreographer` ON `choreographer`.`categoryid`=`category`.`categoryid` WHERE `choreographer`.`categoryid`='"+str(cid)+"'")
#     # s=cmd.fetchall()
#     return render_template('search choreo.html')
#
#
@obj.route('/searchchor',methods=['post','get'])
def searchchor():
    try:
        print("okkkkkkkkkkkkkkkkkkkkkkkkk")
        Eventdate= request.form['textfield']
        print(Eventdate)
        session['ed']=Eventdate
        cmd.execute("SELECT `schedule`.`chorid` ,DATEDIFF(`date`, '"+Eventdate+"'),DATEDIFF( '"+Eventdate+"',DATE) FROM `schedule`  ")
        s = cmd.fetchall()
        print("s",s)
        lid=["0"]
        for r in s:
            d1=abs(int(r[1]))
            d2=abs(int(r[2]))
            if d1<15 or d2<15:
                lid.append(str(r[0]))
        print("okkkkkkkkkkkkkkkkkkkkkkkkkk")
        print("SELECT * FROM `choreographer` WHERE `categoryid`='"+str(session['catid'])+"' AND `loginid` NOT IN("+','.join(lid)+")")
        cmd.execute("SELECT * FROM `choreographer` WHERE `categoryid`='"+str(session['catid'])+"' AND `loginid` NOT IN("+','.join(lid)+")")
        b=cmd.fetchall()
        print(b)
        return render_template('search choreo.html', val1=b)
    except:
        Eventdate=session['ed']
        cmd.execute(
            "SELECT `schedule`.`chorid` ,DATEDIFF(`date`, '" + Eventdate + "'),DATEDIFF( '" + Eventdate + "',DATE) FROM `schedule`  ")
        s = cmd.fetchall()
        print("s", s)
        lid = ["0"]
        for r in s:
            d1 = abs(int(r[1]))
            d2 = abs(int(r[2]))
            if d1 < 15 or d2 < 15:
                lid.append(str(r[0]))
        print("okkkkkkkkkkkkkkkkkkkkkkkkkk")
        print("SELECT * FROM `choreographer` WHERE `categoryid`='" + str(
            session['catid']) + "' AND `loginid` NOT IN(" + ','.join(lid) + ")")
        cmd.execute("SELECT * FROM `choreographer` WHERE `categoryid`='" + str(
            session['catid']) + "' AND `loginid` NOT IN(" + ','.join(lid) + ")")
        b = cmd.fetchall()
        print(b)
        return render_template('search choreo.html', val1=b)



@obj.route('/search_choreo')
def search_choreo():
    cid = request.args.get('id')
    session['catid']=cid
    # cmd.execute("SELECT * FROM `choreographer` WHERE `loginid` NOT IN(SELECT `chorid` FROM `schedule` WHERE '" + str(session['date']) + "'>15) AND `categoryid`='" + str(id) + "'")
    # s = cmd.fetchall()
    # cmd.execute(searchchor"SELECT `choreographer`.*,`category`.* FROM `category` JOIN `choreographer` ON `choreographer`.`categoryid`=`category`.`categoryid` WHERE `choreographer`.`categoryid`='"+str(cid)+"'")
    # s=cmd.fetchall()
    return render_template('search choreo.html')


@obj.route('/phone', methods=['get', 'post'])
def phone():
    cid=request.args.get('id')
    session['cid']=cid
    date=session['ed']

    cmd.execute("SELECT * FROM `public_request` WHERE `chorid`='" + str(cid) + "' AND `userid`='"+str(session['lid'])+"'")
    s = cmd.fetchone()
    print(s, "sss")
    if s is None:
        cmd.execute("insert into public_request values(null,'" + str(session['lid']) + "','" + str(cid) + "','" + str(date) + "','pending')")
        con.commit()
        return '''<script> alert("success"); window.location="/publichome"</script>'''
    else:
        return '''<script> alert("already exist"); window.location="/publichome"</script>'''



@obj.route('/public_send_reqst',methods=['get','post'])
def public_send_reqst():
    chid=session['cid']
    print(chid,"chhhh")
    date=session['ed']

    place=request.form['textfield']
    post = request.form['textfield2']
    pin = request.form['textfield3']
    phone = request.form['textfield4']
    email = request.form['textfield5']
    name = request.form['textfield6']

    cmd.execute("SELECT * FROM `public_request` WHERE `chorid`='"+str(chid)+"' AND `phone`='"+phone+"'")
    s=cmd.fetchone()
    print(s,"sss")
    if s is None:
        cmd.execute("insert into public_request values(null,'"+str(phone)+"','"+str(chid)+"','"+str(date)+"','pending','"+str(place)+"','"+str(post)+"','"+str(pin)+"','"+str(email)+"','"+str(name)+"')")
        con.commit()
        return  '''<script> alert("success"); window.location="/publichome"</script>'''
    else:
        return '''<script> alert("already exist"); window.location="/publichome"</script>'''










@obj.route('/home')
def home():
    return render_template('adhome.html')

@obj.route('/accept',methods=['post','get'])
def accept():
    id=request.args.get('lid')
    cmd.execute("update login set login.type='choreographer' where loginid='"+str(id)+"'")
    con.commit()
    return '''<script>alert("Accepted");window.location='/choreographer'</script>'''


@obj.route('/reject' ,methods=['post','get'])
def reject():
    id=request.args.get('lid')
    cmd.execute("delete from login where loginid='" + str(id) + "'")
    cmd.execute("delete from choreographer where `choreographer`.loginid='" + str(id) + "'")
    con.commit()
    return '''<script>alert("Rejected");window.location='/choreographer'</script>'''



@obj.route('/accept_college',methods=['post','get'])
def accept_college():
    id=request.args.get('lid')
    cmd.execute("update login set login.type='college' where loginid='"+str(id)+"'")
    con.commit()
    return '''<script>alert("Accepted");window.location='/View and approve college'</script>'''

@obj.route('/reject_college' ,methods=['post','get'])
def reject_college():
    id=request.args.get('lid')
    # cmd.execute("delete from login where loginid='" + str(id) + "'")
    cmd.execute("UPDATE `login` SET `login`.`type`='reject' WHERE `login`.`loginid`='"+str(id)+"'")
    con.commit()
    return '''<script>alert("Rejected");window.location='/View and approve college'</script>'''


@obj.route('/accepted_status')
def accepted_status():
    cmd.execute("SELECT`college`.*,`event`.*,`request for choreographer`.* FROM `college` JOIN`event` ON `event`.`collid`=`college`.loginid JOIN `request for choreographer` ON `request for choreographer`.`eventid`=`event`.`eventid` WHERE `request for choreographer`.`chorid`='"+str(session['lid'])+"' and `request for choreographer`.status='accept'")
    s=cmd.fetchall()
    return render_template('accepted status.html',val=s)

@obj.route('/view_assigned_choreo')
def view_assigned_choreo():
    cmd.execute("SELECT `assign`.*,`choreographer`.*,`category`.* FROM `assign` INNER JOIN`choreographer` ON `assign`.`chorid`=`choreographer`.`chorid` INNER JOIN `category` ON `category`.`categoryid`=`choreographer`.`categoryid` WHERE `assign`.`candid`='"+str(session['lid'])+"'")
    s=cmd.fetchall()
    return render_template('view assigned choreo.html',val=s)



@obj.route('/add_event',methods=['post','get'])
def add_event():
    return render_template('add event.html')



@obj.route('/add_event1' ,methods=['post','get'])
def add_event1():
    event=request.form['textfield']
    Date = request.form['Date']
    Time = request.form['Time']
    print(Date)
    print(Time)
    cmd.execute("INSERT INTO `event` VALUES(NULL,'"+event+"','"+str(session['lid'])+"','"+Date+"','"+Time+"','pending')")

    con.commit()
    return '''<script> alert("success"); window.location="/manage_event"</script>'''




@obj.route('/manage_event')
def manage_event():
    cmd.execute("SELECT `event`.* FROM `event` JOIN `college` ON `college`.`loginid`=`event`.`collid` WHERE `event`.`status`='pending' AND `event`.`collid`='"+str(session['lid'])+"'")
    s = cmd.fetchall()
    return render_template('manage event.html',val=s)



@obj.route('/send_reqst',methods=['get','post'])
def send_reqst():
    chid=request.args.get('id')
    print(chid,"chhhh")
    eid= session['iid']
    cmd.execute("SELECT `collid`,`chorid` FROM `request for choreographer` WHERE `collid`='"+str(session['lid'])+"' AND `chorid`='"+str(chid)+"' and eventid='"+str(eid)+"' ")
    s=cmd.fetchone()
    print(s,"sss")
    if s is None:
        cmd.execute("insert into `request for choreographer` values(null,'"+str(chid)+"','"+str(eid)+"',curdate(),'pending','"+str(session['lid'])+"')")
        con.commit()
        return  '''<script> alert("success"); window.location="/collegehome"</script>'''
    else:
        return '''<script> alert("already exist"); window.location="/collegehome"</script>'''




@obj.route('/manage_event_edit')
def manage_event_edit():
    eid=request.args.get('eventid')
    session['id']=eid
    print(eid)
    cmd.execute(" SELECT * FROM EVENT WHERE eventid='"+str(eid)+"'")
    s = cmd.fetchone()
    print(s)
    return render_template('edit event.html',val=s)

@obj.route('/manage_event_edit2',methods=['post','get'])
def manage_event_edit2():
    event = request.form['textfield']
    Date = request.form['Date']
    Time = request.form['Time']
    cmd.execute("update event set event='"+event+"',Date='"+Date+"',Time='"+Time+"' where eventid='" + str(session['id']) + "'")
    con.commit()
    return '''<script> alert("success"); window.location="/collegehome"</script>'''

@obj.route('/manage_event_delete',methods=['get','post'])
def manage_event_delete():
    id=request.args.get('id')
    cmd.execute("UPDATE `event` SET `status`='reject' WHERE `eventid`='"+str(id)+"'")
    con.commit()
    return '''<script> alert("success"); window.location="/manage_event"</script>'''


@obj.route('/manage_event_send_request ')
def manage_event_send_request():
    id = request.args.get('id')
    cmd.execute("select * from choreographer WHERE `categoryid`=")
    s = cmd.fetchall()
    return render_template('v&book choreo.html',val=s)

@obj.route('/view_category_for_event')
def view_category_for_event():
    cmd.execute("select * from category")
    s = cmd.fetchall()
    return render_template('view category.html',val=s)

@obj.route('/assign')
def assign():
    cmd.execute("select * from event WHERE event.collid='"+str( session['lid'])+"'")
    s = cmd.fetchall()
    return render_template('assign.html',val=s)

# @obj.route('/assign_choreo')
# def assign_choreo():
#     return render_template('assign choreo.html')


@obj.route('/assign_choreo1',methods=['post','get'])
def assign_choreo1():
    Choreographer = request.form['select']

    Candidate = request.form['select2']
    print(Choreographer)
    print(Candidate)
    cmd.execute("insert into assign VALUES(null, '" + Choreographer + "','" + Candidate + "')")
    con.commit()
    return '''<script> alert("success"); window.location="/assign_choreo"</script>'''


@obj.route('/assign_choreo',methods=['post','get'])
def assign_choreo2():
    cmd.execute("select * from choreographer")
    s1 = cmd.fetchall()
    cmd.execute("select * from candidate ")
    s = cmd.fetchall()
    return render_template('assign choreo.html',val=s,vals=s1)


# @obj.route('/request2')
# def request2():
#     cmd.execute(" insert into request for choreographer values(null,'"+str(session['lid'])+"','"+ +"','"+Date+"'")
#     return render_template('/manage_event')

@obj.route('/choreographer')
def choreographer():
    cmd.execute("SELECT `choreographer`.*,`login`.`type` FROM `login` JOIN `choreographer` ON `choreographer`.`loginid`=`login`.`loginid` WHERE `login`.`type`='pending'")
    s = cmd.fetchall()
    return render_template('v & approve choreographer.html', val=s)

@obj.route('/View and approve college')
def View_and_approve_college():
    cmd.execute("SELECT `college`.*,`login`.`type` FROM `login` JOIN `college` ON `college`.`loginid`=`login`.`loginid` WHERE `login`.`type`='pending'")
    s = cmd.fetchall()
    return render_template('V&Approve college.html', val=s)


@obj.route('/chore_view_event')
def chore_view_event():
    cmd.execute("SELECT`college`.*,`event`.*,`request for choreographer`.* FROM `college` JOIN`event` ON `event`.`collid`=`college`.loginid JOIN `request for choreographer` ON `request for choreographer`.`eventid`=`event`.`eventid` WHERE `request for choreographer`.`chorid`='"+str(session['lid'])+"' and `request for choreographer`.status='pending'")

    s = cmd.fetchall()


    return render_template('chore view event.html',val=s)


@obj.route('/chore_accept_event_reqst', methods=['post', 'get'])
def chore_accept_event_reqst():
    id = request.args.get('id')
    print(id,"idddddddddd")
    cmd.execute("SELECT `event`.`date`,`request for choreographer`.chorid FROM `event` JOIN`request for choreographer` ON`request for choreographer`.`eventid`=`event`.`eventid` WHERE`request for choreographer`.`reqestid`='"+str(id)+"'")
    s=cmd.fetchone()
    rdate=str(s[0])
    chid=str(s[1])
    print(rdate)
    cmd.execute("UPDATE  `request for choreographer` SET `status`='accept' WHERE `reqestid`='"+str(id)+"' ")
    con.commit()

    cmd.execute("UPDATE  schedule SET `status`='Unavailable' WHERE `date`='" + rdate + "' and chorid='"+chid+"'")

    con.commit()
    return '''<script>alert("Accepted");window.location='/chore_view_event'</script>'''



@obj.route('/chore_reject_event_reqst' ,methods=['post','get'])
def chore_reject_event_reqst():

    id=request.args.get('id')
    # cmd.execute("DELETE FROM `request for choreographer` WHERE `reqestid`='" + str(id) + "'")
    cmd.execute("UPDATE  `request for choreographer` SET `status`='reject' WHERE `reqestid`='"+str(id)+"'")
    con.commit()
    return '''<script>alert("Rejected");window.location='/chore_view_event'</script>'''



@obj.route('/view_request_status')
def view_request_status():
    cmd.execute(" SELECT `event`.*,`request for choreographer` .*,choreographer .* FROM `request for choreographer` JOIN `choreographer` ON `request for choreographer`.chorid=choreographer.loginid JOIN `event` ON `event`.`eventid`=`request for choreographer`.`eventid` WHERE event.collid='"+str(session['lid'])+"'")
    s = cmd.fetchall()
    print(s)
    cmd.execute("select *from candidate")
    a = cmd.fetchall()
    return render_template('choreo respond.html', val=s, vals=a)

@obj.route('/assign_candy')
def assign_candy():
    id = request.args.get('caid')
    cid=request.args.get('cid')
    print(id)
    session['id'] = id
    print("SELECT * FROM `candidate` where  `collid`='"+str(session['lid'])+"' AND `category`='" + str(cid) + "'")
    cmd.execute("SELECT * FROM `candidate` where  `collid`='"+str(session['lid'])+"' AND `category`='" + str(cid) + "'")
    # cmd.execute("SELECT * FROM `candidate` where `category`='" + str(id) + "' AND `collid`='" + str(session['lid']) + "' AND `candidate`.`loginid` NOT IN (SELECT `candid` FROM `assign`)")

    s=cmd.fetchall()
    return render_template('assign choreo.html',val=s)

@obj.route('/assign_candy1',methods=['post','get'])
def assign_candy1():
    Candidate = request.form['select']
    cmd.execute("insert into assign VALUES(null, '" + str(session['id']) + "','" + str(Candidate) + "')")
    con.commit()
    return '''<script> alert("success"); window.location="/collegehome"</script>'''



@obj.route('/assign_choreographer')
def assign_choreographer():
    return render_template('choreo respond.html')



@obj.route('/date')
def date():
    return render_template('date.html')

@obj.route('/collegehome')
def collegehome():
    return render_template('collegehome.html')



@obj.route('/dummy')
def dummy():
    return render_template('dummy.html')


@obj.route('/chorehome')
def chorehome():
    return render_template('chorehome.html')

@obj.route('/Add category')
def Add_category():
    return render_template('add category.html')

@obj.route('/Add_category1',methods=['get','post'])
def Add_category1():
    cat=request.form['textfield']
    cmd.execute("INSERT INTO `category` VALUES(NULL,'"+cat+"')")
    con.commit()
    return '''<script> alert("success"); window.location="home"</script>'''

@obj.route('/candidatehome')
def candidatehome():
    return render_template('candyhome.html')

# @obj.route('/view_and_book_choreographer_pub')
# def view_and_book_choreographer_pub():
#     id=request.args.get('id')
#     cmd.execute("SELECT * FROM `choreographer` WHERE `loginid` NOT IN(SELECT `chorid` FROM `schedule` WHERE '" + str(session['date']) + "'>15) AND `categoryid`='" + str(id) + "'")
#     s = cmd.fetchall()
#     # cmd.execute("SELECT `choreographer`.* FROM `choreographer` JOIN `schedule` ON `choreographer`.`loginid`=`schedule`.`chorid` WHERE `schedule`.`status`='available' AND `choreographer`.`categoryid`='"+str(id)+"'")
#     # s = cmd.fetchall()
    return render_template('v&book choreopub.html',val=s)

@obj.route('/view_and_book_choreographer')
def view_and_book_choreographer():
    id=request.args.get('id')
    # date=session['date']
    # print(date)
    # print("SELECT `choreographer`.* FROM `choreographer` JOIN `schedule` ON `schedule`.`chorid`=`choreographer`.`loginid` AND `schedule`.`date`='"+str(date)+"' AND `schedule`.`status`='available' and `choreographer`.`categoryid`='"+id+"'")
    # cmd.execute("SELECT `choreographer`.* FROM `choreographer` JOIN `schedule` ON `schedule`.`chorid`=`choreographer`.`loginid` AND `schedule`.`date`='"+str(date)+"' AND `schedule`.`status`='available' and `choreographer`.`categoryid`='"+id+"'")

    print("SELECT * FROM `choreographer` WHERE `loginid` NOT IN(SELECT `chorid` FROM `schedule` WHERE DATEDIFF('"+str(session['date'])+"',date)<15) AND `categoryid`='"+str(id)+"'")
    cmd.execute("SELECT * FROM `choreographer` WHERE `loginid` NOT IN(SELECT `chorid` FROM `schedule` WHERE DATEDIFF('"+str(session['date'])+"',date)<15) AND `categoryid`='"+str(id)+"'")
    s = cmd.fetchall()
    return render_template('v&book choreo.html',val=s)

@obj.route('/view_cat')
def view_cat():
    id=request.args.get('id')
    date=request.args.get('date')
    print(date)
    session['date']=date
    session['iid']=id
    cmd.execute("select * from category")
    s = cmd.fetchall()
    return render_template('view cat.html',val=s)

@obj.route('/view_schedule')
def view_schedule():
    id=request.args.get('id')
    session['id']=id
    cmd.execute("SELECT  * FROM `schedule` WHERE `status`='available' AND `chorid`='"+str(id)+"' ORDER BY DATE ASC ")
    # cmd.execute("SELECT * FROM SCHEDULE WHERE `chorid`='"+str(session['id'])+"' ")
    s = cmd.fetchall()
    return render_template('view schedule.html',val=s)





@obj.route('/add_schedule',methods=['post','get'])
def add_schedule():
    return render_template('add sced.html')


@obj.route('/add_schedule1' ,methods=['post','get'])
def add_schedule1():
    From_time = request.form['time']
    To_time = request.form['time1']
    Date= request.form['Date']
    print(From_time)
    print(To_time)
    print(Date)
    cmd.execute("INSERT INTO `schedule` VALUES(NULL,'"+str(session['lid'])+"','"+From_time+"','"+To_time+"','"+Date+"','unavailable')")
    con.commit()
    return '''<script> alert("success"); window.location="/add_schedule"</script>'''

@obj.route('/mng_schedule')
def mng_schedule():
    cmd.execute("SELECT * FROM `schedule` WHERE STATUS !='rejected' AND `chorid`='"+str(session['lid'])+"'")
    s = cmd.fetchall()
    return render_template('manage choreo schedule.html',val=s)

@obj.route('/mng_schedule_delete' ,methods=['post','get'])
def mng_schedule_delete():
    id=request.args.get('lid')
    cmd.execute("delete from schedule where `schedule`.schedid='" + str(id) + "'")

    return '''<script>alert("deleted");window.location='/mng_schedule'</script>'''

@obj.route('/update_choreo_sched1', methods=['post','get'])
def update_choreo_sched1():
    id=request.args.get('lid')
    session['id'] = id
    cmd.execute("SELECT * FROM `schedule` WHERE schedid='" + str(session['id']) + "'")
    s = cmd.fetchone()
    return render_template('update choreo sched.html', val=s)

@obj.route('/update_choreo_sched' ,methods=['post','get'])
def update_choreo_sched():
    time = request.form['time']
    time1 = request.form['time1']
    Date = request.form['Date']
    print(time)
    print(time1)
    print(Date)
    cmd.execute("update schedule set fromtime='"+time+"',totime='"+time1+"',date='"+Date+"'  where schedid='" + str(session['id']) + "'")
    con.commit()
    return '''<script> alert("success"); window.location="/mng_schedule"</script>'''


@obj.route('/view_sched' ,methods=['post','get'])
def view_sched():
    id=request.args.get('id')
    cmd.execute("select * from schedule WHERE `schedid`="+id)
    s = cmd.fetchall()
    return render_template('add schedule.html',val=s)

@obj.route('/manage_category')
def manage_category():

    cmd.execute("SELECT * FROM `category`")
    s = cmd.fetchall()
    return render_template('manage category.html',val=s)

@obj.route('/delete_category1' ,methods=['post','get'])
def delete_category1():
    id=request.args.get('lid')
    cmd.execute("delete from category where `category`.categoryid='" + str(id) + "'")
    con.commit()
    return '''<script>alert("deleted");window.location='/manage_category'</script>'''


@obj.route('/assigned_candy')
def assigned_candy():
    cmd.execute("SELECT `category`.`category`,`candidate`.`fname`,`candidate`.`lname`,`candidate`.`place`,`candidate`.`phone`,`assign`.* FROM `candidate` JOIN `category` ON `candidate`.`category`=`category`.`categoryid` JOIN `assign` ON `assign`.`candid`=`candidate`.`loginid` WHERE `assign`.`chorid`='"+str(session['id'])+"'")
    s = cmd.fetchall()
    return render_template('choreo view assigned candy.html',val=s)

@obj.route('/chore_request_for_event')
def chore_request_for_event():
    cmd.execute("SELECT `event`.*,`college`.`collname` FROM `college`JOIN`event`ON `college`.`loginid`=`event`.`collid` WHERE `event`.`status`='pending'")

    s = cmd.fetchall()


    return render_template('chore view and request for event.html',val=s)

@obj.route('/send_reqstc',methods=['get','post'])
def send_reqstc():
    eid=request.args.get('id')

    cmd.execute("SELECT `eventid`,`chorid` FROM  `rqst for college` WHERE  `chorid`='" + str(session['lid']) + "' AND `eventid`='"+str(eid)+"'")
    s = cmd.fetchone()
    chid= session['lid']
    if s is None:
        cmd.execute("INSERT INTO `rqst for college` VALUES(NULL,'"+str(chid)+"','"+str(eid)+"',CURDATE(),'pending')")
        con.commit()
        return  '''<script> alert("success"); window.location="/chorehome"</script>'''
    else:
         return '''<script> alert("already exist"); window.location="/chorehome"</script>'''


@obj.route('/college_view_event_request')
def college_view_event_request():
    print("SELECT `choreographer`.`fname`,`choreographer`.`lname`,`category`,`reqstcid` FROM `rqst for college`JOIN`event`ON `rqst for college`.`eventid`=`event`.`eventid`JOIN`choreographer`ON`choreographer`.loginid=`rqst for college`.`chorid`JOIN `category`ON `category`.`categoryid`=`choreographer`.`categoryid`AND `event`.`collid`='" + str( session['lid']) + "' AND `rqst for college`.`status`='pending'")

    cmd.execute("SELECT `choreographer`.`fname`,`choreographer`.`lname`,`category`,`reqstcid`,`choreographer`.`phone`,`choreographer`.`email`,`event`.`event` FROM `rqst for college`JOIN`event`ON `rqst for college`.`eventid`=`event`.`eventid`JOIN`choreographer`ON`choreographer`.loginid=`rqst for college`.`chorid`JOIN `category`ON `category`.`categoryid`=`choreographer`.`categoryid`AND `event`.`collid`='" + str( session['lid']) + "' AND `rqst for college`.`status`='pending'")

    s = cmd.fetchall()


    return render_template('accept choreo reqst.html',val=s)




@obj.route('/college_accept_event_reqst', methods=['post', 'get'])
def college_accept_event_reqst():
    id = request.args.get('id')
    print(id)
    # cmd.execute("SELECT `event`.`date`,`rqst for college`.chorid FROM `event` JOIN`rqst for college` ON`rqst for college`.`eventid`=`event`.`eventid` WHERE`rqst for college`.`reqstcid`='"+str(id)+"'")
    # s=cmd.fetchone()
    # rdate=str(s[0])
    # chid=str(s[1])
    # print(rdate)
    cmd.execute(" UPDATE `rqst for college` SET `rqst for college`.`status`='accept' WHERE `rqst for college`.`reqstcid`='"+str(id)+"' ")
    con.commit()

    # cmd.execute("UPDATE  schedule SET `status`='Unavailable' WHERE `date`='" + rdate + "' and chorid='"+chid+"'")
    #
    # con.commit()
    return '''<script>alert("Accepted");window.location='/college_view_event_request'</script>'''



@obj.route('/college_reject_event_reqst' ,methods=['post','get'])
def college_reject_event_reqst():

    id=request.args.get('id')
    # cmd.execute("DELETE FROM `request for choreographer` WHERE `reqestid`='" + str(id) + "'")
    cmd.execute(" UPDATE `rqst for college` SET `rqst for college`.`status`='reject' WHERE `rqst for college`.`reqstcid`='"+str(id)+"'")
    con.commit()
    return '''<script>alert("Rejected");window.location='/college_view_event_request'</script>'''


@obj.route('/view_request_status_of_choreo')
def view_request_status_of_choreo():
    cmd.execute(" SELECT DISTINCT `event`.`event`,`college`.`collname` ,`rqst for college`.* FROM `college` INNER JOIN `event` ON `event`.`collid`=`college`.`loginid` INNER JOIN `rqst for college` ON `rqst for college`.`eventid`=`event`.`eventid` AND `rqst for college`.`chorid`='"+str(session['lid'])+"'")
    s = cmd.fetchall()
    return render_template('view responce of college.html', val=s)


@obj.route('/accepted_status_of_choreo')
def accepted_status_of_choreo():
    cmd.execute("SELECT  `event`.*,`choreographer`.*,`rqst for college`.*,`category`.`category`,`choreographer`.`fname`,`lname`,`category`.`categoryid`,`choreographer`.`loginid` FROM `choreographer` JOIN `category`  ON `choreographer`.`categoryid`=`category`.`categoryid` JOIN `rqst for college` ON `rqst for college`.`chorid`=`choreographer`.`loginid` INNER JOIN `event` ON `event`.`eventid`=`rqst for college`.`eventid` INNER JOIN `college` ON `college`.`loginid`=`event`.`collid` AND `rqst for college`.`status`='accept' AND `college`.`loginid` = '"+str(session['lid'])+"'")
    # `college`.`loginid` = '"+str(session['lid'])+"'
    s=cmd.fetchall()
    return render_template('accepted details of choreo.html',val=s)


@obj.route('/assign_candy_for_direct_view')
def assign_candy_for_direct_view():
    id = request.args.get('caid')
    choid=request.args.get('cid')
    session['choid'] = choid
    cmd.execute("SELECT * FROM `candidate` where `category`='" + str(id) + "' AND `collid`='" + str(session['lid']) + "' AND `candidate`.`loginid` NOT IN (SELECT `candid` FROM `assign`)")
    s = cmd.fetchall()
    return render_template('assign choreo direct rqst.html',val=s)


@obj.route('/assign_candy_for_direct_view1',methods=['post','get'])
def assign_candy_for_direct_view1():
    Candidate = request.form['select']
    cmd.execute("insert into assign VALUES(null, '" + str(session['choid']) + "','" + str(Candidate) + "')")
    con.commit()
    return '''<script> alert("success"); window.location="/collegehome"</script>'''

@obj.route('/choreo_view_accepted_status')
def choreo_view_accepted_status():
    cmd.execute("SELECT  `event`.*,`college`.*,`rqst for college`.*,`category`.`category`,`choreographer`.`fname`,`lname`,`category`.`categoryid`,`choreographer`.`loginid` FROM `choreographer` JOIN `category`  ON `choreographer`.`categoryid`=`category`.`categoryid` JOIN `rqst for college` ON `rqst for college`.`chorid`=`choreographer`.`loginid` INNER JOIN `event` ON `event`.`eventid`=`rqst for college`.`eventid` INNER JOIN `college` ON `college`.`loginid`=`event`.`collid`  AND `choreographer`.`loginid`='"+str(session['lid'])+"'")

    s=cmd.fetchall()
    return render_template('choreo_view_accepted_status.html',val=s)


@obj.route('/add_troupe')
def add_troupe():

    return render_template('add troupe.html')


@obj.route('/add_troupe1',methods=['post'])
def add_troupe1():
    troupe = request.form['textfield']
    category = request.form['textfield66']

    contact = request.form['textfield2']
    email=request.form['textfield3']
    image = request.files['file']
    img=secure_filename(image.filename)
    path=r"./static/troupe"
    image.save(os.path.join(path,img))
    days = request.form['textfield12']
    member = request.form['textfield11']
    fees = request.form['textfield4']
    cmd.execute("insert into troupe values(null,'"+troupe+"','"+str(session['lid'])+"' ,'"+contact+"','"+email+"','"+fees+"','pending','"+member+"','"+days+"','"+img+"','"+category+"')")
    con.commit()
    return '''<script> alert("success"); window.location="/chorehome"</script>'''


@obj.route('/mng_troupe')
def mng_troupe():
    cmd.execute("SELECT * FROM troupe WHERE STATUS='pending' AND `chorid`='"+str(session['lid'])+"' ")
    s=cmd.fetchall()
    return render_template('mngtroupe.html',val=s)

@obj.route('/update_troupe')
def update_troupe():
    id=request.args.get('id')
    session['tid']=id
    cmd.execute("SELECT * FROM troupe WHERE troupeid='"+str(id)+"' ")
    s=cmd.fetchone()
    return render_template('update troupe.html',val=s)

@obj.route('/update_troupe1', methods=['post'])
def update_troupe1():
    try:
        troupe = request.form['textfield']
        contact = request.form['textfield2']
        email = request.form['textfield3']
        fees = request.form['textfield4']

        category = request.form['textfield66']
        image = request.files['file']
        img = secure_filename(image.filename)
        path = r"./static/troupe"
        image.save(os.path.join(path, img))


        members = request.form['textfield10']
        days = request.form['textfield11']
        cmd.execute("update  troupe set tname='" + troupe + "',contact='" + contact + "',email='" + email + "',fee='" + fees + "',members='" + members + "' ,days='" + days + "',image='" + img + "',category='" + category + "'    where troupeid='"+str(session['tid'])+"'")
        con.commit()
        return '''<script> alert("success"); window.location="/mng_troupe"</script>'''

    except Exception as e:
        troupe = request.form['textfield']
        contact = request.form['textfield2']
        email = request.form['textfield3']
        fees = request.form['textfield4']

        category = request.form['textfield66']

        members = request.form['textfield10']
        days = request.form['textfield11']
        cmd.execute(
            "update  troupe set tname='" + troupe + "',contact='" + contact + "',email='" + email + "',fee='" + fees + "',members='" + members + "' ,days='" + days + "',category='" + category + "'    where troupeid='" + str(
                session['tid']) + "'")
        con.commit()
        return '''<script> alert("success"); window.location="/mng_troupe"</script>'''


@obj.route('/delete_troupe')
def delete_troupe():
    id=request.args.get('id')
    cmd.execute("delete from troupe where troupeid='"+str(id)+"'")
    con.commit()
    return '''<script> alert("deleted"); window.location="/mng_troupe"</script>'''

@obj.route('/add_costume')
def add_costume():
    cmd.execute("select * from category ")
    s=cmd.fetchall()
    return render_template('add costume.html',val=s)

@obj.route('/add_costume1', methods=['post'])
def add_costume1():
    category= request.form['select']
    description = request.form['textfield7']
    size = request.form['textfield2']
    rate = request.form['textfield3']
    image = request.files['file']
    img=secure_filename(image.filename)
    path=r"./static/costume"
    image.save(os.path.join(path,img))
    set = request.form['textfield71']
    colour = request.form['textfield72']
    cmd.execute("insert into costume values(null,'"+str(session['lid'])+"','"+str(category)+"','" + img + "','" + rate + "','" + size + "','" + description + "','" + set + "','" + colour + "')")
    con.commit()
    return '''<script> alert("succes"); window.location="/chorehome"</script>'''

@obj.route('/mng_costume')
def mng_costume():
    cmd.execute("SELECT `costume`.*,category.* FROM `costume`JOIN `category`ON `category`.`categoryid`=`costume`.`categoryid` WHERE `costume`.`chorid`='"+str(session['lid'])+"'")
    s=cmd.fetchall()
    return render_template('mngcostume.html',val=s)

@obj.route('/update_costume')
def update_costume():
    id = request.args.get('id')
    session['coid'] = id
    cmd.execute("SELECT * FROM costume WHERE costid='"+str(id)+"'  ")
    s = cmd.fetchone()
    cmd.execute("SELECT * FROM category ")
    s1 = cmd.fetchall()
    return render_template('update costume.html',val=s, vall=s1)

@obj.route('/update_costume1', methods=['post'])
def update_costume1():
    category = request.form['select']
    description = request.form['textfield7']
    size = request.form['textfield2']
    rate = request.form['textfield3']
    image = request.files['file']
    img = secure_filename(image.filename)
    path = r"./static/costume"
    image.save(os.path.join(path, img))
    set = request.form['textfield71']
    colour = request.form['textfield72']
    cmd.execute("update  costume set size='" + size + "',rate='" + rate + "', image='" + img + "',description='"+description+"',sets='" + set + "',colour='" + colour + "',categoryid='" + category + "' where costid='"+str(session['coid'])+"'")
    con.commit()
    return '''<script> alert("success"); window.location="/mng_costume"</script>'''


@obj.route('/delete_costume')
def delete_costume():
    id=request.args.get('id')
    cmd.execute("delete from costume where costid='"+str(id)+"'")
    con.commit()
    return '''<script> alert("deleted"); window.location="/mng_costume"</script>'''


@obj.route('/pub_view_costume')
def pub_view_costume():
    cmd.execute("SELECT `costume`.*,category.* FROM `costume`JOIN `category`ON `category`.`categoryid`=`costume`.`categoryid`")
    s = cmd.fetchall()
    return render_template('public view costume.html',val=s)

@obj.route('/request_costume1')
def request_costume1():
    id=request.args.get('id')
    session['costid']=id
    rate = request.args.get('rate')
    session['rate'] = rate
    return render_template('costume pub reqest.html',days="")

@obj.route('/request_costume1_send',methods=['post'])
def request_costume1_send():
    id = session['costid']
    days = session['no_days']
    totel = session['totel']
    date=request.form['textfield8']
    cmd.execute("INSERT INTO `costume request` VALUES(NULL, '"+str(session['costid'])+"','pending','"+date+"','"+str(session['lid'])+"','"+str(days)+"','"+str(totel)+"')")
    con.commit()
    return '''<script> alert("succes"); window.location="/publichome"</script>'''

@obj.route('/request_troupe')
def request_troupe():
    cmd.execute("SELECT * FROM troupe")
    s = cmd.fetchall()
    return render_template('request troupe.html',val=s)

@obj.route('/Pubdetails_troupe')
def Pubdetails_troupe():
    id = request.args.get('id')
    session['trequestid'] = id
    try:
        fee= request.args.get('fee')
        if fee=="":
            fee=session['fee']
        else:
            session['fee'] = fee
    except Exception as e:
            fee = session['fee']
    return render_template('pub_troupe_book_details.html', day="")

@obj.route('/Pubdetails_troupe1',methods=['post'])
def Pubdetails_troupe1():
    id= session['trequestid']
    # nodays = request.form['textfield5']
    days = session['no_days']
    date=request.form['textfield8']
    totel=session['totel']


    cmd.execute("INSERT INTO `troupe request` VALUES(NULL, '"+str(session['trequestid'])+"','pending','"+date+"','"+str(session['lid'])+"','"+str(days)+"','"+str(totel)+"')")
    con.commit()
    return '''<script> alert("succes"); window.location="/publichome"</script>'''

@obj.route('/chore_view_public_reqst')
def chore_view_public_reqst():
    cmd.execute("SELECT `public`.*,`costume`.`image`,`costume`.`description`,`costume request`.*FROM`costume request`JOIN`costume`ON`costume request`.`costid`=`costume`.`costid` JOIN `public`ON `public`.`lid`=`costume request`.`userid`WHERE `costume`.`chorid`='"+str(session['lid'])+"' AND `costume request`.`status`='pending'")
    s=cmd.fetchall()

    return render_template('choreo view public request.html',val=s)



@obj.route('/chore_accept_public_reqst')
def chore_accept_public_reqst():
    id=request.args.get('id')
    cmd.execute("UPDATE `costume request` SET `costume request`.`status`='accept' WHERE `costume request`.`crequestid`='"+str(id)+"'")
    con.commit()
    return '''<script> alert("accept"); window.location="/chorehome"</script>'''


@obj.route('/chore_reject_public_reqst')
def chore_reject_public_reqst():
    id = request.args.get('id')
    cmd.execute("UPDATE `costume request` SET `costume request`.`status`='reject' WHERE `costume request`.`crequestid`='"+str(id)+"'")
    con.commit()
    return '''<script> alert("rejected"); window.location="/chorehome"</script>'''




@obj.route('/college_request_costume')
def college_request_costume():
    cmd.execute("SELECT `costume`.*,category.* FROM `costume`JOIN `category`ON `category`.`categoryid`=`costume`.`categoryid` WHERE `costume`.`categoryid`=`category`.`categoryid`")
    s = cmd.fetchall()
    return render_template('request costume.html',val=s)

@obj.route('/view_costume_responce')
def view_costume_responce():
    # cmd.execute("SELECT `name` FROM `costume request`")
    # s=cmd.fetchall()
    # cmd.execute("SELECT`phone` FROM`costume request`")
    # s1 = cmd.fetchall()

    cmd.execute("SELECT `costume request`.*,`costume`.*,`choreographer`.`fname`,`choreographer`.`lname`,`choreographer`.`phone`FROM`choreographer` INNER JOIN `costume`ON`costume`.`chorid`=`choreographer`.`loginid` INNER JOIN`costume request`ON `costume request`.`costid`=`costume`.`costid` WHERE `costume request`.`userid`='"+str(session['lid'])+"'AND `costume request`.`status`='pending' OR `costume request`.`status`='accept'")
    s2 = cmd.fetchall()
    return render_template('view costume request status.html',val2=s2)

#
# @obj.route('/view_costume_responce2', methods=['post'])
# def view_costume_responce2():
#     # name=request.form['select']
#     # contact = request.form['select2']
#
#
#     return render_template('view costume request status.html', val2=s2)



@obj.route('/view_troupe_responce')
def view_troupe_responce():
    # cmd.execute("SELECT `name` FROM `troupe request`")
    # s=cmd.fetchall()
    # cmd.execute("SELECT`phone` FROM`troupe request`")
    # s1 = cmd.fetchall()
    cmd.execute(
        " SELECT `troupe request`.*,`troupe`.*,`choreographer`.`fname`,`choreographer`.`lname`,`choreographer`.`phone`FROM`choreographer` INNER JOIN `troupe`ON `troupe`.`chorid`=`choreographer`.`loginid` INNER JOIN `troupe request`ON `troupe request`.`troupeid`=`troupe`.`troupeid` WHERE `troupe request`.userid='" + str(session['lid']) + "'")
    s2 = cmd.fetchall()
    return render_template('view_troupe_request_status.html',val2=s2 )


@obj.route('/view_troupe_responce1', methods=['post'])
def view_troupe_responce1():
    # name=request.form['select']
    # contact = request.form['select2']



    return render_template('view_troupe_request_status.html', val2=s2)




@obj.route('/pub_view_choreo_booking_responce')
def pub_view_choreo_booking_responce():
    # cmd.execute("SELECT `name` FROM `troupe request`")
    # s=cmd.fetchall()
    # cmd.execute("SELECT`phone` FROM`troupe request`")
    # s1 = cmd.fetchall()
    # cmd.execute(
    #     " SELECT `troupe request`.*,`troupe`.*,`choreographer`.`fname`,`choreographer`.`lname`,`choreographer`.`phone`FROM`choreographer` INNER JOIN `troupe`ON `troupe`.`chorid`=`choreographer`.`loginid` INNER JOIN `troupe request`ON `troupe request`.`troupeid`=`troupe`.`troupeid` WHERE `troupe request`.`name`='" + name + "' AND `troupe request`.`phone`='" + contact + "'")
    # s2 = cmd.fetchall()
    return render_template('pub_view_choreo_booking_responce.html')


@obj.route('/pub_view_choreo_booking_responce1', methods=['post'])
def pub_view_choreo_booking_responce1():
    # name=request.form['select']
    # contact = request.form['select2']
    #
    # cmd.execute(" SELECT `troupe request`.*,`troupe`.*,`choreographer`.`fname`,`choreographer`.`lname`,`choreographer`.`phone`FROM`choreographer` INNER JOIN `troupe`ON `troupe`.`chorid`=`choreographer`.`loginid` INNER JOIN `troupe request`ON `troupe request`.`troupeid`=`troupe`.`troupeid` WHERE `troupe request`.`name`='"+name+"' AND `troupe request`.`phone`='"+contact+"'")
    # s2 = cmd.fetchall()

    return render_template('pub_view_choreo_booking_responce.html', val2=s2)


#
# @obj.route('/pub_view_choreo_booking_responce')
# def pub_view_choreo_booking_responce():
#     cmd.execute("SELECT `name` FROM `troupe request`")
#     s=cmd.fetchall()
#     cmd.execute("SELECT`phone` FROM`troupe request`")
#     s1 = cmd.fetchall()
#
#     return render_template('pub_view_choreo_booking_responce.html',val=s ,val1=s1)
#
#
# @obj.route('/pub_view_choreo_booking_responce1', methods=['post'])
# def pub_view_choreo_booking_responce1():
#     name=request.form['select']
#     contact = request.form['select2']
#
#     cmd.execute(" SELECT `troupe request`.*,`troupe`.*,`choreographer`.`fname`,`choreographer`.`lname`,`choreographer`.`phone`FROM`choreographer` INNER JOIN `troupe`ON `troupe`.`chorid`=`choreographer`.`loginid` INNER JOIN `troupe request`ON `troupe request`.`troupeid`=`troupe`.`troupeid` WHERE `troupe request`.`name`='"+name+"' AND `troupe request`.`phone`='"+contact+"'")
#     s2 = cmd.fetchall()
#
#     return render_template('pub_view_choreo_booking_responce.html', val2=s2)



@obj.route('/chore_view_troupe_public_reqst')
def chore_view_troupe_public_reqst():
    cmd.execute("SELECT `public`.*,`troupe`.`tname`,`troupe`.`contact`,`troupe request`.*FROM`troupe request`JOIN`troupe`ON`troupe request`.`troupeid`=`troupe`.`troupeid` JOIN `public`ON `public`.`lid`=`troupe request`.`userid` WHERE `troupe`.`chorid`='"+str(session['lid'])+"'")
    s=cmd.fetchall()

    return render_template('accept or reject troupe.html',val=s)



@obj.route('/chore_accept_public_troupe_reqst')
def chore_accept_public_troupe_reqst():
    id=request.args.get('id')
    cmd.execute("UPDATE `troupe request` SET `troupe request`.`status`='accept' WHERE `troupe request`.`trequestid`='"+str(id)+"'")
    con.commit()
    return '''<script> alert("accept"); window.location="/chorehome"</script>'''


@obj.route('/chore_reject_public_troupe_reqst')
def chore_reject_public_troupe_reqst():
    id = request.args.get('id')
    cmd.execute("UPDATE `troupe request` SET `troupe request`.`status`='reject' WHERE `troupe request`.`trequestid`='"+str(id)+"'")
    con.commit()
    return '''<script> alert("rejected"); window.location="/chorehome"</script>'''

@obj.route('/vt')
def vt():
        id=request.args.get('id')
        fee = request.args.get('fee')
        session['fee']=fee
        cmd.execute("SELECT * FROM troupe WHERE`troupeid`='"+id+"'")
        s = cmd.fetchone()
        print(s)
        return render_template('vt.html', i=s,fee=fee)

@obj.route('/snd_rating')
def snd_rating():
        cmd.execute("SELECT * FROM `choreographer`")
        s = cmd.fetchall()
        return render_template('send rating.html', val=s)

@obj.route('/snd_rating1',methods=['post'])
def snd_rating1():
        cid=request.form['select']
        rating=request.form['select2']

        cmd.execute(" insert into rating values(null,'"+ str(session['lid'])+"','"+ str(cid)+"','"+ str(rating)+"',curdate())")
        con.commit()


        return '''<script> alert("succes"); window.location="/publichome"</script>'''


@obj.route('/View_rating')
def View_rating():
    cmd.execute("SELECT `public`.`name`,`choreographer`.`fname`,`choreographer`.`lname`,`rating`.* FROM `choreographer`JOIN `rating`ON `choreographer`.`loginid`=`rating`.`chorid`JOIN`public`ON`public`.`lid`=`rating`.`candid`")

    s=cmd.fetchall()

    return render_template('view rating.html',val=s)
#
@obj.route('/choreo_View_rating')
def choreo_View_rating():
    cmd.execute(" SELECT `public`.`name`,`rating`.* FROM `rating`JOIN `public`ON`public`.`lid`=`rating`.`candid` WHERE `rating`.`chorid`='"+str(session['lid'])+"'")

    s = cmd.fetchall()
    return render_template('choreo view rating.html',val=s)




@obj.route('/candy_send_rating')
def candy_send_rating():
    cmd.execute("SELECT * FROM `choreographer`")
    s = cmd.fetchall()
    return render_template('candy send rating.html',val=s)


@obj.route('/send_feedback')
def send_feedback():
    return render_template('aend feedback.html')

@obj.route('/View_feedback')
def View_feedback():
    return render_template('viewfeedback.html')



@obj.route('/View complaints and send reply')
def View_complaints_and_send_reply():
    return render_template('v complaint &send reply.html')


@obj.route('/View complaints and send reply chore')
def View_complaints_and_send_reply_chore():
    return render_template('view complaint & send reply choreo.html')


@obj.route('/get_totel', methods=['post'])
def get_totel():
    fee=session['fee']
    print(fee)
    no_days=request.form['textfield5']
    print(no_days)
    session['no_days']=no_days
    totel= int(no_days)*int(fee)
    print(totel)
    session['totel']=totel
    return render_template('pub_troupe_book_details.html',tot=totel,day=no_days)


@obj.route('/get_tote_costumel', methods=['post'])
def get_tote_costumel():
    rate=session['rate']
    no_days=request.form['textfield5']
    session['no_days']=no_days
    totel= int(no_days)*int(rate)
    print(totel)
    session['totel']=totel
    return render_template('costume pub reqest.html',tot=totel,day=no_days)

# SELECT `public`.`name`,`rating`.* FROM `rating`JOIN `public`ON`public`.`lid`=`rating`.`candid` WHERE `rating`.`chorid`=33
@obj.route('/vc')
def vc():
        id=request.args.get('id')
        rate = request.args.get('rate')
        session['rate'] = rate
        cmd.execute("SELECT * FROM costume WHERE`costid`='"+id+"'")
        s = cmd.fetchone()
        print(s)
        return render_template('vc.html', i=s,rate=rate)

@obj.route('/public_request')
def public_request():
    cmd.execute("SELECT `public`.*,`public_request`.`date`,`public_request`.`pubid` FROM `public_request`JOIN `public` ON `public_request`.`userid`=`public`.`lid` WHERE `public_request`.`chorid`='"+str(session['lid'])+"'")
    s = cmd.fetchall()
    return render_template('public request.html',val=s)


@obj.route('/public_reqst_accept')
def public_reqst_accept():
    id=request.args.get('id')
    cmd.execute("UPDATE `public_request` SET `public_request`.`status`='accept' WHERE `public_request`.`pubid`='"+str(id)+"'")
    con.commit()
    return '''<script> alert("accept"); window.location="/chorehome"</script>'''


@obj.route('/public_reqst_reject')
def public_reqst_reject():
    id = request.args.get('id')
    cmd.execute("UPDATE `public_request` SET `public_request``.`status`='accept' WHERE `public_request`.`pubid`='"+str(id)+"'")
    con.commit()
    return '''<script> alert("rejected"); window.location="/chorehome"</script>'''




obj.run(debug=True)