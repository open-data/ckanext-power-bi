from azure.identity import ManagedIdentityCredential, CredentialUnavailableError

from ckan.plugins.toolkit import h, _, config, ObjectNotFound, NotAuthorized


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

    try:
        credential = ManagedIdentityCredential()
    except ValueError:
        raise ObjectNotFound(_("An Azure Client ID has not been configured."))

    err_msg = _("Unable to generate an access token to the Power BI Report.")

    try:
        access_token_obj = credential.get_token(
            'https://analysis.windows.net/powerbi/api/.default')
    except CredentialUnavailableError:
        raise NotAuthorized(err_msg)

    access_token = getattr(access_token_obj, 'token', None)
    if not access_token:
        raise NotAuthorized(err_msg)

    return {
        "type": "report",
        "tokenType": 1,
        "accessToken": access_token,
        "embedUrl":
            "https://app.powerbi.com/reportEmbed?reportId=%s&groupId=%s&language=%s" \
                % (report_id, workspace_id, h.lang()),
        "id": report_id,
        "permissions": 'Read',
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
