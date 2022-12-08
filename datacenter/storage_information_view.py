from django.shortcuts import render

from datacenter.models import Visit


def storage_information_view(request):
    visits = Visit.objects.all().filter(leaved_at__isnull=True)
    non_closed_visits = []
    for visit in visits:
        visits_info = {
            'who_entered': visit.passcard,
            'entered_at': visit.entered_at,
            'duration': visit.format_duration(visit.get_duration()),
        }
        non_closed_visits.append(visits_info)

    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
