import pdb
import string

def remove_punctuation(sentence_chunk):
    '''
    remove puncations from sentences + shift their corrections
    '''

    # handle 'S'
    tokens = sentence_chunk[0].split()[1:]
    punc_list = []
    new_sentence = []
    for i, token in enumerate(tokens):
        if token in string.punctuation:
            punc_list.append(i)
        else:
            token = token.strip(',')
            token = token.strip('-')
            token = token.strip('.')
            token = token.strip('/')
            new_sentence.append(token)

    new_sent = 'S ' + ' '.join(new_sentence)

    # handle 'A'
    new_anns = []
    for annotation in sentence_chunk[1:]:
        columns = annotation.split('|||')
        items = columns[0].split()
        num1 = int(items[1])
        num2 = int(items[2])
        shift = 0
        for i in punc_list:
            if num1 > i:
                shift += 1
        col1 = 'A {} {}'.format(num1-shift, num2-shift)
        new_ann = '|||'.join([col1] + columns[1:])
        new_anns.append(new_ann)

    new_chunk = [new_sent] + new_anns
    # pdb.set_trace()
    return new_chunk

def split_comma_dot_hyphen(sentence_chunk):
    '''
    one years ago,when I just arrived singapore
    => one years ago when I just arrived singapore
    '''

    # handle 'S'
    tokens = sentence_chunk[0].split()[1:]
    punc_list = []
    new_sentence = []
    for i, token in enumerate(tokens):
        if ',' in token:
            for x in token.split(','):
                new_sentence += [x]
            punc_list += [i] * ( len(token.split(',')) -1 )
        elif '.' in token:
            for x in token.split('.'):
                new_sentence += [x]
            punc_list += [i] * ( len(token.split('.')) -1 )
        elif '-' in token:
            for x in token.split('-'):
                new_sentence += [x]
            punc_list += [i] * ( len(token.split('-')) -1 )
        else:
            new_sentence.append(token)

    new_sent = 'S ' + ' '.join(new_sentence)

    # handle 'A'
    new_anns = []
    for annotation in sentence_chunk[1:]:
        columns = annotation.split('|||')
        items = columns[0].split()
        num1 = int(items[1])
        num2 = int(items[2])
        shift = 0
        for i in punc_list:
            if num1 > i:
                shift += 1
        col1 = 'A {} {}'.format(num1+shift, num2+shift)
        new_ann = '|||'.join([col1] + columns[1:])
        new_anns.append(new_ann)

    new_chunk = [new_sent] + new_anns
    # pdb.set_trace()
    return new_chunk

def handle_mec(sentence_chunk):
    tokens = sentence_chunk[0].split()[1:]

    # handle 'A'
    new_anns = []
    for annotation in sentence_chunk[1:]:
        columns = annotation.split('|||')
        err_type = columns[1]
        items = columns[0].split()
        num1 = int(items[1])
        num2 = int(items[2])

        if err_type == 'Mec':
            correction = columns[2]
            if num1 == (num2-1) and correction != '' and correction not in string.punctuation and len(correction.split()) == 1:

                # try:
                tokens[num1] = correction
                # except:
                    # pdb.set_trace()
                    # print('dog')
        else:
            new_anns.append(annotation)

    new_sent = 'S ' + ' '.join(tokens)
    new_chunk = [new_sent] + new_anns
    return new_chunk

def handle_uppercase(sentence_chunk):
    # S
    tokens = sentence_chunk[0].split()[1:]
    new_sent = 'S ' + ' '.join(tokens).lower()

    # handle 'A'
    new_anns = []
    for annotation in sentence_chunk[1:]:
        columns = annotation.split('|||')
        columns[2] = columns[2].lower()

        new_ann = '|||'.join(columns)
        new_anns.append(new_ann)

    new_chunk = [new_sent] + new_anns
    # pdb.set_trace()
    return new_chunk

def remove_comma_correction(sentence_chunk):
    # handle 'S'
    sent = sentence_chunk[0]

    # handle 'A'
    new_anns = []
    for annotation in sentence_chunk[1:]:
        columns = annotation.split('|||')
        correction = columns[2]
        if ',' in correction:
            pass
        else:
            new_anns.append(annotation)

    new_chunk = [sent] + new_anns
    # pdb.set_trace()
    return new_chunk

def handle_apos(sentence_chunk):
    # handle 'S'
    tokens = sentence_chunk[0].split()[1:]
    new_sentence = []
    for i in range(len(tokens)):
        token = tokens[i]
        if token == "n't":
            token = 'not'
        elif token == "'s":
            if tokens[i-1] in ['it', 'he', 'she']:
                token = 'is'
        elif token == "forest'view":
            token = 'forestview'
        else:
            token = token.strip("'")

        new_sentence.append(token)

    new_sent = 'S ' + ' '.join(new_sentence)

    # handle 'A'
    anns =  sentence_chunk[1:]
    new_chunk = [new_sent] + anns
    # pdb.set_trace()
    return new_chunk

def filter_error_types(sentence_chunk,keep):
    # handle 'S'
    sent = sentence_chunk[0]

    # handle 'A'
    new_anns = []
    for annotation in sentence_chunk[1:]:
        columns = annotation.split('|||')
        err_type = columns[1]
        if err_type not in keep:
            pass
        else:
            new_anns.append(annotation)

    new_chunk = [sent] + new_anns
    # pdb.set_trace()
    return new_chunk



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


def main():
    path = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/conll14st-test-data/alt/official-2014.combined-withalt.v1.m2'
    # path = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/conll14st-test-data/exp-pm574/try.m2'
    # out = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/conll14st-test-data/exp-pm574/try.processed.m2'
    out = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/conll14st-test-data/exp-pm574/conll.processed.v2.m2'
    # out = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/conll14st-test-data/exp-pm574/conll.processed-tgt.m2'
    sent_chunks = read(path)

    processed_chunks = []
    for sent_chunk in sent_chunks:
        sent_chunk = remove_punctuation(sent_chunk)
        processed_chunks.append(sent_chunk)

    sent_chunks = processed_chunks
    processed_chunks = []

    for sent_chunk in sent_chunks:
        sent_chunk = handle_uppercase(sent_chunk)
        processed_chunks.append(sent_chunk)


    sent_chunks = processed_chunks
    processed_chunks = []

    for sent_chunk in sent_chunks:
        sent_chunk = handle_mec(sent_chunk)
        processed_chunks.append(sent_chunk)

    sent_chunks = processed_chunks
    processed_chunks = []

    for sent_chunk in sent_chunks:
        sent_chunk = split_comma_dot_hyphen(sent_chunk)
        processed_chunks.append(sent_chunk)

    sent_chunks = processed_chunks
    processed_chunks = []

    for sent_chunk in sent_chunks:
        sent_chunk = remove_comma_correction(sent_chunk)
        processed_chunks.append(sent_chunk)

    sent_chunks = processed_chunks
    processed_chunks = []

    for sent_chunk in sent_chunks:
        sent_chunk = handle_apos(sent_chunk)
        processed_chunks.append(sent_chunk)


    with open(out, 'w') as fout:
        for chunk in processed_chunks:
            fout.write('\n'.join(chunk) + '\n\n')

def get_target_tag(input, output, target):

    sent_chunks = read(input)
    processed_chunks = []

    for sent_chunk in sent_chunks:
        sent_chunk = filter_error_types(sent_chunk, keep=target)
        processed_chunks.append(sent_chunk)


    with open(output, 'w') as fout:
        for chunk in processed_chunks:
            fout.write('\n'.join(chunk) + '\n\n')

def make_target():
    input = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/conll14st-test-data/exp-pm574/conll.processed.noemp.m2'
    outp = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/conll14st-test-data/exp-pm574/conll.processed.'
    for t in ['Vt', 'Vm', 'V0', 'Vform', 'SVA', 'ArtOrDet', 'Nn', 'Npos']:
        output = outp + t + '.m2'
        get_target_tag(input, output, [t])
        print(output, 'done')


def conll2gecsrc():
    path = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/conll14st-test-data/exp-pm574/conll.processed.v2.m2'
    out = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/conll14st-test-data/exp-pm574/conll.processed.gec.src.v2'
    lines_out = []
    with open(path, 'r') as file:
        for line in file:
            if line[0] != 'S':
                continue

            sent = line.split()[1:]
            lines_out.append(' '.join(sent))
    with open(out, 'w') as file:
        for line in lines_out:
            file.write(line + '\n')


if __name__ == '__main__':
    main()
    conll2gecsrc()
    # make_target()
