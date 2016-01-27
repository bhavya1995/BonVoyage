from django.contrib import auth
from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
import json
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils import timezone

from django.core import serializers

from travelRequirement.models import *
from urllib.request import urlopen
import base64
import requests
import datetime
import os
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.decorators.http import require_POST
from jfu.http import upload_receive, UploadResponse, JFUResponse
import xml.etree.ElementTree
import xmltodict
from selenium import webdriver
from bs4 import BeautifulSoup
import time

def home(request):

	url= settings.STATICFILES_DIRS[0]+ '/js/travelDestinations.json';
	destination = json.loads(open( url ).read())
	length=len(destination)
	categories=['Weekend-Getaways','Romantic','Relax','Cultural','Disappear','Adventure','City','With-Friends','With-Family']
	length_i=len(categories)
	i=0;
	dest=[];

	while(i<length_i):

		j=0;
		individual=[];
		obj={};
		while(j<length):

			if(destination[j]['Type'] == categories[i]):

				url="/static/images/IMAGES/"+destination[j]["Image"]
				obj={

					'name' : destination[j]["Name"],
					'image' : url
				}
				individual.append(obj)

			j+=1;

		objFinal={
		
			'type':categories[i],
			'des': individual
		}

		i=i+1;
		dest.append(objFinal);

	return render(request,'home.html',{

		'data':dest
	});

def checkPackage(request):
	id=request.GET.get("id");
	check=request.GET.get("value");	

	package=travelPackage.objects.filter(id=id)[0];

	print(int(check));
	if(int(check) == 1):
		package.selectedForBid=True;

	if(int(check) == 2):
		package.selectedForBid =False;
		
	package.save();	
	return HttpResponse(json.dumps({"status": 1}), content_type="application/json")

def dashboardTravellerSelect(request):
	
	user=request.user;
	id=request.GET.get("q");
	package=travelPackage.objects.filter(travelReqId=id,selectedForBid=0).order_by('price');
	packages=[];
	for p in package:
		obj={

			'id':p.id,
			'name':p.name,
			'price':p.price
		}	
		packages.append(obj);

	return render(request,'DashboardTravellerSelect.html',{

		'firstName':user.first_name,
		'lastName':user.last_name,
		'packages':packages 
});	


def dashboardTraveller(request):
	
	print(request.user)
	user=User.objects.filter(id=request.user.id)[0];
	userReq=travelReq.objects.filter(userId=user.id).order_by('-startDate');
	date=datetime.date.today();
	reqobj=[];
	count1 = -1
	if (userReq.count() == 0):
		count1 = 0
		return  HttpResponseRedirect('/userRequirement')
	
	else:
		for u in userReq:
			end=0
			
			print(u.endDate)
			if(u.endDate == "14 October,2015" or u.endDate == "16 October,2015" or u.endDate == "17 October,2015"):
				end=1;
			count= travelPackage.objects.filter(travelReqId=u.id).count();
			id=u.id;	
			obj={

				'startDate':u.startDate,
				'endDate':u.endDate,
				'budget':u.budget,
				'name':u.reqName,
				'status':u.status,
				'count':count,
				'end':end,
				'id':id
			}
			reqobj.append(obj)

	return render(request,'DashboardTraveller.html',{

		'firstName':user.first_name,
		'lastName':user.last_name,
		'reqobj' :reqobj,
		'count': count1
	});

def dashboardAgent(request):

	user=request.user;
	requirementObj=travelReq.objects.filter(status=0).order_by('-startDate');
	reqobj=[];
	for u in requirementObj:
		packageExist=0;
		packageSelected=0;
		userPackage=travelPackage.objects.filter(travelReqId=u.id, userId=user.id);
		if(len(userPackage)!=0):
			packageExist=1;
			userPackage=userPackage[0];
			if(userPackage.selectedForBid ==1 ):
				packageSelected=1;

		count= travelPackage.objects.filter(travelReqId=u.id).count();
		id=u.id;	
		obj={

			'startDate':u.startDate,
			'endDate':u.endDate,
			'budget':u.budget,
			'name':u.reqName,
			'count':count,
			'package':packageExist,
			'packageSelect':packageSelected,
			'places': u.placeToVisit,
			'id':id
		}
		reqobj.append(obj)
	print(reqobj);	
	return render(request,'DashboardAgent.html',{

		'firstName':user.first_name,
		'lastName':user.last_name,
		'reqobj' :reqobj 
	});	

def bid(request):
	userId=request.user.id;
	id=request.GET.get("q");
	traveller= travelReq.objects.filter(id=id)[0];
	packages=travelPackage.objects.filter(travelReqId=traveller.id).order_by('price');
	place=traveller.placeToVisit;
	places=place.split( );
	user_Traveller= User.objects.filter(id=traveller.userId.id)[0];
	name= user_Traveller.username;
	travellerObj={

		'name' : name,
		'startDate': traveller.startDate,
		'endDate' : traveller.endDate,
		'cities':places
	}
	packageArray=[];
	count=0;
	for p in packages:
		count+=1;
		discount=0;
		savings=0;
		user_Agent= User.objects.filter(id=p.userId.id)[0];
		name= user_Agent.first_name + " " + user_Agent.last_name;
		# if(int(p.bidPrice)!=0):
		discount=int(100-((int(p.price)-int(p.bidPrice))/int(p.price))*100);
		savings=(int(p.price)-int(p.bidPrice));
		newPrice=(int(p.price)-int(p.bidPrice));
		obj={
			'Id':p.id,
			'Username':name,
			'Packagename':p.name,
			'Price':p.price,
			'BidPrice':p.bidPrice,
			'Discount':discount,
			'Savings':savings
		}
		packageArray.append(obj);
	packageArray.sort(key=lambda x: x['Savings'], reverse=False)
	print(packageArray)
	return render(request,'biddingViewTraveller.html',{

			'firstName':request.user.first_name,
			'lastName':request.user.last_name,
			'travelAgents':packageArray,
			'traveller': travellerObj,
			'agentCount':count	
		});	

def userRequirement(request):
	return render(request,'userRequirement.html');

def bid_agent(request):
	
	user=request.user;
	id=request.GET.get("q");
	travelreq= travelReq.objects.filter(id=id)[0];
	# travelpackageid=request.GET.get('q');
	packages=travelPackage.objects.filter(travelReqId=travelreq.id).order_by('price');
	place=travelreq.placeToVisit;
	places=place.split( );
	user_Traveller= User.objects.filter(id=travelreq.userId.id)[0];
	name= user_Traveller.username;
	travellerObj={

		'name' : name,
		'startDate': travelreq.startDate,
		'endDate' : travelreq.endDate,
		'cities':places
	}
	packageArray=[];
	count=0;
	for p in packages:
		count+=1;
		user=0;
		discount=0;
		savings=0;
		user_Agent= User.objects.filter(id=p.userId.id)[0];
		name= user_Agent.first_name + " " + user_Agent.last_name;
		if (request.user.email == p.userId.email):
			user=1;
		# if(int(p.bidPrice)!=0):
		discount=int(100-((int(p.price)-int(p.bidPrice))/int(p.price))*100);
		savings=(int(p.price)-int(p.bidPrice));
		newPrice=(int(p.price)-int(p.bidPrice));
		
		obj={
			'Id':p.id,
			'Username':name,
			'Packagename':p.name,
			'Price':p.price,
			'BidPrice':p.bidPrice,
			'Discount':discount,
			'yser':user,
			'Savings':savings
		}
		packageArray.append(obj);
	print(packageArray)
	packageArray.sort(key=lambda x: x['Savings'], reverse=False)
	
	return render(request,'biddingViewTravelAgent.html',{

			'firstName':request.user.first_name,
			'lastName':request.user.last_name,
			'travelAgents':packageArray,
			'traveller': travellerObj,
			'agentCount':count	
		});

def submitReq (request):
	user = request.user
	startDate = request.GET.get('startDate')
	endDate = request.GET.get('endDate')
	budget = request.GET.get('budget')
	cities = json.loads(request.GET.get('cities'))
	placeToVisit = ""
	for c in cities:
		placeToVisit += c + " "
	requirementObj = travelReq.objects.create(userId = user, startDate = startDate, endDate = endDate, budget = budget, placeToVisit = placeToVisit)
	requirementObj.save()
	print(startDate, endDate, budget, cities)
	return HttpResponse(json.dumps({"status": 1}), content_type="application/json")

def submitBid (request):
	user = request.user
	value = request.GET.get('value')
	id = request.GET.get('id')
	package=travelPackage.objects.filter(id=id)[0];
	package.bidPrice=value;
	package.save();
	return HttpResponse(json.dumps({"status": 1}), content_type="application/json")	

def packageDetails(request):
	id = request.GET.get('id')
	package=travelPackage.objects.filter(id=id)[0];
	data={

		'Price':package.price,
		'Bid':package.bidPrice
	}
	return HttpResponse(json.dumps(data), content_type="application/json")	


def makePackage (request):

	id=request.GET.get("q");
	return render(request, "makePackage.html",{

		'travelReqId':id
	})

def getAirports (request):
	arr = []
	for a in airportDetails.objects.filter(city__icontains=request.GET.get('q')):
		arr.append(a.code + " " + a.name + " " + a.city + " " + a.country)

	return HttpResponse(json.dumps({"data": {"airport":arr}}), content_type="application/json")

def submitPackage (request):

	travelReqId = request.GET.get('travelReqId')
	packageName = request.GET.get('packageName')
	packagePrice = request.GET.get('packagePrice')
	flightDetailsData = json.loads(request.GET.get('flightDetails'))
	hotelDetailsData = json.loads(request.GET.get('hotelDetails'))
	tourGuide = json.loads(request.GET.get('tourGuide'))
	# print(packagePrice, packageName, flightDetails, tourGuide, hotelDetails)
	travelReqObj = travelReq.objects.filter(id = travelReqId)[0]
	travelPackageObj = travelPackage.objects.create(travelReqId= travelReqObj,userId = request.user, name = packageName, price = packagePrice)
	travelPackageObj.save()
	print(travelPackageObj.id)
	for f in flightDetailsData:
		# print(f[])
		flightObj = flightDetails.objects.create(fromPlace = f['departure'], toPlace = f['arrival'], type = f['type'], travelPackageId = travelPackageObj)
		flightObj.save();
	for h in hotelDetailsData:
		hotelObj = hotelDetails.objects.create(name = h['hotelName'], place = h['hotelCity'], roomType = h['roomType'], numOfDays = h['numOfDaysNights'], travelPackageId = travelPackageObj)
		hotelObj.save()
	for d in tourGuide:
		daysSchObj = daysSch.objects.create(dayNum = d['day'], description = d['description'], travelPackageId = travelPackageObj)
		daysSchObj.save()

	return HttpResponse(json.dumps({"status": 1}), content_type="application/json")

def viewPackage(request):
	
	id = request.GET.get('id')
	package=travelPackage.objects.filter(id=id)[0];
	user= User.objects.filter(id=package.userId.id)[0];
	name= user.first_name + " " + user.last_name;
	obj={

		'agentName':name,
		'agentPackageName':package.name,
		'agentPrice':package.price,
		'agentBid':package.bidPrice,
		'agentRemarks':package.remarks
	}

	return HttpResponse(json.dumps(obj), content_type="application/json")

def viewAgentPackage(request):
	
	id = request.GET.get('id');
	package=travelPackage.objects.filter(id=id)[0];
	flightdetails=flightDetails.objects.filter(travelPackageId=package.id);	
	hoteldetails=hotelDetails.objects.filter(travelPackageId=package.id);	
	daysDescription=daysSch.objects.filter(travelPackageId=package.id);	
	user= User.objects.filter(id=package.userId.id)[0];
	name= user.first_name + " " + user.last_name;
	flights=[];
	for flight in flightdetails:
		objflight={
			"DepartureAirport":flight.fromPlace,
			"ArrivalAirport":flight.toPlace,
			"SeatType":flight.type
		}
		flights.append(objflight);

	hotels=[];	
	for hotel in hoteldetails:
		objhotel={
			"HotelName":hotel.name,
			"HotelCity":hotel.place,
			"HotelRoomType":hotel.roomType,
			"HotelNoDays":hotel.numOfDays
		}
		hotels.append(objhotel);	

	description=[];
	for day in daysDescription:
		objday={

			"index":day.dayNum,
			"Details":day.description	
		}	
		description.append(objday);

	obj={

		'Name':name,
		'PackageName':package.name,
		'Price':package.price,
		'Bid':package.bidPrice,
		'Remarks':package.remarks,
		'Airports':flights,
		'Hotels':hotels,
		'Days':description
	}

	return HttpResponse(json.dumps(obj), content_type="application/json")

def viewAgentPackage1(request):
	
	id = request.GET.get('id');
	package=travelPackage.objects.filter(id=id)[0];
	flightdetails=flightDetails.objects.filter(travelPackageId=package.id);	
	hoteldetails=hotelDetails.objects.filter(travelPackageId=package.id);	
	daysDescription=daysSch.objects.filter(travelPackageId=package.id);	
	user= User.objects.filter(id=package.userId.id)[0];
	name= user.first_name + " " + user.last_name;
	flights=[];
	for flight in flightdetails:
		objflight={
			"DepartureAirport":flight.fromPlace,
			"ArrivalAirport":flight.toPlace,
			"SeatType":flight.type
		}
		flights.append(objflight);

	hotels=[];	
	for hotel in hoteldetails:
		objhotel={
			"HotelName":hotel.name,
			"HotelCity":hotel.place,
			"HotelRoomType":hotel.roomType,
			"HotelNoDays":hotel.numOfDays
		}
		hotels.append(objhotel);	

	description=[];
	for day in daysDescription:
		objday={

			"index":day.dayNum,
			"Details":day.description	
		}	
		description.append(objday);

	obj={

		'Name':name,
		'PackageName':package.name,
		'Price':package.price,
		'Bid':package.bidPrice,
		'Remarks':package.remarks,
		'Airports':flights,
		'Hotels':hotels,
		'Days':description
	}

	return HttpResponse(json.dumps(obj), content_type="application/json")

def getConditions(request):
	lat = request.GET.get('lat')
	lon = request.GET.get('lon')
	startDate = request.GET.get('startDate')
	content = urlopen("http://maps.googleapis.com/maps/api/geocode/json?latlng=" + lat + "," + lon + "&sensor=true")
	html = content.read()
	jsonData = json.loads(html.decode())
	jsonData = jsonData['results']
	jsonData = jsonData[0]['address_components']
	flag = 0
	country = ""
	code = ""
	for j in jsonData:
		type = j["types"]
		for t in type:
			if (t == "country"):
				country = j["long_name"]
				code = j["short_name"]
				flag = 1
				break
		if (flag == 1):
			break
	isoObj = isoCode.objects.filter(code__startswith = code)[0]
	month = int(startDate)
	if (month < 10):
		year = "2016"
	else:
		year = "2015"
	# isoObj.code
	encoded = base64.b64encode(b'lhjwdOWWyW8gIysExeXk-6clGoWLol3gLadUmq5y:bhavya')
	encoded = encoded.decode()
	r=requests.request('GET', "https://api.qalendra.com/assets?date=" + year + "-" + startDate + "-28&countryCode=" + isoObj.code + "&perPage=50", headers={"Authorization": "Basic " + encoded});
	jsonCondition = json.loads(r.text)
	print(jsonCondition)
	finalArray = []
	for d in jsonCondition['data']:
		city = d['location']['address']['city']
		state = d['location']['address']['state']
		country = d['location']['address']['country']
		if(city == None):
			city = ""
		if(state == None):
			state = ""
		else:
			state = ", " + state
		if(country == None):
			country = ""
		else:
			country = ", " + country
		print(d)
		temp = {
			"placeName": d['name'],
			"verdict": d['predictions']['data'][0]['verdict'],
			"address": city + state + country,
			# "score": int(d['predictions']['data'][0]['score'])
		}
		finalArray.append(temp)
	print(finalArray)
	# finalArray.sort(key=lambda x: x.score, reverse=True)
	# print(finalArray)
	return HttpResponse(json.dumps(finalArray), content_type="application/json")

@require_POST
def upload( request ):

    # The assumption here is that jQuery File Upload
    # has been configured to send files one at a time.
    # If multiple files can be uploaded simulatenously,
    # 'file' may be a list of files.
    print(request.user)
    file = upload_receive( request )

    feedbackObj = feedback.objects.create(userId = request.user)
    feedbackObj.save()
    instance = feedback_files( fileUpload = file , feedbackId = feedbackObj)
    instance.save()

    basename = os.path.basename( instance.fileUpload.path )

    file_dict = {
        'name' : basename,
        'size' : file.size,

        'url': settings.MEDIA_URL + basename,
        'thumbnailUrl': settings.MEDIA_URL + basename,

        # 'deleteUrl': reverse('jfu_delete', kwargs = { 'pk': instance.pk }),
        # 'deleteType': 'POST',
    }
    return UploadResponse( request, file_dict )

def feedback_render (request):

	id=request.GET.get("q");
	return render(request,'feedback.html',{

		'id':id
	});

@require_POST
def uploadVerify( request ):

    # The assumption here is that jQuery File Upload
    # has been configured to send files one at a time.
    # If multiple files can be uploaded simulatenously,
    # 'file' may be a list of files.
    print("request.user")
    file = upload_receive( request )
    # return
    # feedbackObj = feedback.objects.create(userId = request.user)
    # feedbackObj.save()
    # print(feedbackObj)
    instance = agent_files( fileUpload = file , userId = request.user)
    instance.save()

    basename = os.path.basename( instance.fileUpload.path )

    file_dict = {
        'name' : basename,
        'size' : file.size,

        'url': settings.MEDIA_URL + basename,
        'thumbnailUrl': settings.MEDIA_URL + basename,

        # 'deleteUrl': reverse('jfu_delete', kwargs = { 'pk': instance.pk }),
        # 'deleteType': 'POST',
    }

    return UploadResponse( request, file_dict )

def agentVerification (request):
	return render(request,'agentVerification.html');

def submitFeedback(request):

	id=request.GET.get("id");
	ratingAgent=request.GET.get("ratingAgent");
	ratingUs=request.GET.get("ratingUs");
	review=request.GET.get("review");

	id=int(id);
	ratingAgent=int(ratingAgent);
	userReq=travelReq.objects.filter(id=id)[0];
	print(userReq.userId)
	package= travelPackage.objects.filter(travelReqId=userReq)[0];
	print(package);
	user=User.objects.filter(id=package.userId.id)[0];
	name=user.first_name + " " + user.last_name;

	feedbackObj = feedback.objects.create(userId = request.user,userReqId= userReq, agentId=name, agentRating= ratingAgent, agentReview= review )
	feedbackObj.save();

	return HttpResponse(json.dumps({"status": 1}), content_type="application/json")


def imageProcessing (request):
	imageName = request.GET.get('imageName')
	print("bbb")
	agentFile = agent_files.objects.filter(userId = request.user)
	print(agentFile[0].filename()) 
	for a in agentFile:
		if (a.filename() == imageName):
			currentFile = a
			break
	encoded = base64.b64encode(b'Bon Voyage:+A2FDjUlOxccsxn/DhYhZdGhI')
	encoded = encoded.decode()
	r = requests.request('POST', 'https://cloud.ocrsdk.com/processImage?language=english&exportformat=xml', files={'file': open(a.fileUpload.path, 'rb')}, headers={"Authorization": "Basic " + encoded})
	print(r.text)
	data = xmltodict.parse(r.text)
	# e = xml.etree.ElementTree.parse(r.text).getroot()
	while (1):
		r = requests.request('GET', 'http://cloud.ocrsdk.com/getTaskStatus?taskId=' + data['response']['task']['@id'], headers={"Authorization": "Basic " + encoded})
		data = xmltodict.parse(r.text)
		if (data['response']['task']['@status'] == "Completed"):
			break
	print(data)
	print(data['response']['task']['@resultUrl'])
	r = requests.request('GET', data['response']['task']['@resultUrl'])
	data = xmltodict.parse(r.text)
	for b in data['document']['page']['block']:
		# print(b['text'])
		# print(type(b['text']['par']))
		# ['line'][0]['formatting']['charParams'][0]
		try:
			text = b['text']
		except:
			continue
		try:
			par = text['par'][0]
		except:
			par = text['par']
		# print(par)
		try:
			line = par['line']
		except:
			continue
		try:
			lineNum = line[0]
		except:
			lineNum = line
		# print(line)
		try:
			char1 = lineNum['formatting']['charParams'][0]
			char2 = lineNum['formatting']['charParams'][1]
			# print(char1, char2)
			if (char1['#text'] != 'D' or char2['#text'] != 'L'):
				continue
		except:
			char = lineNum['formatting']['charParams']
			continue
		licenceNum = ""
		for i in lineNum['formatting']['charParams']:
			licenceNum += i['#text']
		print(licenceNum)
		name = ''
		for i in line[1]['formatting']['charParams']:
			# print(i)
			try:
				name += i['#text']
			except:
				name += " "
		print(name)
		fathersName = ''
		for i in line[2]['formatting']['charParams']:
			# print(i)
			try:
				fathersName += i['#text']
			except:
				fathersName += " "
		print(fathersName)
		dob = ''
		for i in line[3]['formatting']['charParams']:
			# print(i)
			try:
				dob += i['#text']
			except:
				dob += " "
		print(dob)
		address = ''
		try:
			abc = text['par'][2]['line'][0]
			lineAdd = text['par'][2]['line']
		except:
			lineAdd = []
			lineAdd.append(text['par'][2]['line'])
		for l in lineAdd:
			for i in l['formatting']['charParams']:
				# print(i)
				try:
					address += i['#text']
				except:
					address += " "
			address += " "
		print(address)
		break
	temp = {
		'licenceNum': licenceNum,
		'name': name,
		'fathersName': fathersName,
		'dob': dob,
		'address': address
	}
	return HttpResponse(json.dumps(temp), content_type="application/json")

def submitAgentDetails(request):
	licenceNum = request.GET.get('licenceNum')
	name = request.GET.get('name')
	fathersName = request.GET.get('fathersName')
	address = request.GET.get('address')
	dob = request.GET.get('dob')
	panNum = request.GET.get('panNum')
	namePan = request.GET.get('namePan')
	fathersNamePan = request.GET.get('fathersNamePan')
	dobPan = request.GET.get('dobPan')
	agentObj = agent_details.objects.create(userId = request.user, licenceNum = licenceNum, name = name, fathersName = fathersName, address = address, dob = dob, panNum = panNum, namePan = namePan, fathersNamePan = fathersNamePan, dobPan = dobPan)
	agentObj.save()
	temp = {
		"statusCus": 1
	}
	return HttpResponse(json.dumps(temp), content_type="application/json")

def submitAgentDetailsPan(request):
	PanCardNo = request.GET.get('PanCardNo')
	name = request.GET.get('name')
	fathersName = request.GET.get('fathersName')
	dob = request.GET.get('dob')
	agent = agent_details.objects.filter(userId = request.user, name = name, fathersName = fathersName)
	agentObj = agent_details.objects.create(userId = request.user, licenceNum = licenceNum, name = name, fathersName = fathersName, address = address, dob = dob)
	agentObj.save()
	temp = {
		"statusCus": 1
	}
	return HttpResponse(json.dumps(temp), content_type="application/json")	

def destinations(request):

	url= settings.STATICFILES_DIRS[0]+ '/js/travelDestinations.json';
	destination = json.loads(open( url ).read())
	length=len(destination)
	categories=['Weekend-Getaways','Romantic','Relax','Cultural','Disappear','Adventure','City','With-Friends','With-Family']
	length_i=len(categories)
	i=0;
	dest=[];

	while(i<length_i):

		j=0;
		individual=[];
		obj={};
		while(j<length):

			if(destination[j]['Type'] == categories[i]):

				url="/static/images/IMAGES/"+destination[j]["Image"]
				obj={

					'name' : destination[j]["Name"],
					'image' : url
				}
				individual.append(obj)

			j+=1;

		objFinal={
		
			'type':categories[i],
			'des': individual
		}

		i=i+1;
		dest.append(objFinal);

	return render(request,'destinations.html',{

		'data':dest
	});

def adminVerification(request):
	agentId = request.GET.get('id')
	print(User.objects.filter(id = agentId))
	user = UserDetails.objects.filter(id = agentId)[0].user
	print(user)
	agentObj = agent_details.objects.filter(userId = user)[0]
	webpage = r"https://dlpay.dimts.in/dldetail/default.aspx"
	searchterm = agentObj.licenceNum
	driver = webdriver.Chrome()
	driver.get(webpage)
	sbox = driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_txtdlno")
	sbox.send_keys(searchterm)
	submit = driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_Button1")
	submit.click()
	time.sleep(10)
	page = driver.page_source
	# print(page)
	soup = BeautifulSoup(page)
	# print(soup)
	counter = 1
	temp = {}
	address = ""
	flag = 0
	for s in soup.select('input'):
		if (counter == 5):
			status = 0
			if (agentObj.licenceNum.replace(" ", "").lower() == s.get('value').replace(" ", "").lower()):
				status = 1
			temp['licenceNum'] = {
				'filled': agentObj.licenceNum,
				'auth': s.get('value'),
				'status': status
			}
			# print(s.get('value'))
		if (counter == 9):
			status = 0
			if (agentObj.name.replace(" ", "").lower() == s.get('value').replace(" ", "").lower()):
				status = 1
			temp['name'] = {
				'filled': agentObj.name,
				'auth': s.get('value'),
				'status': status
			}
		if (counter == 10):
			status = 0
			if (agentObj.fathersName.replace(" ", "").lower() == s.get('value').replace(" ", "").lower()):
				status = 1
			temp['fathersName'] = {
				'filled': agentObj.fathersName,
				'auth': s.get('value'),
				'status': status
			}
		if (counter == 11):
			status = 0
			if (agentObj.dob.replace(" ", "").lower() == s.get('value').replace(" ", "").lower()):
				status = 1
			temp['dob'] = {
				'filled': agentObj.dob,
				'auth': s.get('value'),
				'status': status
			}
		if (counter == 12 or counter == 14 or counter == 15):
			address += s.get('value')
			status = 0
			if (s.get('value').replace(" ", "").lower() in agentObj.address.replace(" ", "").lower()):
				status = 1

			temp['address'] = {
				'filled': agentObj.address,
				'auth': address,
				'status': status
			}

		counter += 1
	print(temp)
	temp['id'] = user.id
	return render(request,'adminVerification.html', {'data': temp})

def allAgents(request):
	user=request.user;
	userList = UserDetails.objects.filter (is_verified = False)
	finalArray = []
	for u in userList:
		print(u.id, u.user)
		try:
			agentObj = agent_details.objects.filter(userId = u.user)[0]
			temp = {
				'id': u.id,
				'namePan': agentObj.namePan,
				'licenceNum': agentObj.licenceNum,
				'panNum': agentObj.panNum,
				'fathersNamePan': agentObj.fathersNamePan,
				'address': agentObj.address,
				'dobPan': agentObj.dobPan,
			}
			finalArray.append(temp)
		except:
			pass
	print(finalArray)
	return render(request,'viewAllUnverified.html', {
		
		'ver': finalArray,
		'firstName':user.first_name,
		'lastName':user.last_name
	});

def login(request):
	email = request.GET.get('email')
	password = request.GET.get('password')
	firstName = request.GET.get('firstName')
	lastName = request.GET.get('lastName')
	number = request.GET.get('number')
	type=request.GET.get('type')

	print(email,password)
	user=User.objects.create(username = email, first_name=firstName,last_name=lastName,is_active=True);
	user.set_password(password)
	user.save()
	if (type == "Traveller"):
		userDetails=UserDetails.objects.create(type=type,user=user,is_verified=True)
	else:
		userDetails=UserDetails.objects.create(type=type,user=user,is_verified=False)
	user = auth.authenticate(username = email, password = password)
	print(user)
	auth.login(request,user)
	temp = {
		'status': 1
	}
	return HttpResponse(json.dumps(temp), content_type="application/json")

def loginCustom (request):
	# pass
	email = request.GET.get('email')
	password = request.GET.get('password')
	user = auth.authenticate(username = email, password = password)
	auth.login(request,user)
	print(user)
	if (user.is_superuser):
		temp = {
			'url': "/allAgents.html"
		}
	else:
		userObj = UserDetails.objects.filter(user = user)[0].type
		if (userObj == "Traveller"):
			temp = {
				'url': "/dashboardTraveller"
			}
		else:
			temp = {
				'url': "/dashboardAgent"
			}
	return HttpResponse(json.dumps(temp), content_type="application/json")
# def createDatabase():

def approve(request):
	id = request.GET.get('id')
	userObj = User.objects.filter(id = id)[0]
	userDetailsObj = UserDetails.objects.filter(user = userObj)[0]
	userDetailsObj.is_verified = True
	userDetailsObj.save()
	temp = {
		'status': 1
	}
	return HttpResponse(json.dumps(temp), content_type="application/json")

def logout(request):
	auth.logout(request);
	return HttpResponse(json.dumps({'status':1}), content_type="application/json");	

def users():

	user=User.objects.create(username = "sukhmeet",email = "s@gmail.com",first_name= "Sukhmeet",last_name= "Singh",is_active=True);
	user.set_password("123")
	user.save()
	userDetails=UserDetails.objects.create(type="Traveller",user= user,is_verified=True)

	user1=User.objects.create(username = "bhavya",email = "b@gmail.com", first_name= "Bhavya",last_name= "Gupta",is_active=True);
	user1.set_password("123")
	user1.save()
	userDetails1=UserDetails.objects.create(type="Traveller",user= user1,is_verified=True)

	user2=User.objects.create(username = "aanchal",email = "a@gmail.com", first_name= "Aanchal",last_name= "Somani",is_active=True);
	user2.set_password("123")
	user2.save()
	userDetails2=UserDetails.objects.create(type="Traveller",user= user2,is_verified=True)

	user3=User.objects.create(username = "vinay",email = "v@gmail.com", first_name= "Vinay",last_name= "Kumar",is_active=True);
	user3.set_password("123")
	user3.save()
	userDetails3=UserDetails.objects.create(type="Travel-Agent",user= user3,is_verified=True)

	user4=User.objects.create(username = "rajesh",email = "r@gmail.com", first_name= "Rajesh",last_name= "Birok",is_active=True);
	user4.set_password("123")
	user4.save()
	userDetails4=UserDetails.objects.create(type="Travel-Agent",user= user4,is_verified=True)

	user5=User.objects.create(username = "himank",email = "h@gmail.com", first_name= "himank",last_name= "Bhalla",is_active=True);
	user5.set_password("123")
	user5.save()
	userDetails5=UserDetails.objects.create(type="Travel-Agent",user= user5,is_verified=True)

	travelreq1=travelReq.objects.create(userId = user, startDate = "25 October,2015", endDate ="16 November,2015",budget= "800000",reqName= "USA Tour",placeToVisit= "Buena Vista, CO 81211, USA Bouton, IA 50039, USA Fort Smith, Unorganized, NT, Canada")	
	travelreq2=travelReq.objects.create(userId = user, startDate = "9 September,2015", endDate ="14 October,2015",budget= "750000",reqName= "Europe",placeToVisit= "Rosdorf, Germany 87-100 Toruń, Poland")	
	travelreq3=travelReq.objects.create(userId = user1, startDate = "27 November,2015", endDate ="31 December,2015",budget= "100000",reqName= "India",placeToVisit= "Shimla, Himachal Pradesh 171002, India Rampur, Himachal Pradesh, India Himachal Pradesh 175123, India")	
	travelreq4=travelReq.objects.create(userId = user2, startDate = "26 November,2015", endDate ="1 December,2015",budget= "50000",reqName= "India",placeToVisit= "Manali")	

	travelpack1=travelPackage.objects.create(travelReqId= travelreq1,userId= user3,name= "USA",price= "650000")
	print(travelpack1)
	travelpack2=travelPackage.objects.create(travelReqId= travelreq2,userId= user3,name= "Europe",price= "650000")
	travelpack3=travelPackage.objects.create(travelReqId= travelreq1,userId= user4,name= "USA Tour",price= "750000")
	travelpack4=travelPackage.objects.create(travelReqId= travelreq1,userId= user5,name= "United States",price= "700000")

	airportdet=flightDetails.objects.create(fromPlace = "DEL Indira Gandhi Intl Delhi India",toPlace = "Boston South Station Boston United States",type = "Economic", travelPackageId =travelpack1 )
	airportdet1=flightDetails.objects.create(fromPlace = "Boston South Station Boston United States",toPlace = "YCG Castlegar Castlegar Canada",type = "Economic", travelPackageId = travelpack1)
	airportdet2=flightDetails.objects.create(fromPlace = "BOM Chhatrapati Shivaji Intl Mumbai India",toPlace = "DCA Washington United States",type = "First Class", travelPackageId = travelpack3)
	airportdet3=flightDetails.objects.create(fromPlace = "MAA Chennai Intl Madras India",toPlace = "LGA La Guardia New York United States",type = "Business", travelPackageId = travelpack4)

	hoteldet1=hotelDetails.objects.create(name= "Abc Hotel",place= "Boston",roomType= "Deluxe",numOfDays= 3,travelPackageId= travelpack1)
	hoteldet2=hotelDetails.objects.create(name= "Def Hotel",place= "Canada",roomType= "Superior",numOfDays= 4,travelPackageId= travelpack1)
	hoteldet3=hotelDetails.objects.create(name= "Efg Hotel",place= "Washington",roomType= "Superior",numOfDays= 5,travelPackageId= travelpack3)
	hoteldet4=hotelDetails.objects.create(name= "Ijl HOtel",place= "New York",roomType= "Deluxe",numOfDays= 4,travelPackageId= travelpack4)

	dayssc1=daysSch.objects.create(dayNum= "1", description= "SIC Crocodile Farm at million year stone park at 15.30 hrs after Coral Island",travelPackageId= travelpack1)
	dayssc2=daysSch.objects.create(dayNum= "2", description= "Coral Island Tour with Indian Lunch on SIC",travelPackageId= travelpack1)
	dayssc3=daysSch.objects.create(dayNum= "3", description= "Universal Studio with one way transfer from Hotel",travelPackageId= travelpack1)
	dayssc4=daysSch.objects.create(dayNum= "1", description= "Half Day city tour on Seat In Coach;Noon till Sunset at Sentosa in Singapore on Seat In Coach",travelPackageId= travelpack3)
	dayssc5=daysSch.objects.create(dayNum= "2", description= "Night Safari on Seat In Coach",travelPackageId= travelpack4)

def imageProcessingPan(request):
	imageName = request.GET.get('imageName')
	print(imageName)
	print("bbb")
	agentFile = agent_files.objects.filter(userId = request.user)
	print(agentFile[0].filename()) 
	for a in agentFile:
		if (a.filename() == imageName):
			currentFile = a
			break
	encoded = base64.b64encode(b'bonvoyage:+SHo7BSd5m11F1VuJ59VuHUB')
	encoded = encoded.decode()
	r = requests.request('POST', 'https://cloud.ocrsdk.com/processImage?language=english&exportformat=xml', files={'file': open(a.fileUpload.path, 'rb')}, headers={"Authorization": "Basic " + encoded})
	print(r.text)
	data = xmltodict.parse(r.text)
	# e = xml.etree.ElementTree.parse(r.text).getroot()
	while (1):
		r = requests.request('GET', 'http://cloud.ocrsdk.com/getTaskStatus?taskId=' + data['response']['task']['@id'], headers={"Authorization": "Basic " + encoded})
		data = xmltodict.parse(r.text)
		if (data['response']['task']['@status'] == "Completed"):
			break
	print(data)
	print(data['response']['task']['@resultUrl'])
	r = requests.request('GET', data['response']['task']['@resultUrl'])
	data = xmltodict.parse(r.text)
	block1 = data['document']['page']['block'][0]
	block2 = data['document']['page']['block'][1]
	name = ""
	for b in block1['text']['par'][2]['line']['formatting']['charParams']:
		try:
			name += b['#text']
		except:
			name += " "
	fathersName = ""
	for b in block2['text']['par'][0]['line'][0]['formatting']['charParams']:
		try:
			fathersName += b['#text']
		except:
			fathersName += " "

	dob = ""
	for b in block2['text']['par'][0]['line'][1]['formatting']['charParams']:
		try:
			dob += b['#text']
		except:
			dob += " "
	panNum = ""
	for b in block2['text']['par'][2]['line']['formatting']['charParams']:
		try:
			panNum += b['#text']
		except:
			panNum += " "
	temp = {
		'panNum': panNum,
		'name': name,
		'fathersName': fathersName,
		'dob': dob
	}
	print(temp)
	return HttpResponse(json.dumps(temp), content_type="application/json")

def adminVerificationPan(request):
	agentId = request.GET.get('id')
	print(User.objects.filter(id = agentId))
	user = UserDetails.objects.filter(id = agentId)[0].user
	print(user)
	agentObj = agent_details.objects.filter(userId = user)[0]
	webpage = r"https://incometaxindiaefiling.gov.in/e-Filing/Services/KnowYourPanLink.html"
	dobsearchterm = agentObj.dobPan
	surnamesearchtermArr = agentObj.namePan.split(' ')
	surnamesearchterm = surnamesearchtermArr[1]
	firstnamesearchterm = surnamesearchtermArr[0]
	driver = webdriver.Chrome()
	driver.get(webpage)
	sbox = driver.find_element_by_css_selector("#dateField")
	sbox.send_keys(dobsearchterm)
	sbox1 = driver.find_element_by_css_selector("#KnowYourPan_userNameDetails_surName")
	sbox1.send_keys(surnamesearchterm)
	sbox2 = driver.find_element_by_css_selector("#KnowYourPan_userNameDetails_firstName")
	sbox2.send_keys(firstnamesearchterm)