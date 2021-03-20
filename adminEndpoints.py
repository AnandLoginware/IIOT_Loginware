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
      
@admin.route('/updateNetworkDetails', methods = ['POST'])
def UpdatenetworkDetails():
    ip = request.get_json()['ip']
    gateway = request.get_json()['gateway']
    dns = request.get_json()['dns']
    networkFileData = "interface eth0 \n static ip_address = {}\n static routers = {}\n static domain_name_servers = {}".format(ip, gateway, dns)
    print(networkFileData)
    try:
        result = networkConf.query.filter_by(id = 1).scalar()
        if result != None:
            db.session.query(networkConf).filter(networkConf.id == 1).update({"ip" : ip, "gateway" : gateway, "dns" : dns})
            db.session.commit()
            with open('/etc/dhcpcd.conf', 'w') as f:
                f.write(networkFileData)
                f.close()
            return jsonify({"result" : {"status" : 1, "message" : "Network details updated successfully"}})
        else:
            networkConfObject = networkConf(ip = ip, gateway = gateway, dns = dns)
            db.session.add(networkConfObject)
            db.session.commit()
            with open('/etc/dhcpcd.conf', 'w') as f:
                f.write(networkFileData)
                f.close()
            return jsonify({"result" : {"status" : 1, "message" : "Network details saved successfully"}})
    except Exception as e:
        return jsonify({"result" : {"status" : 0, "message" : Something went wrong"}})
        
