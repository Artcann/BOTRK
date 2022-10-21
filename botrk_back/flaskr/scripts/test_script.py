import portscanner

target = portscanner.portscan("scanme.nmap.org", 100)
target.scan()
print([target.banners, target.open_ports])