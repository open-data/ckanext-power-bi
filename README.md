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

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

    git clone --branch master --single-branch https://github.com/open-data/ckanext-power-bi.git
    cd ckanext-power-bi
    pip install -e .
    pip install -r requirements.txt

3. Add `power_bi` to the `ckan.plugins` setting in your CKAN
   config file

4. Restart CKAN

## Config settings

```
N/A
```

## License

[MIT](https://raw.githubusercontent.com/open-data/ckanext-power-bi/master/LICENSE)
