import json,re

def normalize(k):

    k = k.lower()
    k = k.strip()
   
    # trim middle whitespace 
    k = re.sub(r'\s+', ' ', k)
    k = k.strip()
    
    # (16g) (32g)
    k = re.sub(r'\(.*[0-9]*g\)', '', k)
    k = k.strip()
    
    return k
    
    
newj = json.loads(open("battery.json").read())
oldj = json.loads(open("D:\\workspace\\lbesecv3\\trunk\\assets\\batterycapacity.ini").read())

newd = newj["type"]
oldd = oldj["type"]

print len(newd)
print len(oldd)

merged = dict()

for k,v in oldd.iteritems():
    merged[k] = v

for k,v in newd.iteritems():
    if not merged.has_key(k):
        merged[(k)] = v

print len(merged)
output = open("batterycapacity.ini", "w")
output.write(json.dumps({"type":oldd}))
output.close()

output = open("merged.csv", "w")
for k,v in merged.iteritems():
    output.write("%s,%s\n" % (k,v))
output.close()

output = open("oldd.csv", "w")
for k,v in oldd.iteritems():
    output.write("%s,%s\n" % (k,v))
output.close()