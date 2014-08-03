import urllib
import urllib2
import requests

def map(ids, f, t, format= 'tab'):
    tool = 'mapping/'
    url = 'http://www.uniprot.org/'
    params = {
        'from': f,
        'to': t,
        'format': 'tab',
        'query': ' '.join(ids)}
    response = requests.post(url + tool, params=params)
    #print params
    page = response.text
    result = dict()
    for row in page.splitlines()[1:]:
        key, value = row.split('\t')
        if key in result:
            result[key].add(value)
        else:
            result[key] = set([value])
    return result



# data = urllib.urlencode(params)
# request = urllib2.Request(url, data)
# contact = ""  # Please set your email address here to help us debug in case of problems.
# request.add_header('User-Agent', 'Python %s' % contact)
# response = urllib2.urlopen(request)
# page = response.read(200000)

ids = ['P01116', 'P15056']
f = 'ACC'
t = ['ENSEMBL_ID',]
#'EMBL_ID', 'P_REFSEQ_AC']
res = map(ids, f, t)
print res
