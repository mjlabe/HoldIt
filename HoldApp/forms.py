from django import forms
from HoldApp.models import Report, Case, HModelData, HModelStuff, GroupRequest, DModelF, DModelD
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ('title', 'summary')


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('reporttitle', 'pdf', )


class HFormData(forms.ModelForm):
    class Meta:
        model = HModelData
        fields = ('data1', 'data2', 'data3', )


class HFormStuff(forms.ModelForm):
    class Meta:
        model = HModelStuff
        fields = ('stuff1', 'stuff2', 'stuff3', )


class DFormF(forms.ModelForm):
    class Meta:
        model = DModelF
        fields = ('fval', )


class DFormD(forms.ModelForm):
    class Meta:
        model = DModelD
        fields = ('dval', )


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class GroupChoiceForm(forms.ModelForm):
    class Meta:
        model = GroupRequest
        fields = ('group', )
