from six import text_type

from ckan.plugins.toolkit import _, ValidationError


def power_bi_report_id(value, context):
    if not value:
        raise ValidationError({"report_id": [_("Report ID required.")]})
    if not isinstance(value, text_type):
        raise ValidationError({"report_id": [_("Report ID must be a string.")]})
    #TODO: regex Power BI Report ID
    return value
