# -*- coding=utf-8 -*-


import requests, json, random, time, base64, uuid
from flask import request, render_template, flash, redirect, url_for, g, current_app
from flask_login import current_user
from .member_module import member_module
from xp_cms.services.hosts_service import HostIPPortService
from quick_encrypt.quick_aes import encode_data, decode_data
from xp_cms.extensions import nosql


@member_module.route("/hosts/apply")
def hosts_apply():
    username = current_user.username
    docker_host = HostIPPortService.get_one_by_field(("container_user", username))
    if docker_host:
        # TODO 如果已经拥有直接跳转到工作台
        return redirect("/")

    docker_host = HostIPPortService.get_free_container(HOST_NAME, username)
    if docker_host:
        # TODO
        passwd = "".join(random.choices(PASSWD_STR, k=10))
        # 创建队列
        data = {
            "container_image": IMAGE_NAME,
            "username": username,
            "network": docker_host.container_network,
            "ip": docker_host.container_ip,
            "port": docker_host.container_port,
            "password": passwd

        }
        # 写入队列
        pass
        data = encrypt_content(json.dumps(data), "AES", AES_KEY, "utf-8")
        res = requests.post("http://"+HOST_NAME+":5010/create_host", data={"data":data})
        res = decrypt_content(res.text, "AES", AES_KEY, "utf-8")
        if res.find("success")!=-1:
            docker_host.container_status = 1
            docker_host.container_endtime = round(time.time()) + 30*24*3600
            docker_host.container_passwd = passwd
            HostIPPortService.update(docker_host)
            return redirect(url_for("member.myhosts"))
        else:
            return res

@member_module.route("/studio/mystudio")
def mystudio():
    docker_host = HostIPPortService.get_one_by_field(("container_user", current_user.username))
    host = None
    container_host_name = None
    token = None
    bio_package = "/mall/create_order/bio_21009"
    netio_package = "/mall/create_order/netio_32100"
    docker_status_api = None
    if docker_host:
        host = True
        container_host_name = docker_host.container_host_name
        api_secret_key = current_app.config['SSO_SECRET_KEY']
        data = {"r": random.random(), "username": current_user.username, "time": time.time() }
        token = encode_data(data, api_secret_key)
        docker_status_api = f"{container_host_name}_{current_app.config['STATUS_API_HOST']}/"

    return render_template("member/{0}/studio/mystudio.html".format(g.client),
                           host=host,
                           docker_status_api=docker_status_api,
                           token=token,
                           bio_package=bio_package,
                           netio_package=netio_package,
                           )


@member_module.route("/host/jupyterlab")
def jupyterlab():
    return redirect(url_for("run_code.jupyterlab"))
