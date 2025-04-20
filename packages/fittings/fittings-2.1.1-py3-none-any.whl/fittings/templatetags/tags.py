from django import template
from django.conf import settings


register = template.Library()


@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")


@register.simple_tag
def get_dt_lang(language):
    """
    Since django language codes and dataTables language codes are not all the same, we need to map one to the other.
    """
    prefix = 'fittings/dt-i18n/'
    special_codes = {
        'de': 'de-DE',
        'en': 'en-GB',
        'es': 'es-ES',
        'zh-hans': 'zh',
        'fr': 'fr-FR',
        'it': 'it-IT'
    }
    if language in special_codes:
        language = special_codes.get(language)

    return f'{prefix}{language}.json'
