from HoldApp.forms import ReportForm, DFormD, DFormF, HFormData, HFormStuff, CaseForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from HoldApp.models import DModel, DModelF, DModelD, Report, HModelData, HModelStuff, CaseD, CaseH, HModel, Case
from django.utils import timezone


def is_contributor(user):
    """Verify User is a Contributor"""

    return user.groups.filter(name='Contributor').exists() | user.groups.filter(name='Worker').exists() | \
           user.groups.filter(name='Admin').exists()


# TODO: use middleware instead of decorators
@user_passes_test(is_contributor)
def new_case(request):
    """Display the New Report form.

    This view combines the Report model and the corresponding data model. This needs to be made into an abstract class
    that can be implemented by ths specific views of different case types.
    """

    # TODO: make this an abstract class to handle every type of report
    if request.method == "POST":
        case_form = CaseForm(request.POST)
        report_form = ReportForm(request.POST)
        data_form = HFormData(request.POST)
        stuff_form = HFormStuff(request.POST)

        if report_form.is_valid() and data_form.is_valid() and stuff_form.is_valid():
            case = case_form.save()
            report = report_form.save()

            hmodeldata, fcreated = HModelData.objects.get_or_create(**data_form.cleaned_data)
            hmodelstuff, dcreated = HModelStuff.objects.get_or_create(**stuff_form.cleaned_data)
            hmodel, dmodelcreated = HModel.objects.get_or_create(data=hmodeldata, stuff=hmodelstuff)

            CaseH.objects.create(report=report, case=case, hmodel=hmodel)

            return redirect('case_list')

    else:
        case_form = CaseForm()
        report_form = ReportForm()
        data_form = HFormData()
        stuff_form = HFormStuff()

    return render(request, "contributor/new_report.html", {'case_form': case_form, 'report_form': report_form,
                                                           'data_form': data_form, 'stuff_form': stuff_form, })


# TODO: ERROR! UNIQUE constraint failed
# TODO: if statement to load specific case type
@user_passes_test(is_contributor)
def case_edit(request, pk):
    case = get_object_or_404(Case, pk=pk)
    report = CaseH.objects.get(case=case).report
    data = CaseH.objects.get(case=case).hmodel.data
    stuff = CaseH.objects.get(case=case).hmodel.stuff

    if request.method == "POST":
        case_form = CaseForm(request.POST, instance=case)
        report_form = ReportForm(request.POST, instance=report)
        data_form = HFormData(request.POST, instance=data)
        stuff_form = HFormStuff(request.POST, instance=stuff)

        if case_form.is_valid() and report_form.is_valid() and data_form.is_valid() and stuff_form.is_valid():
            case.mod_date = timezone.now
            Case.objects.update(**case_form.cleaned_data)
            Report.objects.update(**report_form.cleaned_data)

            hmodeldata, fcreated = HModelData.objects.get_or_create(**data_form.cleaned_data)
            hmodelstuff, dcreated = HModelStuff.objects.get_or_create(**stuff_form.cleaned_data)
            hmodel, dmodelcreated = HModel.objects.get_or_create(data=hmodeldata, stuff=hmodelstuff)

            CaseH.objects.update(report=report, case=case, hmodel=hmodel)

            return redirect('case_list')

    else:
        case_form = CaseForm(instance=case)
        report_form = ReportForm(instance=report)
        data_form = HFormData(instance=data)
        stuff_form = HFormStuff(instance=stuff)

    return render(request, "contributor/new_report.html", {'case_form': case_form, 'report_form': report_form,
                                                              'data_form': data_form, 'stuff_form': stuff_form})


@user_passes_test(is_contributor)
def caseD_edit(request, pk):
    """Display the New Report form.

    This view combines the Report model and the corresponding data model. This needs to be made into an abstract class
    that can be implemented by ths specific views of different case types.
    """

    # TODO: make this an abstract class to handle every type of report
    report = get_object_or_404(Report, pk=pk)
    # TODO: NOT WORKING!!!!
    dval = get_object_or_404(DModelD, pk=DModel.objects.get(report=report.id))
    fval = get_object_or_404(DModelF, pk=DModel.objects.get(report=report.id))
    if request.method == "POST":
        report_form = ReportForm(request.POST, instance=report)
        dval_form = DFormD(request.POST, instance=dval)
        fval_form = DFormF(request.POST, instance=fval)

        if report_form.is_valid() and dval_form.is_valid() and fval_form.is_valid():
            report.mod_date = timezone.now
            report = report_form.save()

            fval, fcreated = DModelF.objects.get_or_create(**fval_form.cleaned_data)
            dval, dcreated = DModelD.objects.get_or_create(**dval_form.cleaned_data)

            DModel.objects.update(dval=dval, fval=fval, report=report)

            return redirect('report_list')

    else:
        report_form = ReportForm(instance=report)
        dval_form = DFormD(instance=dval)
        fval_form = DFormF(instance=fval)

    return render(request, "contributor/new_Genreport.html", {'report_form': report_form, 'dval_form': dval_form,
                                                              'fval_form': fval_form})


@user_passes_test(is_contributor)
def new_Dcase(request):
    """Display the New Report form.

    This view combines the Report model and the corresponding data model. This needs to be made into an abstract class
    that can be implemented by ths specific views of different case types.
    """

    # TODO: make this an abstract class to handle every type of report
    if request.method == "POST":
        case_form = CaseForm(request.POST)
        report_form = ReportForm(request.POST)
        dval_form = DFormD(request.POST)
        fval_form = DFormF(request.POST)

        if case_form.is_valid() and report_form.is_valid() and dval_form.is_valid() and fval_form.is_valid():
            case = case_form.save()
            report = report_form.save()

            dmodelf, fcreated = DModelF.objects.get_or_create(**fval_form.cleaned_data)
            dmodeld, dcreated = DModelD.objects.get_or_create(**dval_form.cleaned_data)
            dmodel, dmodelcreated = DModel.objects.get_or_create(fval=dmodelf, dval=dmodeld)

            CaseD.objects.create(report=report, case=case, dmodel=dmodel)

            return redirect('case_list')

    else:
        case_form = CaseForm()
        report_form = ReportForm()
        dval_form = DFormD()
        fval_form = DFormF()

    return render(request, "contributor/new_Genreport.html", {'case_form': case_form, 'report_form': report_form, 'dval_form': dval_form,
                                                              'fval_form': fval_form})
