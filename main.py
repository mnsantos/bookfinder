from downloader import Downloader
from converter import Converter
from sender import Sender

if __name__ == '__main__':
    downloader = Downloader()
    downloader.download("magnet:?xt=urn:btih:0C15C68FF6B601D6E7E58B01FDCF652FAFE401A8&dn=EPL_Hamlet_(Biling%C3%BCe)&tr=http://tracker.tfile.me/announce&tr=udp://tracker.opentrackr.org:1337/announce&tr=udp://tracker.openbittorrent.com:80&tr=udp://tracker.publicbt.com:80&tr=udp://open.demonii.com:1337/announce")
    #converter = Converter()
    #converter.convert('download/test.epub')
    #sender = Sender('bookfinder1301', 'windows123')
    #sender.send('martin.n.santos@gmail.com', 'download/test.mobi')