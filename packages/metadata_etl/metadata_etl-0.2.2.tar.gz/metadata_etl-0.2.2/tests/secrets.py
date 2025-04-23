"""Test Configuration variables"""

# Note: URLs under https with a self-sign certificate
#       will only work if `ssl_verify == False`
# __APP_URL = 'https://127.0.0.1:8443/dev_metadata'

# Note: URLs under http
#       will only work if `OAUTHLIB_INSECURE_TRANSPORT=1`
# __APP_URL = 'http://127.0.0.1:3000/dev_metadata'

# Note: URLs under https with a valid certificate
#       issued by a certificate authority (CA)
#       will always work!!!

__APP_URL = '<%MYMDC_TEST_WEB_APP_URL%>'
###############################################################################
# Localhost setup:
#
# Listening on http://127.0.0.1:3000
###############################################################################

###############################################################################
# Remote setup:
#
# Listening on PUT_HERE_WEB_APP_URL
###############################################################################

__USER_EMAIL = '<%MYMDC_TEST_USER_EMAIL%>'
__USERNAME = '<%MYMDC_TEXT_USERNAME%>'
__USER_FIRSTNAME = '<%MYMDC_TEST_KEY_FIRSTNAME%>'
__USER_LASTNAME = '<%MYMDC_TEST_KEY_LASTNAME%>'
__CLIENT_ID = '<%MYMDC_TEST_KEY_CLIENT%>'  # noqa
__CLIENT_SECRET = '<%MYMDC_TEST_KEY_SECRET%>'  # noqa

###############################################################################

__OAUTH_TOKEN_URL = '{0}/oauth/token'.format(__APP_URL)
__OAUTH_AUTHORIZE_URL = '{0}/oauth/authorize'.format(__APP_URL)

###############################################################################
#
# Publicly available Variables (Test Purposes)
#
###############################################################################

# OAUTH2 client info used on Unitary tests
CLIENT_OAUTH2_INFO = {
    'email': __USER_EMAIL,
    'id': __CLIENT_ID,
    'secret': __CLIENT_SECRET,
    #
    'auth_url': __OAUTH_AUTHORIZE_URL,
    'token_url': __OAUTH_TOKEN_URL,
    'refresh_url': __OAUTH_TOKEN_URL,
    'scope': '',
}

# User client info used on Unitary tests
USER_INFO = {
    'email': __USER_EMAIL,
    'first_name': __USER_FIRSTNAME,
    'last_name': __USER_LASTNAME,
    'name': __USER_FIRSTNAME + __USER_LASTNAME,
    'nickname': __USERNAME,
    'provider': 'ldap',
    'uid': __USERNAME
}

APP_INFO = {
    "id": __CLIENT_ID,
    "secret": __CLIENT_SECRET,
    "url": __APP_URL,
    "scope": ""
}


###############################################################################
#
# Publicly available Variables (Configuration Purposes)
#
###############################################################################

BASE_API_URL = '{0}/api/'.format(__APP_URL)
