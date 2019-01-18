import pdb
'''
process .m2 file to .ged.tsv format
'''
def read(path):
    with open(path) as file:
        lines = file.readlines()
    sent_chunks = []
    chunk = []
    for line in lines:
        if line == '\n':
            if chunk != []:
                sent_chunks.append(chunk)
                chunk = []
        else:
            chunk.append(line.strip())

    return sent_chunks

def write_gec_txt(m2file, gectxtfile):
    sent_chunks = read(m2file)
    with open(gectxtfile, 'w') as file:
        for sent_chunk in sent_chunks:
            # retrieve S-line
            tokens = sent_chunk[0].split()[1:]

            # For the following file which has '.' at the end
            # /home/alta/BLTSpeaking/ged-kmk/dtal/data/GEM4/M2/NODISFL_train.cuedsorted.M2.txt
            # tokens = tokens[:-1]
            file.write(' '.join(tokens).lower() + '\n')
        print('write done!')

def get_gectgt_chunk(sent_chunk):
    # handle 'S'
    tokens = sent_chunk[0].split()[1:]
    l = len(tokens)

    insertion_dict = {} # key = location, val = correction
    substitution_dict = {} # key = location, val = correction
    complex_dict = {} # key = location, val = (len, corrections)

    # handle 'A'
    for annotation in sent_chunk[1:]:
        columns = annotation.split('|||')
        items = columns[0].split()
        num1 = int(items[1])
        num2 = int(items[2])
        correction = columns[2]

        if num1 < 0:
            continue
        # substitution num1 < num2
        # missing item num1 = num2
        if num1 == num2:
            if num1 == l:
                pass
            else:
                # labels[num1] = 'i'
                # tokens.insert(correction)
                insertion_dict[num1] = correction
        elif num1+1 == num2:
            # labels[num1] = 'i'
            # tokens[num1](correction)
            substitution_dict[num1] = correction

        elif num1 < num2:
            offset = num2 - num1
            # for i in range(diff):
            #     if num1+i >= l:
            #         pass
            #     else:
            #         labels[num1+i] = 'i'
            complex_dict[num1] = (offset, correction)

        else:
            pdb.set_trace()
            print('ERROR')

    new_tokens = []
    skip_postition = []
    for i in range(len(tokens)):
        if i in skip_postition:
            pass
        elif i in insertion_dict.keys():
            new_tokens.append(insertion_dict[i])
            new_tokens.append(tokens[i])
        elif i in substitution_dict.keys():
            if substitution_dict[i] == '':
                pass
            else:
                new_tokens.append(substitution_dict[i])
        elif i in complex_dict.keys():
            offset = complex_dict[i][0]
            for j in range(offset-1):
                skip_postition.append(i+j+1)
            corrections = complex_dict[i][1].split()
            for w in corrections:
                new_tokens.append(w)

        else:
            new_tokens.append(tokens[i])

    return new_tokens


def m2_to_gec_src_tgt():
    m2path = 'lib/dtal-m2/nodisfl_train.clean.m2.txt'
    gecsrc = 'lib/dtal-m2/adapt/nodisfl_train.gec.src'
    gectgt = 'lib/dtal-m2/adapt/nodisfl_train.gec.tgt'


    sent_chunks = read(m2path)

    write_gec_txt(m2path, gecsrc) # the un-corrected version

    gectgt_chunks = []
    for sent_chunk in sent_chunks:
        gectgt_chunk = get_gectgt_chunk(sent_chunk)
        gectgt_chunks.append(gectgt_chunk)
    # pdb.set_trace()

    # write to the output
    with open(gectgt, 'w') as file:
        for chunk in gectgt_chunks:
            file.write(' '.join(chunk).lower())
            file.write('\n')

def main():
    m2_to_gec_src_tgt()

if __name__ == '__main__':
    main()
