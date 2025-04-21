# Corporation Handouts

*This module is under development. Use at your own risks.*

AA module for managing corporation handouts and especially to keep tracks of their fits/ammo to know if they should be fixed.

[![release](https://img.shields.io/pypi/v/aa-corphandouts?label=release)](https://pypi.org/project/aa-corphandouts/)
[![python](https://img.shields.io/pypi/pyversions/aa-corphandouts)](https://pypi.org/project/aa-corphandouts/)
[![django](https://img.shields.io/pypi/djversions/aa-corphandouts?label=django)](https://pypi.org/project/aa-corphandouts/)
[![license](https://img.shields.io/badge/license-MIT-green)](https://gitlab.com/r0kym/aa-corphandouts/-/blob/master/LICENSE)

## Features:

### Screenshots

![index view](./images/index.png)

![doctrine view](./images/doctrine.png)

![corrections view](./images/corrections.png)

## Installation

### Step 1 - Check prerequisites

1. Corporation handouts is a plugin for Alliance Auth. If you don't have Alliance Auth running already, please install it first before proceeding. (see the official [AA installation guide](https://allianceauth.readthedocs.io/en/latest/installation/auth/allianceauth/) for details)
2. The app requires you to have two other applications installed to work properly:
   1. [fittings](https://gitlab.com/colcrunch/fittings)
   2. [allianceauth-corp-tools](https://github.com/Solar-Helix-Independent-Transport/allianceauth-corp-tools/tree/master)

Make sure to have both properly installed before continuing

### Step 2 - Install app

Make sure you are in the virtual environment (venv) of your Alliance Auth installation. Then install the newest release from PyPI:

```bash
pip install aa-corphandouts
```

### Step 3 - Configure Auth settings

Configure your Auth settings (`local.py`) as follows:

- Add `'corphandouts'` to `INSTALLED_APPS`
- Add below lines to your settings file:

```python
CELERYBEAT_SCHEDULE['corphandouts_update_all'] = {
    'task': 'corphandouts.tasks.update_all_doctrine_reports',
    'schedule': crontab(minute='0', hour='*/1'),
}
```

### Step 4 - Finalize App installation

Run migrations & copy static files

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

Restart your supervisor services for Auth.

## Permissions

Permissions overview.

| Name         | Description                             |
|--------------|-----------------------------------------|
| basic_access | Can access the module and see doctrines |



## Commands

The following commands can be used when running the module:

| Name                   | Description                              |
|------------------------|------------------------------------------|
| corphandouts_check_all | Updates all doctrine reports in the auth |
