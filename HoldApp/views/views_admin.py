from HoldApp.forms import ReportForm, SignUpForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def is_admin(user):
    return user.groups.filter(name='Admin').exists()



