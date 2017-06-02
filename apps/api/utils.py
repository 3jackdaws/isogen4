from urllib.request import urlopen, Request
import redis
from hashlib import md5

red = redis.Redis(host='redis', port=6379)

def api_cache(request:Request, exp_time=3600):
    request_hash = md5()
    request_hash.update(request.full_url.encode('utf-8'))
    request_hash.update(str(request.headers).encode('utf-8'))
    request_hash = request_hash.digest()
    try:
        response = red.get(request_hash).decode('utf-8')
        print("API CACHE HIT - %s" % hash)
    except:
        response = urlopen(request).read().decode('utf-8')
        red.setex(request_hash, response, exp_time)
    return response


def file_cache(filepath):
    try:
        response = red.get(filepath).decode('utf-8')
    except:
        response = open(filepath, "rb").read()
        red.setex(filepath, response, 10)
    return response

def github_request(url, exp_time=3600):
    req = Request(url)
    from isogen4.settings import GITHUB_ACCESS_TOKEN
    req.add_header('Authorization', 'token {}'.format(GITHUB_ACCESS_TOKEN))
    response = api_cache(req)
    return response

def get_repo_json(url):
    import json
    repos = json.loads(github_request(url))
    for repo in repos:
        repo['technologies'] = json.loads(github_request(repo['languages_url']))
    return repos
