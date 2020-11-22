from django import forms
from django.core.exceptions import ValidationError

from main_app.common import DisabledFormMixin
from main_app.models import Item

from django import forms

from main_app.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
        widgets = {
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control rounded-2',
                }
            )
        }


class ItemForm(forms.ModelForm):
    # Add class attribute to all form fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Item
        fields = ('type', 'make', 'model', 'build_year', 'description', 'image_type', 'image_url', 'image_file')
        widgets = {
            'image_url': forms.TextInput(
                attrs={
                    'id': 'img_url_input',
                }
            ),
            'image_file': forms.FileInput(
                attrs={
                    # 'class': 'custom-file-input',   # cannot override existing "class" attribute
                    'id': 'img_file_input',
                    'onchange': 'readURL(this);',
                }
            )
        }


class DeleteItemForm(ItemForm, DisabledFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        DisabledFormMixin.__init__(self)


# Adding filter fields for items' listing
class FilterForm(forms.Form):
    ORDER_ASC = 'asc'
    ORDER_DESC = 'desc'
    DATE_ASC = 'date_asc'
    DATE_DESC = 'date_desc'

    ORDER_CHOICES = (
        (ORDER_ASC, 'Make - ascending'),
        (ORDER_DESC, 'Make - descending'),
        (DATE_ASC, 'Published - ascending'),
        (DATE_DESC, 'Published - descending'),
    )

    text = forms.CharField(
        required=False,
    )
    order = forms.ChoiceField(
        choices=ORDER_CHOICES,
        required=False,
    )
