# Magnet2Torrent

A command line tool that converts magnet links in to .torrent files.

### This project is mostly abandoned. I will still merge most pull requests.

## Requirements
* python2.7/3.5
* python-libtorrent (libtorrent-rasterbar version 0.16 or later) for python 2.7 or
  python3-libtorrent for python 3.5

## Install python-libtorrent on Ubuntu
`sudo apt-get install python-libtorrent -y`

## Install python-libtorrent on macOS
`brew install libtorrent-rasterbar --with-python`

## How to Use

    usage: Magnet_To_Torrent2.py [-h] -m MAGNET [-o OUTPUT] [--rewrite-file]
                             [--no-rewrite-file] [--skip-file] [--open-file]

A command line tool that converts magnet links in to .torrent files

optional arguments:

    -h, --help            show this help message and exit
    -m MAGNET, --magnet MAGNET
                            The magnet url
    -o OUTPUT, --output OUTPUT
                            The output torrent file name
    --rewrite-file        Rewrite torrent file if exist(default)
    --no-rewrite-file     Create a new filename if torrent exist.
    --skip-file           Skip file if file already exist.
    --open-file           Open file after conferting.

### Example
`python Magnet_To_Torrent2.py -m "magnet:?xt=urn:btih:49fbd26322960d982da855c54e36df19ad3113b8&dn=ubuntu-12.04-desktop-i386.iso&tr=udp%3A%2F%2Ftracker.openbittorrent.com" -o ubunut12-04.iso`

## Licenses
All code is licensed under the [GPL version 3](http://www.gnu.org/licenses/gpl.html)
