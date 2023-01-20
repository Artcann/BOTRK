from pprint import pprint
import botrk_back.flaskr.scripts.xss_stored_scanner_script

def xssCrawling():
    report = []
    file = open('botrk_back//dirsearch_output_test.txt', 'r')
    file_contents = file.readlines()
    for line in file_contents:
        address = line[13:].split(' ')[0].strip()
        if scan_xss(address, 'http://45.147.96.25:4242/login.php'):
            report.append(address)  
    return(address)


if __name__ == "__main__":
    import sys
    print(xssCrawling())