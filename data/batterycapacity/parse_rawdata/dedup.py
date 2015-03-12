__author__ = 'sunzhennan'

import sys

f = open("result.csv")
result = {}
for line in f:
    csv = line.strip().rstrip().rsplit(",", 1)
    if len(csv) < 2:
        continue
    try:
        capacity = int(csv[-1])
    except ValueError as e:
        continue
    fingerprint = csv[0]
    csv = fingerprint.split("/")
    if len(csv) < 3:
        continue
    vendor = csv[0].lower()
    model = csv[1].lower()

    if (vendor, model) in result:
        result[(vendor, model)].append(capacity)
    else:
        result[(vendor, model)] = [capacity]

for k in result:
    sys.stdout.write("%s,%s,%d:" % (k[0], k[1], len(result[k])))
    for v in result[k]:
        sys.stdout.write("%d," % v)
    sys.stdout.write("\n")
