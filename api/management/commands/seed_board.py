from django.core.management.base import BaseCommand
from api.models import Team, TeamSelection, TeamSelectionSlot


BOARD_TITLE = "Live Team Selection Board"

TEAM_NAMES = [
    "Bobbies 1st Team",
    "Bobbies 2nd Team",
    "Bobbies 3rd Team",
    "Bobbies Seniors",
]


class Command(BaseCommand):
    help = "Seeds 4 teams + 1 live board + 23 slots per team"

    def handle(self, *args, **options):
        # Teams
        teams = []
        for name in TEAM_NAMES:
            team, _ = Team.objects.get_or_create(name=name)
            teams.append(team)

        # Live board
        board, _ = TeamSelection.objects.get_or_create(title=BOARD_TITLE)

        # Slots (23 per team)
        created = 0
        for team in teams:
            for slot_number in range(1, 24):
                _, was_created = TeamSelectionSlot.objects.get_or_create(
                    selection=board,
                    team=team,
                    slot_number=slot_number,
                    defaults={"player": None},
                )
                if was_created:
                    created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed complete: {len(teams)} teams + 1 live board + 23 slots per team (new slots: {created})"
            )
        )
