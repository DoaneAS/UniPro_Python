

def validate_base_sequence(base_sequence, RNAflag=False):
    """Return True if the string in base_sequence contains only T (or U if RNAflag), C, A, and G char; otherwise false"""
    seq = base_sequence.upper()
    return len(seq) == (seq.count('U' if RNAflag else 'T') +
                        seq.count('C') +
                        seq.count('A') +
                        seq.count('G'))


def gc_content(base_seq):
    assert validate_base_sequence(base_seq), \
        'argument has invalid chars'
    seq = base_seq.upper()
    return (base_seq.count('G') + base_seq.count('C') / len(base_seq))

if __name__ == '__main__':
    my_seq = 'ATGCGTGTGCAAGTGCTG'
    res = gc_content(my_seq)
    print res

import sys
sys.version()
