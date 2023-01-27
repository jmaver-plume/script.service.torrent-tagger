# LibreELEC scripts

A list of scripts that I use on LibreELEC.

## LibreELEC Torrent "linker"

### What does it do

Movies or tv shows downloaded from a torrent site (e.g., RARBG) are named in such a way that scraping does not work.  
This script creates new directories and symbol links to files with proper naming, such that scraping software can work correctly.

The packaged is designed to properly parse and link torrents from RARBG.

### Running tests

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

You can then create separate movie and tv show video sources in Kodi.

### TODO

- [ ] Add installation guide (GitHub package + installation script)
- [ ] Add cron job to linker
- [ ] Improve linker to update / refresh library on any change.
- [ ] Add linter
