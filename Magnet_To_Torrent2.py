#!/usr/bin/env python
"""convert magnet link to torrent file.

Created on Apr 19, 2012
@author: dan, Faless

    GNU GENERAL PUBLIC LICENSE - Version 3

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    http://www.gnu.org/licenses/gpl-3.0.txt

"""

import libtorrent as lt
import os.path as pt
import shutil
import sys
import tempfile
from argparse import ArgumentParser
from time import sleep
from os.path import isfile, splitext
try:
    from urllib.parse import unquote
except ImportError:
    from urllib import unquote


def magnet2torrent(magnet, output_name=None):
    """convert magent2torrent."""
    if output_name and \
            not pt.isdir(output_name) and \
            not pt.isdir(pt.dirname(pt.abspath(output_name))):
        print("Invalid output folder: " + pt.dirname(pt.abspath(output_name)))
        print("")
        sys.exit(0)

    tempdir = tempfile.mkdtemp()
    ses = lt.session()
    params = {
        'save_path': tempdir,
        'storage_mode': lt.storage_mode_t(2),
        'paused': False,
        'auto_managed': True,
        'duplicate_is_error': True
    }
    handle = lt.add_magnet_uri(ses, magnet, params)

    print("Downloading Metadata (this may take a while)")
    while (not handle.has_metadata()):
        try:
            sleep(1)
        except KeyboardInterrupt:
            print("Aborting...")
            ses.pause()
            print("Cleanup dir " + tempdir)
            shutil.rmtree(tempdir)
            sys.exit(0)
    ses.pause()
    print("Done")

    torinfo = handle.get_torrent_info()
    torfile = lt.create_torrent(torinfo)

    output = pt.abspath(torinfo.name() + ".torrent")

    if output_name:
        if pt.isdir(output_name):
            output = pt.abspath(pt.join(
                output_name, torinfo.name() + ".torrent"))
        elif pt.isdir(pt.dirname(pt.abspath(output_name))):
            output = pt.abspath(output_name)

    print("Saving torrent file here : " + output + " ...")
    # torcontent = lt.bencode(torfile.generate())  # not used
    f = open(output, "wb")
    f.write(lt.bencode(torfile.generate()))
    f.close()
    print("Saved! Cleaning up dir: " + tempdir)
    ses.remove_torrent(handle)
    shutil.rmtree(tempdir)

    return output


def main():
    """main function."""
    # parsing the argument.
    description = "A command line tool that converts magnet links in to .torrent files"
    parser = ArgumentParser(description=description)
    parser.add_argument('-m', '--magnet', help='The magnet url', required=True)
    parser.add_argument('-o', '--output', help='The output torrent file name')
    # rewrite file option
    parser.add_argument('--rewrite-file', help='Rewrite torrent file if exist(default)',
                        dest='rewrite_file', action='store_true')
    parser.add_argument('--no-rewrite-file',
                        help='Create a new filename if torrent exist.',
                        dest='rewrite_file', action='store_false')
    parser.set_defaults(rewrite_file=True)
    # Skip file if exist option
    parser.add_argument('--skip-file', help='Skip file if file already exist.',
                        dest='skip_file', action='store_true')
    parser.set_defaults(skip_file=False)
    args = parser.parse_args(sys.argv[1:])
    output_name = args.output
    magnet = args.magnet

    # guess the name if output name is not given.
    # in magnet link it is between'&dn' and '&tr'
    if output_name is None:
        output_name = magnet.split('&dn=')[1].split('&tr')[0]
        if '+' in output_name:
            output_name = unquote(output_name)
        output_name += '.torrent'

    # return if user want to skip existing file.
    if isfile(output_name) and args.skip_file:
        print('File [{}] is already exist.'.format(output_name))
        return

    # create fullname if file exist.
    if isfile(output_name) and not args.rewrite_file:
        new_output_name = output_name
        counter = 1
        while isfile(new_output_name):
            non_basename, non_ext = splitext(new_output_name)
            if counter - 1 != 0:
                non_basename = non_basename.rsplit('_{}'.format(counter - 1), 1)[0]
            non_basename += '_{}'.format(counter)
            new_output_name = '{}{}'.format(non_basename, non_ext)
            counter += 1
        output_name = new_output_name

    # encode magnet link if it appear url decoded.
    if magnet != unquote(magnet):
        magnet = unquote(magnet)

    # run the converter
    magnet2torrent(magnet, output_name)


if __name__ == "__main__":
    sys.exit(main())
