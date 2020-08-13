# Importing random to generate random string sequence
import random
# Importing string library function
import string
from flask import Flask,redirect,request,jsonify
from flask_restful import Resource,Api
from flaskext.mysql import MySQL
from flask_cors import CORS
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

mysql=MySQL()

app=Flask(__name__)
CORS(app)
port = 4004
env = "airfone"
if __name__ == "__main__":
    if len(sys.argv) > 1:
        env = sys.argv[1]
        print("env=" + env)
    if len(sys.argv) > 2:
        port = sys.argv[2]
        print("port=" + port)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Akshay9949@'
app.config['MYSQL_DATABASE_DB'] = env
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

api = Api(app)
class Login(Resource):
    # clientAuthentication
    def get(self, phone):
        # establishing connection to the database
        conn = mysql.connect()
        cursor = conn.cursor()

        # for OTP generation
        otp=''.join([random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)for n in range(6)])

        # updating the pre existed otp of the table
        cursor.execute("update loginDetails set otp='" + str(otp) + "' where phone='" + phone + "'")

        # for getting the email registered to send the otp
        cursor.execute("select email from loginDetails where phone='"+phone+"'")
        result=cursor.fetchall()
        if len(result) > 0:
            for row in result:
                toemail= row[0]
        conn.commit()

        # Calling emailattach function using email class
        Email().emailattach("airfoneteam1@gmail.com", toemail, "The OTP for the login is : "+otp,"","")
        return toemail

# Email module to create an conn
class Email:
    def emailattach(self, fromaddr, toaddr, content,filename,path):

        # mail details
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Subject_of_the_mail"
        body = content

        # attach the body with the msg instance
        msg.attach(MIMEText(body, 'plain'))

        # starting the smtp session
        s = smtplib.SMTP('smtp.gmail.com', 587)

        # starting the TLS for security
        s.starttls()

        # Authentication of the server mail
        s.login(fromaddr, "airfone123")

        # Converts the Multipart msg into a string
        text = msg.as_string()

        # with attachment condition
        if(filename and path):
            attachment = open(path, "rb")
            # instance of MIMEBase and named as p
            p = MIMEBase('application', 'octet-stream')

            # To change the payload into encoded form
            p.set_payload((attachment).read())

            # encode into base64
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

            # attach the instance 'p' to instance 'msg'
            msg.attach(p)
            text = msg.as_string()

        s.sendmail(fromaddr, toaddr, text)
        print("email sent")

        # terminating the session
        s.quit()
class a(Resource):
    def get(self, phone,otp):
        # otpValidation
        conn = mysql.connect()
        cursor = conn.cursor()
        data = request.get_json()
        # otp=input("Enter OTP:")
        query = "select email from loginDetails where phone='" + phone + "' && otp='" + otp+ "'"
        cursor.execute(query)
        rows = cursor.fetchall()
        # print(result)

        if len(rows) > 0:
            user = jsonify(rows)
            return user
        return {'user': None}, 404
# defining the url
api.add_resource (Login ,'/login/<string:phone>')
api.add_resource(a,'/mail/<string:phone>/<string:otp>')
app.run(port=port,debug=True)
