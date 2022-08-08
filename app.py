from operator import indexOf
from flask import Flask, render_template, redirect, url_for
from services_supervisor import ServicesSupervisor
import start_vm


vm1 = ServicesSupervisor("EL UNICO QUE FUNCIONA", '10.1.1.102', method='port', port=4090)

## no van, era para poner mas cosas y que parezca que hay mas servicios
TaskCafe = ServicesSupervisor("TaskCafe", '10.1.1.102', method='port', port=3333)
Homeassistant = ServicesSupervisor("Homeassistant", '10.1.1.99', method='port', port=8123)
PiHole = ServicesSupervisor("Pihole", '10.1.1.101', method='ping')
Homer = ServicesSupervisor("Homer", '10.1.1.102', method='port', port=12345)

list_services = [vm1, TaskCafe, Homeassistant, PiHole, Homer]
list_services_names = [service.service_name for service in list_services]

app = Flask(__name__)


#function to separate in diferent lists the list if is greater than 3 and the rest leave in oher list
def split_list(list_to_split, n):
    return [list_to_split[i:i+n] for i in range(0, len(list_to_split), n)]

def rate_services():
    list_services_status = [service.ServiceStatus() for service in list_services]
    list_ = []
    for service, status in zip(list_services, list_services_status):
        list_.append({'title':service.service_name, 'content':'Average (ms):' + str(status['average']) if status['status'] else 'Down', 'type':'ok' if status['status'] else 'warning'})
    list_ = split_list(list_, 3)
    return list_


@app.route("/")
def index():
    cards = rate_services()
    return render_template("index.html",  cards=cards)

@app.route("/app/<string:app>")
def show_app(app):
    #redirect to external web
    sel_serv = list_services[indexOf(list_services_names,app)]
    port = ''
    start_vm(sel_serv.service_name)
    if sel_serv.method == 'port':
        p = str(sel_serv.service_port)
        port = ':' + p
    url = sel_serv.service_ip + port
    return redirect('http://' + url + '/vnc_auto.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('page-404.html'), 404
