# Odoo 17 Project

This repository contains an Odoo 17 setup with a custom module named app_one, including custom property management features, OWL-based client actions, reports, wizard flows, and model extensions.

## Features

- Odoo 17 base installation
- Custom addon: app_one
- Property management module with:
  - property records
  - owner and tag management
  - property history tracking
  - sale order and account move integration
  - custom state transitions and wizard flow
- OWL-based list view client action
- XLSX report generation
- Custom menus and views

## Prerequisites

Before running the project, make sure you have:

- Python 3.10 or 3.11
- PostgreSQL installed and running
- Odoo 17 source code in the workspace
- wkhtmltopdf installed and available in your PATH
- A PostgreSQL database user created for Odoo

## Recommended Environment

- Windows 10/11
- VS Code or PyCharm
- Git

## Clone the Repository

```bash
git clone <your-repo-url>
cd odoo17
```

## Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

## Install Python Dependencies

```bash
pip install -r odoo17\requirements.txt
```

## Database Setup

Create a PostgreSQL database and user, for example:

```sql
CREATE DATABASE odoo17;
CREATE USER odoo WITH PASSWORD 'odoo';
ALTER ROLE odoo WITH SUPERUSER;
```

## Configure Odoo

The configuration file is already available at:

- [odoo.conf](odoo.conf)

Make sure the addons path includes your custom module folder:

```ini
addons_path = C:\Users\ith\PycharmProjects\odoo17\odoo17\addons,
    C:\Users\ith\PycharmProjects\odoo17\odoo17\odoo\addons,
    C:\Users\ith\PycharmProjects\odoo17\custom_addons
```

## Run Odoo

Start the Odoo server with:

```bash
python odoo17\odoo-bin -c odoo.conf -d odoo17
```

Then open your browser at:

```text
http://127.0.0.1:8069
```

## Install the Custom Module

After the server starts:

1. Open Odoo in the browser
2. Log in with your admin account
3. Go to Apps
4. Search for app_one
5. Click Install

## Useful Commands

- Start server:
  ```bash
  python odoo17\odoo-bin -c odoo.conf -d odoo17
  ```

- Install module from terminal:
  ```bash
  python odoo17\odoo-bin -c odoo.conf -d odoo17 -i app_one --stop-after-init
  ```

- Update module from terminal:
  ```bash
  python odoo17\odoo-bin -c odoo.conf -d odoo17 -u app_one --stop-after-init
  ```

## Notes

- If the custom OWL view does not appear, refresh the browser and make sure the app_one module is installed and the server has been restarted.
- For Windows, ensure that wkhtmltopdf is installed and the path is correctly configured in [odoo.conf](odoo.conf).
