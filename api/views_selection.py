import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from .models import Player, TeamSelection, TeamSelectionSlot, Team


BOARD_TITLE = "Live Team Selection Board"


@ensure_csrf_cookie
def live_selection_board(request):
    board = TeamSelection.objects.get(title=BOARD_TITLE)

    players = Player.objects.order_by("last_name", "first_name")

    teams = {}
    for team in Team.objects.order_by("name"):
        slots = (
            TeamSelectionSlot.objects
            .filter(selection=board, team=team)
            .select_related("player")
            .order_by("slot_number")
        )
        teams[team.name] = list(slots)

    return render(request, "api/selection.html", {
        "players": players,
        "teams": teams,
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
