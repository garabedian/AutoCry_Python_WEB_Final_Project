from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DeleteView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from autocry_core.decorators import allowed_groups
from main_app.forms import ItemForm, CommentForm, DeleteItemForm, FilterForm, ContactForm
from main_app.models import Item, Like, Comment
from main_app.serializers import ItemSerializer


def liked_already(pk, current_user):
    return Like.objects.filter(item_id=pk).filter(author_id=current_user).exists()


def extract_filter_values(params):
    order = params['order'] if 'order' in params else FilterForm.ORDER_ASC
    make = params['make'] if 'make' in params or 'model' in params else ''

    return {
        'order': order,
        'make': make,
    }


def landing_page(request):
    return render(request, 'landing_page.html')


# CBV for all items
class ListItemsView(ListView):
    template_name = 'items/item_list.html'
    model = Item
    context_object_name = 'items'
    paginate_by = 6
    order_by = ''
    contains_make = ''

    def dispatch(self, request, *args, **kwargs):
        params = extract_filter_values(request.GET)
        filter_choices = {
            FilterForm.ORDER_ASC: 'make',
            FilterForm.ORDER_DESC: '-make',
            FilterForm.DATE_ASC: 'published_date',
            FilterForm.DATE_DESC: '-published_date',
        }
        self.order_by = filter_choices[params['order']]
        self.contains_make = params['make']
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        order_by = self.order_by
        items_make = self.model.objects.filter(make__icontains=self.contains_make)
        items_model = self.model.objects.filter(model__icontains=self.contains_make)
        result = (items_make | items_model).order_by(order_by)
        return result

    def get_context_data(self, **kwargs):
        filter_form_choices = {
            'make': FilterForm.ORDER_ASC,
            '-make': FilterForm.ORDER_DESC,
            'published_date': FilterForm.DATE_ASC,
            '-published_date': FilterForm.DATE_DESC,
        }
        context = super().get_context_data(**kwargs)
        context['filter_form'] = FilterForm(initial={
            'order': filter_form_choices[self.order_by],
            'make': self.contains_make,
        })

        users = get_user_model().objects.all()

        for item in context['items']:
            item.can_edit = item.author_id == context['view'].request.user.id or context[
                'view'].request.user.is_superuser
            creator = users.filter(id=item.author_id)
            item.creator = creator[0].username

        context['filter_included'] = True
        return context


# FBV for all items
def list_items(request):
    params = extract_filter_values(request.GET)
    filter_choices = {
        FilterForm.ORDER_ASC: 'make',
        FilterForm.ORDER_DESC: '-make',
        FilterForm.DATE_ASC: 'published_date',
        FilterForm.DATE_DESC: '-published_date',
    }
    order_by = filter_choices[params['order']]

    items_make = Item.objects.filter(make__icontains=params['make'])
    items_model = Item.objects.filter(model__icontains=params['make'])
    items = (items_make | items_model).order_by(order_by)

    users = get_user_model().objects.all()

    for item in items:
        item.can_edit = item.author_id == request.user.id or request.user.is_superuser
        creator = users.filter(id=item.author_id)
        item.creator = creator[0].username

    context = {
        'items': items,
        'filter_form': FilterForm(initial=params),
        'items_empty': Item.objects.all().count() <= 0,
        'filter_included': True,
    }

    return render(request, 'items/item_list.html', context)


@allowed_groups(allowed_roles=['superusers', 'users'])
def details_or_comment_item(request, pk):
    item = Item.objects.get(pk=pk)
    if request.method == 'GET':

        users = {}  # id: name
        for user in get_user_model().objects.all():
            users[user.id] = user.username

        current_user = request.user
        item.can_edit = item.author_id == current_user.id or current_user.is_superuser
        item.can_like = liked_already(pk, current_user)

        context = dict(item=item,
                       form=CommentForm(),
                       like=Like.objects.filter(item_id=pk).exists(),
                       users=users,
                       is_author=item.author_id == current_user.id)

        return render(request, 'items/item_detail.html', context)
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            # comment = Comment(comment=form.cleaned_data['text'])      # Pure Form class used
            comment = Comment(comment=form.cleaned_data['comment'])  # ModelForm class used
            comment.item = item  # Attach ForeignKey
            comment.author = request.user
            comment.publish()
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
    current_user = request.user
    if liked_already(pk, current_user):
        Like.objects.filter(item_id=pk).filter(author_id=current_user).delete()
    else:
        like = Like()
        like.item = item
        like.author = current_user
        like.save()
    return redirect('item details or comment', pk)


def persist_item(request, item, template_name):
    item_has_author = item.author_id
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
            elif not entry.image_url:
                entry.image_url = old_image_url
            if not item_has_author:
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

    if item.author_id != request.user.id and not request.user.is_superuser:
        return render(request, '403.html')

    return persist_item(request, item, 'item_edit')


# @login_required(login_url='login user')
@allowed_groups(allowed_roles=['superusers', 'users'])
def create_item(request):
    item = Item()
    return persist_item(request, item, 'item_create')


# CBV for delete item
@method_decorator(allowed_groups(allowed_roles=['superusers', 'users']), name='dispatch')
class DeleteItemView(UserPassesTestMixin, DeleteView):
    fields = '__all__'
    model = Item
    context_object_name = 'item'
    template_name = 'items/item_delete.html'
    success_url = reverse_lazy('list items')
    user = None
    item = None

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        pk = self.kwargs['pk']
        self.item = Item.objects.get(pk=pk)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DeleteItemForm(instance=self.object)
        return context

    # Required by UserPassesTestMixin
    def test_func(self):
        if self.item.author == self.user or self.user.is_superuser:
            return True

        raise PermissionDenied


# FBV for delete item
# @login_required(login_url='login user')
@allowed_groups(allowed_roles=['superusers', 'users'])
def delete_item(request, pk):
    item = Item.objects.get(pk=pk)

    if item.author_id != request.user.id and not request.user.is_superuser:
        return render(request, '403.html')

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


# @login_required(login_url='login user')
@allowed_groups(allowed_roles=['superusers', 'users'])
def contact_us(request):
    if request.method == 'GET':
        form = ContactForm()
        return render(request, 'contact/contact-us.html', {'form': form})

    form = ContactForm(request.POST)
    if form.is_valid():
        # send email code goes here
        sender_name = form.cleaned_data['name']
        sender_email = form.cleaned_data['email']
        login_name = request.user.username

        message = f'{sender_name} ("{login_name}") has sent you a new message:\n\n{form.cleaned_data["message"]}'
        send_mail('New Enquiry', message, sender_email, ['takvor@students.softuni.bg'])
        return render(request, 'contact/email-confirm.html')

    return render(request, 'contact/email-failed.html')


class ListItemsRestView(APIView):
    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response({"items": serializer.data})

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailItemRestView(APIView):
    def get(self, request, pk):
        item = Item.objects.get(pk=pk)
        serializer = ItemSerializer(item)
        return Response({"item": serializer.data})

    def post(self, request, pk):
        item = Item.objects.get(pk=pk)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = Item.objects.get(pk=pk)
        item.delete()
        return Response(status=status.HTTP_200_OK)
