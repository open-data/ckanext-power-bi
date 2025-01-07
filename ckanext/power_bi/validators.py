from re import compile
from six import text_type

from typing import Any
from ckan.types import FlattenKey, FlattenDataDict, FlattenErrorDict, Context

from ckan.plugins.toolkit import _, Invalid
from ckanext.power_bi import helpers

REPORT_ID_PATTERN = compile(
    r'^[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}$')


def power_bi_report_id(key: FlattenKey,
                       data: FlattenDataDict,
                       errors: FlattenErrorDict,
                       context: Context):
    required_locales, _default_locale, _available_locales = \
            helpers.get_supported_locales()

    value = data[key]

    is_required_locale = False
    for locale in required_locales:
        if 'report_id_%s' % locale in key:
            is_required_locale = True
            break

    if is_required_locale and not value:
        # the locale is required
        errors[key].append(_("Power BI Report ID required."))
        return
    elif not value:
        # the local is not required, ignore the missing value
        return
    if not isinstance(value, text_type):
        errors[key].append(_("Power BI Report ID must be a string."))
        return
    if not REPORT_ID_PATTERN.match(value):
        errors[key].append(_("Invalid value for a Power BI Report ID."))


def power_bi_nav_position(value: Any) -> Any:
    if value < 0 or value > 1:
        raise Invalid(_("Power BI Navigation Pane Position "
                        "must be 0 (bottom) or 1 (left)."))
    return value
