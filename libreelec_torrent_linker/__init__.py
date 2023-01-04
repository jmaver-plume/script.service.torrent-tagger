import argparse
import logging
import os
import re
import shutil
from abc import ABC, abstractmethod


class Utils:
    logging = logging.getLogger("Utils")

    @staticmethod
    def init_directories(*directories):
        for directory in directories:
            Utils.init_directory(directory)

    @staticmethod
    def init_directory(directory):
        if os.path.exists(directory):
            shutil.rmtree(directory)
            Utils.logging.debug(f"Deleted {directory}.")

        while os.path.exists(directory):
            pass

        os.makedirs(directory)
        Utils.logging.debug(f"Created {directory}.")


class EdgeCaseNameHandler:
    edge_cases = {
        'The Glory': 'The Glory (2022)'
    }

    @staticmethod
    def get_name(name):
        """Returns <name> if name is not an edge case name, else it returns corrected name."""
        if name in EdgeCaseNameHandler.edge_cases:
            return EdgeCaseNameHandler.edge_cases[name]
        return name

class File:
    def __init__(self, filename, parent):
        self.filename = filename
        self.parent = parent

    def get_path(self):
        return f'{self.parent}/{self.filename}'

    def is_video_file(self):
        _, ext = os.path.splitext(self.filename)
        return bool(re.search(r'\.(mkv|mp4|mov|wmv|avi)', self.filename))


class AbstractLinker(ABC):
    def __init__(self, new_path, scanner):
        super().__init__()
        self.new_path = new_path
        self.scanner = scanner
        self.logging = logging.getLogger(self.__class__.__name__)

    def link(self):
        for item in self.scanner.scan():
            self._link_item(item)

    @abstractmethod
    def _link_item(self, item):
        pass


class Scanner:
    def __init__(self, path):
        self.path = path
        self.logging = logging.getLogger(self.__class__.__name__)


class MovieDirectory:
    def __init__(self, parent_directory, directory_name, children):
        self.parent_directory = parent_directory
        self.directory_name = directory_name
        self.children = children
        self.directory = f'{self.parent_directory}/{self.directory_name}'

    def get_tmdb_movie(self, new_directory):
        # https: // kodi.wiki / view / Naming_video_files / movies
        def _get_tmdb_name():
            split_on_quality = re.split(r'(2160p|1080p|720p)', self.directory_name)
            name = split_on_quality[0].replace('.', ' ').strip()
            split_on_year = re.match(r'(.*) ([0-9]{4})', name).groups()
            if not (len(split_on_year)):
                return name

            name, year = split_on_year
            return f'{name} ({year})'

        def _get_children(_tmdb_name):
            children = []
            for child in self.children:
                if child.is_video_file():
                    _, ext = os.path.splitext(child.filename)
                    filename = f'{_tmdb_name}{ext}'
                    children.append(File(filename, f'{new_directory}/{_tmdb_name}'))
                else:
                    children.append(File(child.filename, f'{new_directory}/{_tmdb_name}'))
            return children

        tmdb_name = _get_tmdb_name()
        return MovieDirectory(
            parent_directory=new_directory,
            directory_name=tmdb_name,
            children=_get_children(tmdb_name),
        )

    @staticmethod
    def is_valid(directory):
        if not os.path.isdir(directory):
            return False

        if not bool(re.search('(2160p|1080p|720p)', directory)):
            return False

        if TvShowEpisodeDirectory.is_valid(directory):
            return False

        if TvShowSeasonDirectory.is_valid(directory):
            return False

        return True


class MovieScanner(Scanner):
    def scan(self):
        """Returns a list of Movies in a directory"""
        all_directories = os.listdir(self.path)
        movie_directories = list(filter(lambda d: MovieDirectory.is_valid(f'{self.path}/{d}'), all_directories))
        scanned_movie_directories = [self._scan_movie_directory(d) for d in movie_directories]
        return scanned_movie_directories

    def _scan_movie_directory(self, movie_directory):
        parent = f'{self.path}/{movie_directory}'
        children = [File(f, parent) for f in os.listdir(parent)]
        self.logging.debug(f"Found {movie_directory}.")
        return MovieDirectory(
            parent_directory=self.path,
            directory_name=movie_directory,
            children=children
        )


class MovieLinker(AbstractLinker):
    def __init__(self, new_path, scanner):
        super().__init__(new_path, scanner)

    def _link_item(self, movie):
        tmdb_movie = movie.get_tmdb_movie(self.new_path)
        os.makedirs(tmdb_movie.directory)
        self.logging.debug(f'Created directory {tmdb_movie.directory}.')
        for i, _ in enumerate(movie.children):
            os.symlink(movie.children[i].get_path(), tmdb_movie.children[i].get_path())
            self.logging.debug(f'Linked src={movie.children[i].get_path()} to dest={tmdb_movie.children[i].get_path()}')


class TMDBTvEpisode:
    def __init__(self, name_directory, season_directory, children):
        self.name_directory = name_directory
        self.season_directory = season_directory
        self.children = children


class TMDBTvSeason:
    def __init__(self, name_directory, season_directory, children):
        self.name_directory = name_directory
        self.season_directory = season_directory
        self.children = children


class TvShowEpisodeDirectory:
    def __init__(self, parent_directory, directory_name, children):
        self.parent_directory = parent_directory
        self.directory_name = directory_name
        self.children = children
        self.directory = f'{self.parent_directory}/{self.directory_name}'

    def get_tmdb_episode(self, new_directory):
        # https: // kodi.wiki / view / Naming_video_files / TV_shows
        name, identifier, season = re.match(r'(.+)\.([sS]([0-9]{2})[eE][0-9]{2}).*', self.directory_name).groups()
        name = name.replace('.', ' ')
        name = EdgeCaseNameHandler.get_name(name)
        season = int(season)
        identifier = identifier.upper()
        children = []
        name_directory = f'{new_directory}/{name}'
        season_directory = f'{new_directory}/{name}/Season {season}'
        for child in self.children:
            if identifier.lower() in child.filename.lower():
                _, ext = os.path.splitext(child.filename)
                filename = f'{name} {identifier}{ext}'
                children.append(File(filename, season_directory))
            else:
                children.append(File(f'{name} {identifier} {child.filename}', season_directory))
        return TMDBTvEpisode(
            name_directory=name_directory,
            season_directory=season_directory,
            children=children
        )

    @staticmethod
    def is_valid(name):
        if not bool(re.search('[sS][0-9]{2}[eE][0-9]{2}', name)):
            return False

        return True


class TvShowSeasonDirectory:
    def __init__(self, parent_directory, directory_name, children):
        self.parent_directory = parent_directory
        self.directory_name = directory_name
        self.children = children
        self.directory = f'{self.parent_directory}/{self.directory_name}'

    def get_tmdb_season(self, new_directory):
        # https: // kodi.wiki / view / Naming_video_files / TV_shows
        # This almost duplicates TV Show Episode
        name, season = re.match(r'(.+)\.[sS]([0-9]{2}).*', self.directory_name).groups()
        name = name.replace('.', ' ')
        name = EdgeCaseNameHandler.get_name(name)
        season = int(season)
        children = []
        name_directory = f'{new_directory}/{name}'
        season_directory = f'{new_directory}/{name}/Season {season}'
        for child in self.children:
            match = re.match(r'.*([sS][0-9]{2}[eE][0-9]{2}).*', child.filename)
            if match is None:
                children.append(File(child.filename, season_directory))
            else:
                identifier = match.groups()[0].upper()
                _, ext = os.path.splitext(child.filename)
                filename = f'{name} {identifier}{ext}'
                children.append(File(filename, season_directory))
        return TMDBTvSeason(
            name_directory=name_directory,
            season_directory=season_directory,
            children=children
        )

    @staticmethod
    def is_valid(name):
        if TvShowEpisodeDirectory.is_valid(name):
            return False

        if not bool(re.search('[sS][0-9]{2}', name)):
            return False

        return True


class TvShowSeasonScanner(Scanner):
    def scan(self):
        """Returns a list of TV Show episodes in a directory"""
        all_directories = os.listdir(self.path)
        directories = list(filter(lambda d: TvShowSeasonDirectory.is_valid(f'{self.path}/{d}'), all_directories))
        scanned = [self._scan_season(s) for s in directories]
        return scanned

    def _scan_season(self, season):
        parent = f'{self.path}/{season}'
        children = [File(f, parent) for f in os.listdir(parent)]
        self.logging.debug(f"Found {season}.")
        return TvShowSeasonDirectory(
            parent_directory=self.path,
            directory_name=season,
            children=children
        )


class TvShowSeasonLinker(AbstractLinker):
    def __init__(self, new_path, scanner):
        super().__init__(new_path, scanner)

    def _link_item(self, season):
        tmdb_season = season.get_tmdb_season(self.new_path)
        if not os.path.exists(tmdb_season.name_directory):
            os.makedirs(tmdb_season.name_directory)
            self.logging.debug(f'Created directory {tmdb_season.name_directory}.')

        if not os.path.exists(tmdb_season.season_directory):
            os.makedirs(tmdb_season.season_directory)
            self.logging.debug(f'Created directory {tmdb_season.season_directory}.')

        for i, _ in enumerate(season.children):
            os.symlink(season.children[i].get_path(), tmdb_season.children[i].get_path())
            self.logging.debug(
                f'Linked src={season.children[i].get_path()} to dest={tmdb_season.children[i].get_path()}')


class TvShowEpisodeScanner(Scanner):
    def scan(self):
        """Returns a list of TvShowEpisodeDirectory"""
        all_directories = os.listdir(self.path)
        directories = list(filter(lambda d: TvShowEpisodeDirectory.is_valid(f'{self.path}/{d}'), all_directories))
        scanned = [self._scan_episode(e) for e in directories]
        return scanned

    def _scan_episode(self, episode):
        parent = f'{self.path}/{episode}'
        children = [File(f, parent) for f in os.listdir(parent)]
        self.logging.debug(f"Found {episode}.")
        return TvShowEpisodeDirectory(
            parent_directory=self.path,
            directory_name=episode,
            children=children
        )


class TvShowEpisodeLinker(AbstractLinker):
    def __init__(self, new_path, scanner):
        super().__init__(new_path, scanner)

    def _link_item(self, episode):
        tmdb_episode = episode.get_tmdb_episode(self.new_path)

        if not os.path.exists(tmdb_episode.name_directory):
            os.makedirs(tmdb_episode.name_directory)
            self.logging.debug(f'Created directory {tmdb_episode.name_directory}.')

        if not os.path.exists(tmdb_episode.season_directory):
            os.makedirs(tmdb_episode.season_directory)
            self.logging.debug(f'Created directory {tmdb_episode.season_directory}.')

        for i, _ in enumerate(episode.children):
            os.symlink(episode.children[i].get_path(), tmdb_episode.children[i].get_path())
            self.logging.debug(
                f'Linked src={episode.children[i].get_path()} to dest={tmdb_episode.children[i].get_path()}')


class Linker:
    def __init__(self, movies_path, tv_shows_path, downloads_path):
        self.movies_path = movies_path
        self.tv_shows_path = tv_shows_path
        self.movie_linker = MovieLinker(movies_path, MovieScanner(downloads_path))
        self.episode_linker = TvShowEpisodeLinker(tv_shows_path, TvShowEpisodeScanner(downloads_path))
        self.season_linker = TvShowSeasonLinker(tv_shows_path, TvShowSeasonScanner(downloads_path))

    def link(self):
        Utils.init_directories(self.movies_path, self.tv_shows_path)

        self.movie_linker.link()
        self.episode_linker.link()
        self.season_linker.link()


def main():
    parser = argparse.ArgumentParser(description='Creates symbolic links with proper naming for LibreELEC scraper.')
    parser.add_argument(
        '--downloads-path',
        required=True,
        help="Absolute path to directory where you have downloaded torrents."
    )
    parser.add_argument(
        '--movies-path',
        required=True,
        help="Absolute path to directory where you will store symbolic links. This directory is the source directory of video source in LibreELEC."
    )
    parser.add_argument(
        '--tv-shows-path',
        required=True,
        help="Absolute path to directory where you will store symbolic links. This directory is the source directory of video source in LibreELEC."
    )
    parser.add_argument(
        '--log-level',
        default="INFO",
        choices=["ERROR", "DEBUG", "INFO"]
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.getLevelName(args.log_level))

    linker = Linker(
        tv_shows_path=args.tv_shows_path,
        downloads_path=args.downloads_path,
        movies_path=args.movies_path,
    )
    linker.link()


if __name__ == "__main__":
    main()
