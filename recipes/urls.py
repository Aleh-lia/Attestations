from django.urls import path, re_path, register_converter
from . import views
from . import converters


register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    # path('', views.index, name='home'),
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    # path('addpage/', views.addpage, name='add_page'),

    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    # path('post/<slug:post_slug>/', views.show_post, name='post'),
    # path('category/<slug:cat_slug>/', views.show_category, name='category'),
    # path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'),
    # path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='edit_page'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'),
    path('category/<slug:cat_slug>/', views.Category.as_view(), name='category'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='edit_page'),
]
