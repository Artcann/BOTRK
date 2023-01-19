import flaskr.services.port_scanner_service as port_scanner_service
import flaskr.services.nikto_scanner_service as nikto_scanner_service
import flaskr.services.dirsearch_scanner_service as dirsearch_scanner_service
import flaskr.services.sqlmap_scanner_service as sql_scanner_service
import flaskr.services.brute_force_service as brute_force_service

from flask import Blueprint, request
from flask_cors import cross_origin
route_bp = Blueprint('route_bp', __name__)

@route_bp.route("/port_scan", methods=['GET'])
@cross_origin(origin="*")
def port_scan():
    return port_scanner_service.getPortScanReport(request.args.get('hostname'))


@route_bp.route("/nikto_scan", methods=['GET'])
@cross_origin(origin="*")
def nikto_scan():
    return nikto_scanner_service.getNiktoScanReport(request.args.get("hostname"))

@route_bp.route("/dirsearch_scan", methods=['GET'])
@cross_origin(origin="*")
def dirsearch_scan():
    return dirsearch_scanner_service.getDirsearchScanReport(request.args.get("hostname"),"testid") #request.args.get("id"))

@route_bp.route("/sqlmap_scan", methods=['GET'])
@cross_origin(origin="*")
def sqlmap_scan():
    return sql_scanner_service.getSqlmapScanReport()

@route_bp.route("/brute_force", methods=['GET'])
@cross_origin(origin="*")
def sqlmap_scan():
    return brute_force_service.bruteForce()