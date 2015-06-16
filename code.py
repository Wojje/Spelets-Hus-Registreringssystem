from flask import Flask, render_template, url_for, request, redirect
import web

app = Flask(__name__)

db = web.database(dbn='mysql', user='testuser', pw='test123', db='TESTDB')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        checked = request.form['name']
        n = db.insert('registrations', member_id=checked)
        return redirect(url_for('index'))
    else:
        checkedIn = db.query("SELECT * FROM member WHERE member.member_id IN (\
        SELECT member_id FROM registrations WHERE DATE(reg_time)=DATE(NOW()) AND \
        member.member_id = registrations.member_id)")
        members = db.query("SELECT * FROM member WHERE member.member_id NOT IN (\
        SELECT member_id FROM registrations WHERE DATE(reg_time)=DATE(NOW()) AND \
        member.member_id = registrations.member_id)")
        return render_template('index.html', checkedIn=checkedIn, members=members)

if __name__ == '__main__':
    app.run()

