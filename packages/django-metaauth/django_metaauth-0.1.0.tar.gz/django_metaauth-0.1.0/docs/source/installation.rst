Installation
============

Requirements
-----------

* Python 3.8 or higher
* Django 3.2 or higher
* Requests 2.25.0 or higher

Installing the package
---------------------

You can install Django MetaAuth using pip:

.. code-block:: bash

    pip install django-metaauth

Or directly from the repository:

.. code-block:: bash

    pip install git+https://github.com/yourusername/django-metaauth.git

Django Configuration
------------------

1. Add "metaauth" to your INSTALLED_APPS setting:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'metaauth',
    ]

2. Include the metaauth URLconf in your project urls.py:

.. code-block:: python

    from django.urls import path, include

    urlpatterns = [
        ...
        path('meta/oauth/', include('metaauth.urls')),
    ]

3. Run migrations to create the metaauth models:

.. code-block:: bash

    python manage.py migrate

4. Configure your Meta (Facebook) app credentials in your settings.py:

.. code-block:: python

    # Meta (Facebook) App credentials
    METAAUTH_FACEBOOK_APP_ID = 'your-app-id'
    METAAUTH_FACEBOOK_APP_SECRET = 'your-app-secret'
    METAAUTH_FACEBOOK_REDIRECT_URI = 'https://yourdomain.com/meta/oauth/redirect' 