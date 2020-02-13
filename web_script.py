from flask import Flask,render_template,request,session,redirect,flash,url_for,send_file
import app1_u
import webbrowser
import web_scr,olx_data,stock
from flask_sqlalchemy import SQLAlchemy
from send_mail_script  import send_mail
from sqlalchemy.sql import func
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import pandas
from file_read import geoconvert
from io import StringIO
global df,df1
global file
lg=[]
app=Flask(__name__)
app.secret_key='ghklll'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:abc123@localhost/mail'
db=SQLAlchemy(app)
@app.route("/")
@app.route("/<int:count>")
@app.route("/<error>")
def home(count=0,error=None):
    if error:
        return render_template("home1.html",count=count,error=error)
    else:
        return render_template("home1.html",count=1)
@app.route("/about")
def about():
        return render_template("about.html")

@app.route("/loginsuccessfull")
@app.route("/loginsuccessfull)/<name>")
def loginsuccessfull(name=None):
     if session.get('logged_in'):
         return render_template("loginsuccessfull.html",name=name)
     else:
          flash('You are not logged in.Please login!!')
          return redirect("/")


@app.route("/Map")
def Map():
 if session.get('logged_in'):
        return render_template("Map_add_polygon_layer.html")
 else:
         flash('You are not logged in.Please login!!')
         return redirect("/")
@app.route("/validate/<int:count>",methods=['POST','GET'])

def validate(count=1):
  if request.method=='GET':
      return redirect("/")
  elif request.method=='POST':
      result=request.form
  for key,values in result.items():
            if key=='name':
                name=result[key]
            if key=='password':
                if result[key]=='admin':
                        session['logged_in']=True
                        return redirect(url_for('loginsuccessfull',name=name))
                        break
                else:
                        count=count+1
                        if(count<=3):
                            return render_template("home1.html",count=count,error="Incorrect Password!! Please enter password again!! "+str(3-(count-1)) +" attempts left")
                        else:
                            return render_template("home1.html",count=count,error=str(count-1)+ "  Attempts failed.Account LOCKED!!")

@app.route("/dictionary/",methods=['POST','GET'])
def dictionary():
  if session.get('logged_in'):
        if request.method=='GET':
            lg.clear()
            return render_template("dict.html")
        elif request.method=='POST':
            result=request.form
            print(result)
            for key,values in result.items():
                  if key=='word':
                      a=app1_u.t_w(result[key])
            if a['flag']==0:
                return render_template("dict.html",flag=0,name=a['l'])
            elif a['flag']==1:
                for x in a['l']:
                    lg.append(x)
                return render_template("dict.html",flag=1,name=a['l'])
            else:
                return render_template("dict_error.html",flag=4,message=" Word Not Found!!")
  else:
      flash('You are not logged in.Please login!!')
      return redirect("/")

@app.route("/t_close/<name>",methods=['POST','GET'])
#@app.route("/t_close/<l>",methods=['POST','GET'])
def t_close(name=None):
        if request.method=='GET':
            return render_template("dict.html")
        elif request.method=='POST':
                if(name in lg ):
                    f=app1_u.t_w(name)
                    return render_template("dict.html",flag=0,name=f['l'])
                    #return render_template("result.html",word=f,l=lg)
                elif(name=='2N'):
                    return render_template("dict.html",flag=2,name=lg)
                else:
                    return render_template("dict_error.html",flag=4,message=" Word Not Found!!")

@app.route("/logout")
def logout():
    session['logged_in']=False
    return render_template("logout.html")

@app.route('/stck/')
def stck():
    a=stock.stock_file()
    return render_template("stock_data.html",script1=a[0],div1=a[1],cdn_js=a[2])



@app.route('/web_scr/')
def web():
    global df
    df=web_scr.web_scr1()
    return render_template("web.html",df=df[-1].to_html())

@app.route('/graph/')
def graph():
    global df
    print(len(df))
    return render_template("graph.html",script=df[0],div=df[1])

@app.route('/olx_fun/', methods=['GET', 'POST'])
@app.route('/olx_fun/<q>', methods=['GET', 'POST'])
def olx_fun(q=None):
    print(q)
    global df1
    if (q== None):
        print(q)
        try:
            df1=olx_data.olx()
            return render_template("olx_d.html",q=q,df1=df1.to_html())
        except:
            df1="Error in Connection"
            return render_template("olx_d.html",q=q,df1=df1)
    elif (q=='T'):
        print(q)
        print(df1)
        olx_data.save_csv(df=df1)
        return render_template("olx_d.html",q=q)


class Data(db.Model):
    __tablename__="height_data"
    id=db.Column(db.Integer,primary_key=True)
    email_=db.Column(db.String(120),unique=True)
    height_=db.Column(db.Integer)

    def __init__(self,email_,height_):
        self.email_=email_
        self.height_=height_

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method=='POST':
        email=request.form["email_name"]
        height=request.form["height"]
        print(email,height)
        #below syntax results in error sqlalchemy.orm.exc.UnmappedInstanceError: Class 'builtins.str' is not mapped
        #db.session.add(email,height)
        #we need to create Data fclass object and then store
        print(db.session.query(Data).filter(Data.email_==email))
        print(db.session.query(Data).filter(Data.email_==email).scalar())
        if db.session.query(Data).filter(Data.email_==email).count()==0:
            data=Data(email,height)
            db.session.add(data)
            db.session.commit()
            avg_height=db.session.query(func.avg(Data.height_)) # this results in query
            print("AVG_query",avg_height)
            avg_height=round(avg_height.scalar(),1)# scalar to get value from query,rounding of to 1
            print("AVG_value",avg_height)
            count=db.session.query(func.count(Data.height_)).scalar()
            print('count',count)
            send_mail(email,height,avg_height,count)
            return render_template("success.html")
        else:
            return render_template("index.html",text="Seems like we have got something from that mail address already")


#app=Flask(__name__)

@app.route("/upload")
def upload():
    return render_template('upload.html')

@app.route("/download",methods=['POST'])
def download():
        global file
    #if request.method=='POST':
        file=request.files["file"]
        print("hjhnj",file)
        print("fileeee",type(file))
        file.save(secure_filename("uploaded"+file.filename))
        file.seek(0)
        content=file.read()
        #b = bytes(content, encoding='utf-8')
        print(type(content))
        a=content.decode()
        print("avnbn,",content.decode())
        a=StringIO(a)
        a1=pandas.read_csv(a,sep=",")
        '''a1=pandas.DataFrame(a1,columns=['Address','City','State','Country','Supermarket Name','Number of Employees'])
        print("after",a1)'''# to convert to dataframe
        a2=geoconvert(a1)
        return render_template('download.html',text=a2.to_html(),f=file.filename,btn="button.html")

@app.route("/save",methods=['POST'])
def save():
    #mess="FIle is saved as "+file_name
    ###flash('Your File has been saved!!')
    return send_file("uploaded"+file.filename,attachment_filename="file.csv",as_attachment=True)

if __name__=="__main__":
    #app.secret_key='ghklll'
    app.run(debug=True)
