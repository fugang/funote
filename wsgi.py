from flask import Flask, render_template, request, g, session, abort,flash
import db
import json
import eventlet
from eventlet import wsgi

SECRET_KEY = "zyHyipIPMTtQUe4P"

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('MINITWIT_SETTINGS', silent=True)
app.debug=True


@app.route("/")
def main():
    regins = db.get_regins()
    regin = session.get("regin",None)
    if not regin:
        session["regin"] = 1
        regin = 1
    else:
        regin = int(regin)
    values = []
    for i in regins: 
        values.append({"title":i.title,
                         "id":i.id,
                        "selected":i.id == regin
                        })
    user = session.get("user",None)
    if not user:
        quilltexts = []
    else:
        quilltexts=db.get_quill_header_by_regin(regin,user)
    return render_template("index.html", quilltext=quilltexts,\
                           regins=values,user=user)
    
@app.route("/note/<tid>",methods=['GET', 'POST'])
def update_note(tid):
    user = session.get("user",None)
    if not user:
        return "no user found", 401
    if request.method=="GET":
        quilltext = db.get_quill_by_id(tid)
        text = quilltext.text
        html = quilltext.html
        db.add_click_quill(tid)
        return html
    elif request.method == "POST":
        html = request.form["html"]
        text = request.form["text"]
        header = text.split("\n")[0]
        values = {"html":html,
                  "header":header,
                  "text":text}
        db.update_quill(tid, values)
        return header
            
@app.route("/note",endpoint="/",methods=['GET', 'POST'])
def new_note():
    regin_id = session.get("regin",None)
    user = session.get("user",None)
    if not user:
        return "not user found",401
    if request.method=="GET":
        return str(session["regin"])
    elif request.method == "POST":
        html = request.form["html"]
        text = request.form["text"]
        header = text.split("\n")[0]
        values = {"header":header,
                  "text":text,
                  "regin_id":regin_id,
                  "user_id":user,
                  "html":html}
        quilltext = db.add_quill(values)
        values = {
            "id": quilltext.id,
            "header":quilltext.header
        }
        return json.dumps(values)

@app.route("/regin", methods=["POST"])
def regin():
    regin = request.form["regin"]
    session["regin"] = regin
    name = session.get("user",None)
    if name:
        quilltext = db.get_quill_header_by_regin(regin,name)
        result = []
        for i in quilltext:
            result.append({"id":i.id,
                      "header":i.header})
        return json.dumps(result)
    else:
        return "no user found", 401


@app.route("/login", methods=["POST"])
def login():
    name = request.form["name"]
    session["user"] = name
    session["regin"] = 1
    quilltexts = db.get_quill_header_by_regin(1,name)
    headers = []
    for i in quilltexts:
        headers.append({"header":i.header,
                        "id":i.id})
    return json.dumps(headers)

@app.route("/logout",methods=["POST"])
def logout():
    session["user"] = None
    session["regin"] = None
    return "logout"
if __name__ == "__main__":
    #app.run("",port=5001, use_reloader=False)
    wsgi.server(eventlet.listen(("0.0.0.0",5000)),app)
