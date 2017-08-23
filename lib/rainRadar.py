# TODO - Change Property to a for loop that adds attribute to a dict with 'name' and 'url' values

from iceScraper import IceScraper

############################################################################################################


class RainRadar(IceScraper):
    """Uses IceScraper module to scrape the urls for MetVuw Charts.
    Chart URLs are stored in class variables."""
    def __init__(self, address):
        super(RainRadar, self).__init__(address)

        self.img06 = self.scrape_url('06')
        self.img12 = self.scrape_url('12')
        self.img18 = self.scrape_url('18')
        self.img24 = self.scrape_url('24')
        self.img30 = self.scrape_url('30')
        self.img36 = self.scrape_url('36')
        self.img42 = self.scrape_url('42')
        self.img48 = self.scrape_url('48')

    #######################################################

    def scrape_url(self, timecode):
        """Searches page source for every img element.
        Searches src for matching timecode and returns matching result."""
        url_list = self.soup.find_all('img')
        for i in url_list:
            url = i.get('src')
            if url[len(url)-6:len(url)-4] == timecode:
                result = 'http://www.metvuw.com/forecast%s' % (url[1::])
                return result

    #######################################################

    @property
    def json_object(self):
        """Returns information in a dictionary, which can easily be serialised using 'jsonify()'."""
        d = {
            'ahead06': self.img06,
            'ahead12': self.img12,
            'ahead18': self.img18,
            'ahead24': self.img24,
            'ahead30': self.img30,
            'ahead36': self.img36,
            'ahead42': self.img42,
            'ahead48': self.img48,
                }
        return d

############################################################################################################


def test():
    t = RainRadar('http://metvuw.com/forecast/forecast.php?type=rain&region=nzsi&noofdays=3')
    print t.scrape_url('12')

if __name__ == '__main__':
    test()
