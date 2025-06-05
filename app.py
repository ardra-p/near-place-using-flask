from flask import Flask , render_template, request, session, redirect, url_for
from models import db ,User, Place
from forms import SignupForm, LoginForm, AddressForm
import os


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Ardra@localhost/learningflask' #connecting to database
app.config['SECRET_KEY']='a_long_random_key'
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/signup', methods=['GET','POST'])
def signup():
    if 'email' in session:
        # protect user from showing signup page by checking the user already logined
        # alreday existing or logined email users can't accsess signup 
        return redirect(url_for('home'))
    form = SignupForm()
    print("FORM TYPE:", type(form))
    print("BASE CLASSES:", SignupForm.__bases__) 
    if request.method=='POST':
        if form.validate() == False:
            return render_template('signup.html',form=form)
        else:
          newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
          db.session.add(newuser)
          db.session.commit()

          session['email'] = newuser.email
          return redirect(url_for('home'))
        
    elif request.method=='GET':
        return render_template('signup.html', form = form )
    
@app.route('/home', methods=['GET','POST'])
def home():
    if 'email' not in session: #protection only email in the session can accses the home page
        return redirect(url_for('login'))
    
    form = AddressForm()
    places=[]
    my_coordinates=(37.433,-122.0333)
    if request.method =='POST':
        if form.validate() == False:
            return render_template('home.html', form=form)
        else:
            # handle the form submission place search section
            address = form.address.data
            #quary for place around it
            p = Place()
            my_coordinates =p.address_to_latlang(address)
            places =p.query(address)
            return render_template('home.html', form=form, my_coordinates=my_coordinates, places=places)

    elif request.method == 'GET':
        return render_template('home.html', form=form,my_coordinates=my_coordinates, places=places)
    

@app.route('/login', methods=['GET','POST'])
def login():
    if 'email' in session: # login page protected can't accsess the users email already the session
        return redirect(url_for('home'))
    form = LoginForm()

    if request.method == 'POST':
        if form.validate()==False:
            return render_template('login.html')
        else:
            email = form.email.data
            password = form.password.data

            user =User.query.filter_by(email=email).first()
            if user is not None and user.check_password(password):
                session['email'] = form.email.data
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('login.html', form=form)

@app.route('/signout')
def signout():
    session.pop('email',None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)

   
