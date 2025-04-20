# Fittings

![pypi latest version](https://img.shields.io/pypi/v/fittings?label=latest)
![python versions](https://img.shields.io/pypi/pyversions/fittings)
![django versions](https://img.shields.io/pypi/djversions/fittings?label=django)
![license](https://img.shields.io/pypi/l/fittings?color=green)

A simple fittings and doctrine management app for [allianceauth](https://gitlab.com/allianceauth/allianceauth).

## Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Updating](#updating)
- [Settings](#settings)
- [Permissions](#permissions)

## Overview

This plugin serves as a replacement for the now defunct fleet-up service integration. It allows you to create and manage ship fits and doctrines all in a
central location for your members to browse.

## Key Features

Fittings offers the following features:

- Support for importing fittings using the EFT format.
  - Support for pulling fits from ESI _Coming Soon_
- Support for exporting fits as EFT format.
- Support for saving fits to EVE via ESI.
- Support for copying fits for use with **_Buy All_**.
- Categorization of your fittings and doctrines to keep things organized
  and easy to manage.
  - Access to categories can be restricted to specific groups.
- Tracks changes to module names.
- [AA-Discordbot](https://github.com/pvyParts/allianceauth-discordbot) Integration for searching/posting fits to discord

## Screenshots

### Dashboard/Doctrine List

![dashboard/doctrine list](https://i.imgur.com/AUla6oR.png)

### Add Fitting

![add fitting](https://i.imgur.com/09Ht3Zy.png)

### Fitting List

![fitting list](https://i.imgur.com/JTyaot7.png)

### View Fitting

![view fitting](https://i.imgur.com/3H2PgXC.png)

### Add Doctrine

![add doctrine](https://i.imgur.com/WWSJHmb.png)

### View Doctrine

![view doctrine](https://i.imgur.com/9IJN3jt.png)

### Add a Category

![add category](https://i.imgur.com/0ytpF66.png)

### View all Categories

![view all categories](https://i.imgur.com/kRyr34p.png)

### View a Category

![view category](https://i.imgur.com/hs7DDqp.png)

## Installation

### 0. Check your MariaDB version

Though AllianceAuth and most of the community plugins available for it work just fine on MariaDB versions in the 10.3 and 10.4
range, this plugin requires version 10.5 or greater.

For instructions on installing newer versions of MariaDB please refer to their documentation [here](https://mariadb.org/download/?t=repo-config)

### 1. Install App

Install the app into your allianceauth virtual environment via PIP.

```bash
$ pip install fittings
```

While the [AA-Discordbot](https://github.com/pvyParts/allianceauth-discordbot) cog is included with the fittings module,
if it is not already installed you can install it along with fittings by using the following command instead (doing so will also ensure the right version is installed if you already have it):

```bash
$ pip install fittings[discordbot]
```

### 2. Configure AA settings

Configure your AA settings (`local.py`) as follows:

- Add `'eveuniverse',` and `'fittings',` to `INSTALLED_APPS`
- Add these line to the bottom of the settings file to have module name updates

### 3. Finalize Install

Run migrations and copy static files.

```bash
$ python manage.py migrate
$ python manage.py collectstatic
```

Restart your supervisor tasks.

### 4. Populate Types

Now that fittings has transitioned to using [django-eveuniverse](https://gitlab.com/ErikKalkoken/django-eveuniverse) to handle static data this step is optional.

You can choose to run the following command to preload the type information for most ships and modules in the game, or you can skip this step and let them be created on an as-needed basis.

Keep in mind that running this command will take a while but will save you time later, if you do not run this command adding fits may take some time if they contain new types.

```bash
$ python manage.py fittings_preload_data
```

## Updating

To update your existing installation of Fittings first enable your virtual environment.

Then run the following commands from your allianceauth project directory (the one that contains `manage.py`).

```bash
$ pip install -U fittings
$ python manage.py migrate
$ python manage.py collectstatic
```

Lastly, restart your supervisor tasks.

_Note: Be sure to follow any version specific update instructions as well. These instructions can be found on the `Tags` page for this repository._

## Settings

| Setting                             | Default | Description                  |
| ----------------------------------- | ------- | ---------------------------- |
| `FITTINGS_AADISCORDBOT_INTEGRATION` | `True`  | Enables the AADiscordbot cog |

## Permissions

| Permission                | Description                                       |
| ------------------------- | ------------------------------------------------- |
| `fitting.access_fittings` | This permission gives users access to the plugin. |
| `doctrine.manage`         | User can add/delete ship fits and doctrines.      |

## Active Developers

- [Col Crunch](http://gitlab.com/colcrunch)
- [Crashtec](https://gitlab.com/huideaki)
