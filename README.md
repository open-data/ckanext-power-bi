[![Tests](https://github.com/open-data/ckanext-power-bi/workflows/Tests/badge.svg?branch=main)](https://github.com/open-data/ckanext-power-bi/actions)

# ckanext-power-bi

CKAN Extentsion for Power BI itegration


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

- Require Locales. Defaults to `None`, meaning that there will be no locale support other than the above Power BI Multiple-Language Reports. `True` means that all offered locales are required fields. `False` means that only the default locale is required, and all other locales are optional.

  *Required:* `False`

  *Default:* `None`

  ```
  ckanext.power_bi.require_locales = True|False
  ```

- Offered Locales. A string list of supported locales. The CKAN Core ones will be used by default.

  *Required:* `False`

  *Default:* `The CKAN Core available locales`

  ```
  ckanext.power_bi.locales_offered = en es fr
  ```


## MSI Configuration

This plugin uses `ManagedIdentityCredential (MSI)` on a system level to authenticate with Azure.

See: https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/qs-configure-portal-windows-vm

See: https://pypi.org/project/azure-identity/
Section: Authenticate with a system-assigned managed identity

## License

[MIT](https://raw.githubusercontent.com/open-data/ckanext-power-bi/master/LICENSE)
