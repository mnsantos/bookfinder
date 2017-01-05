import libtorrent as lt
import time
import logging

class Downloader:

    def download(self, magnet_link):
        logging.info("Downloading..." + magnet_link)
        ses = lt.session()
        ses.listen_on(6881, 6891)

        #e = lt.bdecode(open("test.torrent", 'rb').read())
        #info = lt.torrent_info(e)

        params = { 'save_path': 'download/', 'name': 'lpm'}
        link = magnet_link
        handle = lt.add_magnet_uri(ses, link, params)

        logging.info('Downloading metadata...')
        while (not handle.has_metadata()): time.sleep(1)
        logging.info('Got metadata, starting torrent download...')
        while (handle.status().state != lt.torrent_status.seeding):
            logging.info('%d %% done' % (handle.status().progress*100))
            time.sleep(1)
        return "download/" + handle.name()