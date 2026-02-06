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
            # [수정] SummernoteWidget을 일반 Textarea로 교체
            # Quill이 이 textarea를 찾아서 데이터를 넣어줄 수 있도록 id를 지정합니다.
            'content': forms.Textarea(attrs={
                'class': 'form-control d-none', # Bootstrap의 d-none으로 숨김
                'id': 'quill-content'
            }),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'category': '카테고리',
            'title': '제목',
            'content': '내용',
            'file': '파일 첨부',
        }
