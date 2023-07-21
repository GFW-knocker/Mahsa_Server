import hashlib
import re

from app.models import PROTOCOL_VMESS, PROTOCOL_VLESS, PROTOCOL_TROJAN, PROTOCOL_SOCKS, PROTOCOL_SHADOWSOCKS, \
    PROTOCOL_WIREGUARD


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
    remote_addr = request.META.get('REMOTE_ADDR')
    cf_connecting_ip = request.META.get('HTTP_X_CF_CONNECTING_IP')
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    return {
        "remote_addr": remote_addr,
        "cf_connecting_ip": cf_connecting_ip,
        "forwarded_for": forwarded_for,
    }


def get_protocol(url):
    if url.startswith("vmess://"):
        return PROTOCOL_VMESS
    elif url.startswith("vless://"):
        return PROTOCOL_VLESS
    elif url.startswith("trojan://"):
        return PROTOCOL_TROJAN
    elif url.startswith("wireguard://"):
        return PROTOCOL_WIREGUARD
    elif url.startswith("ss://"):
        return PROTOCOL_SHADOWSOCKS
    elif url.startswith("socks://"):
        return PROTOCOL_SOCKS
    else:
        return None
