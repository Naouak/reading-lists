import requests

class MarvelCalendar:
    calendar_url = "https://bifrost.marvel.com/v1/catalog/comics/calendar/mu?byType=date&offset={}&limit={}&orderBy=in_mu_date%2Bdesc%2Ctitle%2Basc&variants=false&formatType=issue%2Cdigitalcomic%2Cdigitalverticalcomic&dateStart={}&dateEnd={}"

    def check_calendar(self, start, end, limit = 35, page = 0):
        url = self.build_url(start, end, limit, page)
        print(url)
        bifrost_data = requests.get(url).json()
        print(bifrost_data)
        results = bifrost_data['data']['results'] if 'results' in bifrost_data['data'] else []
        if 'total' in bifrost_data['data'] and bifrost_data['data']['total'] > page*limit + limit:
            print("Checking page "+str(page+1))
            results = results + self.check_calendar(start, end, limit, page+1)

        return results

    def build_url(self, start, end, limit, page):
        return self.calendar_url.format(page*limit, limit, start, end)
