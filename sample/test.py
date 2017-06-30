#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import urllib2
import json

class NbService():
    def __init__(self, param):
        self.param = param

    def createRequest(self, path, data):
        url = self.param["baseUrl"] + "/1/" + self.param["tenantId"] + path
        req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
        req.set_proxy("proxygate2.nic.nec.co.jp:8080", "http") # TODO
        req.add_header("X-Application-Id", self.param["appId"])
        req.add_header("X-Application-Key", self.param["appKey"])
        return req

service = NbService({
    "baseUrl": "http://10.164.187.1/api",
    "tenantId": "586da91204e80e089380c531",
    "appId": "586da92104e80e089380c535",
    "appKey": "x80K1BilZVurWiKJFibTvkLfVcOFrpEdvwXkj59b"
});

# login test
data = {
    "username": "user1",
    "password": "Passw0rD"
}

req = service.createRequest("/login", json.dumps(data))

#req = urllib2.Request(baseUrl + "/1/" + tenantId + "/login", json.dumps(data), {'Content-Type': 'application/json'})
#req.set_proxy("proxygate2.nic.nec.co.jp:8080", "http")
#req.add_header("X-Application-Id", appId)
#req.add_header("X-Application-Key", appKey)

f = urllib2.urlopen(req)
res = f.read()
print "Response=", res

json = json.loads(res)
print "sessionToken=", json["sessionToken"]








