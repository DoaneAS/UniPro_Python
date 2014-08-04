

import urllib
import urllib2


def map_unid(uniprotid):
    url = 'http://www.uniprot.org/mapping/'
    params = {
        'from': 'ACC',
        'to': 'GENECARDS_ID',
        'format': 'tab',
        'query': uniprotid
    }

    data = urllib.urlencode(params)
    request = urllib2.Request(url, data)
    contact = "ashley.doane@gmail.com"
    request.add_header('User-Agent', 'Python %s' % contact)
    response = urllib2.urlopen(request)
    page = response.read(200000)
    print page


def get_uniprot_metadata(uniprotid):
    'http://www.uniprot.org/batch/'


if __name__ == '__main__':
    uniprotid = 'P01116'
    map_unid(uniprotid)