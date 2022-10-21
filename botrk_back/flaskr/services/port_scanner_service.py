from flaskr.scripts.portscanner import portscan

def getPortScanReport(target_address):
    target = portscan(target_address, 81)
    target.scan()
    return target.open_ports
