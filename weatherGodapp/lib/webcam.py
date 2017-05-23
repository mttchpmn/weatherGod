from iceScraper import IceScraper

############################################################################################################


class NzskiWebcam(IceScraper):
    def __init__(self, address, mountain):
        super(NzskiWebcam, self).__init__(address)

        base_url = 'www.nzski.com'

        if mountain == 'Coronet Peak':
            self.coronet_express = self.scrape_img_url('title', 'Coronet Express', base_url)
            self.meadow_base = self.scrape_img_url('title', 'Meadow Base', base_url)
            self.top_station = self.scrape_img_url('title', 'Top Station', base_url)
        elif mountain == 'The Remarkables':
            self.base_learners = self.scrape_img_url('title', 'Base / Learners', base_url)
            self.lake_alta = self.scrape_img_url('title', 'Lake Alta', base_url)
            self.sugar_bowl = self.scrape_img_url('title', 'Sugar Bowl', base_url)

############################################################################################################


class AirportWebcam(IceScraper):
    def __init__(self, address):
        super(AirportWebcam, self).__init__(address)

        self.tower = self.scrape_airport_url('tower')
        self.coronet = self.scrape_airport_url('coronet')
        self.stands = self.scrape_airport_url('stands')
        self.lake = self.scrape_airport_url('lake')
        self.remarks = self.scrape_airport_url('remarks')

    #######################################################

    def scrape_airport_url(self, target):
        img_list = self.soup.find_all('img')
        l = len(target)
        for img in img_list:
            src = img.get('src')
            if src[16:16+l:] == target:
                url = 'http://www.queenstownairport.co.nz{}'.format(src)
                return url


############################################################################################################


class StaticWebcam(object):
    def __init__(self):
        self.glenorchy = 'http://www.snowgrass.co.nz/cust/glenorchy_air/images/webcam.jpg'

        self.cecil_peak_north = 'http://www.jablotool.com/webcamera/H1H1ISJWPU/1'
        self.cecil_peak_west = 'http://www.jablotool.com/webcamera/QXG2A2FXGT/1/'

        self.earnslaw = 'http://snapithd.com/static/earnslaw.jpg'
        self.steamer_wharf = 'http://www.southerndiscoveries.co.nz/webcam-images/QTN1/webcam3.jpg?1495416172'

        self.traffic_qn_south = 'http://www.trafficnz.info/camera/621.jpg'
        self.traffic_qn_north = 'http://www.trafficnz.info/camera/622.jpg'

        self.traffic_kbridge = 'http://www.trafficnz.info/camera/623.jpg'
        self.traffic_frankton = 'http://www.trafficnz.info/camera/627.jpg'

############################################################################################################


def main():
    cp = NzskiWebcam('https://www.nzski.com/queenstown/the-mountains/coronet-peak/coronet-peak-weather-report',
                       'Coronet Peak')
    rm = NzskiWebcam('https://www.nzski.com/queenstown/the-mountains/the-remarkables/the-remarkables-weather-report',
                        'The Remarkables')

    ap = AirportWebcam('http://www.queenstownairport.co.nz/travelling/flight-info/webcam')

    # print cp.top_station
    # print cp.meadow_base
    # print cp.coronet_express

    # print rm.base_learners
    # print rm.sugar_bowl
    # print rm.lake_alta

    print ap.tower
    print ap.coronet
    print ap.stands
    print ap.lake
    print ap.remarks

############################################################################################################

if __name__ == '__main__':
    main()
