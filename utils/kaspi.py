def get_kaspi_http_headers(token):
    try:
        token_api = token.token_api
    except AttributeError:
        raise AttributeError("Атрибут token_api не найдено")

    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
        'Content-Type': 'application/vnd.api+json',
        'X-Auth-Token': token_api,
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5"
    }
