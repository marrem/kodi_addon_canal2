from BeautifulSoup import BeautifulSoup
import re

# TODO: null checks (ipv gechainde methods...)
class StreamUrlExtractor:
    def parse_stream_url(self, html):
        """
        Obtain m3u url from player page
        :param html player page:
        :return the m3u url:
        """
        tree = BeautifulSoup(html)
        script = tree.body.script.string
        stream_url_re = re.compile(r"player_hls\(\"(.*?)\"\);")
        stream_url = stream_url_re.search(script).group(1)
        return stream_url



    def parse_player_url(self, html):
        """
        Obtain player iframe html page url from main live.php page
        :param html main page:
        :return the player page url:
        """
        tree = BeautifulSoup(html)
        # Assuming the link to the stream url is the src attribute of the first iframe
        stream_url = tree.iframe['src']
        return stream_url