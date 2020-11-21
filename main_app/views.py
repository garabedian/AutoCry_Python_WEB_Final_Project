from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

from autocry_core.decorators import allowed_groups
from main_app.forms import ItemForm, CommentForm, DeleteItemForm, FilterForm
from main_app.models import Item, Like, Comment


def extract_filter_values(params):
    order = params['order'] if 'order' in params else FilterForm.ORDER_ASC
    text = params['text'] if 'text' in params else ''

    return {
        'order': order,
        'text': text,
    }


# Create your views here.
def landing_page(request):
    return render(request, 'landing_page.html')


def list_items(request):
    params = extract_filter_values(request.GET)
    choices = {
        FilterForm.ORDER_ASC: 'make',
        FilterForm.ORDER_DESC: '-make',
        FilterForm.DATE_ASC: 'published_date',
        FilterForm.DATE_DESC: '-published_date',
    }
    order_by = choices[params['order']]
    items = Item.objects.filter(make__icontains=params['text']).order_by(order_by)

    user = get_user_model()
    users = user.objects.all()

    for item in items:
        item.can_edit = item.author_id == request.user.id or request.user.is_superuser
        creator = users.filter(id=item.author_id)
        item.creator = creator[0].username
        item.empty = Item.objects.all().count() <= 0

    context = {
        'items': items,
        'filter_form': FilterForm(initial=params),
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
            comment.author = request.user
            comment.save()
            return redirect('item details or comment', pk)
        context = {
            'item': item,
            'form': form,
        }

        return render(request, 'items/item_detail.html', context)


# @login_required(login_url='login user')
@allowed_groups(allowed_roles=['superusers', 'users'])
def like_item(request, pk):
    item = Item.objects.get(pk=pk)
    if Like.objects.filter(item_id=pk).exists():
        Like.objects.filter(item_id=pk).delete()
    else:
        like = Like()
        like.item = item
        like.author = request.user
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

        old_image_url = item.image_url
        old_image_file = item.image_file

        form = ItemForm(
            request.POST,
            request.FILES,
            instance=item
        )

        if form.is_valid():
            entry = form.save(commit=False)
            if entry.image_type == 'local_image':
                entry.image_url = ''
            entry.author = request.user
            entry.publish()
            entry.save()
            return redirect('item details or comment', item.pk)

        context = {
            'form': form,
            'item': item,
        }

        item.image_url = old_image_url
        item.image_file = old_image_file

        return render(request, f'items/{template_name}.html', context)


# @login_required(login_url='login user')
@allowed_groups(allowed_roles=['superusers', 'users'])
def edit_item(request, pk):
    item = Item.objects.get(pk=pk)
    return persist_item(request, item, 'item_edit')


# @login_required(login_url='login user')
@allowed_groups(allowed_roles=['superusers', 'users'])
def create_item(request):
    item = Item()
    return persist_item(request, item, 'item_create')


# @login_required(login_url='login user')
@allowed_groups(allowed_roles=['superusers', 'users'])
def delete_item(request, pk):
    item = Item.objects.get(pk=pk)
    if request.method == 'GET':
        form = DeleteItemForm(instance=item)
        context = {
            'form': form,
            'item': item,
        }

        return render(request, 'items/item_delete.html', context)
    else:
        item.delete()

        return redirect('list items')
