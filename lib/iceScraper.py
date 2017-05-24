from bs4 import BeautifulSoup
import requests

############################################################################################################


class IceScraper(object):
    """Uses requests and beautifulsoup libraries to retrieve html content.
    Defines methods to simplify scraping of data.  Not specific to any particular website."""
    def __init__(self, address):
        r = requests.get(address)
        c = r.content
        self.soup = BeautifulSoup(c, "html.parser")

    def item_by_class(self, element, class_name):
        result = self.soup.find(element, {"class": class_name})
        check_result = result.string
        if check_result is not None:
            result = result.string
            result = result.strip()
        else:
            result = result.text
            result = ' '.join(result.split())
        return result

    def list_by_class(self, class_name):
        l = self.soup.findAll("div", {"class": class_name})
        results = []
        for i in l:
            val = i.string
            val = val.strip()
            results.append(val)
        return results

    def list_from_parent(self, element, class_name):
        parent = self.soup.find(element, {"class": class_name})
        l = parent.children
        results = []
        for i in l:
            results.append(i)
        return results

    def dict_from_lists(self, key_list, value_list):
        keys = []
        values = []
        key_length = int(len(key_list))

        for i in key_list:
            val = i.strip()
            keys.append(val)

        for i in value_list[:key_length]:
            val = i.strip()
            values.append(val)

        result = dict(zip(keys, values))
        return result

    def scrape_img_url(self, param, target, base_url):
        img_list = self.soup.find_all('img')
        for img in img_list:
            if img.get(param) == target:
                src = img.get('src')
                url = 'https://{}{}'.format(base_url, src)
                return url
