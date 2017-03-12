from django.conf.urls import url
from rango import views

app_name = 'rango'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index', views.index, name='index'),
    url(r'^about', views.about, name='about'),

    # User of ?P<name>
    # In django, named capturing groups are passed to your view as "KEYWORD ARGUMENTS."
    # Unnamed capturing groups (just a parenthesis) are passed to your view as "ARGUMENTS".
    # The ?P is a named capturing group, as opposed to an unnamed capturing group.
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
    url(r'^add_category/$', views.add_category, name='add_category'),

    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
]