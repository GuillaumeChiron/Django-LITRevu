from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from app.models import Ticket, Review, UserFollow
from app.forms import TicketForm, ReviewForm
from authentication.models import User


@login_required
def home_page(request):
    tickets = Ticket.objects.all().order_by("-time_created")
    reviews = Review.objects.all().order_by("-time_created")
    return render(
        request, "app/home_page.html", {"tickets": tickets, "reviews": reviews}
    )


@login_required
def create_ticket(request):
    form = TicketForm()
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("home-page")
    return render(request, "app/create_ticket.html", {"form": form})


@login_required
def create_review(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    form = ReviewForm()
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("home-page")
    return render(request, "app/create_review.html", {"form": form, "ticket": ticket})


@login_required
def create_ticket_review(request):
    ticket_form = TicketForm()
    review_form = ReviewForm()
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("home-page")
    return render(
        request,
        "app/create_ticket_review.html",
        {"ticket_form": ticket_form, "review_form": review_form},
    )


@login_required
def edit_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    ticket_form = TicketForm(instance=ticket)
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES, instance=ticket)
        if ticket_form.is_valid():
            ticket_form.save()
            return redirect("home-page")
    return render(
        request, "app/edit_ticket.html", {"ticket_form": ticket_form, "ticket": ticket}
    )


@login_required
def delete_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    if request.method == "POST":
        ticket.delete()
        return redirect("home-page")
    return render(request, "app/delete_ticket.html", {"ticket": ticket})


@login_required
def edit_review(request, id):
    review = get_object_or_404(Review, id=id)
    review_form = ReviewForm(instance=review)
    if request.method == "POST":
        review_form = ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review_form.save()
            return redirect("home-page")
    return render(
        request, "app/edit_review.html", {"review_form": review_form, "review": review}
    )


@login_required
def delete_review(request, id):
    review = get_object_or_404(Review, id=id)
    if request.method == "POST":
        review.delete()
        return redirect("home-page")
    return render(request, "app/delete_review.html", {"review": review})


@login_required
def dashboard_follow(request):
    query = request.GET.get("recherche")

    users = []
    users_follows = {}

    following = UserFollow.objects.filter(user=request.user).select_related(
        "followed_user"
    )

    followers = UserFollow.objects.filter(followed_user=request.user).select_related(
        "user"
    )

    if query:
        users = User.objects.filter(username__icontains=query).exclude(
            id=request.user.id
        )
        followed_users_ids = UserFollow.objects.filter(user=request.user).values_list(
            "followed_user_id", flat=True
        )
        for user in users:
            users_follows = {user.username: user.id in followed_users_ids}

    return render(
        request,
        "app/dashboard_follow.html",
        {
            "query": query,
            "users": users,
            "users_follows": users_follows,
            "following": following,
            "followers": followers,
        },
    )


@login_required
def follow_user(request, id):
    user_to_follow = get_object_or_404(User, id=id)

    if request.user != user_to_follow:
        UserFollow.objects.create(user=request.user, followed_user=user_to_follow)
        return redirect("dashboard-follow")


@login_required
def unfollow_user(request, id):
    if request.method == "POST":
        user_to_unfollow = get_object_or_404(User, id=id)

        UserFollow.objects.filter(
            user=request.user, followed_user=user_to_unfollow
        ).delete()
        return redirect("dashboard-follow")
