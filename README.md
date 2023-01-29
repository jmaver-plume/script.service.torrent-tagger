# script.service.torrent-tagger

![run-tests-and-linter](https://github.com/jmaver-plume/libreelec-torrent-linker/actions/workflows/run-tests-and-linter.yml/badge.svg?branch=main)


The movies and tv shows downloaded from a torrent site (e.g., RARBG) are named inappropriately, which causes issues with scraping.

**script.service.torrent-tagger** is a Kodi service add-on that checks, on a configurable interval, the current downloads folder for any movie and tv show files and syncs them with dummy directories containing only symbolic links with proper naming for scraping to work.


## Installation

1. Download the [latest release](https://github.com/jmaver-plume/libreelec-torrent-linker/releases/latest) to your LibreELEC.
2. Install the add-on from the downloaded zip file.


### Video Sources

You need to either update existing TV Shows or Video sources to read from The Movie Database or create new ones.


## Example

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
