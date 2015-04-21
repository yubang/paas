#coding:UTF-8

from flask import Flask
from lib.buildConfig import buildPhpConfig

app=Flask(__name__)

@app.route("/")
def index():
    buildPhpConfig(5,"/etc","","")
    return "debug"
    
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=8000)
