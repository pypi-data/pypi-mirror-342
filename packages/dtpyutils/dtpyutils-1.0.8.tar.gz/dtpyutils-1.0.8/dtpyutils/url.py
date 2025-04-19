from urllib.parse import urlencode, urlparse, parse_qs, urlunparse


def add_query_param(url, params):
    url_parts = urlparse(url)
    query_params = parse_qs(url_parts.query)
    query_params.update(params)
    new_query = urlencode(query_params, doseq=True)
    new_url = urlunparse((
        url_parts.scheme,
        url_parts.netloc,
        url_parts.path,
        url_parts.params,
        new_query,
        url_parts.fragment
    ))
    return new_url
