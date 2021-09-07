from flask import *
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)  #creating the flask class object
app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///info_user.db"   #we are using sqlite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key="hello" #session k time use krte hain,for protection aggainst attackers,they dont know the secret key
db=SQLAlchemy(app)


#here info and info_user are two tables in database
class info(db.Model):#this table is used to store users login data
    sno = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"{self.email}--{self.password}"

class info_books(db.Model):#this table is used to store subjects
    sno = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(30), nullable=False) #email
    sub = db.Column(db.String(30), nullable=False)
    desc = db.Column(db.String(100), nullable=False)


    def __repr__(self):
        return f"{self.email}--{self.password}"



class info_user(db.Model):#this table is used to store  links
    sno = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    id = db.Column(db.String(30), nullable=False)#email
    sub = db.Column(db.String(30), nullable=False)
    link = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f"{self.content}--{self.title}"


@app.route('/') #home page of the website
def home():
    if 'email' in session:
        email=session['email']
        data = info_books.query.all()
        data.reverse()
        return render_template('profile.html',email=email,data=data)
    return render_template('home.html')

@app.route('/login',methods=['POST','GET'])  # for login
def login():
    if 'email' in session:
        email = session['email']
        data = info_books.query.all()
        data.reverse()
        return render_template('profile.html', email=email, data=data)
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        #verify user
        data_users=info.query.all()
        email_flag=False
        for i in data_users:
            if email==i.email:
                email_flag=True
                if password==i.password:
                    session['email']=i.email
                    s=session['email']
                    print("LogIn successfull!")
                    data=info_books.query.all()
                    data.reverse()
                    return render_template('profile.html',email=s,data=data)
                else:
                    msg="You entered incorrect password!"
                    print("You entered incorrect password!")
                    return render_template('login.html',msg=msg)

        if email_flag==False:
            msg="This ID is not registered."
            print("This ID is not registered.")
            return render_template('login.html', msg=msg)

    return render_template('login.html')

@app.route('/signin',methods=['POST','GET'])  # for signin
def signin():
    if 'email' in session:
        email = session['email']
        data = info_user.query.all()
        data.reverse()
        return render_template('profile.html', email=email, data=data)
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        #validation
            #validation of email
        data_users=info.query.all()
        email_flag=True
        for i in data_users:
            if i.email==email:
                email_flag=False
                break
            #validation of password
        password_flag=True
        if len(password)<5:
            password_flag=False
        #validation result
        if email_flag==False:
            msg="The ID you entered is already registered"
            print("The ID you entered is already registered")
            return render_template('signin.html', msg=msg)
        if password_flag==False:
            msg="Password lenght must be greater than 5"
            print("Password lenght must be greater than 5")
            return render_template('signin.html', msg=msg)
        if password_flag and email_flag==True:
            # storing into database
            entry = info(password=password, email=email)
            db.session.add(entry)
            db.session.commit()
            msg="Congratulation..You are SignedIn"
            print("Congratulation..You are SignedIn")
            return render_template('signin.html',msg=msg)

    return render_template('signin.html')

@app.route('/logout')  # for logout
def logout():
    session.pop('email', None)
    return render_template('home.html')

@app.route('/profile',methods=['POST','GET'])  # profile
def profile():  #for going to profile,for making subjects
    if 'email' in session:
        # Creating a subject
        if request.method == 'POST':
            sub = request.form.get('sub')
            # validation of subject
            data_books = info_books.query.all()
            for i in data_books:
                if i.id == session['email'] and i.sub == sub:
                    msg = "This subject is already added."
                    print("This subject is already added.")
                    email = session['email']
                    data = info_books.query.all()
                    data.reverse()
                    return render_template('profile.html', email=email, data=data, msg=msg)
            # adding to database
            desc = request.form.get('desc')
            id = session['email']
            entry = info_books(sub=sub, desc=desc, id=id)
            db.session.add(entry)
            db.session.commit()

            email = session['email']
            data = info_books.query.all()
            data.reverse()
            return render_template('profile.html', email=email, data=data)

        email = session['email']
        data = info_books.query.all()
        data.reverse()
        return render_template('profile.html', email=email, data=data)
    return render_template('home.html')

@app.route('/updateb/<int:i>',methods=['POST','GET'])  # for updating book
def updateb(i):
    if 'email' in session:

        data = info_books.query.filter_by(sno=i).first()
        sub_temp=data.sub
        try:
          if request.method=='POST':
            sub=request.form.get('sub')
            desc=request.form.get('desc')

            # selecting the specific book using th sno(of book list) as key
            data = info_books.query.filter_by(sno=i).first()
            #updating book
            data.sub = sub
            data.desc = desc

            db.session.add(data)
            db.session.commit()
            #BOOK UPDATED


            data = info_books.query.filter_by(sno=i).first()
            print(data.sub)
            try:  # updating all the links that are conneted to that book
                data_ = info_user.query.filter_by(sub=sub_temp)

                for i in data_:
                    print(i.title)
                    data_link = info_user.query.filter_by(sub=sub_temp).first()
                    #updating(link) process
                    data_link.sub = data.sub

                    db.session.add(data_link)
                    db.session.commit()
                    #LINKS UPDATED

            except:
                print("Error occured while deleting-INSIDE")
            data_books= info_books.query.all()
            data_books.reverse()
            return render_template('profile.html', email=session['email'], data=data_books)

          #agar request ni aaya hai
          return render_template('updateb.html',email=session['email'],data=data)
        except:
            print("Error occured while deleting-OUTSIDE")

    return render_template('home.html')

@app.route('/updatel/<int:i>/<sub>', methods=['POST', 'GET'])  # for updating link
def updatel(i,sub):
    if 'email' in session:
        #updating link
        try:
            if request.method == 'POST':
                link = request.form.get('link')
                title = request.form.get('title')
                content = request.form.get('content')

                data = info_user.query.filter_by(sno=i).first()
                data.link = link
                data.title = title
                data.content = content

                db.session.add(data)
                db.session.commit()
                data_links = info_user.query.all()
                data_links.reverse()

                return render_template('addlink.html',sub=sub, data=data_links, email=session['email'])
            data = info_user.query.filter_by(sno=i).first()
            email = session['email']
            return render_template('updatel.html', sub=sub,email=email, data=data)
        except:
            print("Error occured while updating data")
        email = session['email']
        data_links = info_user.query.all()
        data_links.reverse()
        return render_template('updatel.html', sub=sub,email=email, data=data_links)

    return render_template('home.html')

@app.route('/deleteb/<int:i>')  # for deletion of book
def deleteb(i):
    if 'email' in session:
        #deleting book
        try:
            #selecting the specific book using th sno(of book list) as key
            data = info_books.query.filter_by(sno=i).first()
            #print(data.sub)
            try:#deleting all the links that are conneted to that book
                #data = info_user.query.filter_by(sub=data.sub).first()
                data_ = info_user.query.filter_by(sub=data.sub)
                for i in data_:
                    print(i.title)
                    data_link = info_user.query.filter_by(sub=data.sub).first()
                    db.session.delete(data_link)
                    db.session.commit()
            except:
                print("Error occured while deleting-INSIDE")
            #deleting book after deleting all links
            db.session.delete(data)
            db.session.commit()

            #data_links = info_user.query.all()
            #data_links.reverse()#############################
            #return render_template('addlink.html',  data=data_links, email=session['email'])


            # db.session.delete(data)
            # db.session.commit()
        except:
            print("Error occured while deleting-OUTSIDE")

        email = session['email']
        data_books = info_books.query.all()
        data_books.reverse() ######################################

        return render_template('profile.html', email=email, data=data_books)

    return render_template('home.html')


@app.route('/deletel/<int:i>/<sub>')  # for deletion of link
def deletel(i,sub):
    if 'email' in session:
        #deleting link
        try:
            data = info_user.query.filter_by(sno=i).first()
            db.session.delete(data)
            db.session.commit()
        except:
            print("Error occured while deleting")
        data_links = info_user.query.all()
        data_links.reverse()
        return render_template('addlink.html', sub=sub,data=data_links, email=session['email'])

    return render_template('home.html')

@app.route('/addlink/<sub>',methods=['POST','GET'])  # for link addition
def addlink(sub):
    if 'email' in session:
        #adding link
        if request.method=='POST':
            link=request.form.get('link')
            title=request.form.get('title')
            content=request.form.get('content')
            entry = info_user(sub=sub,link=link,title=title,id=session['email'],content=content)
            db.session.add(entry)
            db.session.commit()

            email = session['email']
            data_links = info_user.query.all()
            data_links.reverse()
            return render_template('addlink.html', sub=sub,email=email, data=data_links)

        email = session['email']
        data_links=info_user.query.all()
        data_links.reverse()
        return render_template('addlink.html', email=email, data=data_links,sub=sub)

    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True,port=8000)