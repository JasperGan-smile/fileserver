import os,magic
import re
from genericpath import isdir, isfile
from flask import Flask,send_file,render_template,request


def show_dir(pwd):
    files = os.listdir(pwd)   
    return render_template("index.html",files = files,pwd = pwd)


def send_to_client(pwd):
    path = pwd[:-1]
    return send_file(path,as_attachment=True)

def file_or_dir(pwd):
    if(os.path.isdir(pwd)):
        return show_dir(pwd)
    else:
        return send_to_client(pwd)


app = Flask(__name__)

@app.route('/edit/<path:dummy>')
def editor(dummy):
    file_path = '/'+str(dummy)
    with open(file_path,'r',encoding='utf-8') as f:
        content = f.read()
    return render_template('editor.html',path = file_path,content = content)


@app.route('/save',methods=['POST'])
def save():
    content = request.form['content']
    path = request.form['path']
    with open(path,'w') as f:
        f.write(content)  
    return "saved!"




@app.route('/<path:dummy>')
def fallback(dummy):
    if str(dummy).startswith('edit'): 
        return editor(str(dummy))
    else:
        return file_or_dir('/'+str(dummy)+'/')


@app.route('/')
def index():
   html =  file_or_dir("/")
   return html


if __name__ == '__main__':
   app.run(debug=True)



