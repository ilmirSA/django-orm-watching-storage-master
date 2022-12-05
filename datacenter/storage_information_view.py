from django.shortcuts import render

from datacenter.models import Visit


def storage_information_view(request):
    visits = Visit.objects.all().filter(leaved_at=None)
    non_closed_visits = []
    for visit in visits:
        visits_info = {
            'who_entered': visit.passcard,
            'entered_at': visit.entered_at,
            'duration': Visit.format_duration(Visit.get_duration(visit)),
        }
        non_closed_visits.append(visits_info)

    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
