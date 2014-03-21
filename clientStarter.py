import subprocess
import time
dic = {}
for x in range(1,6):
	time.sleep(1)
	dic[x] = subprocess.Popen(['python','clientGUI.py','test%d'%x], stdout = subprocess.PIPE)
while len(dic.keys()):
	for x in dic.keys():
		if dic[x].poll() == None:
			pass
		else:
			print "test%d: "%x, dic[x].stdout.read()
			del dic[x]
