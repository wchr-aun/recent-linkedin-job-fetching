import re


def remove_subdomain(url):
    # Compile the regex pattern:
    #   - ^(https?://)    => captures the URL scheme (http:// or https://)
    #   - (?:[^./]+\.)*   => non-capturing group matching any subdomain parts ending with a dot
    #   - (?P<domain>[^./]+\.[^:/]+) => captures the base domain and TLD
    #   - (?P<port>:\d+)?  => optionally captures a port (like :8080)
    pattern = re.compile(
        r"^(https?://)"
        r"(?:[^./]+\.)*"
        r"(?P<domain>[^./]+\.[^:/]+)"
        r"(?P<port>:\d+)?"
    )

    return pattern.sub(r"\1\g<domain>\g<port>", url)
