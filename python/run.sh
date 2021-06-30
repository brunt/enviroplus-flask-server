# some notable dependencies to install:
# sudo apt install nginx && pip3 install uwsgi

# host flask app in dev mode:
#FLASK_APP=webserver.py /home/pi/.local/bin/flask run --host=0.0.0.0

# host flask app in "prod" mode:
nohup uwsgi --socket 0.0.0.0:8000 --protocol=http -w webserver:app >/dev/null 2>&1 &