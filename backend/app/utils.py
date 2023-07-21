import hashlib
import re


def validate_ip_address(ip_address):
    # Regular expressions for IPv6 and IPv4 patterns
    ipv6_pattern = re.compile(r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$')
    ipv4_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')

    # Check if the IP address matches the IPv6 or IPv4 pattern
    if re.match(ipv6_pattern, ip_address):
        return 'IPv6'
    elif re.match(ipv4_pattern, ip_address):
        return 'IPv4'
    else:
        return 'Invalid'


def calculate_md5(string):
    md5_hash = hashlib.md5()
    md5_hash.update(string.encode('utf-8'))
    return md5_hash.hexdigest()


def get_client_ip(request):
    ip_observed = request.META.get('REMOTE_ADDR')
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_client = x_forwarded_for.split(',')[0]
    else:
        ip_client = ip_observed

    return ip_observed, ip_client