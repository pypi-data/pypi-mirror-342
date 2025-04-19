# -*- coding=utf-8 -*-
import os, requests, time, random
from requests.exceptions import SSLError
from flask import request, render_template, redirect, url_for,\
    json, current_app
from xp_cms.admin.__main__ import admin_module
from xp_cms.services.user_service import UserService
from xp_cms.services.hosts_service import HostsService, HostIPPortService
from xp_cms.forms.docker_hosts_form import DockerSearchForm, NewStudioForm
from xp_cms.libs.lab_manage import LabManage
from xp_cms.libs.myrsa import MyRsa


myrsa = MyRsa()
@admin_module.route("/studios/launch_studio")
def launch_studio():
    launch_form = NewStudioForm()
    launch_form.agent_domain.choices = [(domain, domain) for domain in NGINX_AGENT_SERVER.keys()]
    if launch_form.validate_on_submit():
        username = launch_form.username.data
        container_type = launch_form.container_type.data
        agent_domain = launch_form.agent_domain.data
        lab_manage = LabManage(username. container_type)

    return render_template("admin/studios/launch_studio.html", launch_form=launch_form)

@admin_module.route("/studios/manage_studio/")
@admin_module.route("/studios/manage_studio/<int:page>")
def manage_studio(page=1):
    search_form = DockerSearchForm()
    launch_form = NewStudioForm()
    q = None
    order = None
    if search_form.validate_on_submit():
        q = search_form.q.data
        field = search_form.field.data
        order = search_form.order.data
        status = search_form.status.data

    else:
        q = request.args.get("q")
        field = request.args.get("field")
        order = request.args.get("order")
        status = request.args.get("status")
        if field not in dict(search_form.field.choices):
            field = search_form.field.choices[0][0]
        if order not in dict(search_form.order.choices):
            order = search_form.order.choices[0][0]
    if q:
        search_form.q.data = q
        search_form.field.data = field
        if field == "host_ip":
            operator = "eq"
        else:
            operator = 'like'
            q = f'%{q}%'
        conditions = [{"field": field, "value": q, "operator": operator}]
    else:
        conditions = []

    if status in dict(search_form.status.choices):
        search_form.status.data = status
        conditions.append({"field": "container_user", "value": None, "operator": "eq" if status=="0" else "neq"})

    if order:
        search_form.order.data = order
        order = {"field": "container_id", "type": ["asc", "desc"][int(order)-1]}
    lab_studios = HostIPPortService.get_many(conditions, page=page, order=order)
    return render_template("admin/studios/manage_studios.html",
                           search_form=search_form,
                           launch_form=launch_form,
                           lab_studios=lab_studios)


@admin_module.route("/studios/exists_container", methods=["POST"])
def exist_container():
    username = request.form.get("username")
    t = int(random.random()*1e10)
    ip = request.form.get("ip")
    message = {"username": username, "t": t}
    message = json.dumps(message)
    sign = myrsa.base64_encode(myrsa.rsa_encrypt(message, f"ssl_files/{ip}_public.key"))
    exists_url = f"http://{ip}:5010/exists_container?sign={sign}&t={t}"
    try:
        res = requests.get(exists_url)
    except Exception as e:
        current_app.logger.error(e)
        return json.jsonify({"error": 10001, "error_message": str(e)})
    else:
        return json.jsonify(res.json())

@admin_module.route("/studios/create_container", methods=["POST"])
def create_container():
    username = request.form.get("username")
    try:
        user_info = UserService.get_user_by_username(username)
        assert user_info != None
    except Exception as e:
        return {"error": 10000, "error_message":"用户不存在"}
    t = int(random.random()*1e10)
    ip = request.form.get("ip")
    container_type = request.form.get("container_type")
    message = {"username": username, "userid": user_info.user_id, "t": t}
    message = json.dumps(message)
    sign = myrsa.base64_encode(myrsa.rsa_encrypt(message, f"ssl_files/{ip}_public.key"))
    create_url = f"http://{ip}:5010/create_lab?sign={sign}&t={t}"
    form_data = {
        "bsoft": "50g",
        "bhard": "55g",
        "docker_image": "192.168.3.50:19000/jupyterlab:1.5",
        "common_python_lib": "/common_python_lib"
    }
    container_option = {
        "basic": {"bsoft": "50g", "bhard": "55g", "mem_limit": "4g"},
        "ai": {"bsoft": "100g", "bhard": "120g", "mem_limit": "8g"},
        "bigdata": {"bsoft": "200g", "bhard": "250g", "mem_limit": "16g"}
    }
    form_data.update(container_option(container_type))
    try:
        lab_studio = HostIPPortService.get_free_container(ip, username)
    except Exception as e:
        return json.jsonify({"error": 10001, "error_message": str(e)})
    if lab_studio:
        form_data['lab_port'] = lab_studio.container_lab_port
        form_data["web_port"] = lab_studio.container_web_port
    else:
        return json.jsonify({"error": 10002, "error_message": "没有闲置的"})
    try:
        res = requests.post(create_url, data=form_data)
    except Exception as e:
        return json.jsonify({"error": 10003, "error_message": str(e)})
    return res.json()


@admin_module.route("/studios/launch_studio", methods=["POST"])
def launch_container():
    username = request.form.get("username")
    t = int(random.random()*1e10)
    ip = request.form.get("ip")
    lab_type = request.form.get("container_type")
    message = {"username": username, "lab_type": lab_type, "t": t}
    message = json.dumps(message)
    sign = myrsa.base64_encode(myrsa.rsa_encrypt(message, f"ssl_files/{ip}_public.key"))
    launch_url = f"http://{ip}:5010/launch_lab?sign={sign}&t={t}"

    try:
        res = requests.get(launch_url)
    except Exception as e:
        return json.jsonify({"error": 20001, "error_message": str(e)})
    return res.json()

@admin_module.route("/studios/exist_agent_domain", methods=["POST"])
def exist_agent_domain():
    username = request.form.get("username")
    ip = request.form.get("ip")
    host = HostsService.get_one_by_field(("host_ip", ip))
    user_studio_url = f"https://{username}.{host.agent_domain}"
    try:
        studio_status = requests.get(user_studio_url)
    except SSLError as e:
        status = "0"
        message = "尚未创建"
    except Exception as e:
        print(e)
    else:
        status = "skip"
        message = user_studio_url
    return json.jsonify({"status": status, "message": message})


@admin_module.route("/studios/create_agent_conf", methods=["post"])
def create_agent_conf():
    username = request.form.get("username")
    ip = request.form.get("ip")
    user_host = HostIPPortService.get_one_by_field(("container_user", username))
    t = int(random.random() * 1e10)
    message = {"username": username,

               "ports":{"lab": user_host.container_lab_port,
                        "web": user_host.container_web_port},
               "t": t
               }

    message = json.dumps(message)
    form_data = {"agent_domain": user_host.host.agent_domain,
                 "ip": user_host.host_ip,
                 }
    sign = myrsa.base64_encode(myrsa.rsa_encrypt(message, f"ssl_files/{user_host.host.agent_domain}_public.key"))
    create_conf_url = f"https://yuanbian_admin.{user_host.host.agent_domain}/create_conf?sign={sign}&t={t}"
    try:
        res = requests.post(create_conf_url, data=form_data)
        assert res.status_code == 200
    except SSLError as e:
        status = "50001"
        message = str(e)
    except Exception as e:
        status = "50002"
        message = str(e)
    else:
        status = "0"
        message = f"https://{username}.{user_host.host.agent_domain}"
    return json.jsonify({"error": status, "message": message})