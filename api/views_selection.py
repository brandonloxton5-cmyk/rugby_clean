import json

from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.db.models import Value, IntegerField
from django.db.models.functions import Coalesce

from .models import Player, TeamSelection, TeamSelectionSlot, Team


BOARD_TITLE = "Live Team Selection Board"


@ensure_csrf_cookie
def live_selection_board(request):
    # Get the live board
    board = TeamSelection.objects.get(title=BOARD_TITLE)

    # Sorting:
    # - sort=name  -> last_name, first_name
    # - sort=pos   -> pref_pos1 (players with no pref_pos1 go to the bottom)
    sort = request.GET.get("sort", "name")  # "name" or "pos"

    players = Player.objects.all()
    if sort == "pos":
        players = players.annotate(
            sort_pos=Coalesce("pref_pos1", Value(999), output_field=IntegerField())
        ).order_by("sort_pos", "last_name", "first_name")
    else:
        players = players.order_by("last_name", "first_name")

    # Build teams + slots
    teams = {}
    for team in Team.objects.order_by("name"):
        slots = (
            TeamSelectionSlot.objects
            .filter(selection=board, team=team)
            .select_related("player")
            .order_by("slot_number")
        )
        teams[team.name] = list(slots)

    # Render
    return render(request, "api/selection.html", {
        "players": players,
        "teams": teams,
        "sort": sort,
        "board_title": BOARD_TITLE,
    })


@require_POST
def assign_player(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
        player_id = int(payload["player_id"])
        team_name = payload["team_name"]
        slot_number = int(payload["slot_number"])
    except Exception:
        return HttpResponseBadRequest("Bad JSON payload")

    board = TeamSelection.objects.get(title=BOARD_TITLE)
    team = Team.objects.get(name=team_name)
    player = Player.objects.get(id=player_id)

    slot = TeamSelectionSlot.objects.get(
        selection=board, team=team, slot_number=slot_number
    )
    slot.player = player
    slot.save()

    return JsonResponse({"ok": True})


@require_POST
def clear_slot(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
        slot_id = int(payload["slot_id"])
    except Exception:
        return HttpResponseBadRequest("Bad JSON payload")

    slot = TeamSelectionSlot.objects.get(id=slot_id)
    slot.player = None
    slot.save()

    return JsonResponse({"ok": True})
