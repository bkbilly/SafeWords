#!/usr/bin/env python

from flask import Flask, send_from_directory, request, Response
from functools import wraps
import os
import json


class Safewords():
    """docstring for Safewords"""

    def __init__(self, safewordsFile):
        self.safewordsFile = safewordsFile

    def append(self, safewords):
        with open(self.safewordsFile, 'a') as f:
            for item in safewords:
                print item
                f.write("%s\n" % item)

    def getFirst(self):
        firstSafeword = "No More"
        allWordLists = self.getAllWordLists()
        if len(allWordLists) > 0:
            firstSafeword = allWordLists[0]
            del allWordLists[0]
            with open(self.safewordsFile, 'w') as f:
                for item in allWordLists:
                    f.write("%s" % item)
        return firstSafeword

    def clear(self):
        with open(self.safewordsFile, 'w') as f:
            f.write("")

    def getAllWordLists(self):
        allWordLists = []
        if(os.path.exists(self.safewordsFile)):
            with open(self.safewordsFile) as data_file:
                allWordLists = data_file.readlines()
        return allWordLists


app = Flask(__name__)
wd = os.path.dirname(os.path.realpath(__file__))
webDirectory = os.path.join(wd, 'web')
safewordsFile = os.path.join(wd, "safewords.txt")
mySafeWords = Safewords(safewordsFile)


def check_auth(username, password):
    myuser = "admin"
    mypass = "admin"
    return username == myuser and password == mypass


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/')
@requires_auth
def index():
    return send_from_directory(webDirectory, 'index.html')


@app.route('/main.css')
@requires_auth
def main():
    return send_from_directory(webDirectory, 'main.css')


@app.route('/icon.png')
@requires_auth
def icon():
    return send_from_directory(webDirectory, 'icon.png')


@app.route('/mycss.css')
@requires_auth
def mycss():
    return send_from_directory(webDirectory, 'mycss.css')


@app.route('/mycssMobile.css')
@requires_auth
def mycssMobile():
    return send_from_directory(webDirectory, 'mycssMobile.css')


@app.route('/myjs.js')
@requires_auth
def myjs():
    return send_from_directory(webDirectory, 'myjs.js')


@app.route('/jquery.js')
@requires_auth
def jqueryfile():
    return send_from_directory(webDirectory, 'jquery.js')


@app.route('/getSafeword')
@requires_auth
def getSafeword():
    return json.dumps(mySafeWords.getFirst())


@app.route('/getSafewordsLeft')
@requires_auth
def getSafewordsLeft():
    return json.dumps(len(mySafeWords.getAllWordLists()))


@app.route('/appendSafewords', methods=['Get', 'POST'])
@requires_auth
def appendSafewords():
    safewordList = request.args.getlist('safewordList[]')
    if safewordList is not None:
        mySafeWords.append(safewordList)
    return ""


@app.route('/clearSafewords')
@requires_auth
def clearSafewords():
    mySafeWords.clear()
    return ""


if __name__ == "__main__":
    app.run(debug=True)
