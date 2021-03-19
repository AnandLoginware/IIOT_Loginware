from flask import Blueprint, request, jsonify
from models import *
from flask_sqlalchemy import SQLAlchemy

admin = Blueprint('admin', __name__)

@admin.route('/getServerIP', methods = ['GET'])
def getServerIP():
    try:
        result = serverConf.query.get(1)
        if result != None:
            serverIp = result.ip
            print(serverIp)
            return jsonify({"result" : {"status" : 1, "data" : serverIp, "message" : "success"}})
        else:
            return jsonify({"result" : {"status" : 1, "message" : "no previous data found", "data" : ""}})
    except Exception as e:
        print(e)
        return jsonify({"result" : {"status" : 0, "data" : "", "message" : "failed"}})
        