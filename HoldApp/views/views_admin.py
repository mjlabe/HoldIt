from HoldApp.forms import ReportForm, SignUpForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from ..models.models import Case
from django.utils.timezone import datetime, timedelta
from django.db.models import Q
import pytz


def is_admin(user):
    return user.groups.filter(name='Admin').exists()


def date_filter_queryset(start, end):
    # get all cases before the start date that are NOT COMPLETE
    past_queue_queryset = Case.objects.exclude(status='C').filter(created_date__lt=start).all()

    # Get COUNT of all cases before start date range that are NEW
    past_queue_count = past_queue_queryset.filter(status='N').all().count()

    # Get COUNT of all cases before start date range that are IN PROGRESS
    past_in_progress_count = past_queue_queryset.filter(status='P').all().count()

    # get all NEW cases in date range
    range_queryset = Case.objects.filter(created_date__range=[start, end]).all()

    data = [
        ['Date'], ['Queue'], ['New'], ['In Progress'], ['Complete'],
    ]

    # loop through each month in the range
    for m in range(start.month, end.month):
        # set range to one month
        start = start.replace(day=1, month=m)
        end = start.replace(day=1, month=m + 1)

        # add date as column header
        data[0].append(str(start.date()))

        # QUEUE
        # get number of cases that were !complete or !in progress in the month and
        data[1].append(range_queryset.filter(Q(created_date__lt=end) &
                                             ((Q(date_complete__lt=start) & Q(date_in_progress__lt=start)) |
                                              (Q(date_complete__isnull=True) & Q(date_in_progress__isnull=True)))) \
                       .all().count() + past_queue_count)

        # NEW
        # get number of cases added in the month
        data[2].append(range_queryset.filter(created_date__range=[start, end]).all().count())

        # IN PROGRESS
        # get number of "In Progress" cases in queue in the month
        data[3].append(range_queryset.filter(date_in_progress__range=[start, end]).count() + past_in_progress_count)

        # COMPLETE
        # get number of cases completed in the month
        data[4].append(range_queryset.filter(status='C', date_complete__range=[start, end]).all().count())

    return data


@user_passes_test(is_admin)
def metrics(request):

    error = {'start': '', 'end': ''}

    # default start and end date, first hit

    current_date_time = datetime.now()
    start = current_date_time.replace(day=1, month=current_date_time.month - 2, hour=0, minute=0, second=0,
                                      microsecond=0, tzinfo=pytz.UTC)
    end = current_date_time.replace(day=1, month=current_date_time.month + 1, hour=0, minute=0, second=0,
                                    microsecond=0, tzinfo=pytz.UTC)

    context = {'data': date_filter_queryset(start, end), 'start': start.strftime("%Y-%m-%d"),
               'end': end.strftime("%Y-%m-%d"), 'error': error}

    # if change in start and end date
    if request.method == "POST":

        start = datetime.strptime(request.POST.get('start', ''), '%Y-%m-%d').replace(tzinfo=pytz.UTC)
        end = datetime.strptime(request.POST.get('end', ''), '%Y-%m-%d').replace(tzinfo=pytz.UTC)

        if start < end:

            # TODO: load same data as before invalid POST
            # TODO: doesn't work before january because I'm looping just by month #

            error['start'] = ''
            error['end'] = ''

            context = {'data': date_filter_queryset(start, end), 'start': start.strftime("%Y-%m-%d"),
                       'end': end.strftime("%Y-%m-%d")}
            return render(request, 'admin/metrics.html', context)

        else:

            error['end'] = "ERROR: End Date must come after Start Date"

    return render(request, 'admin/metrics.html', context)
