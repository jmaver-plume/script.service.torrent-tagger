# LibreELEC Torrent "linker"

The movies and tv shows downloaded from a torrent site (e.g., RARBG) are named so that scraping does not work.
*LibreELEC Torrent "linker"* is a python script and a cronjob that creates new directories and symbolic links to files with proper naming so scraping software can work correctly.


## Installation

```shell
# Get the latest release from https://github.com/jmaver-plume/libreelec-torrent-linker/releases/latest
wget https://github.com/jmaver-plume/libreelec-torrent-linker/archive/refs/tags/{version}.zip
unzip {version}.zip
cd libreelec-torrent-linker-1.0.0

# Help
./install.py -h 

# Example
./install.py --downloads-path /path/to/downloads --tv-shows-path /path/to/tv --movies-path /path/to/movies
```

### Video Sources

You need to either update existing TV Show or Video sources to read from The Movie Database or create new ones. 

## Running tests

```shell
python3 -m unittest discover -s .
```


### Install

TODO

### Usage

Execute the script in the following way:
```shell
libreelec_torrent_linker -h

libreelec_torrent_linker --downloads-path "/path/to/downloads/complete" \
--movies-path "/path/to/movies" \
--tv-shows-path "/path/to/tv_shows"  
```

If you have the following Downloads directory structure

```shell
.
|-- /path/to/torrent_downloads
|   |-- Counterpart.S01.2160p.STAN.WEB-DL.x265.10bit.HDR.AAC5.1-WHOSNEXT[rartv]
|       |-- counterpart.s01e01.hdr.2160p.web.h265-whosnext.mkv
|       |-- counterpart.s01e02.hdr.2160p.web.h265-whosnext.mkv
|       |-- counterpart.s01e03.hdr.2160p.web.h265-whosnext.mkv
|   |-- Glass.Onion.A.Knives.Out.Mystery.2022.1080p.WEBRip.x265-RARBG
|       |-- Glass.Onion.A.Knives.Out.Mystery.2022.1080p.WEBRip.x265-RARBG.mp4
|       |-- Subs
|           |-- 2_English.srt
|           |-- 3_English.srt
```

it will create the following directories and files.
```shell
.
|-- /path/to/movies
|   |-- Glass Onion A Knives Out Mystery (2022)
|       |-- Glass Onion A Knives Out Mystery (2022).mp4
|       |-- Subs
|           |-- 2_English.srt
|           |-- 3_English.srt
|-- /path/to/tv_shows
|   |-- Counterpart
|       |-- Season 1
|           |-- Counterpart S01E01.mkv
|           |-- Counterpart S01E02.mkv
|           |-- Counterpart S01E03.mkv
```

### TODO

- [ ] Add linter
