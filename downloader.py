import libtorrent as lt
import time

class Downloader:

    def download(self, magnet_link):
        print "Downloading..."
        ses = lt.session()
        ses.listen_on(6881, 6891)

        #e = lt.bdecode(open("test.torrent", 'rb').read())
        #info = lt.torrent_info(e)

        params = { 'save_path': 'download/'}
        link = magnet_link
        handle = lt.add_magnet_uri(ses, link, params)

        print 'downloading metadata...'
        while (not handle.has_metadata()): time.sleep(1)
        print 'got metadata, starting torrent download...'
        while (handle.status().state != lt.torrent_status.seeding):
            print '%d %% done' % (handle.status().progress*100)
            time.sleep(1)

        # h = ses.add_torrent(params)

        # s = h.status()
        # while (not s.is_seeding):
        #         s = h.status()

        #         state_str = ['queued', 'checking', 'downloading metadata', \
        #                 'downloading', 'finished', 'seeding', 'allocating']
        #         print '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
        #                 (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
        #                 s.num_peers, state_str[s.state])

        #         time.sleep(1)
        # return "filePath"