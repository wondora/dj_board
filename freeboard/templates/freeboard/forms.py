from django import forms
from .models import Post, Category

# SummernoteWidget 임포트는 더 이상 필요 없으므로 제거합니다.

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'content', 'file']
        
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '제목을 입력하세요'
            }),
            # Quill 에디터의 데이터를 전달받을 숨겨진 Textarea입니다.
            'content': forms.Textarea(attrs={
                'class': 'form-control d-none', # 화면에서 숨김 (Bootstrap 클래스)
                'id': 'quill-content'           # 자바스크립트가 데이터를 채울 때 사용
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
        
        labels = {
            'category': '카테고리',
            'title': '제목',
            'content': '내용',
            'file': '파일 첨부',
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        # 카테고리 선택 기본 문구 설정 (선택 사항)
        self.fields['category'].empty_label = "카테고리를 선택하세요"
        # [!!!중요!!!] 이 줄을 추가해주세요.
        # 내용(content) 필드의 HTML required 속성을 강제로 끕니다.
        # 이렇게 하면 브라우저 에러(focus error)가 사라집니다.
        self.fields['content'].required = False
