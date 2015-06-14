import web
from web import form

db = web.database(dbn='mysql', user='testuser', pw='test123', db='TESTDB')
render = web.template.render('templates/')

urls = ('/', 'index')
app = web.application(urls, globals())

myform = form.Form()

class index: 
    def GET(self): 
        members = db.select('member')
        return render.index(members)

    def POST(self): 
        post_data=web.input(name=[])
        for checked in post_data.name:
            n = db.insert('registrations', member_id=checked)

if __name__=="__main__":
    web.internalerror = web.debugerror
    app.run()

