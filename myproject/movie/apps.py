from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MovieConfig(AppConfig):
    name = 'movie'
    verbose_name = _('movie')

    def ready(self):
        import movie.signals  # noqa
