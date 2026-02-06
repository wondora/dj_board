from django.shortcuts import render, get_object_or_404, redirect
from freeboard.models import Post, Category
from freeboard.forms import PostForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging

# 로거 설정
logger = logging.getLogger(__name__)

@login_required
def post_list(request):
    category_slug = request.GET.get('category')
    page = request.GET.get('page', 1)
    query = request.GET.get('q', '')  # 검색어 파라미터

    # 'None' 문자열 또는 빈 문자열 처리
    if category_slug == 'None' or category_slug == '':
        category_slug = None

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = Post.objects.filter(category=category).select_related('category')
    else:
        posts = Post.objects.all().select_related('category')
        category = None

    # 검색어 필터링
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

    # ============================================================
    # ▼ [추가됨] 페이지네이션 Sliding Window 로직 (항상 5개 유지)
    # ============================================================
    max_index = 5  # 화면에 보여줄 버튼 개수
    current_page = paged_posts.number
    total_pages = paginator.num_pages

    # 1. 현재 페이지를 중심으로 범위 설정 (예: 3페이지면 1~5)
    start_index = current_page - 2
    end_index = current_page + 2

    # 2. 시작점이 1보다 작으면, 부족한 만큼 뒤로 밈 (1페이지일 때 1~5로 만듦)
    if start_index < 1:
        end_index += (1 - start_index)
        start_index = 1

    # 3. 끝점이 전체 페이지를 넘으면, 넘친 만큼 앞으로 당김
    if end_index > total_pages:
        start_index -= (end_index - total_pages)
        end_index = total_pages
        
        # 3-1. 당겼는데 시작점이 1보다 작아지면 1로 고정 (전체 페이지가 5개 미만일 때)
        if start_index < 1:
            start_index = 1

    custom_range = range(start_index, end_index + 1)
    # ============================================================

    categories = Category.objects.all()
    
    return render(request, 'freeboard/post_list.html', {
        'posts': paged_posts,
        'categories': categories,
        'current_category': category,
        'query': query,
        'custom_range': custom_range, # 템플릿으로 전달!
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
        form = PostForm(request.POST, request.FILES, instance=post)
        file_clear = 'file-clear' in request.POST
        
        # 파일 삭제 로직
        if file_clear and post.file:
            old_file_path = post.file.path
            # 파일이 실제로 존재할 때만 삭제 시도
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