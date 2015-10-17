from django.conf.urls import include, url,patterns
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',

	url(r'^admin/', include(admin.site.urls)),
	url(r'^$', 'bonvoyage.views.home'),
	url(r'^dashboardTraveller/bid', 'bonvoyage.views.bid'),
	url(r'^dashboardAgent/bid', 'bonvoyage.views.bid_agent'),	
	url(r'^userRequirement/$', 'bonvoyage.views.userRequirement'),	
	url(r'^submitReq/$', 'bonvoyage.views.submitReq'),
	url(r'^submitBid/$', 'bonvoyage.views.submitBid'),
	url(r'^getPackageDetails/$', 'bonvoyage.views.packageDetails'),
	url(r'^makePackage/$', 'bonvoyage.views.makePackage'),
	url(r'^getAirports/$', 'bonvoyage.views.getAirports'),
	url(r'^submitPackage/$', 'bonvoyage.views.submitPackage'),
	url(r'^viewPackage/$','bonvoyage.views.viewPackage'),
	url(r'^viewAgentPackage/$','bonvoyage.views.viewAgentPackage'),
	url(r'^viewAgentPackage1/$','bonvoyage.views.viewAgentPackage1'),
	url(r'^getConditions/$', 'bonvoyage.views.getConditions'),
	url(r'^dashboardTraveller/$', 'bonvoyage.views.dashboardTraveller'),
	url(r'^dashboardTraveller/select/$', 'bonvoyage.views.dashboardTravellerSelect'),
	url(r'^dashboardAgent/$', 'bonvoyage.views.dashboardAgent'),
	url(r'^checkPackage/$', 'bonvoyage.views.checkPackage'),
	url(r'upload/', 'bonvoyage.views.upload', name = 'jfu_upload' ),
	url(r'^feedback/$', 'bonvoyage.views.feedback_render'),	
	url(r'^agentVerification.html/$', 'bonvoyage.views.agentVerification'),	
	url(r'uploadVerify/', 'bonvoyage.views.uploadVerify', name = 'uploadVerify'),
	url(r'imageProcessing/', 'bonvoyage.views.imageProcessing'),
	url(r'imageProcessingPan/', 'bonvoyage.views.imageProcessingPan'),
	url(r'submitFeedback/', 'bonvoyage.views.submitFeedback'),
	url(r'submitAgentDetails/', 'bonvoyage.views.submitAgentDetails'),
	url(r'destinations/', 'bonvoyage.views.destinations'),
	url(r'adminVerification.html/', 'bonvoyage.views.adminVerification'),
	url(r'adminVerificationPan/', 'bonvoyage.views.adminVerificationPan'),
	url(r'allAgents.html/', 'bonvoyage.views.allAgents'),
	url(r'login/', 'bonvoyage.views.login'),
	url(r'loginCustom/', 'bonvoyage.views.loginCustom'),
	url(r'approve/', 'bonvoyage.views.approve'),
	url(r'logout', 'bonvoyage.views.logout'),
)+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    

