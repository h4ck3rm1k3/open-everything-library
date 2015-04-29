import re

for x in xrange(0,45):
    filename = "text%d.md" % x
    f = open(filename)
    data = ""
    for x in f.readlines():
        data = data + x
        
    heading = re.findall(r'\#\s+([\w\:\.\- ]+)\n',data)
    if len(heading):
        h = heading[0]
        h = h.rstrip()

        h = h.replace(" ","_")
        h = h.replace(".","_")
        h = h.replace(":","_")
        h = h.replace("-","_")

        #print "Page", filename
        print "* [[{0}]]".format(h)

        o = open ("../open-everything-library.wiki/" + h + ".md","w")
        o.write(data)
        o.close()
        #pass
    else:

        print data
        

