import web
from web import form

db = web.database(dbn='mysql', user='testuser', pw='test123', db='TESTDB')
render = web.template.render('templates/')

urls = ('/', 'index', '/delete', 'delete')
app = web.application(urls, globals())

class index: 
    def GET(self): 
        checkedIn = db.query("SELECT * FROM member WHERE member.member_id IN (\
        SELECT member_id FROM registrations WHERE DATE(reg_time)=DATE(NOW()) AND \
        member.member_id = registrations.member_id)")
        
        members = db.query("SELECT * FROM member WHERE member.member_id NOT IN (\
        SELECT member_id FROM registrations WHERE DATE(reg_time)=DATE(NOW()) AND \
        member.member_id = registrations.member_id)")
        return render.index(checkedIn, members)

    def POST(self): 
        post_data=web.input(name=[])
        for checked in post_data.name:
            n = db.insert('registrations', member_id=checked)
        raise web.seeother('/')

#class delete:
#    def POST(self):
        

if __name__=="__main__":
    web.internalerror = web.debugerror
    app.run()

