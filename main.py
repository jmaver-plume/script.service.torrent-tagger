import re
import os


def is_tv_show_dir(dir_name):
    return bool(re.search('S[0-9]{2}(E[0-9]{2})?', dir_name))


def is_movie_dir(dir_name):
    return bool(re.search('(2160p|1080p|720p)', dir_name))


def partition_dirs(dirs):
    tv_show_dirs = [d for d in dirs if is_tv_show_dir(d[1])]
    movie_dirs = [d for d in dirs if is_movie_dir(d) and d not in tv_show_dirs]
    return tv_show_dirs, movie_dirs


# TODO: raise Exception
def get_tmdb_name(original):
    pattern = r'(2160p|1080p|720p)'
    l = re.split(pattern, original)
    if not(len(l) > 1):
        return

    name = l[0].replace('.', ' ').strip()
    l2 = re.match(r'(.*) ([0-9]{4})', name).groups()
    if not(len(l2) == 2):
        return

    name, year = l2
    return f'{name} ({year})'


def handle_movie_dir(d):
    path, name = d
    tmdb_name = get_tmdb_name(name)
    if tmdb_name is None:
        return

    # TODO: Move to variable, move to init
    s_path = '/Users/user/Downloads_s'
    if not(os.path.exists(s_path)):
        os.makedirs(s_path)

    tmdb_path = f'{s_path}/{tmdb_name}'
    if not(os.path.exists(tmdb_path)):
        os.makedirs(tmdb_path)

    for v in os.listdir(f'{path}/{name}'):
        if name in v:
            src_name = v

    src_name, src_file_extension = os.path.splitext(src_name)
    src = f'{path}/{name}/{src_name}{src_file_extension}'
    dest = f'{tmdb_path}/{tmdb_name}{src_file_extension}'
    os.symlink(src, dest)


def handle_movie_dirs(dirs):
    for d in dirs:
        handle_movie_dir(d)


def handle_tv_show_dirs(dirs):
    pass


def main():
    # get all directories from folder
    # OPTIONAL: store a cache for performance reasons
    # if folder name is a film then
    #   tmdb_name = parse(original)
    #   mkdir movies/tmdb_name
    #   symbolic link

    tv_show_dirs, movie_dirs = partition_dirs('/Users/user/Downloads')
    handle_movie_dirs(movie_dirs)
    handle_tv_show_dirs(tv_show_dirs)

    movies = [
        'Knives.Out.2019.2160p.BluRay.HEVC.TrueHD.7.1.Atmos-EATDIK',
        'Glass.Onion.A.Knives.Out.Mystery.2022.1080p.WEBRip.x265-RARBG',
        'Strange.World.2022.1080p.AMZN.WEBRip.DDP5.1.x264-FLUX',
        'High.Heat.2022.1080p.AMZN.WEBRip.DDP5.1.x264-FLUX',
    ]

    parsed = [get_tmdb_name(movie) for movie in movies]
    print(parsed)


if __name__ == '__main__':
    main()
