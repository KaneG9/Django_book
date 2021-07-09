from django.core.exceptions import ValidationError
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from lists.models import Item, List
from lists.forms import ItemForm

def home_page(request):
  return render(request, 'home.html', {'form': ItemForm()})

def view_list(request, list_id):
  list_ = List.objects.get(id=list_id)
  if request.method == 'POST':  
    try:
      item = Item.objects.create(text=request.POST['item_text'], list=list_)
      item.full_clean()
      return redirect(list_)
    except ValidationError:
      item.delete()
      error = "You can't have an empty list item"
      return render(request, 'list.html', {'error': error, 'list': list_})
    
  return render(request, 'list.html', {'list': list_})

def new_list(request):
  list_ = List.objects.create()
  item = Item.objects.create(text=request.POST['item_text'], list=list_)
  try:
    item.full_clean()
  except ValidationError:
    list_.delete()
    error = "You can't have an empty list item"
    return render(request, 'home.html', {'error': error})
  return redirect(list_)
