from re import compile
from six import text_type

from ckan.plugins.toolkit import _, Invalid

REPORT_ID_PATTERN = compile(
    r'^[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}$')


def power_bi_report_id(value):
    if not value:
        raise Invalid(_("Power BI Report ID required."))
    if not isinstance(value, text_type):
        raise Invalid(_("Power BI Report ID must be a string."))
    if not REPORT_ID_PATTERN.match(value):
        raise Invalid(_("Invalid value for a Power BI Report ID."))
    return value
