from ckan.plugins.toolkit import get_validator, asbool, config

from ckanext.power_bi import helpers


def get_view_schema():
    boolean_validator = get_validator('boolean_validator')
    int_validator = get_validator('int_validator')
    report_id_validator = get_validator('power_bi_report_id')
    nav_pos_validator = get_validator('power_bi_nav_position')

    i18n_enabled = asbool(config.get(
            'ckanext.power_bi.internal_i18n', False))
    required_locales, default_locale, available_locales = \
        helpers.get_supported_locales()

    schema = {
        'report_id_%s' % default_locale: [report_id_validator],
        'bookmarks_pane': [boolean_validator],
        'filter_pane': [boolean_validator],
        'filter_pane_collapse': [boolean_validator],
        'nav_pane': [boolean_validator],
        'nav_pane_position': [int_validator,
                              nav_pos_validator],
    }

    if not i18n_enabled:
        # using Power BI Multiple-Language Reports
        # do not need the multiple language fields.
        return schema

    for locale in available_locales:
        if locale == default_locale:
            continue
        schema['report_id_%s' % locale] = [report_id_validator]

    return schema
