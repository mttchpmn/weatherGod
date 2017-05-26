# TODO - Fix bug for altitudes over 10,000m (250mb)

from pprint import pprint
import requests

############################################################################################################


class Sounding(object):
    def __init__(self, station_number, index):
        self.station_number = station_number
        self.index = index

        self.data = self.combine_AABB_dicts()
        self.valid_from = self.valid_from()

    ####################################################

    def combine_AABB_dicts(self):
        AA = self.process_raw_data('TTAA')
        BB = self.process_raw_data('TTBB')

        for i in BB:
            AA.append(i)
        AABB = sorted(AA, key=lambda k: k['pressure'])
        AABB = list(reversed(AABB))

        return AABB

    def process_raw_data(self, level):
        raw_data = self.get_response(level)
        list_1d = self.list_1d(raw_data, level)
        list_2d = self.list_2d(list_1d, level)
        dct = self.list_2d_to_dict(list_2d, level)
        return dct

    def valid_from(self):
        AA = self.get_response('TTAA')
        BB = self.get_response('TTBB')
        AA_valid = AA[self.index]['validFrom']
        BB_valid = BB[self.index]['validFrom']
        if AA_valid == BB_valid:
            return AA_valid
        else:
            return '"ValidFrom" times do not match.'

    ####################################################

    def get_response(self, level):
        """Retrieves 3 latest soundings from Metservice API for given Level"""
        url = 'http://www.metservice.com/publicData/codedDataUPPERTEMPS_{}'.format(level)
        r = requests.get(url)
        response = r.json()
        return response

    ####################################################

    def list_1d(self, content, level):
        """Converts raw data from API to 1D list, given index (0 is most recent)
        List contains every chunk from Raw Data.  Excluding starting space, first two chunks
        are timecode and station ID."""
        data = content[self.index]['data']
        data = data.replace('<br>', ' ')
        data = data.replace('=', '')
        data = data.split(level)

        for i in data:
            if self.station_number in i:
                data = i
        data = data.split(' ')
        del data[0]  # Deletes blank index at start of list
        return data

    ####################################################

    def list_2d(self, list_1d, level):
        """Converts 1 dimensional list to 2 dimensional list.  Every list index contains 2 chunks.
        Chunks are pres/alt and temp/dp for TTAA, and pres and temp/dp for TTBB. Note that station and
        timecode are stripped from list."""
        if level == 'TTAA':
            data = list_1d[2:19:]
            del data[2]
        elif level == 'TTBB':
            data = list_1d[2::]
            for i in data[::2]:
                if int(i[2]) == 2 and int(i[3]) <= 5:
                    end_index = data.index(i) + 2
                    break
            data = data[:end_index:]
        list_2d = [data[i:i+2] for i in range(0, len(data), 2)]
        return list_2d

    ####################################################

    def list_2d_to_dict(self, list_2d, level):
        """Converts the 2d list to a dictionary, with keys for pressure, altitude (if TTAA), 
        temperature and dewpoint; values are returned as floats."""
        l = []
        for i in list_2d:
            d = {}

            if level == 'TTAA':
                pressure, altitude = self.pressure_and_altitude(level, i[0])
                d['pressure'] = pressure
                d['altitude'] = altitude
            elif level == 'TTBB':
                pressure = self.pressure_and_altitude(level, i[0])
                d['pressure'] = pressure

            temp, dewpoint = self.temp_and_dewpoint(i[1])
            d['temp'] = temp
            d['dewpoint'] = dewpoint

            l.append(d)
        return l

    ####################################################

    def high_low(self, number):
        if int(number) <= 5:
            return True
        else:
            return False

    def pressure_and_altitude(self, level, chunk):
        """Accepts 5 digit chunk of information and breaks apart pressure and altitude section codes;
        pressure and altitude is then evaluated to return actual values."""
        if level == 'TTAA':
            press = chunk[0:2]
            alt = chunk[2:5]

            if press == '99':
                altitude = 0
                if alt[0] == '0':
                    pressure = int(alt) + 1000
                else:
                    pressure = int(alt)
            elif press == '00':
                pressure = 1000
                altitude = int(alt)
            elif press == '85':
                pressure = 850
                altitude = int(alt) + 1000
            elif press == '70':
                pressure = 700
                if self.high_low(alt[0]):  # Is this statement robust enough?????
                    altitude = int(alt) + 3000
                else:
                    altitude = int(alt) + 2000
            elif press == '50' or '40' or '30':
                pressure = int(press) * 10
                altitude = int(alt) * 10
            else:
                pressure = int(press) * 10
                altitude = (int(alt) * 10) + 10000

            return pressure, altitude

        elif level =='TTBB':
            pres = chunk[2:5]
            if pres[0] == '0':
                pressure = int(pres) + 1000
            else:
                pressure = int(pres)

            return pressure

    ####################################################

    def temp_and_dewpoint(self, chunk):
        temp = chunk[0:3]
        dd = chunk[3:5]

        if int(temp[2]) % 2 != 0:
            temp = int(temp) * -1
        temp = float(int(temp)) / 10

        if float(dd) >= 50:
            dd = float(dd) - 50
        else:
            dd = float(dd) / 10
        dewpoint = float(temp) - float(dd)
        dewpoint = round(dewpoint, 2)

        return temp, dewpoint


############################################################################################################
# TESTING

test = Sounding('93844', 0)
print test.valid_from

pprint(test.data)