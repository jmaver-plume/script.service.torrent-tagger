import time
import xbmc
import xbmcaddon

from resources.lib.linker import Linker, MovieLinker, MovieScanner, TvShowLinker, TvShowEpisodeScanner, \
    DownloadsDirectory, Utils, TvShowSeasonScanner


def main():
    addon = xbmcaddon.Addon()
    monitor = xbmc.Monitor()

    i = 0
    while not monitor.abortRequested():
        if monitor.waitForAbort(10):
            break
        i += 10
        if i == 300:
            i = 0
            xbmc.log(f"[{time.time()}]:  Running linker!", level=xbmc.LOGINFO)
            utils = Utils(xbmc)

            tv_shows_path = addon.getSetting('tv_shows_path')
            movies_path = addon.getSetting('movies_path')
            downloads_path = addon.getSetting('downloads_path')
            downloads_state_path = addon.getSetting('downloads_state_path')

            movie_scanner = MovieScanner(downloads_path, xbmc)
            tv_show_episode_scanner = TvShowEpisodeScanner(downloads_path, xbmc)
            tv_show_season_scanner = TvShowSeasonScanner(downloads_path, xbmc)
            downloads_directory = DownloadsDirectory(downloads_path, downloads_state_path, xbmc)
            movie_linker = MovieLinker(movies_path, movie_scanner, xbmc, utils)
            episode_linker = TvShowLinker(movies_path, tv_show_episode_scanner, xbmc, utils)
            season_linker = TvShowLinker(movies_path, tv_show_season_scanner, xbmc, utils)

            linker = Linker(
                tv_shows_path=tv_shows_path,
                downloads_path=downloads_path,
                movies_path=movies_path,
                downloads_state_path=downloads_state_path,
                xbmc=xbmc,
                movie_linker=movie_linker,
                episode_linker=episode_linker,
                season_linker=season_linker,
                downloads_directory=downloads_directory,
                utils=utils
            )
            linker.link()


if __name__ == '__main__':
    main()
