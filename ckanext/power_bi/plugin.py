from flask import has_request_context

from typing import Dict, Any
from ckan.types import Validator, DataDict, Context, Callable
from ckan.common import CKANConfig

import ckan.plugins as plugins
from ckan.lib.plugins import DefaultTranslation

from ckanext.power_bi import validators, helpers, schema


class PowerBiViewPlugin(plugins.SingletonPlugin, DefaultTranslation):
    """
    Integrate Power BI JS library and MSI Auth into a CKAN view.
    """
    plugins.implements(plugins.IConfigurer, inherit=True)
    plugins.implements(plugins.IValidators, inherit=True)
    plugins.implements(plugins.IResourceView, inherit=True)
    plugins.implements(plugins.ITranslation, inherit=True)
    plugins.implements(plugins.ITemplateHelpers, inherit=True)

    # IConfigurer
    def update_config(self, config: 'CKANConfig'):
        plugins.toolkit.add_template_directory(config, 'templates')
        plugins.toolkit.add_resource('assets', 'ckanext-power-bi')
        plugins.toolkit.add_public_directory(config, 'assets/images')

    # IValidators
    def get_validators(self) -> Dict[str, Validator]:
        return {'power_bi_report_id': validators.power_bi_report_id,
                'power_bi_workspace_id': validators.power_bi_workspace_id,
                'power_bi_nav_position': validators.power_bi_nav_position}

    # IResourceView
    def can_view(self, data_dict: DataDict) -> bool:
        return True

    def setup_template_variables(self,
                                 context: Context,
                                 data_dict: DataDict) -> Dict[str, Any]:
        report_config = None
        error = None

        i18n_enabled = plugins.toolkit.asbool(
            plugins.toolkit.config.get(
                'ckanext.power_bi.internal_i18n', False))
        required_locales, default_locale, available_locales = \
            helpers.get_supported_locales()

        try:
            report_config = helpers.get_report_config(data_dict)
        except (plugins.toolkit.ObjectNotFound,
                plugins.toolkit.NotAuthorized) as e:
            error = e
            pass

        fullscreen = False
        if (
          has_request_context() and
          hasattr(plugins.toolkit.request, 'view_args') and
          plugins.toolkit.request.view_args.get('view_id')):
            fullscreen = True

        return {'power_bi_report_config': report_config,
                'power_bi_error': error,
                'required_locales': required_locales,
                'default_locale': default_locale,
                'available_locales': available_locales,
                'i18n_enabled': i18n_enabled,
                'fullscreen': fullscreen}

    def view_template(self,
                      context: Context,
                      data_dict: DataDict) -> str:
        return 'power_bi/power_bi_view.html'

    def form_template(self,
                      context: Context,
                      data_dict: DataDict) -> str:
        return 'power_bi/power_bi_form.html'

    def info(self) -> Dict[str, Any]:
        return {
            'name': 'power_bi_view',
            'title': plugins.toolkit._('Power BI'),
            'filterable': False,
            'icon': 'power-bi',
            'default_title': plugins.toolkit._('Power BI'),
            'preview_enabled': False,
            'schema': schema.get_view_schema(),
            'iframed': False
        }

    # DefaultTranslation, ITranslation
    def i18n_domain(self) -> str:
        return 'ckanext-power-bi'

    # ITemplateHelpers
    def get_helpers(self) -> Dict[str, Callable[..., Any]]:
        return {'power_bi_icon_uri': helpers.power_bi_icon_uri}
