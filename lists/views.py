from django.shortcuts import render, redirect

from .models import Item, List


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    to_do_list = List.objects.get(id=list_id)
    return render(request, 'list.html', {'to_do_list': to_do_list})


def new_list(request):
    to_do_list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], to_do_list=to_do_list)
    return redirect('/lists/{}/'.format(to_do_list.id))


def add_item(request, list_id):
    to_do_list = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], to_do_list=to_do_list)
    return redirect('/lists/{}/'.format(to_do_list.id))
