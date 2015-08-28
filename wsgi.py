from flask import Flask, render_template, request, g, session
import db
import json
import eventlet
from eventlet import wsgi

SECRET_KEY = "zyHyipIPMTtQUe4P"

app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True
app.config.from_envvar('MINITWIT_SETTINGS', silent=True)
app.debug=True


@app.route("/")
def main():
    quilltexts = db.get_quill_header_by_regin(1)
    regins = db.get_regins()
    session["regin"] = 1
    return render_template("index.html", quilltext=quilltexts,regins=regins)
    
@app.route("/note/<tid>",methods=['GET', 'POST'])
def update_note(tid):
    if request.method=="GET":
        quilltext = db.get_quill_by_id(tid)
        text = quilltext.text
        html = quilltext.html
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
    regin_id = session["regin"]
    if request.method=="GET":
        return str(session["regin"])
    elif request.method == "POST":
        html = request.form["html"]
        text = request.form["text"]
        header = text.split("\n")[0]
        values = {"header":header,
                  "text":text,
                  "regin_id":regin_id,
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
    quilltext = db.get_quill_header_by_regin(regin)
    result = []
    for i in quilltext:
        result.append({"id":i.id,
                      "header":i.header})
    return json.dumps(result)

@app.route("/login", methods=["POST"])
def login():
    name = request.form["name"]
    session["user"] = name
    return name
    
if __name__ == "__main__":
    #app.run("",port=5001, use_reloader=False)
    wsgi.server(eventlet.listen(("0.0.0.0",5001)),app)
