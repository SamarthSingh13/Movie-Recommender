import requests


baseurl = "https://api.themoviedb.org/3/"
api_key = "5ee2bfd3c10aaeb6eefd31d8242fb986"
base_img_url = ""
def search_movie(query):
    url = baseurl + "search/movie?api_key=" + api_key + "&query=" + query
    response = requests.get(url)
    data = response.json()
    results = data['results']
    if results == []:
        return None
    return results[0]
    # for res in results:
    #     if query.lower() in [res["title"].lower(), res["original_title"].lower()]:
    #         return res
    #
    # return None

def get_base_img_url():
    global base_img_url
    if base_img_url == "":
        url = baseurl + "configuration?api_key=" + api_key
        response = requests.get(url)
        data = response.json()
        base_img_url = data["images"]["secure_base_url"]
    return base_img_url

def get_img_url(query):
    res = search_movie(query)
    if res is None:
        return ""
    size = "w185"
    img_path = res["poster_path"]
    if img_path is None:
        img_path = res["backdrop_path"]

    if img_path is None:
        return ""
    url = get_base_img_url() + size + img_path
    return url
