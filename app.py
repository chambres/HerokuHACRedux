from flask import Flask, render_template, request, redirect, session, url_for, make_response, jsonify
import requests
import api
from datetime import datetime as dt
from datetime import timedelta


app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')
app.secret_key = 'hinjakuhinjaku'


def uri_exists_get(uri: str) -> bool:
    try:
        response = requests.get(uri)
        try:
            response.raise_for_status()
            return True
        except requests.exceptions.HTTPError:
            return False
    except requests.exceptions.ConnectionError:
        return False


@app.route('/', methods=['GET', 'POST'])
def loggingin():
    if request.cookies.get('username') is not None and request.cookies.get('password') is not None and request.cookies.get('link') is not None:
        return redirect(url_for('home'))

    if request.cookies.get('error') == "True":
        resp = make_response(render_template('index.html', error="There has been an error. Try re-entering your username and password"))
        resp.set_cookie('error', '', expires=0)
        return resp
    

    
    else:
        if request.method == 'POST':
            username = request.form['username'] 
            password = request.form['pass']
            link = request.form['link']
            remember = request.form.get('remember-me')

            test = "https://" + link + f"/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess%2fHomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess%2f"
            if uri_exists_get(test) == False:
                return render_template('index.html', error="Your Homeaccess link is invalid. Remember that the link must be entered in its simplest form: such as homeaccess.katyisd.org")


            resp = make_response(redirect(url_for('home')))

            expiry = dt.now() + timedelta(days=1460) 

            resp.set_cookie('username', username, expires=expiry)
            resp.set_cookie('password', password, expires=expiry)
            resp.set_cookie('link', link, expires=expiry)
            if remember == "on":
                resp.set_cookie('remember', 'True', expires=expiry)
            else:
                resp.set_cookie('remember', 'False')

            return resp




        return render_template('index.html')

@app.route('/home/')
def home():

    if request.cookies.get('username') is None or request.cookies.get('password') is None or request.cookies.get('link') is None:
        return redirect('/')

    


    return render_template('home.html')

@app.route('/_get_data/', methods=['POST'])
def get_data():
    
    a = api.main(request.cookies.get('username'), request.cookies.get("password"), request.cookies.get('link'))

    if a == "error":
        resp = make_response(jsonify({'data': "error"}))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('password', '', expires=0)
        resp.set_cookie('link', '', expires=0)
        resp.set_cookie('remember', '', expires=0)
        resp.set_cookie('error', 'True')

        return resp


 
    classes = a.keys()

    resp = make_response(render_template('grades.html', classes=classes, grades=a))
    

    return jsonify({'data': render_template('grades.html', classes=classes, grades=a)})


if __name__ == '__main__':  
    app.run()
    
                                        