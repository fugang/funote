# -*- coding: cp936 -*-
import db


##values = {"header":"testpybbb","text":"pythonsdft",
##          "html":"<div>python test result</div>",
##          "user_id":"abc",
##          "regin_id":1}
##quil = db.add_quill(values)
##print quil.id
##
for i in db.get_quill_header_by_regin(1,"test"):
    print  i.header, i.click_count
    

db.add_click_quill(1)    
##print  db.get_quill_by_id(1).text

##values = {"text":"change","html":"<div>chagne</div>"}
##db.update_quill(1,values)

##values = {"title":u"生活"}
##regin = db.add_regin(values)
##print regin.id, regin.title

##for i in db.query_text(u"必要"):
##    print i.id
##    print "+++"
