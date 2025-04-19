from django.core.cache import cache
from django.db.utils import IntegrityError
from django.http import HttpRequest
from django.test import TestCase

from ..models import BlockedIP
from ..utils import (
    BLOCKLIST_CACHE_KEY,
    COOLDOWN,
    update_blocklist,
    check_blocklist,
    get_blocklist,
    remove_from_blocklist,
    user_ip_from_request,
)


class UtilsTests(TestCase):
    def setUp(self):
        cache.delete(BLOCKLIST_CACHE_KEY)

    def tearDown(self):
        cache.delete(BLOCKLIST_CACHE_KEY)

    def test_get_list(self):
        cache.set(BLOCKLIST_CACHE_KEY, ["1.1.1.1"])
        result = get_blocklist()
        self.assertEqual(result, {"1.1.1.1"})

    def test_check_blocklist(self):
        ip_set = {(ip := "9.9.9.9")}
        update_blocklist(ip_set)
        self.assertTrue(check_blocklist(ip))

    def test_update_blocklist(self):
        ips = {"2.2.2.2", "3.3.3.3"}
        update_blocklist(ips)
        result = get_blocklist()
        self.assertEqual(result, ips)

    def test_update_blocklist_defaults_and_params(self):
        update_blocklist(set(["4.4.4.4"]))
        blocked = BlockedIP.objects.get(ip="4.4.4.4")
        self.assertEqual(blocked.reason, "")
        self.assertEqual(blocked.cooldown, COOLDOWN)
        update_blocklist(
            set(["5.5.5.5"]), reason=(expected_reason := "TOS"), cooldown=(expected_cooldown := 99)
        )
        blocked = BlockedIP.objects.get(ip="5.5.5.5")
        self.assertEqual(blocked.reason, expected_reason)
        self.assertEqual(blocked.cooldown, expected_cooldown)

    def test_add_duplicate(self):
        ip = "9.9.9.9"
        update_blocklist(ip)
        try:
            update_blocklist(ip)
        except IntegrityError:
            self.fail("update_blocklist failed to handle duplicate IP")

    def test_remove(self):
        ip_as_list = ["1.1.1.1"]
        cache.set(BLOCKLIST_CACHE_KEY, ip_as_list)
        assert get_blocklist() == set(ip_as_list)
        remove_from_blocklist(ip_as_list)
        self.assertEqual(get_blocklist(refresh_cache=True), set())

    def test_get_user_ip(self):
        request = HttpRequest()
        result = user_ip_from_request(request)
        self.assertEqual(result, "")
        ip = "4.4.4.4"
        for key in ["HTTP_X_REAL_IP", "REMOTE_ADDR"]:
            request.META[key] = ip
            self.assertEqual(user_ip_from_request(request), ip)
            del request.META[key]
        request.META["HTTP_X_FORWARDED_FOR"] = "5.5.5.5,6.6.6.6"
        result = user_ip_from_request(request)
        self.assertEqual(result, "5.5.5.5")
