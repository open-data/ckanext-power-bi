import ckan.plugins as plugins
from ckan.lib.plugins import DefaultTranslation

from ckanext.power_bi import validators, helpers


class PowerBiViewPlugin(plugins.SingletonPlugin, DefaultTranslation):
    """
    Integrate Power BI JS library and MSI Auth into a CKAN view.
    """
    plugins.implements(plugins.IConfigurer, inherit=True)
    plugins.implements(plugins.IValidators, inherit=True)
    plugins.implements(plugins.IResourceView, inherit=True)
    plugins.implements(plugins.ITranslation, inherit=True)

    # IConfigurer

    def update_config(self, config):
        plugins.toolkit.add_template_directory(config, 'templates')
        plugins.toolkit.add_resource('assets', 'ckanext-power-bi')

    # IValidators

    def get_validators(self):
        return {
            'power_bi_report_id': validators.power_bi_report_id,
        }

    # IResourceView

    def can_view(self, data_dict):
        return True

    def setup_template_variables(self, context, data_dict):
        report_config = None
        error = None
        try:
            report_config = helpers.get_report_config(data_dict)
        except (plugins.toolkit.ObjectNotFound,
                plugins.toolkit.NotAuthorized) as e:
            error = e
            pass
        return {'power_bi_report_config': report_config,
                'power_bi_error': error,}

    def view_template(self, context, data_dict):
        return 'power_bi/power_bi_view.html'

    def form_template(self, context, data_dict):
        return 'power_bi/power_bi_form.html'

    def info(self):
        report_id_validator = plugins.toolkit.get_validator(
                                'power_bi_report_id')
        boolean_validator = plugins.toolkit.get_validator(
                                'boolean_validator')
        return {
            'name': 'power_bi_view',
            'title': plugins.toolkit._('Power BI'),
            'filterable': False,
            'icon': 'windows',
            'default_title': plugins.toolkit._('Power BI'),
            'preview_enabled': False,
            'schema': {
                'report_id': [report_id_validator],
                'fullscreen': [boolean_validator],
                'filter_pane': [boolean_validator],
                'nav_pane': [boolean_validator],
            },
        }

    # DefaultTranslation, ITranslation

    def i18n_domain(self):
        return 'ckanext-power-bi'
