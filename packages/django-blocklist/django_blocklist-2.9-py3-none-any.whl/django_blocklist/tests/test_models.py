import datetime
import pytest
import unittest
from datetime import timezone

from ..models import BlockedIP


@pytest.mark.django_db
class DateTests(unittest.TestCase):
    def setUp(self):
        BlockedIP.objects.all().delete()
        self.ip = "1.1.1.1"

    def test_days_left(self):
        two_days_ago = datetime.datetime.now(timezone.utc) - datetime.timedelta(days=2)
        BlockedIP.objects.create(ip=self.ip, cooldown=3, last_seen=two_days_ago)
        entry = BlockedIP.objects.get(ip=self.ip)
        remaining = entry.cooldown - (datetime.datetime.now(timezone.utc) - entry.last_seen).days
        self.assertEqual(remaining, 1)

    def test_last_seen_not_auto_set(self):
        b = BlockedIP.objects.create(ip=self.ip)
        self.assertIs(b.last_seen, None)
