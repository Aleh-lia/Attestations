from django.urls import path, re_path, register_converter
from . import views
from . import converters


register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'),
    path('category/<slug:cat_slug>/', views.Category.as_view(), name='category'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='edit_page'),
]
