from HoldApp.forms import ReportForm, SignUpForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from ..models.models import Case
from django.utils.timezone import datetime, timedelta

def is_admin(user):
    return user.groups.filter(name='Admin').exists()


def date_filter_queryset(queue_queryset, date_queryset, start, end):
    # get number of items in queue before end date
    queue_count = queue_queryset.filter(created_date__lt=end).count()

    # get total number of new cases in date range
    new_count = date_queryset.filter(created_date__range=[start,end]).count()

    # get number of "In Progress" cases
    nInProgressCases = queue_queryset.filter(status='P').count()

    # get number of cases completed in range
    nCompleteCases = Case.objects.filter(status='C', mod_date__range=[start, end]).all().count()


@user_passes_test(is_admin)
def metrics(request):
    # if change in start and end date
    if request.method == "POST":
        #do stuff
        # current_date_time = datetime.now()
        # start = current_date_time - timedelta(calendar.month)
        # end = datetime.now()
        return render(request, 'admin/metrics.html')

    # default start and end date, first hit
    else:
        current_date_time = datetime.now()
        start = current_date_time.replace(day=1, month=current_date_time.month-2, hour=0, minute=0, second=0,
                                          microsecond=0)
        end = current_date_time.replace(day=1, month=current_date_time.month+1, hour=0, minute=0, second=0,
                                        microsecond=0)

        # get number of cases before the start date that are still not complete
        old_queue_queryset = Case.objects.exclude(status='C').filter(created_date__lt=start).all().count()

        # get all cases that were not complete in the date range
        queue_queryset = Case.objects.exclude(status='C').filter(created_date__lt=end).all()

        # get all cases in date range
        new_queryset = Case.objects.filter(created_date__range=[start, end]).all()

        data = [
            ['Month'], ['Queue'], ['New'], ['In Progress'], ['Complete'],
        ]

        # data = []
        queue_count = []
        new_count = []
        n_queued_in_progress_cases =[]
        n_complete_cases = []

        # loop through each month in the range
        for m in range(start.month, end.month):

            start = start.replace(month=m)
            end = start.replace(month=m+1)

            data[0].append(str(start.date()))

            # get number of cases that were !complete or !in progress in the month
            data[1].append(queue_queryset.filter(date_complete__lt=end, date_in_progress__lt=end).all().count()+old_queue_queryset)

            # get number of cases added in the month
            data[2].append(new_queryset.filter(created_date__range=[start, end]).all().count())

            # get number of "In Progress" cases in queue in the month
            data[3].append(queue_queryset.filter(date_in_progress__range=[start, end]).count())

            # get number of cases completed in the month
            # TODO: fix repeated query
            data[4].append(Case.objects.filter(status='C', date_complete__range=[start, end]).all().count())

            # data_month = [str(start), queue_count, new_count, n_queued_in_progress_cases, n_complete_cases]
            #
            # data.append(data_month)

        # data = SimpleDataSource(data=data)
        # chart_metric = ColumnChart(data)  # options={'isStacked': True}
        # context = {'chart_metric': chart_metric}
        context = {'data': data}
        return render(request, 'admin/metrics.html', context)

    # data = [
    #     ['Year', 'Sales', 'Expenses'],
    #     [2004, 1000, 400],
    #     [2005, 1170, 460],
    #     [2006, 660, 1120],
    #     [2007, 1030, 540]
    # ]
    # # DataSource object
    # data_source = SimpleDataSource(data=data)
    # # Chart object
    # chart = LineChart(data_source)
    # context = {'chart': chart}
    # return render(request, 'admin/metrics.html', context)


