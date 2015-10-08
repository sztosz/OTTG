from django.shortcuts import render, redirect

from .models import Item, List


def home_page(request):
    return render(request, 'home.html')


def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})


def new_list(request):
    to_do_list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], to_do_list=to_do_list)
    return redirect('/lists/the-only-list-in-the-world/')
