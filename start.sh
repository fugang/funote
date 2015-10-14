#uwsgi --socket 0.0.0.0:8080 --protocol=http -w wsgi:app
uwsgi --socket /tmp/funote.sock -w wsgi:app --chmod-socket=666
