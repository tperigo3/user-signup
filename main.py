from flask import Flask, request, redirect, render_template
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/", methods =['GET','POST'])
def user_signup():
   
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify_password']
        email = request.form['email']   
        template = jinja_env.get_template('form.html')
        username_error = ''
        password_error = ''
        verify_password_error = ''
        email_error =''
        
        if len(username) < 3 or len(username) > 20:
            username_error = "Your username is out of range (3-20 characters)"
        for char in username:
            if char == " ":
                username_error = "Your username can not contain a space"
       
        if len(password) < 3 or len(password) > 20:
            password_error = "Your password is out of range (3-20 characters)"
        for char in password:
            if char == " ":
                password_error = "Your password can not contain a space"
       
        if verify_password != password:
            verify_password_error = "Your passwords do not match"
       
        if email:
            if len(email) < 3 or len(email) > 20:
                email_error = "Your email is out of range (3-20 characters)"
            for char in email:
                if " " in email:
                    email_error = "Your email can not contain a space"
            if email.count('@') != 1:
                email_error = "Your email must contain only one @ symbol"
            if email.count(".") != 1:
                email_error = "Your email must contain only one ."
       
        if (not username_error and not password_error and not verify_password_error and not email_error):
            return redirect('/welcome?username={0}'.format(username))
        
        else:
            return render_template('form.html', 
            username_error = username_error,
            password_error = password_error,
            verify_password_error = verify_password_error,
            email_error = email_error,
            username = username,
            password = '',
            verify_password = '',
            email = email)

    return render_template('form.html')

@app.route('/welcome')
def welcome_message():
    username = request.args.get('username')
    return render_template('welcome.html',
        username = username)

app.run()