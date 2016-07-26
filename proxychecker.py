#!/usr/bin/python
import requests
import json
#import gevent
import threading

url = 'https://ifconfig.co/json' # checker url
verify=False#Verify ssl certificate
numOfThreads = 1000
working = []
proxies = []
threadList = []
def chunkify(lst,n):
	return [ lst[i::n] for i in xrange(n) ]
def check(proxies):
	for i in proxies:
		item=i.rstrip()
		proxies = {"https":item}
		try:
			r = requests.get(url,verify=verify,timeout=10,proxies=proxies)
			output = json.loads(r.content)
			#if output["country"]!="Pakistan":
			working.append(item)
			print ("%s,%s"% (output["ip"],output["country"]))
		except Exception, detail:
			return False
if __name__ == "__main__":
	f = open('proxy.txt', 'r')
	proxylist = f.readlines()
	print "Number of Proxies to Check ",len(proxylist)
	proxylist=chunkify(proxylist,numOfThreads)
	for i in range(0,numOfThreads):
		#threadList.append(gevent.spawn(check, proxylist[i]))
		t= threading.Thread(target=check,args=(proxylist[i],))
		t.start()
		threadList.append(t)
	# Wait for all threads to complete
	#gevent.joinall(threadList)
	for t in threadList:
		t.join()
	with open('working_proxy.txt', 'a') as out_file:
		out_file.write('\n'.join(working)) # This will create a string with all of the items in data separated by new-line characters
		out_file.write("\n")
	print "Number of working proxies ",len(working)
	print "Exiting Main Thread"
