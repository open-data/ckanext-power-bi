from azure.identity import (
    ManagedIdentityCredential,
    CredentialUnavailableError
)
import requests
import base64
import json

from typing import List, Tuple, Dict, Any
from ckan.types import DataDict

from ckan.lib.helpers import ckan_version
from ckan.plugins.toolkit import (
    h,
    _,
    config,
    ObjectNotFound,
    NotAuthorized
)

from logging import getLogger
import traceback


log = getLogger(__name__)

POWER_BI_LANG_LOCALES = {
    'ar': 'SA',
    'bg': 'BG',
    'ca': 'ES',
    'cs': 'CZ',
    'da': 'DK',
    'de': 'DE',
    'el': 'GR',
    'en': 'US',
    'es': 'ES',
    'et': 'EE',
    'eU': 'ES',
    'fi': 'FI',
    'fr': 'FR',
    'gl': 'ES',
    'he': 'IL',
    'hi': 'IN',
    'hr': 'HR',
    'hu': 'HU',
    'id': 'ID',
    'it': 'IT',
    'ja': 'JP',
    'kk': 'KZ',
    'ko': 'KR',
    'lt': 'LT',
    'lv': 'LV',
    'ms': 'MY',
    'nb': 'NO',
    'nl': 'NL',
    'pl': 'PL',
    'pt': 'BR',
    'ro': 'RO',
    'ru': 'RU',
    'sk': 'SK',
    'sl': 'SI',
    'sr': 'Cyrl-RS',
    'sv': 'SE',
    'th': 'TH',
    'tr': 'TR',
    'uk': 'UA',
    'vi': 'VN',
    'zh': 'CN'
}


def _get_access_token() -> str:
    """
    Uses ManagedIdentityCredential (MSI) on a sytem level
    to generate an access token with the Power BI API scope permissions.
    """
    try:
        credential = ManagedIdentityCredential()
    except ValueError:
        raise ObjectNotFound(_("An Azure Client ID has not been configured."))

    err_msg = _("Unable to generate an access token to Azure.")

    try:
        access_token_obj = credential.get_token(
            'https://analysis.windows.net/powerbi/api/.default')
    except CredentialUnavailableError:
        raise NotAuthorized(err_msg)

    access_token = getattr(access_token_obj, 'token', None)

    if not access_token:
        raise NotAuthorized(err_msg)

    return access_token


def _get_embed_token(access_token: str,
                     group_id: str,
                     report_id: str) -> str:
    """
    Uses the passed Azure access token to retrieve an
    embed token for the given Power BI report.

    The embed token retrieved will have only Read/View access,
    without saving the report potential.
    """
    embed_token = None

    org_name = config.get('ckanext.power_bi.org_name', 'myorg')

    if not org_name:
        raise ObjectNotFound(_("A Power BI Organization "
                               "has not been configured."))

    response = None
    try:
        response = requests.request(
            method='POST',
            url='https://api.powerbi.com/v1.0/%s/groups'
                '/%s/reports/%s/GenerateToken'
                % (org_name, group_id, report_id),
            json={
                'accessLevel': 'View',
                'allowSaveAs': False},
            headers={
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'User-agent': 'CKAN/{}'.format(ckan_version())},
            verify=True
        )
    except Exception:
        log.info('Failed to retrieve Power BI embed token')
        log.info(traceback.format_exc())
        pass

    if response is not None:
        try:
            response_data = response.json()
            embed_token = response_data.get('token')
        except Exception:
            log.info('Failed to parse Power BI embed token')
            log.info(traceback.format_exc())
            pass

    if not embed_token:
        raise NotAuthorized(_("Unable to generate an embed "
                              "token for the Power BI Report."))

    return embed_token


def get_report_config(data_dict: DataDict) -> Dict[str, Any]:
    """
    Authenticates with Power BI and builds config for a report.
    """
    resource_view = data_dict.get('resource_view', {})
    is_public = resource_view.get('public_report', False)

    workspace_id = resource_view.get('workspace_id', None)
    if not is_public:
        workspace_id = config.get('ckanext.power_bi.workspace_id')
    if not workspace_id:
        raise ObjectNotFound(_("A Power BI Workspace ID "
                               "has not been configured."))

    current_lang = h.lang() or 'en'
    report_id = resource_view.get('report_id_%s' % current_lang)
    if not report_id:
        raise ObjectNotFound(_("Missing Power BI Report ID."))

    embed_token = 'any'
    if not is_public:
        access_token = _get_access_token()
        embed_token = _get_embed_token(access_token, workspace_id, report_id)

    # default: hide bookmarks pane
    show_bookmarks = resource_view.get('bookmarks_pane', False)

    # default: show filter pane
    show_filters = resource_view.get('filter_pane', True)

    # default: collapse filter pane
    collapse_filters = resource_view.get('filter_pane_collapse', True)
    expand_filters = False if collapse_filters else True

    # default: show nav pane
    show_navigate = resource_view.get('nav_pane', True)

    # default: nav pane bottom position
    navigate_pos = resource_view.get('nav_pane_position', 0)

    # default: no page
    page = resource_view.get('page_%s' % current_lang, None)

    # default: no bookmark
    bookmark = resource_view.get('bookmark_%s' % current_lang, None)

    locale_format = current_lang if current_lang not in \
        POWER_BI_LANG_LOCALES else '%s-%s' % (
            current_lang, POWER_BI_LANG_LOCALES[current_lang])

    embed_uri = 'https://app.powerbi.com/reportEmbed?' \
                'reportId={report}&groupId={workspace}'.format(
                    report=report_id, workspace=workspace_id)
    if is_public:
        encoded_report = json.dumps(
            {'k': report_id, 't': workspace_id}).encode('utf-8')
        encoded_report = base64.b64encode(encoded_report).decode('utf-8')
        embed_uri = 'https://app.powerbi.com/view?r={report}'.format(
                        report=encoded_report)

    if page:
        embed_uri += '&pageName=%s' % page

    if bookmark:
        embed_uri += '&bookmark=%s' % bookmark

    report_config = {
        "type": "report",
        "tokenType": 1,  # 1 == Embed
        "accessToken": embed_token,
        "embedUrl": embed_uri,
        "id": report_id,
        "permissions": 0,  # 0 == Read
        "settings": {
            "localeSettings": {
                "language": current_lang,
                "formatLocale": locale_format,
            },
            "panes": {
                "bookmarks": {
                    "visible": show_bookmarks,
                },
                "fields": {  # requires edit perms
                    "expanded": False,
                    "visible": False,
                },
                "filters": {
                    "expanded": expand_filters,
                    "visible": show_filters,
                },
                "pageNavigation": {
                    "position": navigate_pos,
                    "visible": show_navigate,
                },
                "selection": {  # requires edit perms
                    "visible": False,
                },
                "syncSlicers": {  # requires edit perms
                    "visible": False,
                },
                "visualizations": {  # requires edit perms
                    "expanded": False,
                    "visible": False}}}}

    if page:
        report_config['pageName'] = page

    if bookmark:
        report_config['bookmark'] = {'name': bookmark}

    return report_config


def get_supported_locales() -> Tuple[List[str], str, List[str]]:
    required_locales = config.get(
        'ckanext.power_bi.required_locales', '').split()

    default_locale = config.get('ckan.locale_default', 'en')

    if default_locale not in required_locales:
        # always require the default locale
        required_locales.append(default_locale)

    available_locales = []
    core_locales = []

    core_locale_objects = h.get_available_locales()
    for locale_obj in core_locale_objects:
        core_locales.append(locale_obj.short_name)

    offered_locales = config.get(
        'ckanext.power_bi.locales_offered', '').split()

    if offered_locales:
        for locale in offered_locales:
            if locale not in core_locales:
                # we should only support locales that CKAN has
                continue
            available_locales.append(locale)
    else:
        available_locales = core_locales

    return required_locales, default_locale, available_locales


def power_bi_icon_uri() -> str:
    if config.get('ckan.root_path'):
        # if using a root_path, get the url_for_static
        return h.url_for_static('/power_bi.svg')
    return '/power_bi.svg'
