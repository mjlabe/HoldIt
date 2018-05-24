from HoldApp.forms import SignUpForm, GroupChoiceForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect


def index(request):
    return render(request, 'public/index.html')


def header(request):
    return render(request, 'base/header.html')


def footer(request):
    return render(request, 'base/footer.html')


def success(request):
    return render(request, 'registration\signup_success.html')


def signup(request):
    """Display the signup form.

    This view uses the User model and GroupRequest model to save a new User, so that the access (Group) requested is
    associated with the user. It automatically logs in the user after the user signs up and redirects them to the
    success page. It is possible to make the new account inactive by default (this could be used instead of the "User"
    privilege for example) and the code to do that is commented out below.
    """

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        group_form = GroupChoiceForm(request.POST)

        # TODO: notify user when an incorrect password is entered and limit number of tries
        if form.is_valid():
            # uncomment the code below to make the new account inactive until an admin approves
            # user = form.save(commit=False)
            # user.is_active = False
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            group = group_form.save(commit=False)
            group.user = user
            group.save()

            login(request, user)
            return redirect('success')

    else:
        form = SignUpForm()
        group_form = GroupChoiceForm()

    return render(request, 'registration\signup.html', {'form': form, 'group_form': group_form, })
