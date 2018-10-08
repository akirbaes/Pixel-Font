def printchars():
	for i in range(512):
		if(i%16==0 and i>0):
			print()
		try:
			if(chr(i)!="\n" and chr(i)!="\t"):
				print(end=chr(i))
			else:
				print(end=" ")
		except:
			print(end=" ")
			#print(end="?")
