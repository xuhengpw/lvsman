#coding:utf-8
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponseRedirect
from configs.config import Get_data, Add_data
import os

current_path = os.getcwd()
def play(request):
	vip_port = Get_data("vip_nodes","vip",current_path + '/configs/config.ini').display()
	node_ips = Get_data("vip_nodes","nodes",current_path + '/configs/config.ini').display()
	return render_to_response('play.html', {
		'title':'删的就是你',
		'vip_port':vip_port,
		'node_ips':node_ips
		}, context_instance=RequestContext(request))

def del_vip(request):
	check_box_list = request.REQUEST.getlist("check_box_list")
	for ip in check_box_list:
		os.popen("fab del_vip:ip=%s" % (ip))
		os.popen("fab init_config")
	return HttpResponseRedirect('/play/')

def del_node(request):
	check_box_list = request.REQUEST.getlist("check_box_list_1")
	for ips in check_box_list:
		ip = ips.split(':')[0]
		port = ips.split(':')[1]
		now_vip = Get_data("vip_nodes","vip",current_path + '/configs/config.ini').display()
		for vip in now_vip:
			if port in vip:
				os.popen("fab del_node:vip=%s,node=%s" % (vip,ip))
				os.popen("fab init_config")
	return HttpResponseRedirect('/play/')
