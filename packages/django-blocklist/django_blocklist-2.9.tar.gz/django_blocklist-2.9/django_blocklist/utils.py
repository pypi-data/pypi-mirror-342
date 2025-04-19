import logging
from datetime import datetime
from typing import Optional

from django.conf import settings
from django.core.cache import cache
from django.http import HttpRequest

from .apps import Config
from .models import BlockedIP


logger = logging.getLogger(__name__)
BLOCKLIST_CACHE_KEY = "django-blocklist-ips"
CACHE_TTL = settings.BLOCKLIST_CONFIG.get("cache-ttl", Config.defaults["cache-ttl"])
COOLDOWN = settings.BLOCKLIST_CONFIG.get("cooldown", Config.defaults["cooldown"])


def user_ip_from_request(request: HttpRequest) -> str:
    """Returns user's IP. If IP can't be determined, return empty string and log a warning."""
    keys = ["HTTP_X_REAL_IP", "REMOTE_ADDR"]
    for key in keys:
        if ip := request.META.get(key):
            return ip
    # `HTTP_X_FORWARDED_FOR` is a comma-separated list with originating IP first
    if forwarded := request.META.get("HTTP_X_FORWARDED_FOR"):
        return forwarded.split(",")[0]
    logger.warning("No IP address could be found on request: {}".format(request.META))
    return ""


def get_blocklist(refresh_cache: bool = False) -> set:
    """Read the blocklist from cache and return it as a set. Read from database if cache is expired or `refresh_cache` is True."""
    blocked_ips = cache.get(BLOCKLIST_CACHE_KEY)
    if blocked_ips is None or refresh_cache is True:
        blocked_ips = set(o.ip for o in BlockedIP.objects.all())
        cache.set(BLOCKLIST_CACHE_KEY, list(blocked_ips), CACHE_TTL)
        logger.info(f"Read {len(blocked_ips)} IPs from blocklist storage; cached.")
    return set(blocked_ips)


def check_blocklist(ip: str) -> bool:
    return ip in get_blocklist()


def update_blocklist(ips: set, reason="", cooldown: Optional[int] = None, last_seen: Optional[datetime] = None) -> None:
    """
    Add the provided IPs to the blocklist, with optional `reason` and `cooldown`.
    Refreshes the cache when complete.
    """
    if cooldown is None:
        cooldown = COOLDOWN
    for ip in ips:
        entry, new = BlockedIP.objects.get_or_create(ip=ip)
        entry.reason = reason
        entry.cooldown = cooldown
        entry.last_seen = last_seen
        entry.save()
        if new:
            logger.info(f"Added blocklist entry: {ip}, {reason=} {cooldown=}")
        else:
            logger.info(f"Updated blocklist entry for {ip}: {reason=} {cooldown=}")
    # Update cache
    get_blocklist(refresh_cache=True)


def remove_from_blocklist(ip: str) -> bool:
    """Remove the IP from the blocklist. Return True if successful, False if it wasn't found."""
    try:
        BlockedIP.objects.get(ip=ip).delete()
        # Ensure cached blocklist is up to date
        get_blocklist(refresh_cache=True)
        return True
    except BlockedIP.DoesNotExist:
        logger.warning(f"Removal of {ip} requested, but not found in blocklist.")
        return False
