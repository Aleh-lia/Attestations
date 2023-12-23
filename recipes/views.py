from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView

from recipes.forms import *
from recipes.models import *
from recipes.utils import *


# menu = [{'title': "О сайте", 'url_name': 'about'},
#         {'title': "Добавить рецепт", 'url_name': 'add_page'},
#         {'title': "Обратная связь", 'url_name': 'contact'},
#         ]
#
#
# entrance = [{'title': "Регистрация", 'url_name': 'registration'},
#             {'title': "Войти", 'url_name': 'login'},
#             ]


# def index(request):
#     posts = Recipes.published.all()
#
#     context = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#         'entrance': entrance,
#         'cat_selected': 0,
#     }
#     return render(request, 'recipes/index.html', context=context)


# class Home(TemplateView):
#     template_name = 'recipes/index.html'
#     extra_context = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': Recipes.published.all().select_related('cat'),
#         'entrance': entrance,
#         'cat_selected': 0,
#     }

class Home(DataMixin, ListView):
    template_name = 'recipes/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0


    def get_queryset(self):
        return Recipes.published.all().select_related('cat')


@login_required
def about(request):
    contact_list = Recipes.objects.all()
    paginator = Paginator(contact_list, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recipes/about.html', {'title': 'О сайте', 'page_obj': page_obj})


class ShowPost(DataMixin, DetailView):
    template_name = 'recipes/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Recipes.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'recipes/addpage.html'
    title_page = 'Добавление рецепта'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context

    def form_valid(self, form):
        r = form.save(commit=False)
        r.author = self.request.user
        return super().form_valid(form)


class UpdatePage(DataMixin, UpdateView):
    model = Recipes
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'recipes/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование рецепта'


class Category(DataMixin, ListView):
    template_name = 'recipes/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Recipes.published.filter(cat__slug=self.kwargs['cat_slug']).select_related("cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title = 'Категория - ' + cat.name,
                                      cat_selected = cat.pk)


class TagPostList(DataMixin, ListView):
    template_name = 'recipes/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context,
                                      title='Тег - ' + tag.tag)

    def get_queryset(self):
        return Recipes.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def registration(request):
    return HttpResponse("Регистрация")



def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


# def show_post(request, post_slug):
#     post = get_object_or_404(Recipes, slug=post_slug)
#
#     context = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'entrance': entrance,
#         'cat_selected': 1,
#     }
#     return render(request, 'recipes/post.html', context)



# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # try:
#             #     Recipes.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except:
#             #     form.add_error(None, "Ошибка добавления поста")
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#
#     context = {
#         'menu': menu,
#         'title': 'Добавление статьи',
#         'form': form
#     }
#     return render(request, 'recipes/addpage.html', context)


# class AddPage(View):
#     def get(self, request):
#         form = AddPostForm()
#         data = {
#             'menu': menu,
#             'title': 'Добавление рецепта',
#             'form': form
#         }
#         return render(request, 'recipes/addpage.html', data)
#
#     def post(self, request):
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         context = {
#             'menu': menu,
#             'title': 'Добавление рецепта',
#             'form': form
#         }
#         return render(request, 'recipes/addpage.html', context)


# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug)
#     posts = Recipes.published.filter(category=category.pk)
#     context = {
#         'title': f'Рубрика: {category.name}',
#         'menu': menu,
#         'posts': posts,
#         'entrance': entrance,
#         'cat_selected': category.pk,
#     }
#     return render(request, 'recipes/index.html', context=context)

# def show_tag_postlist(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.tags.filter(is_published=Recipes.Status.PUBLISHED)
#
#     context = {
#         'title': f"Тег: {tag.tag}",
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None,
#     }
#
#     return render(request, 'recipes/index.html', context=context)



# class Home(DataMixin, ListView):
#     template_name = 'recipes/index.html'
#     context_object_name = 'posts'
#     title_page = 'Главная страница'
#     cat_selected = 0
#
#     def get_queryset(self):
#         return Recipes.published.all().select_related('cat')


# @login_required
# def about(request):
#     contact_list = Recipes.published.all()
#     paginator = Paginator(contact_list, 3)
#
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     return render(request, 'recipes/about.html',
#                   {'title': 'О сайте', 'page_obj': page_obj})


# class ShowPost(DataMixin, DetailView):
#     template_name = 'recipes/post.html'
#     slug_url_kwarg = 'post_slug'
#     context_object_name = 'post'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return self.get_mixin_context(context, title=context['post'].title)
#
#     def get_object(self, queryset=None):
#         return get_object_or_404(Recipes.published, slug=self.kwargs[self.slug_url_kwarg])


#
#
#
# class UpdatePage(DataMixin, UpdateView):
#     model = Recipes
#     fields = ['title', 'content', 'photo', 'is_published', 'cat']
#     template_name = 'recipes/addpage.html'
#     success_url = reverse_lazy('home')
#     title_page = 'Редактирование статьи'
#
#
# def contact(request):
#     return HttpResponse("Обратная связь")
#
#
# def login(request):
#     return HttpResponse("Авторизация")
#
#
# class WomenCategory(DataMixin, ListView):
#     template_name = 'recipes/index.html'
#     context_object_name = 'posts'
#     allow_empty = False
#
#     def get_queryset(self):
#         return Recipes.published.filter(cat__slug=self.kwargs['cat_slug']).select_related("cat")
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         cat = context['posts'][0].cat
#         return self.get_mixin_context(context,
#                                       title='Категория - ' + cat.name,
#                                       cat_selected=cat.pk,
#                                       )
#
#
# def page_not_found(request, exception):
#     return HttpResponseNotFound("<h1>Страница не найдена</h1>")
#
#
# class TagPostList(DataMixin, ListView):
#     template_name = 'recipes/index.html'
#     context_object_name = 'posts'
#     allow_empty = False
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
#         return self.get_mixin_context(context, title='Тег: ' + tag.tag)
#
#     def get_queryset(self):
#         return Recipes.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')



