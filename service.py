import xbmc
import xbmcaddon

from resources.lib.linker import Linker, MovieLinker, MovieScanner, TvShowLinker, TvShowEpisodeScanner, \
    DownloadsDirectory, Utils, TvShowSeasonScanner, Logger


def main():
    addon = xbmcaddon.Addon()
    monitor = xbmc.Monitor()

    tv_shows_path = addon.getSetting('tv_shows_path')
    movies_path = addon.getSetting('movies_path')
    downloads_path = addon.getSetting('downloads_path')
    downloads_state_path = addon.getSetting('downloads_state_path')
    interval_in_seconds = int(addon.getSetting('interval_in_seconds'))

    logger = Logger(xbmc)
    utils = Utils(logger)
    movie_scanner = MovieScanner(downloads_path, logger)
    tv_show_episode_scanner = TvShowEpisodeScanner(downloads_path, logger)
    tv_show_season_scanner = TvShowSeasonScanner(downloads_path, logger)
    downloads_directory = DownloadsDirectory(downloads_path, downloads_state_path, logger)
    movie_linker = MovieLinker(movies_path, movie_scanner, logger, utils)
    episode_linker = TvShowLinker(tv_shows_path, tv_show_episode_scanner, logger, utils)
    season_linker = TvShowLinker(tv_shows_path, tv_show_season_scanner, logger, utils)

    linker = Linker(
        tv_shows_path=tv_shows_path,
        downloads_path=downloads_path,
        movies_path=movies_path,
        downloads_state_path=downloads_state_path,
        xbmc=xbmc,
        logger=logger,
        movie_linker=movie_linker,
        episode_linker=episode_linker,
        season_linker=season_linker,
        downloads_directory=downloads_directory,
        utils=utils
    )

    i = 0
    tick = 10
    while not monitor.abortRequested():
        if monitor.waitForAbort(tick):
            break
        i += tick
        if i >= interval_in_seconds:
            i = 0
            logger.debug('Running linker!')
            linker.link()


if __name__ == '__main__':
    main()
