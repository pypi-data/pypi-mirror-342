Usage
=====

This guide covers how to use Django MetaAuth in your Django project.

OAuth Flow
---------

The basic OAuth flow with Meta (Facebook) consists of these steps:

1. Redirect the user to the Meta authentication page
2. User authorizes your app
3. Meta redirects back to your app with an authorization code
4. Your app exchanges the code for an access token
5. Access token is stored for future API calls

Initiating the OAuth Flow
------------------------

To initiate the OAuth flow, direct your users to the install URL:

.. code-block:: html

    <a href="{% url 'meta-install' %}">Connect with Meta</a>

This will redirect them to Meta's authentication page where they can authorize your app.

Handling Tokens
--------------

After successful authentication, the access token is stored in the Token model. You can retrieve it in your views like this:

.. code-block:: python

    from metaauth.models import Token
    
    def your_view(request):
        # Get the most recent token
        token = Token.objects.latest('created_at')
        access_token = token.token
        
        # Use the token for Meta API calls
        # ...
        
        return render(request, 'your_template.html')

Custom Success and Error Pages
----------------------------

You can create custom success and error pages by overriding the templates:

1. Create a template at `templates/metaauth/success.html` in your project
2. Create a template at `templates/metaauth/error.html` in your project

Django will use your custom templates instead of the default ones provided by the app.

Alternatively, you can configure different URLs for success and error redirects:

.. code-block:: python

    METAAUTH_SUCCESS_URL = '/your-custom-success-url/'
    METAAUTH_ERROR_URL = '/your-custom-error-url/' 