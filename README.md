# Magnet2Torrent

A command line tool that converts magnet links into .torrent files.

## Requirements
* python2.7/3.5
* python-libtorrent (libtorrent-rasterbar version 0.16 or later) for python 2.7 or
  python3-libtorrent for python 3.5

### Install python-libtorrent on Ubuntu
`sudo apt-get install python-libtorrent -y`

### Install python-libtorrent on macOS/Mac
`brew install libtorrent-rasterbar --with-python`

## How to Use

## Usage

    usage: Magnet2Torrent.py [-h] -m MAGNET [-o OUTPUT] [--rewrite-file]
                             [--no-rewrite-file] [--skip-file] [--open-file]

A command line tool that converts magnet links into .torrent files

Optional arguments:

    -h, --help            Show this help message and exit.
    -m MAGNET, --magnet MAGNET
                          The magnet url.
    -o OUTPUT, --output OUTPUT
                          The output torrent file name.
    --rewrite-file        Rewrite torrent file if it already exists (default).
    --no-rewrite-file     Create a new filename if torrent exists.
    --skip-file           Skip file if it already exists.
    --open-file           Open file after converting.

## Example

    python Magnet2Torrent.py -m "magnet:?xt=urn:btih:49fbd26322960d982da855c54e36df19ad3113b8&dn=ubuntu-12.04-desktop-i386.iso&tr=udp%3A%2F%2Ftracker.openbittorrent.com" -o ubunut12-04.iso

## Licenses
All code is licensed under the [GPL version 3](http://www.gnu.org/licenses/gpl.html)
