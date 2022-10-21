import flaskr.services.port_scanner_service as port_scanner_service

from flask import Blueprint
route_bp = Blueprint('route_bp', __name__)

@route_bp.route("/port_scan/<address>")
def port_scan(address):
    return port_scanner_service.getPortScanReport(address)