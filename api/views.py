from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import TeamSelection


def _can_edit(request) -> bool:
    """
    Editors are:
    - superusers
    - or users in the 'Bulletin Admin' group
    """
    user = request.user
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name="Bulletin Admin").exists()


def home(request):
    # Portal page with buttons
    return render(request, "api/home.html", {"can_edit": _can_edit(request)})


def live_board(request):
    board = TeamSelection.objects.prefetch_related(
        "slots__team",
        "slots__player",
    ).first()

    teams = []
    if board:
        # Group slots per team
        team_map = {}
        for s in board.slots.all():
            team_map.setdefault(s.team, []).append(s)

        # Sort slots within each team
        for team, slots in team_map.items():
            slots.sort(key=lambda x: x.slot_number)
            starters = [s for s in slots if 1 <= s.slot_number <= 15]
            bench = [s for s in slots if 16 <= s.slot_number <= 23]
            teams.append({"team": team, "starters": starters, "bench": bench})

        # Sort teams alphabetically
        teams.sort(key=lambda x: x["team"].name)

    return render(request, "api/live_board.html", {"board": board, "teams": teams})


@login_required
def selection_board(request):
    # This page is the "fast edit board" — only editors may access it.
    if not _can_edit(request):
        return HttpResponseForbidden("Not allowed.")
    return render(request, "api/selection.html")
