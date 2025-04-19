from datetime import timezone
import datetime
import logging

from django.conf import settings
from django.http import HttpResponseBadRequest

from .apps import Config
from .models import BlockedIP
from .utils import get_blocklist, user_ip_from_request


logger = logging.getLogger(__name__)


def denial_template():
    return settings.BLOCKLIST_CONFIG.get("denial-template") or Config.defaults["denial-template"]


class BlocklistMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DEBUG:
            return self.get_response(request)
        elif user_ip_from_request(request) in get_blocklist():
            try:
                entry = BlockedIP.objects.get(ip=user_ip_from_request(request))
            except BlockedIP.DoesNotExist:
                # IP was in cache but not in DB, so don't block
                return self.get_response(request)
            logger.warning("{} request blocked from {}".format(request.method, entry.ip))
            entry.last_seen = datetime.datetime.now(timezone.utc)
            entry.tally += 1
            entry.save()
            return HttpResponseBadRequest(denial_template().format(ip=entry.ip, cooldown=entry.cooldown))
        else:
            return self.get_response(request)
