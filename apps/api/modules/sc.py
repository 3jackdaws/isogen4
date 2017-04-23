from urllib.request import Request, urlopen
from urllib.parse import urlencode
import json


API_BASE = "https://api.soundcloud.com"
CLIENT_ID = "3565524c74b5001489385a411137f6e2"
CLIENT_SECRET = "b86833932d85229693af65801073fa67"


def form_request(base_url, **kwargs):
    params = dict(kwargs, client_id=CLIENT_ID)
    fullurl = base_url + "?" + urlencode(params)
    request = Request(fullurl)
    return request

def get_json(request:Request):
    return json.loads(urlopen(request).read().decode('utf-8'))

def get_track(id):
    request = form_request(API_BASE + "/tracks/" + id)
    return get_json(request)

def resolve(url):
    base = "http://api.soundcloud.com/resolve"
    request = form_request(base, url=url)
    return get_json(request)

def is_downloadable(object):
    return "stream_url" in object

def get_title(track_object):
    return track_object['title']


def get_stream_as_resource(track_object):
    if is_downloadable(track_object):
        stream = track_object['stream_url']
        request = form_request(stream)
        return urlopen(request)
    else:
        print("Object is not a track")




# track = get_track("13158665")
# print(track['downloadable'])
# stream_url = form_request(track['stream_url'])
# print(stream_url.full_url)

track = resolve("https://soundcloud.com/ofdream/pryda-shadows-ofdream-vision")

print(get_title(track))