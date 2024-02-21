import ckan.plugins as plugins
from ckan.lib.plugins import DefaultTranslation

from ckanext.power_bi import validators, helpers


class PowerBiPlugin(plugins.SingletonPlugin, DefaultTranslation):
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
        plugins.toolkit.add_public_directory(config, 'public')
        plugins.toolkit.add_resource('public', 'ckanext-power-bi')

    # IValidators

    def get_validators(self):
        return {
            'power_bi_report_id': validators.power_bi_report_id,
        }

    # IResourceView

    def can_view(self, data_dict):
        return True

    def setup_template_variables(self, context, data_dict):
        return {'power_bi_report_config':
                    helpers.get_report_config(context, data_dict)}

    def view_template(self, context, data_dict):
        return 'power_bi/power_bi_view.html'

    def form_template(self, context, data_dict):
        return 'power_bi/power_bi_form.html'

    def info(self):
        return {
            'name': 'power_bi_view',
            'title': plugins.toolkit._('Power BI'),
            'filterable': False,
            'icon': 'windows',
            'default_title': plugins.toolkit._('Power BI'),
            'preview_enabled': False,
            'schema': {
                'report_id': [plugins.toolkit.get_validator(
                    'power_bi_report_id')],
            }
        }

    # DefaultTranslation, ITranslation

    def i18n_domain(self):
        return 'ckanext-power-bi'
