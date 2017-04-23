import threading
import time
from isogen4.models import Log
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from wsgiref.util import FileWrapper
import os

def snippets(request):
    main_stylesheets = """
        <link rel="stylesheet" href="/static/css/semantic.min.css">
        <link rel="stylesheet" href="/static/css/extra.css">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css">
    """

    main_js = """
        <script src="/static/js/jquery.min.js"></script>
        <script src="/static/js/semantic.min.js"></script>
        <script src="/static/js/isogen.js"></script>
    """


    return { "css_main":main_stylesheets, "js_main":main_js}


def async_defer(sleep_for, task, *args, **kwargs):
    def wait():
        print("Defered task started: {}".format(task.__name__))
        time.sleep(sleep_for)
        return task(*args, **kwargs)

    thread = threading.Thread(target=wait, args=args, kwargs=kwargs)
    thread.setDaemon(True)
    thread.start()

def async_run(task, *args, **kwargs):
    thread = threading.Thread(target=task, args=args, kwargs=kwargs)
    thread.setDaemon(True)
    thread.start()


def view_metrics_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request:HttpRequest):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        path = request.get_full_path()
        ip = request.META.get('REMOTE_ADDR')
        log = Log(ip=ip, path=path)
        async_run(log.save)

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware



def send_file(request, filename):
    """
    Send a file through Django without loading the whole file into
    memory at once. The FileWrapper will turn the file object into an
    iterator for chunks of 8KB.
    """
    wrapper = FileWrapper(open(filename, "rb"))
    response = HttpResponse(wrapper, content_type='X-DOWNLOAD')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename)
    print("sending dl")
    return response
