from django.contrib import admin

from .models import (
    Player,
    Team,
    TeamSelection,
    TeamSelectionSlot,
)

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")
    search_fields = ("first_name", "last_name")


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class TeamSelectionSlotInline(admin.TabularInline):
    model = TeamSelectionSlot
    extra = 0
    autocomplete_fields = ("player", "team")
    ordering = ("team", "slot_number")


@admin.register(TeamSelection)
class TeamSelectionAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
    inlines = [TeamSelectionSlotInline]


@admin.register(TeamSelectionSlot)
class TeamSelectionSlotAdmin(admin.ModelAdmin):
    list_display = ("selection", "team", "slot_number", "player")
    list_filter = ("team", "selection")
    search_fields = ("player__first_name", "player__last_name", "team__name", "selection__title")
    autocomplete_fields = ("player", "team", "selection")
    ordering = ("selection", "team", "slot_number")
