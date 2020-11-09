from django.shortcuts import render, redirect

from main_app.forms import ItemForm, CommentForm
from main_app.models import Item, Like, Comment


# Create your views here.
def landing_page(request):
    return render(request, 'landing_page.html')


def list_items(request):
    context = {
        'items': Item.objects.all(),
    }

    return render(request, 'items/item_list.html', context)


def details_or_comment_item(request, pk):
    item = Item.objects.get(pk=pk)
    if request.method == 'GET':
        context = dict(item=item, form=CommentForm(), like=Like.objects.filter(item_id=pk).exists())

        return render(request, 'items/item_detail.html', context)
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            # comment = Comment(comment=form.cleaned_data['text'])      # Pure Form class used
            comment = Comment(comment=form.cleaned_data['comment'])  # ModelForm class used
            comment.item = item  # Attach ForeignKey
            comment.save()
            return redirect('item details or comment', pk)
        context = {
            'item': item,
            'form': form,
        }

        return render(request, 'items/item_detail.html', context)


def like_item(request, pk):
    item = Item.objects.get(pk=pk)
    if Like.objects.filter(item_id=pk).exists():
        Like.objects.filter(item_id=pk).delete()
    else:
        like = Like()
        like.item = item
        like.save()
    return redirect('item details or comment', pk)


def persist_item(request, item, template_name):
    if request.method == 'GET':
        form = ItemForm(instance=item)

        context = {
            'form': form,
            'item': item,
        }

        return render(request, f'items/{template_name}.html', context)
    else:
        form = ItemForm(
            request.POST,
            instance=item
        )
        if form.is_valid():
            form.save()
            return redirect('item details or comment', item.pk)

        context = {
            'form': form,
            'item': item,
        }

        return render(request, f'items/{template_name}.html', context)


def edit_item(request, pk):
    item = Item.objects.get(pk=pk)
    return persist_item(request, item, 'item_edit')


def create_item(request):
    item = Item()
    return persist_item(request, item, 'item_create')


def delete_item(request, pk):
    item = Item.objects.get(pk=pk)
    if request.method == 'GET':
        context = {
            'item': item,
        }

        return render(request, 'items/item_delete.html', context)
    else:
        item.delete()
        return redirect('list items')
