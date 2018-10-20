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



if __name__ == '__main__':
    main3()
