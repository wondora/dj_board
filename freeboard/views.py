from django.shortcuts import render, get_object_or_404, redirect
from freeboard.models import Post, Category
from freeboard.forms import PostForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def post_list(request):
    category_slug = request.GET.get('category')
    page = request.GET.get('page', 1)
    query = request.GET.get('q', '')  # 검색어 파라미터 추가

    # 'None' 문자열 또는 빈 문자열이 넘어올 경우, None으로 처리하여 전체 게시글을 보여주도록 함
    if category_slug == 'None' or category_slug == '':
        category_slug = None

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = Post.objects.filter(category=category).select_related('category')
    else:
        posts = Post.objects.all().select_related('category')
        category = None

    # 검색어가 있으면 제목 또는 내용에 포함된 게시글만 필터링
    if query:
        posts = posts.filter(title__icontains=query) | posts.filter(content__icontains=query)
        posts = posts.distinct()

    posts = posts.order_by('-created_at')

    paginator = Paginator(posts, 15)  # 한 페이지에 15개씩
    try:
        paged_posts = paginator.page(page)
    except PageNotAnInteger:
        paged_posts = paginator.page(1)
    except EmptyPage:
        paged_posts = paginator.page(paginator.num_pages)

    categories = Category.objects.all()
    return render(request, 'freeboard/post_list.html', {
        'posts': paged_posts,
        'categories': categories,
        'current_category': category,
        'query': query,  # 검색어 템플릿에 전달
    })

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'freeboard/post_detail.html', {'post': post})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            return redirect('freeboard:post_list')
    else:
        form = PostForm()
    return render(request, 'freeboard/post_form.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        import logging
        logger = logging.getLogger(__name__)

        form = PostForm(request.POST, request.FILES, instance=post)
        file_clear = 'file-clear' in request.POST
        new_file_uploaded = 'file' in request.FILES

        # 파일 삭제 체크가 되어 있으면 기존 파일을 먼저 삭제
        if file_clear and post.file:
            old_file_path = post.file.path
            if old_file_path and os.path.exists(old_file_path):
                try:
                    os.remove(old_file_path)
                except Exception as e:
                    logger.error(f'파일 삭제 중 오류: {e}')
            post.file = None
            post.save()

        if form.is_valid():
            post = form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': '/board/'})
            return redirect('freeboard:post_list')
        else:
            logger.error(f"폼 검증 실패: {form.errors}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'freeboard/post_form.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('freeboard:post_list')
    return render(request, 'freeboard/post_confirm_delete.html', {'object': post})