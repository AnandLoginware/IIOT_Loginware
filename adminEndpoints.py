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
       
@admin.route('/updateServerIP', methods = ['POST'])
def serverConfiguration():
  endpoint = request.get_json()['endpoint'] 
  try:
      result=serverConf.query.filter_by(id = 1).scalar()
      if result != None:
          db.session.query(serverConf).filter(serverConf.id == 1).update({serverConf.ip:endpoint})
          db.session.commit()
          return jsonify({"result" : {"message" : "server credentials updated successfully", "status" : 1}})
      else:
          serverConfObj = serverConf(id = 1,ip = endpoint)
          db.session.add(serverConfObj) 
          db.session.commit()
          return jsonify({"result" : {"message" : "server credentials saved successfully", "status" : 1}})  
  except Exception as e:
      print(e)   
      return jsonify({"result" : {"message" : "something went wrong", "status" : 0}})
