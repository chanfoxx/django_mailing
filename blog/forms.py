from django import forms
from blog.models import Blog


class BlogForm(forms.ModelForm):
    """Форма для блоговых записей."""
    class Meta:
        model = Blog
        exclude = ('slug', 'view_count', 'creator',)
