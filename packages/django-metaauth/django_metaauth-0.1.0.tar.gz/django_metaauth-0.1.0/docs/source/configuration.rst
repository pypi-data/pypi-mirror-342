Configuration
=============

Django MetaAuth can be configured with the following settings in your Django project's settings.py file:

Basic Settings
-------------

METAAUTH_FACEBOOK_APP_ID
~~~~~~~~~~~~~~~~~~~~~~~
Your Facebook App ID. This is required for the app to function.

.. code-block:: python

    METAAUTH_FACEBOOK_APP_ID = 'your-app-id'

METAAUTH_FACEBOOK_APP_SECRET
~~~~~~~~~~~~~~~~~~~~~~~~~~
Your Facebook App Secret. This is required for the app to function.

.. code-block:: python

    METAAUTH_FACEBOOK_APP_SECRET = 'your-app-secret'

METAAUTH_FACEBOOK_REDIRECT_URI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The redirect URI for OAuth. This must match the redirect URI configured in your Facebook App.

.. code-block:: python

    METAAUTH_FACEBOOK_REDIRECT_URI = 'https://yourdomain.com/meta/oauth/redirect'

Advanced Settings
---------------

METAAUTH_FACEBOOK_API_VERSION
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Facebook API version to use. Defaults to 'v21.0'.

.. code-block:: python

    METAAUTH_FACEBOOK_API_VERSION = 'v21.0'

METAAUTH_FACEBOOK_REQUIRED_SCOPES
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Required permission scopes for your app. Defaults to ['ads_management', 'pages_show_list'].

.. code-block:: python

    METAAUTH_FACEBOOK_REQUIRED_SCOPES = ['ads_management', 'pages_show_list']

METAAUTH_FACEBOOK_CONFIG_ID
~~~~~~~~~~~~~~~~~~~~~~~~~
Optional configuration ID for Facebook App. Defaults to None.

.. code-block:: python

    METAAUTH_FACEBOOK_CONFIG_ID = 'your-config-id'

URL Settings
-----------

METAAUTH_SUCCESS_URL
~~~~~~~~~~~~~~~~~~
URL to redirect after successful authentication. Defaults to '/meta/oauth/success'.

.. code-block:: python

    METAAUTH_SUCCESS_URL = '/meta/oauth/success'

METAAUTH_ERROR_URL
~~~~~~~~~~~~~~~~
URL to redirect after failed authentication. Defaults to '/meta/oauth/error'.

.. code-block:: python

    METAAUTH_ERROR_URL = '/meta/oauth/error' 