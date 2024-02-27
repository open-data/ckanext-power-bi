from re import compile
from six import text_type

from ckan.plugins.toolkit import _
from ckanext.power_bi import helpers

REPORT_ID_PATTERN = compile(
    r'^[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}$')


def power_bi_report_id(key, data, errors, context):
    require_locales, default_locale, available_locales = \
            helpers.get_supported_locales()

    value = data[key]

    if require_locales and not value:
        # all locales are required, force a value onto all locales.
        errors[key].append(_("Power BI Report ID required."))
        return
    elif 'report_id_%s' % default_locale in key and not value:
        # not all locales are required,
        # only force a value onto the default locale.
        errors[key].append(_("Power BI Report ID required."))
        return
    elif not value:
        # not all locales are required,
        # so we can ignore the missing value.
        return
    if not isinstance(value, text_type):
        errors[key].append(_("Power BI Report ID must be a string."))
        return
    if not REPORT_ID_PATTERN.match(value):
        errors[key].append(_("Invalid value for a Power BI Report ID."))
