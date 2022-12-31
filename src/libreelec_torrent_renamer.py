import logging
import re
import os
import traceback

DOWNLOADS_PATH = os.getenv("DOWNLOADS_PATH")
MOVIES_SYMBOLIC_PATH = os.getenv("MOVIES_SYMBOLIC_PATH")
TV_SHOWS_SYMBOLIC_PATH = os.getenv("TV_SHOWS_SYMBOLIC_PATH")


def is_tv_show_episode_dir(dir_name):
    return bool(re.search('[sS][0-9]{2}[eE][0-9]{2}', dir_name))


def is_tv_show_season_dir(dir_name):
    return not(is_tv_show_episode_dir(dir_name)) and bool(re.search('S[0-9]{2}', dir_name))


def is_tv_show_dir(dir_name):
    return is_tv_show_season_dir(dir_name) or is_tv_show_episode_dir(dir_name)


def is_movie_dir(dir_name):
    return not(is_tv_show_dir(dir_name)) and bool(re.search('(2160p|1080p|720p)', dir_name))


class ParseMovieException(Exception):
    pass


def get_tmdb_name(original):
    split_on_quality = re.split(r'(2160p|1080p|720p)', original)
    if not(len(split_on_quality) > 1):
        raise ParseMovieException(f'Title {original} does not have a valid quality.')

    name = split_on_quality[0].replace('.', ' ').strip()
    split_on_year = re.match(r'(.*) ([0-9]{4})', name).groups()
    if not(len(split_on_year) == 2):
        raise ParseMovieException(f'Title {original} does not have a year.')

    name, year = split_on_year
    return f'{name} ({year})'


def is_video_file(name):
    _, ext = os.path.splitext(name)
    return bool(re.search(r'\.(mkv|mp4|mov|wmv|avi)', name))


def find_video_file(name, dirs):
    src_name = next((file for file in dirs if name in file), None)
    if src_name is None:
        raise ParseMovieException(f'Directory {name} does not contain a video file with the same name.')
    return os.path.splitext(src_name)


def find_tv_show_file(dirs):
    src_name = next((file for file in dirs if is_video_file(file) and is_tv_show_episode_dir(file)), None)
    if src_name is None:
        raise ParseMovieException(f'Directory does not contain an episode video file.')
    return os.path.splitext(src_name)


def handle_movie_dir(movie_dir):
    tmdb_name = get_tmdb_name(movie_dir)

    symbolic_movie_dir = f'{MOVIES_SYMBOLIC_PATH}/{tmdb_name}'
    if not(os.path.exists(symbolic_movie_dir)):
        os.makedirs(symbolic_movie_dir)

    # Symbolic link the video file
    src_name, src_file_extension = find_video_file(movie_dir, os.listdir(f'{DOWNLOADS_PATH}/{movie_dir}'))
    src = f'{DOWNLOADS_PATH}/{movie_dir}/{movie_dir}{src_file_extension}'
    dest = f'{MOVIES_SYMBOLIC_PATH}/{tmdb_name}/{tmdb_name}{src_file_extension}'
    os.symlink(src, dest)

    # Symbolic link all other files except the video file
    for v in os.listdir(f'{DOWNLOADS_PATH}/{movie_dir}'):
        if movie_dir not in v:
            os.symlink(f'{DOWNLOADS_PATH}/{movie_dir}/{v}', f'{MOVIES_SYMBOLIC_PATH}/{tmdb_name}/{v}')


def handle_movie_dirs(movie_dirs):
    for movie_dir in movie_dirs:
        try:
            handle_movie_dir(movie_dir)
        except Exception as e:
            logging.error(traceback.format_exc())


def create_tv_show_name_folder(name):
    s_root_folder = f'{TV_SHOWS_SYMBOLIC_PATH}/{name}'
    if not (os.path.exists(s_root_folder)):
        os.mkdir(s_root_folder)
    return s_root_folder


def create_tv_show_season_folder(name, season):
    s_season_folder = f'{TV_SHOWS_SYMBOLIC_PATH}/{name}/Season {season}'
    if not (os.path.exists(s_season_folder)):
        os.mkdir(s_season_folder)
    return s_season_folder


def handle_tv_show_season_dir(tv_show_dir):
    name, season = re.match(r'(.+)\.S([0-9]{2}).*', tv_show_dir).groups()
    name = name.replace('.', ' ')
    season = int(season)

    create_tv_show_name_folder(name)
    s_season_folder = create_tv_show_season_folder(name, season)

    # Create symlink for each episode
    tv_show_dir_absolute_path = f'{DOWNLOADS_PATH}/{tv_show_dir}'
    for episode in os.listdir(tv_show_dir_absolute_path):
        if is_tv_show_episode_dir(episode):
            v = re.match(r'.*(S[0-9]{2}E[0-9]{2}).*', episode).groups()
            src = f'{tv_show_dir_absolute_path}/{episode}'
            _, ext = os.path.splitext(episode)
            dest = f'{s_season_folder}/{name} {v[0]}{ext}'
            os.symlink(src, dest)

    # Create symlink for Subs
    if os.path.exists(f'{tv_show_dir_absolute_path}/Subs'):
        sub_folders = [v for v in os.listdir(f'{tv_show_dir_absolute_path}/Subs')]
        print(sub_folders)
        for folder in sub_folders:
            v = re.match(r'.*(S[0-9]{2}E[0-9]{2}).*', folder).groups()
            if len(v) != 1:
                print('Not found')
                continue
            srt_files = [v for v in os.listdir(f'{tv_show_dir_absolute_path}/Subs/{folder}') if bool(re.search(r'.*\.srt', v))]
            for srt_file in srt_files:
                src = f'{tv_show_dir_absolute_path}/Subs/{folder}/{srt_file}'
                dest = f'{s_season_folder}/{name} {v[0]}_{srt_file}'
                os.symlink(src, dest)


def handle_tv_show_season_dirs(dirs):
    for _dir in dirs:
        try:
            handle_tv_show_season_dir(_dir)
        except Exception as e:
            logging.error(traceback.format_exc())


def handle_tv_show_episode_dir(tv_show_dir):
    name, season, episode = re.match(r'(.+)\.S([0-9]{2})(E[0-9]{2}).*', tv_show_dir).groups()
    name = name.replace('.', ' ')
    season = int(season)

    create_tv_show_name_folder(name)
    s_season_folder = create_tv_show_season_folder(name, season)

    # Symlink episode
    src_name, src_file_extension = find_tv_show_file(os.listdir(f'{DOWNLOADS_PATH}/{tv_show_dir}'))
    v = re.match(r'.*([sS][0-9]{2}[eE][0-9]{2}).*', src_name).groups()
    src = f'{DOWNLOADS_PATH}/{tv_show_dir}/{src_name}{src_file_extension}'
    dest = f'{s_season_folder}/{name} {v[0].upper()}{src_file_extension}' # TODO: move to same function
    os.symlink(src, dest)


def handle_tv_show_episode_dirs(dirs):
    for _dir in dirs:
        try:
            handle_tv_show_episode_dir(_dir)
        except Exception as e:
            logging.error(traceback.format_exc())


def init():
    if not(os.path.exists(MOVIES_SYMBOLIC_PATH)):
        os.makedirs(MOVIES_SYMBOLIC_PATH)

    if not(os.path.exists(TV_SHOWS_SYMBOLIC_PATH)):
        os.makedirs(TV_SHOWS_SYMBOLIC_PATH)


def main():
    init()
    dirs = os.listdir(DOWNLOADS_PATH)

    movie_dirs = list(filter(is_movie_dir, dirs))
    handle_movie_dirs(movie_dirs)

    tv_show_season_dirs = list(filter(is_tv_show_season_dir, dirs))
    handle_tv_show_season_dirs(tv_show_season_dirs)

    tv_show_episode_dirs = list(filter(is_tv_show_episode_dir, dirs))
    handle_tv_show_episode_dirs(tv_show_episode_dirs)


if __name__ == '__main__':
    main()
