from datetime import datetime

import django
from django.db import models
from django.utils import timezone


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )

    def get_duration(self):
        current_time = django.utils.timezone.localtime(self.leaved_at).replace(microsecond=0)
        entered_time = django.utils.timezone.localtime(self.entered_at).replace(microsecond=0)
        return current_time - entered_time

    @staticmethod
    def format_duration(time):
        convert_to_str = str(time)
        convert_to_datetime = datetime.strptime(convert_to_str, '%H:%M:%S')
        time = datetime.strftime(convert_to_datetime, '%Hч %Mмин')
        return time

    def is_visit_long(self, minutes=60):
        time_in_seconds = self.get_duration().total_seconds() // 60
        return time_in_seconds > minutes
