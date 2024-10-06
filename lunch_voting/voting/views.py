import json
import os
from typing import List
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from .models import Vote
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth import logout

from openai import OpenAI

with open("openai-token.txt", "r") as f:
    OPENAI_TOKEN = f.read().strip()
    os.environ["OPENAI_API_KEY"] = OPENAI_TOKEN

OPENAI_CLIENT = OpenAI()

def get_best_food(foods : List[str]) -> str:
    response = OPENAI_CLIENT.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a food critic and you are evaluating which food is the best. You have tasted all of them, and now it's time to choose the best option. Respond briefly."},
            {"role": "user", "content": f"Choose from the following: {', '.join(foods)}"}
        ],
    )
    print(f"Response: {response}")
    response = str(response.choices[0].message.content)
    return response


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

    # Update vote count in the JSON file
    votes = load_votes()

    chat_gpt_recommendation = get_best_food([rest + ": " + fdata[0] for rest, fdata in votes.items() if len(fdata) > 3])

    # After the user has voted, the page will display the vote counts
    if request.method == "POST":
        # The user submits a vote, that gives a single vote (1-5) to one of the restaurants
        restaurants = votes.keys()
        # Get the given ratings for each restaurant
        print(f"Restaurants: {restaurants}")
        print(f"POST: {request.POST}")
        ratings = {}
        for restaurant in restaurants:
            try:
                print(f"Rating: {request.POST.get(f'{restaurant}_rating')}")
                rating = int(request.POST.get(f"{restaurant}_rating"))
            except:
                print(f"Rating not found for {restaurant}")
                rating = 0
            ratings[restaurant] = rating

        print(f"Ratings: {ratings}")

        if True:
            # Save the user's vote
            # Vote.objects.create(user=request.user, menu_item=ratings)
            
            # {"r1" : [food, ratings_sum, count], "r2" : [food, ratings_sum, count]}
            # Update all restaurants whose rating != 0
            for restaurant, rating in ratings.items():
                if rating != 0:
                    votes[restaurant][1] += rating
                    votes[restaurant][2] += 1
                    # update the average rating
                    if len(votes[restaurant]) == 3:
                        votes[restaurant].append(rating)
                    else:
                        votes[restaurant][3] = round(votes[restaurant][1] / votes[restaurant][2], 1)
            save_votes(votes)

            return JsonResponse({"status": "success", "votes": votes, "chat_gpt_recommendation": chat_gpt_recommendation})

    votes = load_votes()
    print(f"Votes: {votes}")
    return render(request, 'voting/lunch_menu.html', {"votes": votes, "user_has_voted": user_has_voted, "username": request.user.username, "chat_gpt_recommendation": chat_gpt_recommendation})

def logout_view(request):
    logout(request)
    print(f"Logged out user")
    return redirect('lunch_menu')


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