cython _sorts.pyx
gcc -c -fPIC -I/usr/include/python2.7/ _sorts.c
gcc -shared _sorts.o -o _sorts.so
