from subprocess import Popen, PIPE
import time

def getDirsearchScanReport(url):
    print(url)
    file_id = "dirsearch_output_test"
    process = Popen(["dirsearch", "-u", url, "-w botrk_back/wordlist.txt", "-t 80", "-r", "--recursion-depth=1", "--suffixes=.php", "-o", file_id], stdout=PIPE)
    start = time.time()
    print("start dirsearch scanning...")
    f = open(file_id, 'r')
    report = f.read()
    print (report)

    return report

getDirsearchScanReport("http://45.147.96.25:4242/")