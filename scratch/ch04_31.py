### Example 4-31: Reading sequences from a GenBank file

def get_Uniprot_items_and_AAsequence_from_file(filename):
    with open(filename) as file:
        return [get_ids(file), get_items(file), get_sequence(file)]

def get_ids(kras):
    line = kras.readline()
    while not line.startswith('VERSION'):
        line = kras.readline()
    parts = line.split()                   # split at whitespace; removes \n
    assert 3 == len(parts), parts          # should be VERSION acc GI:id
    giparts = parts[2].partition(':')
    assert giparts[2], giparts             # if no colon, [1] & [2] are empty
    assert giparts[2].isdigit()            # all numbers?
    return (parts[1], giparts[2])

def get_items(kras, testfn=None):
    """Return all the items in kras; if testfn then include only those
    items for which testfn is true"""
    return [item for item in item_generator(kras)
            if not testfn or testfn(item)]

def get_sequence(kras):
    """Return the DNA sequence found at end of kras"""
    # When this is called the ORIGIN line should have just been read,
    # so we just have to read the sequence lines until the // at the end
    seq = ''
    line = kras.readline()
    while not line.startswith('//'):
        seq += line[10:-1].replace(' ', '')
        line = kras.readline()
    return seq

def skip_intro(kras):
    """Skip introductory text that appears before the first item in
    kras"""
    line = kras.readline()
    while not line.startswith('FEATURES'):
        line = kras.readline()

attribute_prefix = 21*' ' + '/'
def is_attribute_start(line):
    return line and line.startswith(attribute_prefix)

def is_feature_start(line):
    return line and line[5] != ' '

def item_generator(kras):
    """Return a generator that produces a FASTA sequence from kras
    each time it is called"""
    skip_intro(kras)
    line = kras.readline()
    while not line.startswith('ORIGIN'):
        assert is_feature_start(line)      # line should start a feature
        feature, line =  read_feature(kras, line)
        # need to keep line to feed back to read_feature
        yield feature

def read_feature(kras, line):
    feature = line.split()
    props = {}
    line = kras.readline()
    while not is_feature_start(line):
        key, value = line.strip()[1:].split('=')
        # remove initial / and split into [feature, value]
        if value[0] == '"':
            value = value[1:]              # remove first "; remove final " later
        fullvalue, line = read_value(kras, line, value)
        # need to keep line to feed back to read_value
        props[key] = fullvalue
    feature.append(props)
    return feature, line

def read_value(kras, line, value):
    line = kras.readline()
    while (not is_attribute_start(line) and
           not is_feature_start(line)):
        value += line.strip()
        line = kras.readline()
    if value[-1] == '"':
        value = value[:-1]                 # remove final "
    return value, line

data = get_GenBank_items_and_sequence_from_file('../data/sample.gb')

pprint.pprint(data)
