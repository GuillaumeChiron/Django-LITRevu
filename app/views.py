from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator

from app.models import Ticket, Review, UserFollow
from app.forms import TicketForm, ReviewForm
from authentication.models import User

from itertools import chain


# Affichage des posts sur le flux personnalisé
@login_required
def home_page(request):
    # Stock tous les tickets de l'utilisateur et de ses abonnements
    tickets = Ticket.objects.filter(
        Q(user=request.user) | Q(user__followed_by__user=request.user)
    ).distinct()

    # Stock toutes les reviews de l'utilisateur et de ses abonnements
    # Stock également les reviews liées au ticket de l'utilisateur
    reviews = Review.objects.filter(
        Q(ticket__user=request.user)
        | Q(user=request.user)
        | Q(user__followed_by__user=request.user)
    ).distinct()

    reviewed_ticket_ids = (
        Review.objects.all().values_list("ticket_id", flat=True).distinct()
    )

    # Tri les posts de façon antéchronoligique
    posts = sorted(
        chain(tickets, reviews),
        key=lambda x: x.time_created,
        reverse=True,
    )

    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_posts = paginator.get_page(page_number)

    context = {"page_posts": page_posts, "reviewed_ticket_ids": reviewed_ticket_ids}
    return render(request, "app/home_page.html", context=context)


# Affichage des posts de l'utilisateur concerné
@login_required
def post_page(request):
    # Stock les tickets de l'utilisteur
    # Stock les reviews de l'utilisateur et celles lié aux tickets de l'utilisateur
    tickets = Ticket.objects.filter(user=request.user).distinct()
    reviews = Review.objects.filter(
        Q(ticket__user=request.user) | Q(user=request.user)
    ).distinct()
    reviewed_ticket_ids = (
        Review.objects.all().values_list("ticket_id", flat=True).distinct()
    )

    # Tri les posts de façon antéchronologique
    posts = sorted(
        chain(tickets, reviews),
        key=lambda x: x.time_created,
        reverse=True,
    )

    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_posts = paginator.get_page(page_number)

    context = {"page_posts": page_posts, "reviewed_ticket_ids": reviewed_ticket_ids}

    return render(request, "app/post_page.html", context=context)


# Mise en place d'un forulaire pour la création d'un ticket
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


# Mise en place d'un formulaire pour la création d'une review
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


# Mise en place d'un double formulaire pour créer un ticket et une review en une seule fois
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


# Possiblité de modifier un ticket
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


# Possibilité de supprimer un ticket
@login_required
def delete_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    if request.method == "POST":
        ticket.delete()
        return redirect("home-page")
    return render(request, "app/delete_ticket.html", {"ticket": ticket})


# Possibilité de modifier une review
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


# Possiblité de supprimer une review
@login_required
def delete_review(request, id):
    review = get_object_or_404(Review, id=id)
    if request.method == "POST":
        review.delete()
        return redirect("home-page")
    return render(request, "app/delete_review.html", {"review": review})


# Page de suivi (recherche, abonnements et abonnés)
@login_required
def dashboard_follow(request):
    query = request.GET.get("recherche")

    users = []
    users_follows = {}
    # Stock tous les abonnements de l'utilisateur
    following = UserFollow.objects.filter(user=request.user).select_related(
        "followed_user"
    )
    # Stock tous les les abonnés de l'utilisateur
    followers = UserFollow.objects.filter(followed_user=request.user).select_related(
        "user"
    )
    # Stock dans users les personnes recherchées
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


# Permet de suivre un utilisateur
@login_required
def follow_user(request, id):
    user_to_follow = get_object_or_404(User, id=id)

    if request.user != user_to_follow:
        UserFollow.objects.create(user=request.user, followed_user=user_to_follow)
        return redirect("dashboard-follow")


# Permet de ne plus suivre un utilisateur
@login_required
def unfollow_user(request, id):
    if request.method == "POST":
        user_to_unfollow = get_object_or_404(User, id=id)

        UserFollow.objects.filter(
            user=request.user, followed_user=user_to_unfollow
        ).delete()
        return redirect("dashboard-follow")
