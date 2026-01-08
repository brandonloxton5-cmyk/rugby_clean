from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import BulletinItem

BULLETIN_ADMIN_GROUP = "Bulletin Admin"


def is_bulletin_admin(user) -> bool:
    return user.is_authenticated and (
        user.is_superuser or user.groups.filter(name=BULLETIN_ADMIN_GROUP).exists()
    )


def board(request):
    # show open + done (latest first)
    items = BulletinItem.objects.all().order_by("-created_at")
    return render(request, "bulletin/board.html", {
        "items": items,
        "can_edit": is_bulletin_admin(request.user),
    })


@login_required
def add_item(request):
    if not is_bulletin_admin(request.user):
        return HttpResponseForbidden("Not allowed.")
    if request.method == "POST":
        # template sends name="title"
        text = (request.POST.get("title") or "").strip()
        if text:
            BulletinItem.objects.create(text=text[:280], created_by=request.user)
    return redirect("bulletin:board")


@login_required
def mark_done(request, pk: int):
    if not is_bulletin_admin(request.user):
        return HttpResponseForbidden("Not allowed.")
    if request.method == "POST":
        item = get_object_or_404(BulletinItem, pk=pk)
        item.is_done = True
        item.save(update_fields=["is_done"])
    return redirect("bulletin:board")


@login_required
def delete_item(request, pk: int):
    if not is_bulletin_admin(request.user):
        return HttpResponseForbidden("Not allowed.")
    if request.method == "POST":
        item = get_object_or_404(BulletinItem, pk=pk)
        item.delete()
    return redirect("bulletin:board")
