def snippets(request):
    main_stylesheets = """
        <link rel="stylesheet" href="/static/css/semantic.min.css">
        <link rel="stylesheet" href="/static/css/extra.css">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css">
    """

    main_js = """
        <script src="/static/js/jquery.min.js"></script>
        <script src="/static/js/semantic.min.js"></script>
    """
    return { "css_main":main_stylesheets, "js_main":main_js}