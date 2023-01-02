# LibreELEC Torrent "renamer"

## What does it do

Movies or a tv shows downloaded from a torrent site (e.g., RARBG) are named in such a way that scraping does not work.  
This script creates new directories and symbol links to files with proper naming, such that scraping software can work correctly.


## Running tests

```shell
python3 -m unittest discover -s .
```


## How to use

First copy and paste the script to your LibreELEC using something like `scp`. 

Execute the script in the following way:
```shell
DOWNLOADS_PATH="/path/to/downloads/complete" \
MOVIES_SYMBOLIC_PATH="/path/to/movies" \
TV_SHOWS_SYMBOLIC_PATH="/path/to/tv_shows" \
python movie_linker.py
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

You can then create movie and tv show libraries.

## TODO

- [ ] Add `rm -rf MOVIES_SYMBOLIC_PATH TV_SHOWS_SYMBOLIC_PATH` at the start of the script to make script idempotent.
- [ ] Write "how to add script to exec"
- [ ] Write "how to enable automatic scraping on start libreelec"
- [ ] Add section "how to clean up library after deleting a file"
- [ ] Write proper tests
- [ ] Add GitHub actions on pull request run tests and run linter