#!/usr/bin/env python3 

import os
import glob
import shutil
import optparse
import errno
import sys

def extract_options(options):
    parser = optparse.OptionParser()
    parser.add_option('-S', '--source', action='store', dest='sourcedir', default='/media/julianarhee/Elements/head-fixed-behavior', help='Local hard drive to transfer to remote')
    parser.add_option('-H', '--datadir', action='store', dest='datadir', default='/home/julianarhee/Documents/video_data', help='Path to raw data dir')
    parser.add_option('-D', '--dest', action='store', dest='destdir', default='/n/coxfs01/behavior-data/head-fixed/raw-video-data', help='destination dir on coxfs01')
    (options, args) = parser.parse_args()

    return options


def copy_files(src, dst):
    print("Copying files from SRC to DST:")
    print("--- copy src: %s" % src)
    print("--- copy dst: %s" % dst)

    try:
        shutil.copy(src, dst)
    except shutil.Error as e:
        # directories are the same:
        print("Directory not copies: Error: %s" % e)

    except OSError as e:
        # src not a directory
        if e.errno == errno.EDNOTDIR:
            shutil.copy(src, dest)
        else:
            print("Director not copied. Error: %s" % e)
            print("--- SRC: %s" % src)
            print("--- DST: %" % dst)

def move_files(src, dst):
    fnames = os.listdir(src)

    print("Moving %i files from SRC to DST:" % len(fnames))
    print("--- SRC: %s" % src)
    print("--- DST: %s" % dst)

    shutil.move(src, dst)
    print("... done moving files")

def main(options):
    opts = extract_options(options)
    
    current_data = os.listdir(opts.datadir)
    print("Found %i datasets to transfer." % len(current_data))

    # Move to local hard drive: 
    for d in current_data:
        src = os.path.join(opts.datadir, d)
        dst = os.path.join(opts.sourcedir, d)
        move_files(src, dst)

    # Copy to remote:
    data_to_copy = os.listdir(opts.sourcedir)
    for d in data_to_copy: 
        if os.path.exists(os.path.join(opts.destdir, d)):
            if len(os.listdir(os.path.join(opts.destdir, d))) == len(os.listdir(os.path.join(opts.sourcedir, d))):
                continue
            else:
                copy_files(os.path.join(opts.sourcedir, d), os.path.join(opts.destdir, d))
        else:
            shutil.copytree(os.path.join(opts.sourcedir, d), os.path.join(opts.destdir, d))

if __name__ == '__main__':
    main(sys.argv[1:])
    print("***** DONE! *****")
    



