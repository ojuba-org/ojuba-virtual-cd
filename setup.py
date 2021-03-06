#! /usr/bin/python
import sys, os, os.path
from distutils.core import setup
from glob import glob

# to install type: 
# python setup.py install --root=/

def no_empty(l):
    return filter(lambda (i,j): j, l)

def recusive_data_dir(to, src, l=None):
    D=glob(os.path.join(src,'*'))
    files=filter( lambda i: os.path.isfile(i), D )
    dirs=filter( lambda i: os.path.isdir(i), D )
    if l==None: l=[]
    l.append( (to , files ) )
    for d in dirs: recusive_data_dir( os.path.join(to,os.path.basename(d)), d , l)
    return l

locales=map(lambda i: ('share/'+i,[''+i+'/ojuba-virtual-cd.mo',]),glob('locale/*/LC_MESSAGES'))
data_files=[]
data_files.extend(locales)
setup (name='OjubaVirtualCD', version='0.2.0',
            description='Ojuba Virtual CD/DVD using fuseiso',
            author='Muayyad Saleh Alsadi',
            author_email='alsadi@ojuba.org',
            url='http://git.ojuba.org/',
            license='Waqf',
            #packages=['OjubaVirtualCD'],
            py_modules = ['OjubaVirtualCD'],
            scripts=['ojuba-virtual-cd'],
            classifiers=[
                    'Development Status :: 4 - Beta',
                    'Intended Audience :: End Users/Desktop',
                    'Operating System :: POSIX',
                    'Programming Language :: Python',
                    ],
            data_files=data_files
)


