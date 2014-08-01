import urllib
import urllib2

url = 'http://www.uniprot.org/mapping/'

params = {
    'from': 'ACC',
    'to': 'P_REFSEQ_AC',
    'format': 'tab',
    'query': 'P13368 P20806 Q9UM73 P97793 Q17192'
}

data = urllib.urlencode(params)
request = urllib2.Request(url, data)
contact = "ashley.doane@gmail.com"
request.add_header('User-Agent', 'Python %s' % contact)
response = urllib2.urlopen(request)
page = response.read(200000)
