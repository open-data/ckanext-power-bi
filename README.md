[![Tests](https://github.com/open-data/ckanext-power-bi/workflows/Tests/badge.svg?branch=main)](https://github.com/open-data/ckanext-power-bi/actions)

# ckanext-power-bi

CKAN Extentsion for Power BI itegration. This plugin provides a new Resource View called `Power BI`. This plugin is meant for viewing Power BI Reports only. As such, all embed tokens are only generated with `View` permissions. This also means that the panes inside of the embedded reports will be limited to the View Only panes (exception for the Bookmarks pane, for any existing Report Bookmarks).


## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.6 and earlier | Not tested    |
| 2.7             | Not tested    |
| 2.8             | Not tested    |
| 2.9             | Yes    |

| Python version    | Compatible?   |
| --------------- | ------------- |
| 2.9 and earlier | Yes    |
| 3.0 and later             | Not tested    |

## Installation

To install ckanext-power-bi:

1. Activate your CKAN virtual environment, for example:

     `. /usr/lib/ckan/default/bin/activate`

2. Clone the source and install it on the virtualenv

    - `git clone --branch master --single-branch https://github.com/open-data/ckanext-power-bi.git`
    - `cd ckanext-power-bi`
    - `pip install -e .`
    - `pip install -r requirements.txt` (`requirements-py2.txt` for Python 2)

3. Add `power_bi_view` to the `ckan.plugins` setting in your CKAN
   config file

4. Restart CKAN

## Config settings

- The Power BI Workspace ID (a.k.a. Group ID).

  *Required:* `True`

  *Default:* `None`

  ```
  ckanext.power_bi.workspace_id = <Power BI Workspace ID>
  ```
- The Power BI / Azure Organization (tennant) name. This option is more for future proofing the Power BI API endpoints within this code. Currently, the Power BI API does not support specific tennant/organization targeting.

  *Required:* `False`

  *Default:* `myorg`

  ```
  ckanext.power_bi.org_name = <Power BI / Azure Organization ID>
  ```

### i18n Support

By default, the view will request the Power BI Report in the current language of CKAN. This assumes that you are using [Multiple-Language Reports](https://learn.microsoft.com/en-us/power-bi/guidance/multiple-language-translation)

For more information on how to set up your Reports for translation, see [this blog post.](https://powerbi.microsoft.com/en-ca/blog/building-multi-language-reports-for-power-bi-in-2023/)

If you are not using Power BI Multiple-Language Reports, you are able to enable locale support in this plugin. This will add Report ID fields for each supported locale.

- Enable internal i18n support. Specifies to use the multiple language fields instead of the Power BI Multiple-Language Reports. Use this if you are not translating your Reports in Power BI.

  *Required:* `False`

  *Default:* `False`

  ```
  ckanext.power_bi.internal_i18n = True
  ```

- Offered Locales. A string list of supported locales. The CKAN Core ones will be used by default.

  *Required:* `False`

  *Default:* `The CKAN Core available locales`

  ```
  ckanext.power_bi.locales_offered = en es fr
  ```

- Required Locales. A string list of locales which will be required for the view Report ID fields. The CKAN default locale will ALWAYS be a required locale, even if it is omitted from this list.

  *Required:* `False`

  *Default:* `CKAN default locale`

  ```
  ckanext.power_bi.required_locales = en fr
  ```


## MSI Configuration

This plugin uses `ManagedIdentityCredential (MSI)` on a system level to authenticate with Azure.

See: https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/qs-configure-portal-windows-vm

See: https://pypi.org/project/azure-identity/ (section: Authenticate with a system-assigned managed identity)

## License

[MIT](https://raw.githubusercontent.com/open-data/ckanext-power-bi/master/LICENSE)
