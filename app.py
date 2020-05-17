from gevent.pywsgi import WSGIServer
from flask import Flask
from os import path, remove
import requests
from pathlib import Path

app = Flask(__name__)

SECONDS_IN_DAY = 60 * 60 * 24

@app.route("/")
def hello():
        return "Softcatalà | VirtualBox ⟹ Transifex importer"

@app.route("/virtualbox.ts")
def virtualbox_ts():
        
        filename = 'VirtualBox_xx_YY.ts'
        localfile = 'data/' + filename
        maybe_download_file(localfile, filename)
        
        return Path(localfile).read_text()

def maybe_download_file(localfile, filename):
        
        if path.exists(localfile):
                age = path.getmtime(localfile)
                if age > SECONDS_IN_DAY:
                        remove(localfile)
        
        if not path.exists(localfile):
                base = "https://www.virtualbox.org/download/testcase/nls/6.1/"
                r = requests.get(base+filename, allow_redirects=True)
                new_content = r.text.replace('<numerusform></numerusform>', '<numerusform></numerusform><numerusform></numerusform>')
                open(localfile, 'w').write(new_content)

        
        

http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()


