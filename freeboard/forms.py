from django import forms
from .models import Post, Category
from django_summernote.widgets import SummernoteWidget

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'content', 'file']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '제목을 입력하세요'}),
            'content': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'category': '카테고리',
            'title': '제목',
            'content': '내용',
            'file': '파일 첨부',
        }
