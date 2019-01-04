'''
quick fix for writing scp
'''
from helper import make_scp
import sys

def main():
    if len(sys.argv) != 4:
        print('Usage: python3 write_scp.py scp_path lat_path num_sent')
        return 
    scp_path = sys.argv[1]
    lat_path = sys.argv[2]
    num = int(sys.argv[3])

    make_scp(scp_path, lat_path, num)
if __name__ == '__main__':
    main()
