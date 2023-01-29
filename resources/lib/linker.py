import hashlib
import os
import re
import shutil
from abc import ABC, abstractmethod


# Utils
class Utils:
    def __init__(self, xbmc):
        self.xbmc = xbmc

    def safe_delete_directory(self, directory):
        if not os.path.exists(directory):
            return

        shutil.rmtree(directory)
        self.xbmc.log(f"Deleted {directory}.", level=self.xbmc.LOGDEBUG)

    def init_directories(self, *directories):
        for directory in directories:
            self.init_directory(directory)

    def init_directory(self, directory):
        if os.path.exists(directory):
            shutil.rmtree(directory)
            self.xbmc.log(f"Deleted {directory}.", level=self.xbmc.LOGDEBUG)

        while os.path.exists(directory):
            pass

        os.makedirs(directory)
        self.xbmc.log(f"Created {directory}.", level=self.xbmc.LOGDEBUG)

    def safe_makedirs(self, _dir):
        if not os.path.exists(_dir):
            os.makedirs(_dir)
            self.xbmc.log(f'Created directory {dir}.', level=self.xbmc.LOGDEBUG)

    def get_all_descendants(self, directory):
        descendants = []
        for root, dirs, files in os.walk(directory):
            for descendant in sorted(files + dirs):
                descendants.append(os.path.join(root, descendant))
        return set(sorted(descendants))


class DownloadsDirectory:
    def __init__(self, downloads_path, state_path, xbmc):
        self.downloads_path = downloads_path
        self.state_path = state_path
        self.xbmc = xbmc

    def contains_changes(self):
        saved_state = self.get_saved_state()
        current_state = self.get_current_state()
        return current_state != saved_state

    def update_state(self):
        current_state = self.get_current_state()
        with open(self.state_path, 'w') as f:
            f.write(current_state)

    def get_saved_state(self):
        if not os.path.exists(self.state_path):
            return None

        with open(self.state_path, 'r') as f:
            return f.read()

    def get_current_state(self):
        descendants = self._get_all_descendants()
        return hashlib.md5(descendants.encode()).hexdigest()

    def _get_all_descendants(self):
        descendants = []
        for root, dirs, files in os.walk(self.downloads_path):
            for descendant in sorted(files + dirs):
                descendants.append(os.path.join(root, descendant))
        return '::'.join(descendants)


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


class TMDBTvShow:
    def __init__(self, name_directory, season_directory, children):
        self.name_directory = name_directory
        self.season_directory = season_directory
        self.children = children


# Directories
class AbstractDirectory(ABC):
    def __init__(self, parent_directory, directory_name, children):
        self.parent_directory = parent_directory
        self.directory_name = directory_name
        self.children = children
        self.directory = f'{self.parent_directory}/{self.directory_name}'

    @abstractmethod
    def get_tmdb_directory(self, tmdb_directory_path):
        pass

    @staticmethod
    @abstractmethod
    def is_valid(directory):
        pass


class MovieDirectory(AbstractDirectory):
    def get_tmdb_directory(self, tmdb_directory_path):
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
                    children.append(File(filename, f'{tmdb_directory_path}/{_tmdb_name}'))
                else:
                    children.append(File(child.filename, f'{tmdb_directory_path}/{_tmdb_name}'))
            return children

        tmdb_name = _get_tmdb_name()
        return MovieDirectory(
            parent_directory=tmdb_directory_path,
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


class TvShowEpisodeDirectory(AbstractDirectory):
    def get_tmdb_directory(self, tmdb_directory_path):
        # https: // kodi.wiki / view / Naming_video_files / TV_shows
        name, identifier, season = re.match(r'(.+)\.([sS]([0-9]{2})[eE][0-9]{2}).*', self.directory_name).groups()
        name = name.replace('.', ' ')
        name = EdgeCaseNameHandler.get_name(name)
        season = int(season)
        identifier = identifier.upper()
        children = []
        name_directory = f'{tmdb_directory_path}/{name}'
        season_directory = f'{tmdb_directory_path}/{name}/Season {season}'
        for child in self.children:
            if identifier.lower() in child.filename.lower():
                _, ext = os.path.splitext(child.filename)
                filename = f'{name} {identifier}{ext}'
                children.append(File(filename, season_directory))
            else:
                children.append(File(f'{name} {identifier} {child.filename}', season_directory))
        return TMDBTvShow(
            name_directory=name_directory,
            season_directory=season_directory,
            children=children
        )

    @staticmethod
    def is_valid(directory):
        if not bool(re.search('[sS][0-9]{2}[eE][0-9]{2}', directory)):
            return False

        return True


class TvShowSeasonDirectory(AbstractDirectory):
    def get_tmdb_directory(self, tmdb_directory_path):
        # https: // kodi.wiki / view / Naming_video_files / TV_shows
        # This almost duplicates TV Show Episode
        name, season = re.match(r'(.+)\.[sS]([0-9]{2}).*', self.directory_name).groups()
        name = name.replace('.', ' ')
        name = EdgeCaseNameHandler.get_name(name)
        season = int(season)
        children = []
        name_directory = f'{tmdb_directory_path}/{name}'
        season_directory = f'{tmdb_directory_path}/{name}/Season {season}'
        for child in self.children:
            match = re.match(r'.*([sS][0-9]{2}[eE][0-9]{2}).*', child.filename)
            if match is None:
                children.append(File(child.filename, season_directory))
            else:
                identifier = match.groups()[0].upper()
                _, ext = os.path.splitext(child.filename)
                filename = f'{name} {identifier}{ext}'
                children.append(File(filename, season_directory))
        return TMDBTvShow(
            name_directory=name_directory,
            season_directory=season_directory,
            children=children
        )

    @staticmethod
    def is_valid(directory):
        if TvShowEpisodeDirectory.is_valid(directory):
            return False

        if not bool(re.search('[sS][0-9]{2}', directory)):
            return False

        return True


# Scanners
class AbstractScanner(ABC):
    def __init__(self, path, xbmc):
        self.path = path
        self.xbmc = xbmc

    def scan(self):
        all_directories = os.listdir(self.path)
        filtered_directories = self._filter_directories(all_directories)
        mapped_directories = self._map_directories(filtered_directories)
        return mapped_directories

    @abstractmethod
    def _filter_directories(self, directories):
        pass

    @abstractmethod
    def _map_directories(self, directories):
        pass


class MovieScanner(AbstractScanner):
    def _map_directories(self, directories):
        return [self._scan_movie_directory(d) for d in directories]

    def _filter_directories(self, directories):
        return list(filter(lambda d: MovieDirectory.is_valid(f'{self.path}/{d}'), directories))

    def _scan_movie_directory(self, movie_directory):
        parent = f'{self.path}/{movie_directory}'
        children = [File(f, parent) for f in os.listdir(parent)]
        self.xbmc.log(f"Found {movie_directory}.", level=self.xbmc.LOGDEBUG)
        return MovieDirectory(
            parent_directory=self.path,
            directory_name=movie_directory,
            children=children
        )


class TvShowSeasonScanner(AbstractScanner):
    def _filter_directories(self, directories):
        return list(filter(lambda d: TvShowSeasonDirectory.is_valid(f'{self.path}/{d}'), directories))

    def _map_directories(self, directories):
        return [self._scan_season(s) for s in directories]

    def _scan_season(self, season):
        parent = f'{self.path}/{season}'
        children = [File(f, parent) for f in os.listdir(parent)]
        self.xbmc.log(f"Found {season}.", level=self.xbmc.LOGDEBUG)
        return TvShowSeasonDirectory(
            parent_directory=self.path,
            directory_name=season,
            children=children
        )


class TvShowEpisodeScanner(AbstractScanner):
    def _filter_directories(self, directories):
        return list(filter(lambda d: TvShowEpisodeDirectory.is_valid(f'{self.path}/{d}'), directories))

    def _map_directories(self, directories):
        return [self._scan_episode(e) for e in directories]

    def _scan_episode(self, episode):
        parent = f'{self.path}/{episode}'
        children = [File(f, parent) for f in os.listdir(parent)]
        self.xbmc.log(f"Found {episode}.", level=self.xbmc.LOGDEBUG)
        return TvShowEpisodeDirectory(
            parent_directory=self.path,
            directory_name=episode,
            children=children
        )


# Linkers
class AbstractLinker(ABC):
    def __init__(self, new_path, scanner, xbmc, utils):
        super().__init__()
        self.new_path = new_path
        self.scanner = scanner
        self.xbmc = xbmc
        self.utils = utils

    def link(self):
        for directory in self.scanner.scan():
            self._link_directory(directory)

    @abstractmethod
    def _link_directory(self, directory):
        pass


class MovieLinker(AbstractLinker):
    def __init__(self, new_path, scanner, xbmc, utils):
        super().__init__(new_path, scanner, xbmc, utils)

    def _link_directory(self, directory):
        tmdb_directory = directory.get_tmdb_directory(self.new_path)
        self.utils.safe_makedirs(tmdb_directory.directory)
        for i, _ in enumerate(directory.children):
            os.symlink(directory.children[i].get_path(), tmdb_directory.children[i].get_path())
            self.xbmc.log(
                'Linked src={0} to dest={1}.'
                .format(directory.children[i].get_path(), tmdb_directory.children[i].get_path()),
                level=self.xbmc.LOGDEBUG
            )


class TvShowLinker(AbstractLinker):
    def __init__(self, new_path, scanner, xbmc, utils):
        super().__init__(new_path, scanner, xbmc, utils)

    def _link_directory(self, directory):
        tmdb_directory = directory.get_tmdb_directory(self.new_path)
        self.utils.safe_makedirs(tmdb_directory.name_directory)
        self.utils.safe_makedirs(tmdb_directory.season_directory)
        for i, _ in enumerate(directory.children):
            os.symlink(directory.children[i].get_path(), tmdb_directory.children[i].get_path())
            self.xbmc.log(
                f'Linked src={directory.children[i].get_path()} to dest={tmdb_directory.children[i].get_path()}',
                level=self.xbmc.LOGDEBUG
            )


class Linker:
    def __init__(
            self,
            movies_path,
            tv_shows_path,
            downloads_path,
            downloads_state_path,
            xbmc,
            movie_linker,
            episode_linker,
            season_linker,
            downloads_directory,
            utils
    ):
        self.movies_path = movies_path
        self.tv_shows_path = tv_shows_path
        self.downloads_path = downloads_path
        self.downloads_state_path = downloads_state_path
        self.movie_linker = movie_linker
        self.episode_linker = episode_linker
        self.season_linker = season_linker
        self.downloads_directory = downloads_directory
        self.xbmc = xbmc
        self.utils = utils

    def link(self):
        if not self.downloads_directory.contains_changes():
            self.xbmc.log('No changes detected in the downloads directory.', level=self.xbmc.LOGDEBUG)
            return

        prev_movies_descendants = self.utils.get_all_descendants(self.movies_path)
        prev_tv_shows_descendants = self.utils.get_all_descendants(self.tv_shows_path)

        self.utils.init_directories(self.movies_path, self.tv_shows_path)

        self.movie_linker.link()
        self.episode_linker.link()
        self.season_linker.link()

        next_movies_descendants = self.utils.get_all_descendants(self.movies_path)
        next_tv_shows_descendants = self.utils.get_all_descendants(self.tv_shows_path)

        deleted_movie_descendants = prev_movies_descendants.difference(next_movies_descendants)
        deleted_tv_shows_descendants = prev_tv_shows_descendants.difference(next_tv_shows_descendants)
        if len(deleted_movie_descendants) != 0 or len(deleted_tv_shows_descendants) != 0:
            self.xbmc.log(f'deleted_movie_descendants={deleted_movie_descendants}', level=self.xbmc.LOGINFO)
            self.xbmc.log(f'deleted_tv_shows_descendants={deleted_tv_shows_descendants}', level=self.xbmc.LOGINFO)
            self.xbmc.executebuiltin('CleanLibrary(video)')

        new_movie_descendants = next_movies_descendants.difference(prev_movies_descendants)
        new_tv_shows_descendants = next_tv_shows_descendants.difference(prev_tv_shows_descendants)
        if len(new_movie_descendants) != 0 or len(new_tv_shows_descendants) != 0:
            self.xbmc.log(f'new_movie_descendants={new_movie_descendants}', level=self.xbmc.LOGINFO)
            self.xbmc.log(f'new_tv_shows_descendants={new_tv_shows_descendants}', level=self.xbmc.LOGINFO)
            self.xbmc.executebuiltin('UpdateLibrary(video)')

        self.downloads_directory.update_state()
        self.xbmc.log('Updated state', level=self.xbmc.LOGDEBUG)
