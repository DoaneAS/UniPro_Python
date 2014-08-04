"""
python script retrieves uniprot sequence and metadata for list of uniprot ids

"""
import requests
import sys
import argparse

url = 'http://www.uniprot.org/'


def parse_uniprot(uni_txt):
    """
    Parses the text of metadata retrieved from uniprot.org.

    Only a few fields have been parsed, but this provides a
    template for the other fields.

    A single description is generated from joining alternative
    descriptions.

    Returns a dictionary with the main UNIPROT ACC as keys.
    """

    tag = None
    uniprot_id = None
    metadata_by_acc = {}
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
            metadata_by_acc[uniprot_id] = {
                'id': uniprot_id,
                'is_reviewed': is_reviewed,
                'length': length,
                'sequence': '',
                'accs': [],
                'gene': [],
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
                    entry['pdb'] = words[1][:-1]
                if 'pdbs' not in entry:
                    entry['pdbs'] = []
                entry['pdbs'].append(words[1][:-1])
            if 'RefSeq' in words[0]:
                if 'refseq' not in entry:
                    entry['refseq'] = []
                ids = [w[:-1] for w in words[1:]]
                entry['refseq'].extend(ids)
            if 'KEGG' in words[0]:
                if 'kegg' not in entry:
                    entry['kegg'] = []
                ids = [w[:-1] for w in words[1:]]
                ids = filter(lambda w: len(w) > 1, ids)
                entry['kegg'].extend(ids)
            if 'GO' in words[0]:
                if 'go' not in entry:
                    entry['go'] = []
                entry['go'].append(' '.join(words[1:]))
            if 'Pfam' in words[0]:
                if 'pfam' not in entry:
                    entry['pfam'] = []
                entry['pfam'].append(words[1][:-1])

        if tag == "OS":
            if 'organism' not in entry:
                entry['organism'] = ""
            entry['organism'] += line
    #     if tag == "DE":
    #         if 'descriptions' not in entry:
    #             entry['descriptions'] = []
    #         entry['descriptions'].append(line)
    #     if tag == "CC":
    #         if 'comment' not in entry:
    #             entry['comment'] = ''
    #         entry['comment'] += line + '\n'

    # for entry in metadata_by_acc.values():
    #     descriptions = entry['descriptions']
    #     for i in reversed(range(len(descriptions))):
    #         description = descriptions[i]
    #         if 'Short' in description or 'Full' in description:
    #             j = description.find('=')
    #             descriptions[i] = description[j + 1:].replace(';', '')
    #         else:
    #             del descriptions[i]
    #     entry['description'] = '; '.join(descriptions)

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
    #return uni_txt
    res = parse_uniprot(uni_txt)
    return res



import sys

if __name__ == '__main__':
    ids = ['P01116', 'P15056']
    res = pull_uni(ids)
    #sys.stdout = open('log.txt', 'a')
    F = open('resfile.pkl', 'wb')
    import pickle
    pickle.dump(res, F)
    F.close()
    import json
    R = json.dumps(res)
    json.dump(res, fp=open('res4json.txt', 'w'), indent=4)
    json.dump(res, fp=open('res6json.json', 'w'), indent=4)
    print json.dumps(res, sort_keys=True, indent=4, separators=(',', ': '))



    #print >> afile, res