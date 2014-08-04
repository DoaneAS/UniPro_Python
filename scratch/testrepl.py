import requests
import sys
import argparse
import pprint
import json

url = 'http://www.uniprot.org/'
ids = ['P01116', 'P15056']

def pull_uni(ids, format='txt'):
    """ request entries by uniprot acc using batch retrieval
    Args:
        ids: list of ids to retrieve
        format: txt by default
        possible formats:
        txt, xml, rdf, fasta, gff"""

    tool = 'batch/'
    if type(ids) is not list:
        ids = [ids]
    query = ' '.join(ids)
    query = list(set(query.split()))
    queries = [query[i:i + 100] for i in xrange(0, len(query), 100)]
    data = {'format': format}
    responses = [
        requests.post(url + tool, data=data, files={'file': ' '.join(query)}) for query in queries]
    uni_txt = ''.join([response.text for response in responses])
    return uni_txt
    #res = parse_uniprot(uni_txt)
    #return res
uni_txt = pull_uni(ids)
#json.dump(uni_txt, fp=open('unparsed.txt', 'w'), indent=4)

tag = None
uniprot_id = None
metadata_by_seqid = {}
for l in uni_txt.splitlines():
    ttag = l[:5].strip()
    if ttag and ttag != tag:
        tag = ttag
    line = l[5:].strip()
    words = line.split()
    if tag == "ID":
        uniprot_id = words[0]
        is_reviewed = words[1].startswith('Reviewed')
        length = int(words[2])
        metadata_by_seqid[uniprot_id] = {
            'id': uniprot_id,
            'is_reviewed': is_reviewed,
            'length': length,
            'sequence': '',
            'gene': [],
            'gn': "",
            'accs': [],
        }
        entry = metadata_by_seqid[uniprot_id]
    if tag == "SQ":
        if words[0] != "SEQUENCE":
            entry['sequence'] += ''.join(words)
    if tag == "GN":
        if 'gene' not in entry:
            entry['gene'] = []
            parts = words[0].split("=")
            entry['gene'].append(parts[1])
    if tag == "AC":
        if 'accs' not in entry:
            entry['accs'] = []
        accs = [c.replace(";","") for c in words]
        entry['accs'].extend(accs)

pprint.pprint(metadata_by_seqid)
import os
d = os.getcwd()
print d

#pprint.pprint(uni_txt)