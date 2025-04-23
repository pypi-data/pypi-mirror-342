
""" 
linkfixer.py

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
    base_domain: str = None,
    default_scheme: str = "https",
    force_https: bool = False,
    force_www: bool = False,
    remove_tracking: bool = True,
    remove_query_string: bool = False,
    clear_paths: bool = False,
    remove_trailing_slash: bool = False,
    strip_fragment: bool = False,
    add_query: dict = None,
    output: str = "url",
    allow_non_http: bool = True,
    blacklist_domains: set = None,
    allowlist_tlds: set = None,
    shortlink_domains: set = None,
    tracking_params: set = None,
    idn_format: str = "punycode",
    verify_dns: bool = False,
    verbose: bool = False
) -> dict:
    blacklist_domains = blacklist_domains or set()
    shortlink_domains = shortlink_domains or DEFAULT_SHORTLINK_DOMAINS
    tracking_params = tracking_params or DEFAULT_TRACKING_PARAMS
    add_query = add_query or {}

    raw_url = raw_url.strip()
    orginal_raw_url = raw_url

    # Step 1: Prepend scheme if missing to aid parsing
    if not raw_url.startswith(("http://", "https://")):
        raw_url = f"{default_scheme}://{raw_url}"

    parsed_raw = urlparse(raw_url)

    # Step 2: If raw_url doesn't contain a hostname, check base_domain
    if not parsed_raw.hostname:
        if not base_domain:
            return {
                "success": False,
                "error": "Missing domain — please provide a valid raw_url or base_domain"
            }
        if not base_domain.startswith(("http://", "https://")):
            base_domain = f"{default_scheme}://{base_domain}"
        parsed_base = urlparse(base_domain)

        if not parsed_base.hostname:
            return {
                "success": False,
                "error": "Base domain is invalid — missing hostname"
            }

        # Attach base domain host to relative raw_url
        joined_url = f"{parsed_base.scheme}://{parsed_base.netloc.rstrip('/')}/{orginal_raw_url.lstrip('/')}"
        parsed = urlparse(joined_url)
    else:
        parsed = parsed_raw

    # Final scheme logic
    if parsed.scheme not in ["http", "https"]:
        if allow_non_http:
            final_scheme = parsed.scheme
        else:
            final_scheme = default_scheme
    else:
        final_scheme = "https" if force_https else parsed.scheme

    # Normalize hostname
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

    if verify_dns:
        try:
            socket.gethostbyname(hostname)
        except Exception:
            return {"success": False, "error": f"Domain not resolvable: {hostname}"}

    # Query parameters
    query_dict = dict(parse_qsl(parsed.query))
    if remove_tracking:
        query_dict = {k: v for k, v in query_dict.items() if k not in tracking_params}
    query_dict.update(add_query or {})
    query = "" if remove_query_string else urlencode(query_dict)

    # Path and fragments
    path = "" if clear_paths else parsed.path
    if remove_trailing_slash and path.endswith("/") and path != "/":
        path = path.rstrip("/")
    fragment = "" if strip_fragment else parsed.fragment

    # Domain validation
    domain = hostname.lower()
    if blacklist_domains and domain in blacklist_domains:
        return {"success": False, "error": f"Blocked domain: {domain}"}
    if allowlist_tlds is not None:
        tld = "." + domain.split(".")[-1] if "." in domain else ""
        if tld not in allowlist_tlds:
            return {"success": False, "error": f"Disallowed TLD: {tld}"}

    # Final assembly
    final_url = urlunparse(parsed._replace(
        scheme=final_scheme,
        netloc=netloc,
        path=path,
        query=query,
        fragment=fragment
    ))

    return {
        "success": True,
        "url": final_url,
        "is_shortlink": domain in shortlink_domains,
        "parts": {
            "scheme": final_scheme,
            "netloc": netloc,
            "path": path,
            "query": query,
            "fragment": fragment,
            "original_input": raw_url
        } if output == "parts" else None
    }