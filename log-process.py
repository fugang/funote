import re
import os
import sys

d = {}

def process_log(log, n):
    requests = get_requests(log)
    files = get_files(requests,n)
    totals = file_occur(files)

def get_requests(f):
    log_line = f.read()
    pat = (r''
           '(\d+.\d+.\d+.\d+)\s-\s-\s' #IP address
           '\[(.+)\]\s' #datetime
           '"GET\s(.+)\s\w+/.+"\s\d+\s' #requested file
           '\d+\s"(.+)"\s' #referrer
           '"(.+)"' #user agent
        )
    requests = find(pat, log_line, None)
    return requests

def find(pat, text, match_item):
    match = re.findall(pat, text)
    if match:
        return match
    else:
        return False

def get_files(requests,n):
    #get requested files with req
    requested_files = []
    for req in requests:
        #req[2] for req file match, change to
        #data you want to count totals
        requested_files.append(req[n])
    return requested_files

def file_occur(files):
    #file occurrences in requested files
    for file in files:
        d[file] = d.get(file,0)+1

if __name__ == '__main__':
    if len(sys.argv) < 2:
        n = 0
    n = int(sys.argv[1])
    for i in os.listdir("/var/log/nginx/"):
        if i.find("access") == -1:
            continue
        name = "/var/log/nginx/"+i 
        log_file = open(name, 'r')
        process_log(log_file, n)
    print d
