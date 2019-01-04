'''
fill the empty lines due to tokens (words) not being in the n-gram LM
'''

import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: fix_ngram_rescore_output.py src hyp")
        return

    src = sys.argv[1]
    hyp = sys.argv[2]

    with open(src, 'r') as src_f:
        lines1 = src_f.readlines()
        
    with open(hyp, 'r') as hyp_f:
        lines2 = hyp_f.readlines()
        
    if len(lines1) != len(lines2):
        print("Legnths do not match!")
        return
    
    for i in range(len(lines1)):
        l1 = lines1[i]
        l2 = lines2[i]
        if l2 == '\n' and l1 != '\n':
            lines2[i] = l1
            
    with open(hyp, 'w') as out:
        for line in lines2:
            out.write(line)
            
    print('done')



if __name__ == '__main__':
    main()
