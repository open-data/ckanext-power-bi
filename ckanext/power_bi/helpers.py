from azure.identity import ManagedIdentityCredential, CredentialUnavailableError
import requests

from ckan.lib.helpers import ckan_version
from ckan.plugins.toolkit import h, _, config, ObjectNotFound, NotAuthorized


def _get_access_token():
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


def _get_embed_token(access_token, group_id, report_id):
    """
    Uses the passed Azure access token to retrieve an
    embed token for the given Power BI report.

    The embed token retrieved will have only Read/View access,
    without saving the report potential.
    """
    embed_token = None

    org_name = config.get('ckanext.power_bi.org_name')

    if not org_name:
        raise ObjectNotFound(_("A Power BI Organization "
                               "has not been configured."))

    response = requests.request(
        method='POST',
        url='https://api.powerbi.com/v1.0/%s/groups'
            '/%s/reports/%s/GenerateToken'\
            % (org_name, group_id, report_id),
        json={
            'accessLevel': 'View',
            'allowSaveAs': False,
        },
        headers={
            'Authorization': 'Bearer {}'.format(access_token),
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-agent': 'CKAN/{}'.format(ckan_version()),
        },
        verify=True
    )

    try:
        response_data = response.json()
        embed_token = response_data.get('token')
    except Exception:
        pass

    if not embed_token:
        raise NotAuthorized(_("Unable to generate an embed "
                              "token for the Power BI Report."))

    return embed_token


def get_report_config(data_dict):
    """
    Authenticates with Power BI and builds config for a report.
    """
    workspace_id = config.get('ckanext.power_bi.workspace_id')
    if not workspace_id:
        raise ObjectNotFound(_("A Power BI Workspace ID has not been configured."))

    report_id = data_dict.get('resource_view', {}).get('report_id')
    if not report_id:
        raise ObjectNotFound(_("Missing Power BI Report ID."))

    access_token = _get_access_token()
    embed_token = _get_embed_token(access_token, workspace_id, report_id)

    return {
        "type": "report",
        "tokenType": 1,  # 1 == Embed
        "accessToken": embed_token,
        "embedUrl":
            "https://app.powerbi.com/reportEmbed?reportId=%s&groupId=%s&language=%s" \
                % (report_id, workspace_id, h.lang()),
        "id": report_id,
        "permissions": 0,  # 0 == Read
        "settings": {
            "localSettings": {
                "language": h.lang(),
                "formatLocale": "CA",
            },
            "filterPaneEnabled": data_dict.get('resource_view', {})\
                .get('filter_pane', False),
            "navContentPaneEnabled": data_dict.get('resource_view', {})\
                .get('nav_pane', False),
        },
    }
