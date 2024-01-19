import urllib.parse


def add_domain_prefix(url: str, prefix: str) -> str:
    """
    Adds prefix to server name in url

    Example:
    _add_prefix("https://example.com/path", "test") -> "https://test.example.com/path"

    :param url:    - base url to modify
    :param prefix: - prefix to add to base url domain
    :return:       - composed url

    """
    parsed_url = urllib.parse.urlsplit(url)
    new_parsed_url = parsed_url._replace(netloc=f"{prefix}.{parsed_url.netloc}")
    return new_parsed_url.geturl()
