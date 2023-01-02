import os
import re

from libreelec_torrent_linker.file import File
from libreelec_torrent_linker.linker import AbstractLinker
from libreelec_torrent_linker.scanner import Scanner
from libreelec_torrent_linker.tv_show_linker import TvShowEpisodeDirectory, TvShowSeasonDirectory


class MovieDirectory:
    def __init__(self, parent_directory, directory_name, children):
        self.parent_directory = parent_directory
        self.directory_name = directory_name
        self.children = children
        self.directory = f'{self.parent_directory}/{self.directory_name}'

    def get_tmdb_movie(self, new_directory):
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





