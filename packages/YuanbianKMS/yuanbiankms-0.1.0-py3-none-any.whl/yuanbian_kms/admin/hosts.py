# -*- coding=utf-8 -*-
from flask import (request, render_template, redirect, url_for, current_app,
                   flash)
from xp_cms.admin import admin_module
from xp_cms.services.hosts_service import HostsService, HostIPPortService
from xp_cms.forms.docker_hosts_form import NewHostForm


@admin_module.route("/studios/manage")
def manage_host():
    hosts = HostsService.list_hosts()
    # container_hosts = []
    # for host in hosts:
    #     host = host[0]
    #     container_num = HostIPPortService.count_hosts(host)
    #     container_used_num = HostIPPortService.count_hosts(host, 1)
    #     container_hosts.append({
    #         "host_name": host,
    #         "container_num": container_num[0],
    #         "container_used_num": container_used_num[0]
    #     })

    return  render_template("admin/hosts/manage_host.html", hosts=hosts)


@admin_module.route("/studios/add", methods=["GET", "POST"])
def new_host():
    form = NewHostForm()
    if form.validate_on_submit():
        host_name = form.host_name.data
        host_ip = form.host_ip.data
        agent_domain = form.agent_domain.data
        host_type = form.host_type.data
        container_maxnumber = form.container_maxnumber.data
        port_start = form.port_start.data
        new_host = {
            "host_name"          : host_name,
            "host_ip"            : host_ip,
            "agent_domain"       : agent_domain,
            "host_type"          : host_type,

        }
        host = HostsService.get_one_by_field(("host_ip", host_ip))
        if host is None:
            try:
                host = HostsService.add_by_dicts(new_host)
            except Exception as e:
                current_app.logger.error(e)
        if host:
            if port_start == 0:
                port_start = 10000

            for i in range(container_maxnumber):
                lab_port = port_start
                web_port = port_start+1
                try:
                    container = HostIPPortService.check_port_exits( host_ip, (lab_port, web_port))
                except Exception as e:
                    current_app.logger.error(e)
                else:
                    port_start += 2
                    if container:
                        flash(f"port:{lab_port}, {web_port} 已经存在，拒绝录入")
                        continue

                    container_port = {
                        "host_ip": host_ip,
                        "container_lab_port": f"{lab_port}",
                        "container_web_port": f"{web_port}",
                    }
                    HostIPPortService.add_by_dicts(container_port)


        return redirect(url_for("admin.manage_host"))
    return render_template("admin/hosts/new_host.html", form=form)


@admin_module.route("/studios/test_container")
def test_container():
    pass