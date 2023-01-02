import os
import re

from libreelec_torrent_linker.file import File
from libreelec_torrent_linker.linker import AbstractLinker
from libreelec_torrent_linker.scanner import Scanner


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
        name, identifier, season = re.match(r'(.+)\.([sS]([0-9]{2})[eE][0-9]{2}).*', self.directory_name).groups()
        name = name.replace('.', ' ')
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
        # This almost duplicates TV Show Episode
        name, season = re.match(r'(.+)\.[sS]([0-9]{2}).*', self.directory_name).groups()
        name = name.replace('.', ' ')
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
            self.logging.debug(f'Linked src={episode.children[i].get_path()} to dest={tmdb_episode.children[i].get_path()}')



