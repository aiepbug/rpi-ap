WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]

INTERFACES = [
    {'name':'lo','type':'loopback','macaddress':'00:00:00:00:00:00'},
    {'name':'wlan0','type':'wireless','macaddress':'00:21:6a:1f:db:60'}]
ADAPTER = {
            'lo':['00:00:00:00:00:00','loopback','127.0.0.1','255.255.255.0'],
            'wlan0':['00:21:6a:1f:db:60','wireless','192.168.0.1','255.255.255.0']
            }