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
                'accs': [],
            }
            entry = metadata_by_seqid[uniprot_id]
            print metadata_by_seqid
        if tag == "SQ":
            if words[0] != "SEQUENCE":
                entry['sequence'] += ''.join(words)
        if tag == "AC":
            accs = [w.replace(";", "") for w in words]
            entry['accs'].extend(accs)
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
        if tag == "GN":
            if 'gene' not in entry and len(words) > 0:
                pieces = words[0].split("=")
                if len(pieces) > 1 and 'name' in pieces[0].lower():
                    entry['gene'] = pieces[1].replace(';', '').replace(',', '')
        if tag == "OS":
            if 'organism' not in entry:
                entry['organism'] = ""
            entry['organism'] += line
        if tag == "DE":
            if 'descriptions' not in entry:
                entry['descriptions'] = []
            entry['descriptions'].append(line)
        if tag == "CC":
            if 'comment' not in entry:
                entry['comment'] = ''
            entry['comment'] += line + '\n'

    for entry in metadata_by_seqid.values():
        descriptions = entry['descriptions']
        for i in reversed(range(len(descriptions))):
            description = descriptions[i]
            if 'Short' in description or 'Full' in description:
                j = description.find('=')
                descriptions[i] = description[j + 1:].replace(';', '')
            else:
                del descriptions[i]
        entry['description'] = '; '.join(descriptions)

    print metadata_by_seqid
