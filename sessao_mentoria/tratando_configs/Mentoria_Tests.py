#!/usr/bin/python 
# coding=UTF-8 
import json


#Tratar a entrada dados
template_string_alert = "info {}"
stream = open("config_test.json", "r")
configs = json.loads(stream.read())
print(template_string_alert.format(configs["metric"]))
stream.close()