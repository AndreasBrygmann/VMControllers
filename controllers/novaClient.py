from novaclient import client as novaclient
from keystoneauth1 import session
from keystoneauth1.identity import v3

def NovaClient():

    auth = v3.ApplicationCredential(auth_url='',
                                    application_credential_id='',
                                    application_credential_secret='')
    sess = session.Session(auth=auth)
    nova = novaclient.Client("2.0", session=sess)
    return nova