from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile, ChatMessage


@require_http_methods(["GET", "POST"])
@csrf_protect
def login_view(request):
    """Custom login page; staff users only."""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("dashboard_index")
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        if user.is_staff:
            login(request, user)
            return redirect(request.GET.get("next") or "dashboard_index")
        form.add_error(None, "Staff access required.")
    return render(request, "login.html", {"form": form})


@require_http_methods(["GET", "POST"])
def logout_view(request):
    logout(request)
    return redirect("login")


@staff_member_required
def dashboard_index(request):
    """List all users with last login and Gemini API key (from shared DB)."""
    users = User.objects.all().order_by("-last_login")
    profile_by_user_id = {p.user_id: p for p in UserProfile.objects.all()}
    rows = [
        {"user": u, "profile": profile_by_user_id.get(u.id)}
        for u in users
    ]
    return render(request, "dashboard/index.html", {"rows": rows})


@staff_member_required
def chat_history(request, username=None):
    """List user prompts. If username is given (URL or query), show only that user's chat history."""
    # username can come from URL path (e.g. /chat-history/john/) or query (?username=john)
    username = username or request.GET.get("username", "").strip()
    user_messages = (
        ChatMessage.objects.filter(role="user")
        .select_related("session", "session__user")
        .order_by("-timestamp")
    )
    if username:
        user_messages = user_messages.filter(session__user__username__iexact=username)
    # Users who have at least one user message (for "View as" switcher)
    users_with_chat = (
        User.objects.filter(
            id__in=ChatMessage.objects.filter(role="user").values_list("session__user_id", flat=True).distinct()
        )
        .order_by("username")
        .values_list("username", flat=True)
    )
    return render(
        request,
        "dashboard/chat_history.html",
        {
            "user_messages": user_messages,
            "filter_username": username,
            "users_with_chat": list(users_with_chat),
        },
    )
