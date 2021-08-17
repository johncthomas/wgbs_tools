#!/usr/bin/python3 -u

import argparse
import os.path as op
import os
import subprocess
from pathlib import Path
from utils_wgbs import eprint, IllegalArgumentError


path = Path(op.realpath(__file__))
refdir = op.join(path.parent.parent.parent, 'references')

def print_genomes():
    print('Existing references:')
    for d in get_genomes():
        print(d)

def get_genomes():
    r = []
    for d in os.listdir(refdir):
        if op.isdir(op.join(refdir, d)):
            r.append(d)
    return r

def set_def_ref(name):
    if name not in get_genomes():
        print_genomes()
        raise IllegalArgumentError(f'Invalid reference: {name}')
    dst = 'default'
    c = os.getcwd()
    try:
        os.chdir(refdir)
        if op.islink(dst):
            os.unlink(dst)
        os.symlink(name, dst)
    except Exception as e:
        os.chdir(c)
        raise e
    os.chdir(c)

def parse_args():
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('--name', help='name of the genome (e.g. hg19, mm9...).')
    parser.add_argument('-ls', action='store_true',
            help='print a list of existing genomes')
    args = parser.parse_args()
    return args


def main():
    """
    Change the default genome reference.
    """
    args = parse_args()
    if args.name:
        set_def_ref(args.name)
    if args.ls:
        print_genomes()


if __name__ == '__main__':
    main()
