import json
from flask import Blueprint, request
import flaskr.services.port_scanner_service as port_scanner_service
import flaskr.services.nikto_scanner_service as nikto_scanner_service
import flaskr.services.dirsearch_scanner_service as dirsearch_scanner_service
import flaskr.services.sql_scanner_service as sql_scanner_service
import flaskr.services.brute_force_service as brute_force_service
import flaskr.services.command_injection_service as command_injection
import flaskr.services.xss_scan_service as xss_scan_service
from flask_cors import cross_origin, CORS

route_bp = Blueprint('route_bp', __name__)
CORS(route_bp)

@route_bp.route("/port_scan", methods=['GET'])
@cross_origin(origin="*")
def port_scan():
    return port_scanner_service.getPortScanReport(request.args.get('hostname'))

@route_bp.route("/reverse_shell", methods=['GET'])
@cross_origin(origin="*")
def reverse_shell():
    args = request.args
    command_injection.reverse_shell(listenner_url = args.get('listenner_url'),listenner_port = args.get('listenner_port'))
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@route_bp.route("/dirsearch_scan", methods=['GET'])
@cross_origin(origin="*")
def dirsearch_scan():
    return dirsearch_scanner_service.getDirsearchScanReport(request.args.get("hostname"))

@route_bp.route("/sqlmap_scan", methods=['GET'])
@cross_origin(origin="*")
def sqlmap_scan():
    return sql_scanner_service.scanSQLInjection()

@route_bp.route("/brute_force_scan", methods=['GET'])
@cross_origin(origin="*")
def brute_force():
    return brute_force_service.bruteForce()

@route_bp.route("/xss", methods=['GET'])
@cross_origin(origin="*")
def xss_crawling():
    return xss_scan_service.xssCrawling() 
