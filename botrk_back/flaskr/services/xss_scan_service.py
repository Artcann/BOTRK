from pprint import pprint
from ..scripts.xss_scanner_script import scan_xss

def xssCrawling():
    xssStored = []
    xssReflected = []
    xssDict = {
        "xxsStored": xssStored,
        "xssReflected": xssReflected
    }

    file = open('dirsearch_output_test.txt', 'r')
    file_contents = file.readlines()
    for line in file_contents:
        address = line[13:].split(' ')[0].strip()
        if scan_xss(address, 'http://45.147.96.25:4242/login.php'):
            if scan_xss(address, 'http://45.147.96.25:4242/login.php', stored_check= True):
                xssReflected.append(address)                
            else:
                xssStored.append(address)

    return(xssDict)