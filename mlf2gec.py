'''
(1) GED: 1best.mlf <=> gec.tsv
(2) GEC: 1best.mlf <=> gec.txt
'''

import sys
from helper import mlf_to_sentences

def main():
    if len(sys.argv) != 3:
        print("Usage: mlf2gec.py mlf out")
        return

    mlf = sys.argv[1]
    out = sys.argv[2]

    gecout = out + '.gec.out.txt'
    gectsv = out + '.gec.out.tsv'

    sentences = mlf_to_sentences(mlf)

    with open(gecout, 'w') as file:
        for sentence in sentences:
            file.write(' '.join(sentence[1:-1]) + '\n')

    with open(gectsv, 'w') as file:
        for sentence in sentences:
            for word in sentence:
                file.write(word + '\n')
            file.write('\n')


if __name__ == '__main__':
    main()
