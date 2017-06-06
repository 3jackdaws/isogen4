from urllib.request import urlopen, Request
import redis
from hashlib import md5
from threading import Timer

red = redis.Redis(host='redis', port=6379)
maintain_dict = {}

def delete_timer_then_call(timer_hash, function):
    def wrap(*args, **kwargs):
        print("Delete %s " % timer_hash)
        del maintain_dict[timer_hash]
        return function(*args, **kwargs)
    return wrap


def api_cache(request: Request, exp_time=3600, maintain=False, refetch=False):
    request_hash = md5()
    request_hash.update(request.full_url.encode('utf-8'))
    request_hash.update(str(request.headers).encode('utf-8'))
    request_hash = request_hash.digest()

    response = red.get(request_hash)
    if response:
        response = response.decode('utf-8')

    if refetch or not response:
        response = urlopen(request).read().decode('utf-8')
        red.setex(request_hash, response, exp_time)
    if maintain:
        if request_hash not in maintain_dict:
            print("Request to maintain request")
            t = Timer(exp_time - 60, delete_timer_then_call(request_hash, api_cache), [request, exp_time, True, True])
            t.start()
            maintain_dict[request_hash] = t
    return response


def file_cache(filepath):
    return open(filepath, "rb").read()

def github_request(url, exp_time=3600):
    req = Request(url)
    from isogen4.settings import GITHUB_ACCESS_TOKEN
    req.add_header('Authorization', 'token {}'.format(GITHUB_ACCESS_TOKEN))
    response = api_cache(req, maintain=True)
    return response

def get_repo_json(url):
    import json
    repos = json.loads(github_request(url))
    for repo in repos:
        repo['technologies'] = json.loads(github_request(repo['languages_url']))
    return repos
