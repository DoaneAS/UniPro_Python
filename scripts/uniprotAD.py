import requests
import sys
import argparse

url = 'http://www.uniprot.org/'


def get_parts(uni_txt):
    for line in uni_txt.splitlines():
        k, v = [line[:5].strip(), line[5:].strip()]
        return k, v.split()


def parse_uniprot(uni_txt):
    """Parse metadata text from uniprot.org

     Returns a dictionary with the UNIPROT ACC as keys.
     """
    uniprot_id = None
    metadata_by_acc = {}
    tag = None
    # with get_parts
    for l in uni_txt.splitlines():
        ttag = l[:5].strip()
        if ttag and ttag != tag:
            tag = ttag
        words = (l[5:].strip()).split()
        if tag == "ID":
            uniprot_id = words[0]
            is_reviewed = words[1].startswith('Reviewed')
            length = int(words[2])
            metadata_by_acc[uniprot_id] = {
                'id': uniprot_id,
                'is_reviewed': is_reviewed,
                'length': length,
                'sequence': '',
                'accs': [],
                'gene': [],
                'refseq': []
            }
            entry = metadata_by_acc[uniprot_id]

        if tag == "SQ":
            if words[0] != "SEQUENCE":
                entry['sequence'] += ''.join(words)

        if tag == "AC":
            accs = [w.replace(";", "") for w in words]
            entry['accs'].extend(accs)

        if tag == "GN":
            if 'gene' not in entry:
                entry['gene'] = []
            parts = words[0].split("=")
            entry['gene'].append(parts[1])

        if tag == "DR":
            if 'PDB' in words[0]:
                if 'pdb' not in entry:
                    entry['pdb'] = [words[1][:-1]]
                if 'pdbs' not in entry:
                    entry['pdbs'] = []
                entry['pdbs'].append(words[1][:-1])
            if 'RefSeq' in words[0]:
                if 'refseq' not in entry:
                    entry['refseq'] = []
                ids = [w[:-1] for w in words[1:]]
                entry['refseq'].extend(ids)

        if tag == "DE":
            # if "RecName" in words[0]:
            if 'full_name' not in entry:
                fid = [w.replace("Full=", " ") for w in words[1:]]
            entry['full_name'] = [" ".join(fid[0:])]

    return metadata_by_acc


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
    # return uni_txt
    res = parse_uniprot(uni_txt)
    return res


import sys
import pprint

if __name__ == '__main__':
    ids = ['P01116', 'P15056']
    res = pull_uni(ids)
    pprint.pprint(res)
    import json
    json.dump(res, fp=open('uniprot_result.txt', 'w'), indent=4)
    json.dump(res, fp=open('uniprot_result.json', 'w'), indent=4)
    print json.dumps(res, sort_keys=True, indent=4, separators=(',', ': '))
