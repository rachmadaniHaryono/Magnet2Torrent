#!/usr/bin/env python
"""convert magnet link to torrent file.

Created on Apr 19, 2012 @author: dan, Faless
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

import os
import os.path as pt
import shutil
import subprocess
import sys
import tempfile
from argparse import ArgumentParser
from time import sleep
try:
    from urllib.parse import unquote
except ImportError:
    from urllib import unquote
import libtorrent as lt


class Magnet2Torrent:
    """class for converter from magnet link to torrent."""

    def __init__(self, magnet, output_name=None):
        """init function.

        check for validity of the input.

        Raises:
            ValueError: if input is not valid this error will be raise
        """
        if output_name and \
                not pt.isdir(output_name) and \
                not pt.isdir(pt.dirname(pt.abspath(output_name))):
            raise ValueError("Invalid output folder: " + pt.dirname(pt.abspath(output_name)))
        self.output_name = output_name
        # create tempdir
        self.tempdir = tempfile.mkdtemp()
        # create session
        self.ses = lt.session()
        # one could want to set this
        # ses.listen_on(6881, 6882)

        # add 'url'. for add_torrent()
        params = {
            'url': magnet,
            'save_path': self.tempdir,
            'storage_mode': lt.storage_mode_t(2),
            'paused': False,
            'auto_managed': True,
            'duplicate_is_error': False
        }
        self.handle = self.ses.add_torrent(params)

    def run(self):
        """run the converter.

        using the class attribute initiated at init function.

        Returns:
            Filename of created torrent.

        Raises:
            KeyboardInterrupt: This error caused by user to stop this.
            When downloading metada from magnet link,
            it require additional step before the error reraised again.
        """
        print("Downloading Metadata (this may take a while)")
        # used to control "Maybe..." and "or the" msgs
        # after sleep(1)
        wait_time = 1
        soft_limit = 120

        while not self.handle.has_metadata():
            try:
                sleep(1)
                if wait_time > soft_limit:
                    print("Download is taking a long time, maybe there is an "
                          "issue with the magnet link or your network connection")
                    soft_limit += 30
                wait_time += 1
            except KeyboardInterrupt:
                print("Aborting...")
                self.ses.pause()
                print("Cleanup dir " + self.tempdir)
                shutil.rmtree(self.tempdir)
                raise
        self.ses.pause()
        print("Done")

        torinfo = self.handle.get_torrent_info()
        torfile = lt.create_torrent(torinfo)

        output = pt.abspath(torinfo.name() + ".torrent")

        if self.output_name:
            if pt.isdir(self.output_name):
                output = pt.abspath(pt.join(self.output_name, torinfo.name() + ".torrent"))
            elif pt.isdir(pt.dirname(pt.abspath(self.output_name))):
                output = pt.abspath(self.output_name)

        print("Saving torrent file here : " + output + " ...")
        # torcontent = lt.bencode(torfile.generate())  # not used
        f = open(output, "wb")
        f.write(lt.bencode(torfile.generate()))
        f.close()
        print("Saved! Cleaning up dir: " + self.tempdir)
        self.ses.remove_torrent(self.handle)
        shutil.rmtree(self.tempdir)

        return output


def open_default_app(filepath):
    """open filepath with default application for each operating system."""
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', filepath))
    elif os.name == 'nt':
        os.startfile(filepath)
    elif os.name == 'posix':
        subprocess.call(('xdg-open', filepath))


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
    # open file after creating torrent file
    parser.add_argument('--open-file', help='Open file after converting.',
                        dest='open_file', action='store_true')
    parser.set_defaults(open_file=False)
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
    if pt.isfile(output_name) and args.skip_file:
        print('File [{}] is already exist.'.format(output_name))
        # still open file if file already existed.
        if args.open_file:
            open_default_app(output_name)
        return

    # create fullname if file exist.
    if pt.isfile(output_name) and not args.rewrite_file:
        new_output_name = output_name
        counter = 1
        while pt.isfile(new_output_name):
            non_basename, non_ext = pt.splitext(new_output_name)
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
    conv = Magnet2Torrent(magnet, output_name)
    conv.run()

    if args.open_file:
        open_default_app(output_name)


if __name__ == "__main__":
    sys.exit(main())
