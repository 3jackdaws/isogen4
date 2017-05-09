from urllib.request import Request, urlopen
from urllib.parse import urlencode
import json
import mutagen
import os


API_BASE = "https://api.soundcloud.com"
CLIENT_ID = "3565524c74b5001489385a411137f6e2"
CLIENT_SECRET = "b86833932d85229693af65801073fa67"

DOWNLOAD_DIR = "/tmp/"

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

def get_300px_album_art(track_object):
    art_url = track_object['artwork_url']  # type: str
    return art_url.replace('large', 't300x300')

def embed_artwork(audio:mutagen.File, artwork_url):
    print(artwork_url)
    audio.tags.add(
        mutagen.id3.APIC(
            encoding=3,
            mime='image/jpeg',
            type=3,
            desc=u'Cover',
            data=urlopen(artwork_url).read()
        )
    )
    return audio

def set_artist_title(audio:mutagen.File, artist, title):
    frame = mutagen.id3.TIT2(encoding=3)
    frame.append(title)
    audio.tags.add(frame)
    frame = mutagen.id3.TPE1(encoding=3)
    frame.append(artist)
    audio.tags.add(frame)
    return audio


def file_from_track(track):
    filename = DOWNLOAD_DIR + track['title'] + ".mp3"
    print("Attempt fetch: {}".format(filename))
    if not os.path.exists(filename):
        print("File not found: get resource")
        stream = get_stream_as_resource(track)
        print("Write file")
        with open(filename, "wb+") as file:
            file.write(stream.read())
            file.close()
        print("Open file for tag writing")
        audio = mutagen.File(filename)
        audio.add_tags()
        audio = set_artist_title(audio, track['user']['username'], track['title'])
        audio = embed_artwork(audio, get_300px_album_art(track))
        audio.save(filename, v1=2)
        print("saved file")
    return filename
