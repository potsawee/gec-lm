import sys
from helper import AgidHandler
from tqdm import tqdm

def main():
    orig_dict = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/train.lst'
    wlist = []
    with open(orig_dict, 'r') as file:
        for line in file:
            word = line.strip()
            wlist.append(word)

    print('count = ', len(wlist))

    a = AgidHandler()
    a.read_infl('/home/alta/imports/agid-2016.01.19/infl.txt')

    for word in tqdm(a.word_keys):
        word = word.upper()
        if word not in wlist:
            wlist.append(word)
        else:
            pass

    print('count = ', len(wlist))

def main2():
    a = AgidHandler()
    a.read_infl('/home/alta/imports/agid-2016.01.19/infl.txt')
    wlist = a.word_keys

    agid_dict = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/agid.lst'
    with open(agid_dict, 'w') as file:
        for word in wlist:
            file.write('{}\n'.format(word.upper()))

    print('count = ', len(wlist))

def main3():
    a = AgidHandler()
    a.read_infl('/home/alta/imports/agid-2016.01.19/infl.txt')
    wlist = [x[0] for x in a.word_keys.items()]

    orig_dict = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/train.lst'

    with open(orig_dict, 'r') as file:
        lines = file.readlines()
        for line in tqdm(lines):
            word = line.strip()
            if word not in wlist:
                wlist.append(word)

    combined = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/combined.lst'
    with open(combined, 'w') as file:
        for word in wlist:
            file.write('{}\n'.format(word.upper()))

def gedtsv(path, out):
    wlist = []
    with open(path, 'r') as file:
        for line in file:
            if line == '\n':
                continue
            word = line.split()[0].strip().upper()
            if word not in wlist:
                wlist.append(word)

    with open(out, 'w') as file:
        for word in wlist:
            file.write('{}\n'.format(word.upper()))

<<<<<<< HEAD
def gecsrc():
    path = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/conll14st-test-data/exp-pm574/conll.processed.gec.src'
    out = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/wlists/conll.lst'
    wlist = []
    with open(path, 'r') as file:
        for line in file:
            if line == '\n':
                continue
            for word in line.split():
                if word not in wlist:
                    wlist.append(word)
    lmax = 0
    wmax = None
    for word in wlist:
        l = len(word)
        if l > lmax:
            lmax = l
            wmax = word
    print(lmax)
    print(wmax)
    with open(out, 'w') as file:
        for word in wlist:
            file.write('{}\n'.format(word.upper()))


if __name__ == '__main__':
    # path = sys.argv[1]
    # out = sys.argv[2]
    # gedtsv(path, out)
    gecsrc()
=======

if __name__ == '__main__':
    path = sys.argv[1]
    out = sys.argv[2]
    gedtsv(path, out)
>>>>>>> 5f0f592fb532515cb220975e95eae033862543c2
