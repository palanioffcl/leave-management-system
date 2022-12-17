from flask import Flask,render_template,request,redirect,url_for
import sqlite3

con=sqlite3.connect("lms.db")
con.execute("CREATE TABLE IF NOT EXISTS leave(id INTEGER PRIMARY KEY,fname TEXT,lname TEXT,designation TEXT, type TEXT, email TEXT,reason TEXT)")
con.close()
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/new', methods=['GET','POST'])
def new(): 
    if request.method=='POST':
        s_fname=request.form['fname']
        s_lname=request.form['lname']
        s_des=request.form['desn']
        s_addr=request.form['type']
        s_mail=request.form['mail']
        from_=request.form['from']
        till=request.form['till']
        s_remarks=request.form['remarks']
        
        with sqlite3.connect("lms.db") as con:
            cur=con.cursor()
            cur.execute("INSERT INTO leave (fname,lname,designation,type,email,from_,till,reason) VALUES (?,?,?,?,?,?,?,?)",(s_fname,s_lname,s_des,s_addr,s_mail,from_,till,s_remarks))
            con.commit()      
    return render_template('new.html')


@app.route('/admin/all')
def all():
    con = sqlite3.connect("lms.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from leave")
    rows = cur.fetchall()
    return render_template("all.html",rows=rows)


@app.route('/delete/<string:sl>',methods=['GET'])
def delete(sl):
    with sqlite3.connect("lms.db") as con:
            cur=con.cursor()
            cur.execute("DELETE FROM leave WHERE id=?",(sl,))
            con.commit()      
    return redirect(url_for('all'))



if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
