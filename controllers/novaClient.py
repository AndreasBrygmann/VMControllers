from novaclient import client as novaclient
from keystoneauth1 import session
from keystoneauth1.identity import v3

def NovaClient():

    auth = v3.ApplicationCredential(auth_url='https://pegasus.sky.oslomet.no:5000/v3',
                                    application_credential_id='bf1cb183404d4490ae0d04f3737c4c9a',
                                    application_credential_secret='6stPHUnryXuL9Yo_3TWqVnm7jWodPYBJzv5SyUpXfPzm4ZCK0W739bH4QXuqHwIwMkBK6nGopXVTRDnTlfCbqg')
    sess = session.Session(auth=auth)
    nova = novaclient.Client("2.0", session=sess)
    return nova