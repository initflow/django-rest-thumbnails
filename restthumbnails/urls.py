from django.conf import settings
try:
    from django.conf.urls import url
except ImportError:
    from django.conf.urls.defaults import  url

from restthumbnails.defaults import URL_REGEX
from restthumbnails.views import ThumbnailView


urlpatterns = [
    url(regex=URL_REGEX,
        view=ThumbnailView.as_view(),
        name="get_thumbnail")]
