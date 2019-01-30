"""
Add bias to a lattice file
    - add bias (b) to the arcs appearing in the reference


"test-v3/conll/rescore-1B-rnnlm300-300-t050/lattices/sentence2.rec"
0 0 <s> 0.000000
0 0 GENETIC -11.265489
0 0 RISK -5.387525
0 0 REFERS -9.138419
0 0 MORE -8.812930
0 0 TO -0.719627
0 0 YOUR -6.608528
0 0 CHANCE -9.218029
0 0 OF -0.915680
0 0 INHERITING -7.505935
0 0 DISORDER -10.895185
0 0 OR -7.586551
0 0 DISEASE -7.063920
0 0 </s> -4.043802


N=30   L=32
I=0    t=0.00  W=CHANCE
I=1    t=0.00  W=OF
I=2    t=0.00  W=INHERITING
I=3    t=0.00  W=AN
I=4    t=0.00  W=CHANCE
I=5    t=0.00  W=OF
I=6    t=0.00  W=INHERITING
I=7    t=0.00  W=A
I=8    t=0.00  W=CHANCE
I=9    t=0.00  W=OF
I=10   t=0.00  W=INHERITING
I=11   t=0.00  W=THE
I=12   t=0.00  W=!NULL
I=13   t=0.00  W=<s>
I=14   t=0.00  W=GENETIC
I=15   t=0.00  W=RISK
I=16   t=0.00  W=REFERS
I=17   t=0.00  W=MORE
I=18   t=0.00  W=TO
I=19   t=0.00  W=YOUR
I=20   t=0.00  W=CHANCE
I=21   t=0.00  W=OF
I=22   t=0.00  W=INHERITING
I=23   t=0.00  W=!NULL
I=24   t=0.00  W=!NULL
I=25   t=0.00  W=DISORDER
I=26   t=0.00  W=OR
I=27   t=0.00  W=DISEASE
I=28   t=0.00  W=</s>
I=29   t=0.00  W=!NULL

J=0     S=19   E=0    a=0.00      l=-9.218  r=0.000
J=1     S=0    E=1    a=0.00      l=-0.916  r=0.000
J=2     S=1    E=2    a=0.00      l=-7.506  r=0.000
J=3     S=2    E=3    a=0.00      l=-5.676  r=0.000
J=4     S=19   E=4    a=0.00      l=-9.218  r=0.000
J=5     S=4    E=5    a=0.00      l=-0.916  r=0.000
J=6     S=5    E=6    a=0.00      l=-7.506  r=0.000
J=7     S=6    E=7    a=0.00      l=-3.748  r=0.000
J=8     S=19   E=8    a=0.00      l=-9.218  r=0.000
J=9     S=8    E=9    a=0.00      l=-0.916  r=0.000
J=10    S=9    E=10   a=0.00      l=-7.506  r=0.000
J=11    S=10   E=11   a=0.00      l=-1.864  r=0.000
J=12    S=12   E=13   a=0.00      l=0.000   r=0.000
J=13    S=13   E=14   a=0.00      l=-11.265 r=0.000
J=14    S=14   E=15   a=0.00      l=-5.388  r=0.000
J=15    S=15   E=16   a=0.00      l=-9.138  r=0.000
J=16    S=16   E=17   a=0.00      l=-8.813  r=0.000
J=17    S=17   E=18   a=0.00      l=-0.720  r=0.000
J=18    S=18   E=19   a=0.00      l=-6.609  r=0.000
J=19    S=19   E=20   a=0.00      l=-9.218  r=0.000
J=20    S=20   E=21   a=0.00      l=-0.916  r=0.000
J=21    S=21   E=22   a=0.00      l=-7.506  r=0.000
J=22    S=22   E=23   a=0.00      l=0.000   r=0.000
J=23    S=3    E=24   a=0.00      l=0.000   r=0.000
J=24    S=7    E=24   a=0.00      l=0.000   r=0.000
J=25    S=11   E=24   a=0.00      l=0.000   r=0.000
J=26    S=23   E=24   a=0.00      l=0.000   r=0.000
J=27    S=24   E=25   a=0.00      l=-10.895 r=0.000
J=28    S=25   E=26   a=0.00      l=-7.587  r=0.000
J=29    S=26   E=27   a=0.00      l=-7.064  r=0.000
J=30    S=27   E=28   a=0.00      l=-4.044  r=0.000
J=31    S=28   E=29   a=0.00      l=0.000   r=0.000

"""

import gzip
import sys
import pdb

def read_lattice(latpath):

    with gzip.open(latpath, 'rb') as file:
        lines = file.readlines()

    lines = [line.decode('UTF-8').strip() for line in lines]

    # skip headers
    header = lines[:6]
    a = lines[5].split()
    N = int(a[0].strip('N='))
    L = int(a[1].strip('L='))


    idx0 = 6

    _nodes = lines[idx0:idx0+N]
    _edges = lines[idx0+N:idx0+N+L]

    nodes = {} # nodes[I] = word
    edges = {} # edges[J] = (node_s, node_e, score)

    for line in _nodes:
        items = line.split()
        I = int(items[0].strip('I='))
        # t = float(items[1].strip('t='))
        W = items[2].strip('W=').lower()
        nodes[I] = W

    for line in _edges:
        items = line.split()
        J = int(items[0].strip('J='))
        S = int(items[1].strip('S='))
        E = int(items[2].strip('E='))

        a = float(items[3].strip('a='))
        l = float(items[4].strip('l='))
        r = float(items[5].strip('r='))

        edges[J] = (S, E, a, l, r)

    return header, nodes, edges

def read_reference(refpath):
    """
    reference aka source to GEC system
    return:
        references where
            references[0] = [('<s>', 'keeping'), ('keeping', 'the'), ('the', 'secret'), ...]
            etc
    """
    references = []
    with open(refpath, 'r') as file:
        for line in file:
            words = line.strip().split()
            words = ['<s>'] + words
            words = words + ['</s>']

            ref = []

            for i in range(len(words)-1):
                ref.append((words[i], words[i+1]))

            references.append(ref)

    return references

def add_bias(bias, refpath, latdir_in, latdir_out):
    references = read_reference(refpath=refpath)
    num_lat = len(references)
    for i in range(num_lat):
        lat_in = latdir_in + "/sentence{}.lat.gz".format(i)
        lat_out = latdir_out + "/sentence{}.lat.gz".format(i)
        header, nodes, edges = read_lattice(latpath=lat_in)
        reference = references[i]

        for j, val in edges.items():
            S, E, a, l, r = val
            word_s = nodes[S]
            word_e = nodes[E]

            if (word_s, word_e) in reference:
                a += bias

            edges[j] = (S,E,a,l,r)

        write_new_lattice(lat_out, header, nodes, edges)


def write_new_lattice(latpath, header, nodes, edges):
    with gzip.open(latpath, 'wb') as file:
        for line in header:
            line = line + '\n'
            file.write(line.encode())

        for i, word in nodes.items():

            if word not in ['<s>', '</s>']:
                word = word.upper()

            line = "I={}\tt=0.00\tW={}\n".format(i, word)
            file.write(line.encode())

        for j, val in edges.items():

            S, E, a, l, r = val

            line = "J={}\tS={}\tE={}\ta={:.2f}\tl={:.3f}\tr={:.3f}\n".format(j,S,E,a,l,r)
            file.write(line.encode())

    print("wrote: ", latpath)
    return

if __name__ == '__main__':
    refpath = 'tmp-bias/conll_first4.gec.src'
    latdir_in = 'tmp-bias/lat_in'
    latdir_out = 'tmp-bias/lat_out'

    bias = 50

    add_bias(bias, refpath, latdir_in, latdir_out)
