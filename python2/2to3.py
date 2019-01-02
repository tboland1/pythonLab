import urllib2

try:
        x = urllib2.urlopen("http://pythonprogramming.net").read()
            print x
except Exception, e:
        print str(e)

