from typing import Set
import uuid
from django import template
from django.db.models.base import Model
from django.http.response import HttpResponse, HttpResponseForbidden
from django.http.request import HttpRequest
from django.shortcuts import render
from django.template import loader
from datetime import datetime
from base64 import b64decode
from . import models


def is_credential_valid(request: HttpRequest) -> models.Credential:
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            if auth[0].lower() == "basic":
                uname, passwd = b64decode(auth[1]).decode('utf-8').split(':')
                try:
                    id = uuid.UUID(uname)
                    key = uuid.UUID(passwd)
                    cred: models.Credential = models.Credential.objects.get(
                        id=id)
                    if cred.key == key:
                        return cred
                    else:
                        return None
                except models.Credential.DoesNotExist:  # User doesn't exist
                    return None
                except ValueError:  # Malformed UUID or auth string
                    return None
    return None

# Create your views here.


def create_user(request: HttpRequest):
    template = loader.get_template('create_user.html')
    credential = models.Credential()
    credential.save()
    context = {
        'id': credential.id,
        'key': credential.key,
    }
    return HttpResponse(template.render(context, request))


def update_ip(request: HttpRequest):
    credential = is_credential_valid(request)
    if credential == None:
        return HttpResponseForbidden()

    hostname: str = request.GET['hostname']
    address: str = request.GET['myip']

    host: models.Host = {}
    existed = False

    try:
        host = models.Host.objects.get(hostname=hostname, user=credential.id)
        existed = True
        host.address = address
        host.save()
    except models.Host.DoesNotExist:
        host = models.Host()
        host.hostname = hostname
        host.address = address
        host.updated = datetime.now()
        host.user = credential
        host.save()
    # ignore Model.MultipleObjectsReturned and let it throw

    template = loader.get_template('updated.html')
    context = {
        'hostname': hostname,
        'address': address,
        'existed': existed
    }
    return HttpResponse(template.render(context, request))


def query_hosts_by_cred(request: HttpRequest):
    credential = is_credential_valid(request)
    if credential == None:
        return HttpResponseForbidden()

    hosts = models.Host.objects.filter(user=credential.id)
    hosts_set: Set[models.Host] = set(hosts)

    template = loader.get_template('query_hosts.html')
    context = {
        'hosts': hosts_set
    }
    return HttpResponse(template.render(context, request))


def query_ip_by_hostname(request: HttpRequest):
    hostname: str = request.GET['hostname']

    try:
        host = models.Host.objects.get(hostname=hostname)
        template = loader.get_template('updated.html')
        context = {
            'hostname': hostname,
            'address': host.address,
        }
        return HttpResponse(template.render(context, request))
    except models.Host.DoesNotExist:
        return FileNotFoundError()
