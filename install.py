#!/usr/bin/env python2.7
"""
Script to install dotfiles
Copyright 2012 Kevin S Lin

Basic Usage:
    ./install.py
"""
import os

def _collect_files(suffix, ignore_dirs = []):
    """
    Collect all files by searching recursively via current directory.
    Will ignore directories specified by ignore_dirs
    @params:
        suffix - suffix to search for
        ignore_dirs - list of directories to ignore
    @return:
        List of tuples (path, [files])
    eg.
        [(path, [ foo.symlink]), (...),...]
    """
    out = []
    walker = os.walk(".")
    for path, directory, files in walker:
        for inum, dname in enumerate(directory):
            # filter out all unwanted directories
            if (dname in ignore_dirs): del directory[inum]
        # gets all files that match the suffix
        match = filter(lambda x: x.endswith(suffix), files)
        # filter out unwanted suffix
        if (match):
            out.append((path, match))
    return out

def get_response(fname):
    prompt = "%s exists. [s]kip, [S]kip All, [o]verwrite: " % fname
    resp = ''
    while (resp not in ['s', 'S', 'o']):
        resp = raw_input(prompt)
    return resp


def get_symlinks():
    """
    Get all files ending in .symlink
    @return:
    List of tuples (path, [files])
    eg.
    [(path, [ foo.symlink]), (...),...]
    """
    res = _collect_files("symlink")
    return res


### Main
def install(args=None):
    """
    Install dotfiles in computer
    :params target:
    :params skip_all:
    """

    print (args)
    print ("dest: %s" % args.target)
    symlinks = get_symlinks()

    for path, links in symlinks:
        for link in links:
            # Create link to new file
            fname = "." + link.rsplit(".symlink")[0]
            fpath_old = os.path.join(path, link)
            fpath = os.path.join(args['target'], fname)

            # handle file collisions
            flag_create = True
            resp = None
            if (os.path.exists(fpath)):
                # skip all on, then skip file
                if (args['skip_all']):
                    flag_create = False
                else:
                    resp = get_response(fname)
                    if (resp == 's'):
                        flag_create = False
                    elif (resp == 'S'):
                        args['skip_all'] = True
                        flag_create = False
                    elif (resp.lower() == 'o'):
                        print ("overwriting...")
                        os.remove(fpath)
                    else:
                        # code should not get here
                        raise("Something bad has happened")
            # Create hard link to dot file
            if (flag_create):
                print("linking %s to %s" % (fname, fpath))
                if not args['dry_run']: os.link(fpath_old, fpath)
            else:
                print("skipping %s" % fname)
    print("done :)")

def main():
    #TODO(HACK)
    from collections import defaultdict
    args = defaultdict(list)
    args['target'] = os.path.expanduser("~")
    install(args)

if __name__ == "__main__":
    main()
