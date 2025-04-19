from datetime import timezone
import datetime

from django.contrib.humanize.templatetags.humanize import intcomma, naturaltime
from django.db import models
from django.db.models import CharField, DateTimeField, GenericIPAddressField, IntegerField
from django.utils import timezone as utils_timezone

from .apps import Config


class BlockedIP(models.Model):
    ip = GenericIPAddressField(primary_key=True, verbose_name="IP")
    datetime_added = DateTimeField(default=utils_timezone.now, db_index=True)
    last_seen = DateTimeField(blank=True, null=True, db_index=True)
    cooldown = IntegerField(
        default=Config.defaults["cooldown"],
        help_text="Cooldown period; number of days with no connections before IP is dropped from blocklist",
    )
    reason = CharField(blank=True, max_length=255, default="", db_index=True)
    tally = IntegerField(default=0, help_text="Number of times this IP has been blocked since datetime_added")

    class Meta:
        get_latest_by = "datetime_added"
        ordering = ["-last_seen", "-datetime_added", "ip"]
        verbose_name = "blocked IP"

    def __str__(self) -> str:
        return self.ip

    def verbose_str(self):
        timespan = naturaltime(self.datetime_added).replace(" ago", "")
        return (
            f"{self.ip}"
            + f" -- {intcomma(self.tally)} blocks in {timespan}"
            + (f" -- seen {naturaltime(self.last_seen)}" if self.last_seen else "")
            + f" -- {self.cooldown} day cooldown"
            + f"{' -- ' + self.reason if self.reason else ''}"
        )

    def has_expired(self):
        """Has the IP cooled long enough to be removed from the list?"""
        quiet_time = datetime.datetime.now(timezone.utc) - (self.last_seen or self.datetime_added)
        return quiet_time.days >= self.cooldown
