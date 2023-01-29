import time
import xbmc

from resources.lib.linker import Linker


def main():
    monitor = xbmc.Monitor()

    i = 0
    while not monitor.abortRequested():
        if monitor.waitForAbort(10):
            break
        i += 10
        if i == 300:
            i = 0
            xbmc.log(f"[{time.time()}]:  Running linker!", level=xbmc.LOGINFO)
            linker = Linker(
                tv_shows_path='/storage/tvshows',
                downloads_path='/storage/transmission/downloads/complete',
                movies_path='/storage/movies',
                downloads_state_path='/storage/.cache/.torrent-tagger',
                xbmc=xbmc
            )
            linker.link()


if __name__ == '__main__':
    main()
