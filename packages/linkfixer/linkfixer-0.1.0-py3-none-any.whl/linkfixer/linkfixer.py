
""" 
url_normalizer.py

A powerful utility to clean, normalize, and validate user-provided URLs.

Features:
- Scheme enforcement and HTTPS forcing
- www prefix option
- Query and path cleanup
- Trailing slash control
- Fragment handling
- Add or override query parameters
- IDN support (punycode or unicode)
- DNS resolution check
- Shortlink detection
- Developer verbose mode

Author: Renukumar R
"""

from urllib.parse import urlparse, urlunparse, urlencode, parse_qsl
import idna
import socket

DEFAULT_TRACKING_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid", "fbclid"
}

DEFAULT_SHORTLINK_DOMAINS = {
    "bit.ly", "t.co", "tinyurl.com", "goo.gl", "rebrand.ly"
}

def normalize_url(
    raw_url: str,
    *,
    default_scheme: str = "https",
    force_https: bool = False,
    force_www: bool = False,
    remove_tracking: bool = True,
    remove_query_string: bool = False,
    clear_paths: bool = False,
    remove_trailing_slash: bool = False,
    strip_fragment: bool = False,
    add_query: dict = None,
    output: str = "url",  # "url" or "parts"
    allow_non_http: bool = True,
    blacklist_domains: set = None,
    allowlist_tlds: set = None,
    shortlink_domains: set = None,
    tracking_params: set = None,
    idn_format: str = "punycode",  # "unicode" or "punycode"
    verify_dns: bool = False,
    verbose: bool = False
) -> dict:
    blacklist_domains = blacklist_domains or set()
    shortlink_domains = shortlink_domains or DEFAULT_SHORTLINK_DOMAINS
    tracking_params = tracking_params or DEFAULT_TRACKING_PARAMS
    add_query = add_query or {}

    raw_url = raw_url.strip()

    if "://" not in raw_url:
        raw_url = f"{default_scheme}://{raw_url}"

    parsed = urlparse(raw_url)

    if parsed.scheme not in ["http", "https"]:
        if allow_non_http:
            final_scheme = parsed.scheme
        else:
            final_scheme = default_scheme
            new_netloc = parsed.netloc
            new_path = parsed.path

            if not new_netloc and new_path:
                path_parts = new_path.lstrip("/").split("/", 1)
                new_netloc = path_parts[0]
                new_path = "/" + path_parts[1] if len(path_parts) > 1 else ""

            parsed = parsed._replace(
                netloc=new_netloc,
                path=new_path
            )
    else:
        final_scheme = default_scheme if not force_https else "https"

    if not parsed.netloc and parsed.path:
        parsed = parsed._replace(netloc=parsed.path, path='')

    try:
        hostname = parsed.hostname.encode("idna").decode("ascii")
    except Exception:
        hostname = parsed.hostname or ""

    if idn_format == "unicode":
        try:
            hostname = idna.decode(hostname)
        except Exception:
            pass

    netloc = hostname
    if parsed.port:
        netloc += f":{parsed.port}"

    if force_www and not hostname.startswith("www."):
        netloc = "www." + hostname

    if verbose:
        print(f"[Normalized Hostname]: {hostname}")

    if verify_dns:
        try:
            socket.gethostbyname(hostname)
        except Exception:
            return {"success": False, "error": f"Domain not resolvable: {hostname}"}

    query = parsed.query
    if remove_tracking and query:
        query_dict = dict(parse_qsl(query))
        query_dict = {k: v for k, v in query_dict.items() if k not in tracking_params}
    else:
        query_dict = dict(parse_qsl(query))

    query_dict.update(add_query)
    query = "" if remove_query_string else urlencode(query_dict)

    path = "" if clear_paths else parsed.path
    if remove_trailing_slash and path.endswith("/") and path != "/":
        path = path.rstrip("/")

    fragment = "" if strip_fragment else parsed.fragment

    domain = hostname.lower()
    if blacklist_domains and domain in blacklist_domains:
        return {"success": False, "error": f"Blocked domain: {domain}"}
    if allowlist_tlds is not None:
        tld = "." + domain.split(".")[-1] if "." in domain else ""
        if tld not in allowlist_tlds:
            return {"success": False, "error": f"Disallowed TLD: {tld}"}

    final_url = urlunparse(parsed._replace(
        scheme=final_scheme,
        netloc=netloc,
        path=path,
        query=query,
        fragment=fragment
    ))

    is_shortlink = domain in shortlink_domains

    return {
        "success": True,
        "url": final_url,
        "is_shortlink": is_shortlink,
        "parts": {
            "scheme": final_scheme,
            "netloc": netloc,
            "path": path,
            "query": query,
            "fragment": fragment,
            "original_input": raw_url
        } if output == "parts" else None
    }
