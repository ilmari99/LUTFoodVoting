import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from .models import Vote
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth import logout


# Load vote counts from JSON file
def load_votes():
    with open('voting/votes.json', 'r') as f:
        return json.load(f)

def save_votes(votes):
    with open('voting/votes.json', 'w') as f:
        json.dump(votes, f)

@login_required
def lunch_menu_view(request):
    today = timezone.now().date()
    user_has_voted = Vote.objects.filter(user=request.user, date=today).exists()

    # After the user has voted, the page will display the vote counts
    if request.method == "POST":
        menu_item = request.POST.get("menu_item")

        if True:
            # Save the user's vote
            #Vote.objects.create(user=request.user, menu_item=menu_item)
            
            # Update vote count in the JSON file
            votes = load_votes()
            if menu_item in votes:
                votes[menu_item] += 1
            else:
                votes[menu_item] = 1
            save_votes(votes)

            return JsonResponse({"status": "success", "votes": votes})

    votes = load_votes()
    return render(request, 'voting/lunch_menu.html', {"votes": votes, "user_has_voted": user_has_voted, "username": request.user.username})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout


def register_view(request):
    error_message = None
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log the user in after successful registration
            login(request, user)
            print(f"User {user.username} has registered successfully")
            return redirect('lunch_menu')  # Redirect to the voting page after login
        else:
            error_message = "There was an error with your registration. Please check the form and try again."
    else:
        form = CustomUserCreationForm()
    return render(request, 'voting/register.html', {'form': form, 'error_message': error_message})