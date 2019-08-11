import json

with open('theData.txt','r') as f:
	dct = json.loads(f.read().strip())

print(dct['4'])
