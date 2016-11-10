from flask import render_template, flash, redirect, request
from app import app
from .forms import LoginForm
import os
# index view function suppressed for brevity
@app.route('/')
@app.route('/index')
def index():
    return "<h2>/root</h2>"
@app.errorhandler(404)
def page_not_found(error):
    return 'URL tidak tersedia', 404
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])
@app.route('/ap')
def ap():
    return render_template('ap/index.html')

@app.route('/ap_setup',methods=['GET','POST'])
def ap_setup():
    return render_template('ap/setup.html')\

@app.route('/simpan_interfaces',methods=['POST'])
def simpan_interfaces():
    interface = request.form['interface']
    ip = request.form['ip']
    netmask = request.form['netmask']
    os.system('ifconfig ' + interface + ' inet ' + ip + ' netmask ' + netmask)
    return ''
@app.route('/simpan_route',methods=['POST'])
def simpan_route():
    gw = request.form['gw']
    dns1 = request.form['dns1']
    dns2 = request.form['dns2']
    os.system('route add default gw ' + gw)
    return ''

@app.route('/nat',methods=['GET','POST'])
def nat():
    import os
    nat = request.form['nat']
    interface = request.form['interface']

    if nat=='1':
        f = open('/proc/sys/net/ipv4/ip_forward', 'w')
        f.write('1')
        f.close()
        os.system('iptables -t nat -A POSTROUTING -o '+interface+' -j MASQUERADE')
    elif nat=='0':
        f = open('/proc/sys/net/ipv4/ip_forward', 'w')
        f.write('0')
        f.close()
        os.system('iptables -F')
    f = open('/proc/sys/net/ipv4/ip_forward', 'rb')
    status = f.read()
    f.close()
    return status

@app.route('/simpan_data',methods=['POST','GET'])
def simpan_data():
    data = request.form['json']
    return data

@app.route('/konfig',methods=['GET','POST'])
def konfig():
    param = request.form['param']
    if param=='interfaces':
        import netifaces
        interfaces = netifaces.interfaces()
        results = {}
        for iface in interfaces :
            macaddr = netifaces.ifaddresses(iface)[netifaces.AF_LINK][0]['addr']
            results[iface]=macaddr
        return render_template('ap/interfaces.html',data=results,adapter=app.config['ADAPTER'])

    elif param=='ipaddress':
        import netifaces
        gws = netifaces.gateways()
        if len(gws['default']) ==0:
            gws['default']['0.0.0.0','lo']
        else:
            gws['default'][netifaces.AF_INET]
        interfaces = netifaces.interfaces()
        results = {}
        for iface in interfaces :
            ipaddress = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']
            netmask = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['netmask']
            results[iface]=ipaddress,netmask
        with open("/etc/resolv.conf", "r") as readFile:
            dns = [line.split(" ")[1].strip() for line in readFile.readlines() if line.startswith("nameserver")]
        with open("/proc/sys/net/ipv4/ip_forward", "r") as readFile:
            nat = readFile.read()
        return render_template('ap/ipaddress.html',gws=gws,dns=dns,nat=nat,data=results,adapter=app.config['ADAPTER'])

    elif param=='baca':
        f = open('/etc/network/interface','r')
        status = f.read()
        f.close()
        return status
