import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from .models import Vote
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

# Load menu from a JSON file
with open('voting/lunch_menus.json') as f:
    LUNCH_MENUS = json.load(f)

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

    if request.method == "POST":
        menu_item = request.POST.get("menu_item")
        if not user_has_voted:
            # Save the user's vote
            Vote.objects.create(user=request.user, menu_item=menu_item)
            
            # Update vote count in the JSON file
            votes = load_votes()
            if menu_item in votes:
                votes[menu_item] += 1
            else:
                votes[menu_item] = 1
            save_votes(votes)

            return JsonResponse({"status": "success", "votes": votes})

    votes = load_votes() if user_has_voted else None
    return render(request, 'voting/lunch_menu.html', {"menus": LUNCH_MENUS, "votes": votes, "user_has_voted": user_has_voted})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log the user in after successful registration
            login(request, user)
            return redirect('lunch_menu')  # Redirect to the voting page after login
    else:
        form = CustomUserCreationForm()
    return render(request, 'voting/register.html', {'form': form})