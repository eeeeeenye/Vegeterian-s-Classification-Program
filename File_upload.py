from flask import Flask, render_template, request, redirect, url_for
from setuptools import find_namespace_packages
from werkzeug.utils import secure_filename
from werkzeug.utils import send_from_directory
import webParsing as wp
import test


app = Flask(__name__)
f_name = ""
result = ""


@app.route('/')
def upload_file():
    return render_template('index.html')

@app.route('/uploader',methods=['GET','POST'])
def file_upload():
    global f_name, result

    if request.method =='POST':
        f = request.files['file']
        f_name = f.filename
        print(f_name)
        url = './static/' + secure_filename(f.filename)
        f.save(url)
        result = test.main(url)
        return redirect(url_for("view"))


@app.route('/view', methods = ['GET', 'POST'])
def view():
    global f_name,result
    print(f_name,result)
    return render_template('result.html', f_name=f_name, result=result) 


if __name__ == '__main__':
    app.run(debug=True)

