from django.shortcuts import get_object_or_404
from django.shortcuts import render

from datacenter.models import Passcard
from datacenter.models import Visit


def passcard_info_view(request, passcode):
    this_passcard_visits = []
    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)

    for visit in visits:
        visit_information = {
            'entered_at': visit.entered_at,
            'duration': Visit.get_duration(visit),
            'is_strange': Visit.is_visit_long(visit)
        }
        this_passcard_visits.append(visit_information)

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
