from django.db import models


class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    id_number = models.CharField(max_length=20, blank=True, default="")
    phone_number = models.CharField(max_length=20, blank=True, default="")

    available = models.BooleanField(default=True)
    injured = models.BooleanField(default=False)
    fees_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class TeamSelection(models.Model):
    """
    One “live board”. We keep it simple: one row that represents the current board.
    """
    title = models.CharField(max_length=120, default="Live Team Selection Board")

    def __str__(self):
        return self.title


class TeamSelectionSlot(models.Model):
    """
    A slot is a row like: (board, team, slot_number, player)
    slot_number is 1..23 per team.
    """
    selection = models.ForeignKey(TeamSelection, on_delete=models.CASCADE, related_name="slots")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="slots")
    slot_number = models.PositiveIntegerField()
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ("selection", "team", "slot_number")
        ordering = ["team__name", "slot_number"]

    def __str__(self):
        p = self.player or "-"
        return f"{self.selection} | {self.team} | {self.slot_number} | {p}"
