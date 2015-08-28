# -*- coding: cp936 -*-
import db


values = {"header":"testpybbb","text":"pythonsdft",
          "html":"<div>python test result</div>",
          "regin_id":2}
quil = db.add_quill(values)
print quil.id

##for i in db.get_quill_by_regin(1):
##    print i.header, i.text, i.html
    
for i in  db.get_quill_header_by_regin(1):
    print i.header, i.id
    
##print  db.get_quill_by_id(1).text

##values = {"text":"change","html":"<div>chagne</div>"}
##db.update_quill(1,values)

##values = {"title":u"生活"}
##regin = db.add_regin(values)
##print regin.id, regin.title
