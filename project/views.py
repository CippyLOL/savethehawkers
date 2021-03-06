from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import numpy
import math
from .models import *
from django import forms
from ipstack import GeoLookup
import requests
import json
# NoReverseMatch: edity is not a name - probably didnt indicate app name in some html
# NoReverseMatch: argument (",") does not match.... - didnt include argument when your path requires one <str:...>
# NoReverseMatch: path does not exist - name you put is diff from "name" in urls
class CreateForm(forms.Form):
    latitude = forms.FloatField(label = "Latitude")
    longtitude = forms.FloatField(label = "longtitude")
    name = forms.CharField(label = "name", max_length = 200)
    stalltype = forms.CharField(label = "stalltype", max_length = 50)
    address = forms.CharField(label = "address", max_length = 200)
    hours = forms.CharField(label = "hours", max_length = 300)
    reco = forms.CharField(label = "reco", max_length = 100)
    details = forms.CharField(label = "details", max_length = 1000)
    contributor = forms.CharField(label = "contributor", max_length = 100)

class NewTaskForm (forms.Form):
    search = forms.CharField(label = "Food Recommendation:", min_length = 1, max_length = 50)
    postalcode = forms.IntegerField(label = "Postal Code:", min_value=1, max_value = 999999)

def distance(origin, destination):
 
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km
 
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
 
    return d


def index(request):
    if request.method == "POST":
        history = History.objects.filter(id__in=[1,2,3,4,5,6])
        pagenumber = 1
        postalcode = request.POST["postalcode"]
        if not postalcode:
            return render(request, "project/index.html",{
                "message": "Enter a postal code.",
                "form": NewTaskForm(),
                "postalcode": postalcode,
                "pagenumber": pagenumber,
                "no": "no",
                "history": history
            })
        try:
            val = int(postalcode)
        except ValueError:
            return render(request, "project/index.html",{
                "message": "Please insert a number.",
                "form": NewTaskForm(),
                "postalcode": postalcode,
                "pagenumber": pagenumber,
                "no": "no",
                "history": history
            })
        try:
            address = f"https://developers.onemap.sg/commonapi/search?searchVal={postalcode}&returnGeom=Y&getAddrDetails=Y&pageNum=1"
            response = requests.get(address)
            data = response.text
            parse_json = json.loads(data)
            latorigin = float(parse_json['results'][0]['LATITUDE'])
        except IndexError:
            return render(request, "project/index.html",{
                "message": "Postal Code does not exist!",
                "form": NewTaskForm(),
                "postalcode": postalcode,
                "pagenumber": pagenumber,
                "no": "no",
                "history": history
            })    
        address = f"https://developers.onemap.sg/commonapi/search?searchVal={postalcode}&returnGeom=Y&getAddrDetails=Y&pageNum=1"
        response = requests.get(address)
        data = response.text
        parse_json = json.loads(data)
        latorigin = float(parse_json['results'][0]['LATITUDE'])
        longorigin = float(parse_json['results'][0]['LONGITUDE'])
        place = parse_json['results'][0]['ADDRESS']
    #
        hawk = HawkerStall.objects.all()
        number = [0] * len(hawk)
        count = 0
        for haw in hawk.iterator():
            lat = haw.latitude
            long = haw.longtitude
            origin = (latorigin, longorigin)
            destination = (lat, long)
            km = distance(origin, destination)
            km = km * 1000
            number[count] = round(km)
            count += 1
        #an array of the indexes after sorting
        s = numpy.array(number)
        sort_index = numpy.argsort(s)
        new_list = [x+1 for x in sort_index]
        number.sort()
        latitudes = [0] * len(hawk)
        longtitudes = [0] * len(hawk)
        names = [0] * len(hawk)
        addresses = [0] * len(hawk)
        recos = [0] * len(hawk)
        hours = [0] * len(hawk)
        details = [0] * len(hawk)
        contributors = [0] * len(hawk)
        # this will start from the numbers 4, then to 1, then to 6....
        for i in new_list:
            for j in range(len(addresses)):
                if addresses[j] != 0:
                    j = j+1
                else:
                    ha = HawkerStall.objects.get(id = i)
                    latitudes[j] = ha.latitude
                    longtitudes[j] = ha.longtitude
                    names[j] = ha.name
                    addresses[j] = ha.address
                    recos[j] = ha.reco
                    hours[j] = ha.hours
                    details[j] = ha.details
                    contributors[j] = ha.contributor
                    break
        myhouselat = [latorigin] * len(hawk)
        myhouselong = [longorigin] * len(hawk)
        latandlong = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong2 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong3 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong4 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong5 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong6 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        return render(request, "project/index.html",{
            "postalcode": postalcode,
            "pagenumber": pagenumber,
            "latitudes": latitudes,
            "longtitudes": longtitudes,
            "names": names,
            "addresses": addresses,
            "recos": recos,
            "hours": hours,
            "details": details,
            "contributors": contributors,
            "numbers": number,
            "latandlong": latandlong,
            "latandlong2": latandlong2,
            "latandlong3": latandlong3,
            "latandlong4": latandlong4,
            "latandlong5": latandlong5,
            "latandlong6": latandlong6,
            "form": NewTaskForm()
        })
    history = History.objects.filter(id__in=[1,2,3,4,5,6])
    return render(request, "project/index.html",{
        "no": "no",
        "form": NewTaskForm(),
        "history": history,
    })

def nextindex(request, pagenumber):
    if request.method == "POST":
        page = int(pagenumber) + 1
        postalcode = request.POST["postalcode"]
        if not postalcode:
            return render(request, "project/index.html",{
                "message": "Enter a postal code.",
                "form": NewTaskForm()
            })
        try:
            val = int(postalcode)
        except ValueError:
            return render(request, "project/index.html",{
                "message": "Please insert a number.",
                "form": NewTaskForm()
            })
        try:
            post = Zipcode.objects.get(postal = postalcode)
        except Zipcode.DoesNotExist:
            return render(request, "project/index.html",{
                "message": "Postal Code does not exist in the database!",
                "form": NewTaskForm()
            })
        place = Zipcode.objects.filter(postal = postalcode)
        latorigin = place.first().latitude
        longorigin = place.first().longtitude
    #
        hawk = HawkerStall.objects.all()
        number = [0] * len(hawk)
        count = 0
        for haw in hawk.iterator():
            lat = haw.latitude
            long = haw.longtitude
            origin = (latorigin, longorigin)
            destination = (lat, long)
            km = distance(origin, destination)
            km = km * 1000
            number[count] = round(km)
            count += 1
        #an array of the indexes after sorting
        s = numpy.array(number)
        sort_index = numpy.argsort(s)
        new_list = [x+1 for x in sort_index]
        number.sort()
        latitudes = [0] * len(hawk)
        longtitudes = [0] * len(hawk)
        names = [0] * len(hawk)
        addresses = [0] * len(hawk)
        recos = [0] * len(hawk)
        hours = [0] * len(hawk)
        details = [0] * len(hawk)
        contributors = [0] * len(hawk)
        # this will start from the numbers 4, then to 1, then to 6....
        for i in new_list:
            for j in range(len(addresses)):
                if addresses[j] != 0:
                    j = j+1
                else:
                    ha = HawkerStall.objects.get(id = i)
                    latitudes[j] = ha.latitude
                    longtitudes[j] = ha.longtitude
                    names[j] = ha.name
                    addresses[j] = ha.address
                    recos[j] = ha.reco
                    hours[j] = ha.hours
                    details[j] = ha.details
                    contributors[j] = ha.contributor
                    break
        myhouselat = [latorigin] * (len(hawk) - (6*(page-1)))
        myhouselong = [longorigin] * (len(hawk) - (6*(page-1)))
        latandlong = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong2 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong3 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong4 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong5 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong6 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        return render(request, "project/index.html",{
            "pagenumber": page,
            "postalcode": postalcode,
            "latitudes": latitudes[(6*(page-1)):],
            "longtitudes": longtitudes[(6*(page-1)):],
            "names": names[(6*(page-1)):],
            "addresses": addresses[(6*(page-1)):],
            "recos": recos[(6*(page-1)):],
            "hours": hours[(6*(page-1)):],
            "details": details[(6*(page-1)):],
            "contributors": contributors[(6*(page-1)):],
            "numbers": number[(6*(page-1)):],
            "latandlong": latandlong,
            "latandlong2": latandlong2,
            "latandlong3": latandlong3,
            "latandlong4": latandlong4,
            "latandlong5": latandlong5,
            "latandlong6": latandlong6,
            "form": NewTaskForm()
        })

def stalltype(request):
    if request.method == "POST":
        pagenumber = 1
        stalltypes = request.POST["stalltype"]
        postalcode = request.POST["postalcode"]
        history = History.objects.filter(id__in=[1,2,3,4,5,6])
        try:
            address = f"https://developers.onemap.sg/commonapi/search?searchVal={postalcode}&returnGeom=Y&getAddrDetails=Y&pageNum=1"
            response = requests.get(address)
            data = response.text
            parse_json = json.loads(data)
            latorigin = float(parse_json['results'][0]['LATITUDE'])
        except IndexError:
            return render(request, "project/index.html",{
                "message": "Postal Code does not exist!",
                "form": NewTaskForm(),
                "postalcode": postalcode,
                "pagenumber": pagenumber,
                "no": "no",
                "history": history
            })    
        address = f"https://developers.onemap.sg/commonapi/search?searchVal={postalcode}&returnGeom=Y&getAddrDetails=Y&pageNum=1"
        response = requests.get(address)
        data = response.text
        parse_json = json.loads(data)
        latorigin = float(parse_json['results'][0]['LATITUDE'])
        longorigin = float(parse_json['results'][0]['LONGITUDE'])
        place = parse_json['results'][0]['ADDRESS']
        results = HawkerStall.objects.filter(stalltype = stalltypes)
        if not results:
            return render(request, "project/index.html", {
                "searchmessage": "That shit doesnt exist lmao",
                "form": NewTaskForm()
            })
        number = [0] * len(results)
        count = 0
        for res in results.iterator():
            lat = res.latitude
            long = res.longtitude
            origin = (latorigin, longorigin)
            destination = (lat, long)
            km = distance(origin, destination)
            km = km * 1000
            number[count] = round(km)
            count += 1
        #an array of the indexes after sorting
        s = numpy.array(number)
        sort_index = numpy.argsort(s)
        #original number = [2022, 3104, 1012...]
        #number = [1012, 2022, 3104...]
        #new_list = [3, 1, 2...]
        number.sort()
        latitudes = [0] * len(results)
        longtitudes = [0] * len(results)
        names = [0] * len(results)
        addresses = [0] * len(results)
        recos = [0] * len(results)
        hours = [0] * len(results)
        details = [0] * len(results)
        contributors = [0] * len(results)
        # this will start from the numbers 4, then to 1, then to 6....
        for i in sort_index:
            for j in range(len(addresses)):
                if addresses[j] != 0:
                    j = j+1
                else:
                    ha = results[int(i)]
                    latitudes[j] = ha.latitude
                    longtitudes[j] = ha.longtitude
                    names[j] = ha.name
                    addresses[j] = ha.address
                    recos[j] = ha.reco
                    hours[j] = ha.hours
                    details[j] = ha.details
                    contributors[j] = ha.contributor
                    break
        myhouselat = [latorigin] * len(results)
        myhouselong = [longorigin] * len(results)
        latandlong = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong2 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong3 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong4 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong5 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong6 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        return render(request, "project/stall.html",{
            "pagenumber": pagenumber,
            "stalltypes": stalltypes,
            "postalcode": postalcode,
            "latitudes": latitudes,
            "longtitudes": longtitudes,
            "names": names,
            "addresses": addresses,
            "recos": recos,
            "hours": hours,
            "details": details,
            "contributors": contributors,
            "numbers": number,
            "latandlong": latandlong,
            "latandlong2": latandlong2,
            "latandlong3": latandlong3,
            "latandlong4": latandlong4,
            "latandlong5": latandlong5,
            "latandlong6": latandlong6,
            "form": NewTaskForm()
        })
    return render(request, "project/index.html",{
        "form": NewTaskForm()
    })

def nextstall(request, pagenumber):
    if request.method == "POST":
        page = int(pagenumber) + 1
        stalltypes = request.POST["stalltype"]
        postalcode = request.POST["postalcode"]
        place = Zipcode.objects.filter(postal = postalcode)
        latorigin = place.first().latitude
        longorigin = place.first().longtitude
        results = HawkerStall.objects.filter(stalltype = stalltypes)
        if not results:
            return render(request, "project/index.html", {
                "searchmessage": "That shit doesnt exist lmao",
                "form": NewTaskForm()
            })
        number = [0] * len(results)
        count = 0
        for res in results.iterator():
            lat = res.latitude
            long = res.longtitude
            origin = (latorigin, longorigin)
            destination = (lat, long)
            km = distance(origin, destination)
            km = km * 1000
            number[count] = round(km)
            count += 1
        #an array of the indexes after sorting
        s = numpy.array(number)
        sort_index = numpy.argsort(s)
        #original number = [2022, 3104, 1012...]
        #number = [1012, 2022, 3104...]
        #new_list = [3, 1, 2...]
        number.sort()
        latitudes = [0] * len(results)
        longtitudes = [0] * len(results)
        names = [0] * len(results)
        addresses = [0] * len(results)
        recos = [0] * len(results)
        hours = [0] * len(results)
        details = [0] * len(results)
        contributors = [0] * len(results)
        # this will start from the numbers 4, then to 1, then to 6....
        for i in sort_index:
            for j in range(len(addresses)):
                if addresses[j] != 0:
                    j = j+1
                else:
                    ha = results[int(i)]
                    latitudes[j] = ha.latitude
                    longtitudes[j] = ha.longtitude
                    names[j] = ha.name
                    addresses[j] = ha.address
                    recos[j] = ha.reco
                    hours[j] = ha.hours
                    details[j] = ha.details
                    contributors[j] = ha.contributor
                    break
        myhouselat = [latorigin] * (len(results) - (6*(page-1)))
        myhouselong = [longorigin] * (len(results) - (6*(page-1)))
        latandlong = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong2 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong3 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong4 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong5 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong6 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        return render(request, "project/search.html",{
            "pagenumber": page,
            "stalltypes": stalltypes,
            "postalcode": postalcode,

            "latitudes": latitudes[(6*(page-1)):],
            "longtitudes": longtitudes[(6*(page-1)):],
            "names": names[(6*(page-1)):],
            "addresses": addresses[(6*(page-1)):],
            "recos": recos[(6*(page-1)):],
            "hours": hours[(6*(page-1)):],
            "details": details[(6*(page-1)):],
            "contributors": contributors[(6*(page-1)):],
            "numbers": number[(6*(page-1)):],
            "latandlong": latandlong,
            "latandlong2": latandlong2,
            "latandlong3": latandlong3,
            "latandlong4": latandlong4,
            "latandlong5": latandlong5,
            "latandlong6": latandlong6,
            "form": NewTaskForm()
        })
    return render(request, "project/index.html",{
        "form": NewTaskForm()
    })


def search(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            pagenumber = 1
            search = form.cleaned_data["search"]
            postalcode = form.cleaned_data["postalcode"]
            history = History.objects.filter(id__in=[1,2,3,4,5,6])
        try:
            address = f"https://developers.onemap.sg/commonapi/search?searchVal={postalcode}&returnGeom=Y&getAddrDetails=Y&pageNum=1"
            response = requests.get(address)
            data = response.text
            parse_json = json.loads(data)
            latorigin = float(parse_json['results'][0]['LATITUDE'])
        except IndexError:
            return render(request, "project/index.html",{
                "message": "Postal Code does not exist!",
                "form": NewTaskForm(),
                "postalcode": postalcode,
                "pagenumber": pagenumber,
                "no": "no",
                "history": history
            })    
        address = f"https://developers.onemap.sg/commonapi/search?searchVal={postalcode}&returnGeom=Y&getAddrDetails=Y&pageNum=1"
        response = requests.get(address)
        data = response.text
        parse_json = json.loads(data)
        latorigin = float(parse_json['results'][0]['LATITUDE'])
        longorigin = float(parse_json['results'][0]['LONGITUDE'])
        place = parse_json['results'][0]['ADDRESS']
        results = HawkerStall.objects.filter(reco__contains = search)
        if not results:
            return render(request, "project/index.html", {
                "searchmessage": "No related results.",
                "form": NewTaskForm(),
                "postalcode": postalcode,
                "pagenumber": pagenumber,
                "no": "no",
            })
        number = [0] * len(results)
        count = 0
        for res in results.iterator():
            lat = res.latitude
            long = res.longtitude
            origin = (latorigin, longorigin)
            destination = (lat, long)
            km = distance(origin, destination)
            km = km * 1000
            number[count] = round(km)
            count += 1
        #an array of the indexes after sorting
        s = numpy.array(number)
        sort_index = numpy.argsort(s)
        #original number = [2022, 3104, 1012...]
        #number = [1012, 2022, 3104...]
        #new_list = [3, 1, 2...]
        number.sort()
        latitudes = [0] * len(results)
        longtitudes = [0] * len(results)
        names = [0] * len(results)
        addresses = [0] * len(results)
        recos = [0] * len(results)
        hours = [0] * len(results)
        details = [0] * len(results)
        contributors = [0] * len(results)
        # this will start from the numbers 4, then to 1, then to 6....
        for i in sort_index:
            for j in range(len(addresses)):
                if addresses[j] != 0:
                    j = j+1
                else:
                    ha = results[int(i)]
                    latitudes[j] = ha.latitude
                    longtitudes[j] = ha.longtitude
                    names[j] = ha.name
                    addresses[j] = ha.address
                    recos[j] = ha.reco
                    hours[j] = ha.hours
                    details[j] = ha.details
                    contributors[j] = ha.contributor
                    break
        myhouselat = [latorigin] * len(results)
        myhouselong = [longorigin] * len(results)
        latandlong = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong2 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong3 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong4 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong5 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong6 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        return render(request, "project/search.html",{
            "pagenumber": pagenumber,
            "search": search,
            "postalcode": postalcode,
            "latitudes": latitudes,
            "longtitudes": longtitudes,
            "names": names,
            "addresses": addresses,
            "recos": recos,
            "hours": hours,
            "details": details,
            "contributors": contributors,
            "numbers": number,
            "latandlong": latandlong,
            "latandlong2": latandlong2,
            "latandlong3": latandlong3,
            "latandlong4": latandlong4,
            "latandlong5": latandlong5,
            "latandlong6": latandlong6,
            "form": NewTaskForm()
        })
    return render(request, "project/index.html",{
        "form": NewTaskForm()
    })

def next(request, pagenumber):
    if request.method == "POST":
        page = int(pagenumber) + 1
        search = request.POST["search"]
        postalcode = request.POST["postalcode"]
        place = Zipcode.objects.filter(postal = postalcode)
        latorigin = place.first().latitude
        longorigin = place.first().longtitude
        results = HawkerStall.objects.filter(reco__contains = search)
        if not results:
            return render(request, "project/index.html", {
                "searchmessage": "That shit doesnt exist lmao",
                "form": NewTaskForm()
            })
        number = [0] * len(results)
        count = 0
        for res in results.iterator():
            lat = res.latitude
            long = res.longtitude
            origin = (latorigin, longorigin)
            destination = (lat, long)
            km = distance(origin, destination)
            km = km * 1000
            number[count] = round(km)
            count += 1
        #an array of the indexes after sorting
        s = numpy.array(number)
        sort_index = numpy.argsort(s)
        #original number = [2022, 3104, 1012...]
        #number = [1012, 2022, 3104...]
        #new_list = [3, 1, 2...]
        number.sort()
        latitudes = [0] * len(results)
        longtitudes = [0] * len(results)
        names = [0] * len(results)
        addresses = [0] * len(results)
        recos = [0] * len(results)
        hours = [0] * len(results)
        details = [0] * len(results)
        contributors = [0] * len(results)
        # this will start from the numbers 4, then to 1, then to 6....
        for i in sort_index:
            for j in range(len(addresses)):
                if addresses[j] != 0:
                    j = j+1
                else:
                    ha = results[int(i)]
                    latitudes[j] = ha.latitude
                    longtitudes[j] = ha.longtitude
                    names[j] = ha.name
                    addresses[j] = ha.address
                    recos[j] = ha.reco
                    hours[j] = ha.hours
                    details[j] = ha.details
                    contributors[j] = ha.contributor
                    break
        myhouselat = [latorigin] * (len(results) - (6*(page-1)))
        myhouselong = [longorigin] * (len(results) - (6*(page-1)))
        latandlong = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong2 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong3 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong4 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong5 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong6 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        return render(request, "project/search.html",{
            "pagenumber": page,
            "search": search,
            "postalcode": postalcode,

            "latitudes": latitudes[(6*(page-1)):],
            "longtitudes": longtitudes[(6*(page-1)):],
            "names": names[(6*(page-1)):],
            "addresses": addresses[(6*(page-1)):],
            "recos": recos[(6*(page-1)):],
            "hours": hours[(6*(page-1)):],
            "details": details[(6*(page-1)):],
            "contributors": contributors[(6*(page-1)):],
            "numbers": number[(6*(page-1)):],
            "latandlong": latandlong,
            "latandlong2": latandlong2,
            "latandlong3": latandlong3,
            "latandlong4": latandlong4,
            "latandlong5": latandlong5,
            "latandlong6": latandlong6,
            "form": NewTaskForm()
        })
    return render(request, "project/index.html",{
        "form": NewTaskForm()
    })

def info(request, name):
    stall = HawkerStall.objects.filter(name = name)
    return render(request, "project/info.html",{
        "stalls": stall.first(),
        "form": NewTaskForm(),
    })

def edity(request, name):
    if request.method == "POST":
        latitude = request.POST["latitude"]
        longtitude = request.POST["longtitude"]
        stalltype = request.POST["stalltype"]
        address = request.POST["address"]
        hours = request.POST["hours"]
        reco = request.POST["reco"]
        details = request.POST["details"]
        #contributor = request.POST["contributor"]
        f = HawkerStall.objects.get(name = name)
        f.latitude = latitude
        f.longtitude = longtitude
        f.stalltype = stalltype
        f.address = address
        f.hours = hours
        f.reco = reco
        f.details = details
        f.save()
        return HttpResponseRedirect(reverse("savethehawkers:info", args=(name,)))
    else:
        return render(request, "project/index.html")

def delete(request, name):
    g = HawkerStall.objects.filter(name = name).first()
    g.latitude = 0
    g.longtitude = 0
    g.stalltype = ""
    g.address = ""
    g.hours = ""
    g.reco = ""
    g.details = ""
    g.name = ""
    g.contributor = ""
    g.save()
    return HttpResponseRedirect(reverse("savethehawkers:index"))

def creations(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            latitude = form.cleaned_data["latitude"]
            longtitude = form.cleaned_data["longtitude"]
            name = form.cleaned_data["name"]
            stalltype = form.cleaned_data["stalltype"]
            address = form.cleaned_data["address"]
            hours = form.cleaned_data["hours"]
            reco = form.cleaned_data["reco"]
            details = form.cleaned_data["details"]
            contributor = form.cleaned_data["contributor"]
            h = HawkerStall(latitude= latitude, longtitude= longtitude, name= name, stalltype = stalltype, address = address, hours = hours, reco = reco, details = details, contributor = contributor)
            i = History(latitude= latitude, longtitude= longtitude, name= name, stalltype = stalltype, address = address, hours = hours, reco = reco, details = details, contributor = contributor)
            h.save()
            i.save()
            return HttpResponseRedirect(reverse("savethehawkers:info", args=(name,)))
    else:
        return render(request, "project/create.html",{
            "form": NewTaskForm(),
            "form3": CreateForm(),
            })

###########################
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("savethehawkers:index"))
        else:
            return render(request, "project/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "project/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("savethehawkers:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "project/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "project/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("savethehawkers:index"))
    else:
        return render(request, "project/register.html")
