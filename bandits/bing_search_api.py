import requests # Get from https://github.com/kennethreitz/requests
import string

class BingSearchAPI():
    bing_api = "https://api.datamarket.azure.com/Data.ashx/Bing/Search/v1/Composite?"

    def __init__(self, key):
        self.key = key

    def replace_symbols(self, request):
        # Custom urlencoder.
        # They specifically want %27 as the quotation which is a single quote '
        # We're going to map both ' and " to %27 to make it more python-esque
        request = string.replace(request, "'", '%27')
        request = string.replace(request, '"', '%27')
        request = string.replace(request, '+', '%2b')
        request = string.replace(request, ' ', '%20')
        request = string.replace(request, ':', '%3a')
        return request

    def search(self, sources, query, params):
        request =  'Sources="' + sources    + '"'
        request += '&Query="'  + str(query) + '"'
        for key,value in params.iteritems():
            request += '&' + key + '=' + str(value)
        request = self.bing_api + self.replace_symbols(request)
        return requests.get(request, auth=(self.key, self.key))


if __name__ == "__main__":
    my_key = "[your key]"
    query_string = "Brad Pitt"
    bing = BingSearchAPI(my_key)
    params = {'$format': 'json',
              '$top': 10,
              '$skip': 0}
    print bing.search('image',query_string,params).json()
