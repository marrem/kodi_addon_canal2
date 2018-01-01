from unittest import TestCase, main
from canal2.stream_url_extractor import parse_player_url, parse_stream_url


class TestStreamExtractor(TestCase):

    def __init__(self, test_case_names):
        super(TestStreamExtractor, self).__init__(test_case_names)

    def test_parse_player_url(self):
        # mainpage = urlopen('http://www.canal2international.net/live.php')
        mainpage = open("canal2live.html")
        result = parse_player_url(mainpage)
        self.assertEqual("http://canal2.hexaglobe.com/index.php?m=142f16594ee92132d9b5bd9afaa5cf67&t_hex=58b1f512&targetfile=canal2inte.smil", result)


    def test_parse_stream_url(self):
        playerpage = open("canal2player.html")
        result = parse_stream_url(playerpage)
        self.assertEqual("http://canal2-live-p2-cdn.hexaglobe.net/46b20a25cbd94f12fe77d8c1f1c3d836/58b2e0aa/canal2intepri_fre.smil/playlist.m3u8", result)

if __name__ == '__main__':
    main()
