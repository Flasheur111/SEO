import requests

class BingSearchAPI:
    bing_api = "https://api.datamarket.azure.com/Data.ashx/Bing/Search/Image?"

    def __init__(self, key):
        self.key = key

    def replace_symbols(self, request):
        request = str.replace(request, "'", '%27')
        request = str.replace(request, '"', '%27')
        request = str.replace(request, '+', '%2b')
        request = str.replace(request, ' ', '%20')
        request = str.replace(request, ':', '%3a')
        return request

    def search(self, query, params):
        request = 'Query="' + query + '"'
        for key, value in params.items():
            request += '&' + key + '=' + str(value)
        request = self.bing_api + self.replace_symbols(request)
        output = requests.get(request, auth=(self.key, self.key))
        return output
