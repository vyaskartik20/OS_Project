import sys
# sys.path.append('..')

from Files import lib

if __name__ == '__main__':
    lib.FileServer().start(8888)
