
#service register
##Usage 
All responses will have the form
'''json
{
	"data":"Mixed type holding the content of the response",
	"message":"Description of what happend"
}
'''

##List all devices

#Defination

'GET/service'

***Responses***
'200 OK' on sucess
'''json
{
	Service:foo
	Port:8080
	Maintainer:abc@foo.nl
	Labels:
	-groups:api
	-team:it
}

'''

##Registering new service
##Defination

'POST/service'

***Arguments***
---These are the mandatory fields: 
---* Service : The service name, must be unique (should be a name from 4 to 30 characters). 
---* Port : Which port the service should run on (should be a valid port). 
---* Maintainer : The person that is responsible for the service (should be a valid email). 
---* Labels : Can be multiple labels, following a key:value convention.

***Responsee***
-'201 created' on success
'''json 
{
	Service:foo
	Port:8080
	Maintainer:abc@foo.nl
	Labels:
	-groups:api
	-team:it
}
'''
##Lookup service details
***Response***
--'404 Not Found' if service doesnot exist
--'200 OK ' on success

--if we retrieve services passing the name attribute, it should return just that specific one:
'GET/Service/name'

./manager.py info --name foobar
'''json 
{
	Service:foo
	Port:8080
	Maintainer:abc@foo.nl
	Labels:
	-groups:api
	-team:it
}
'''
--If we pass the all attribute, it should show all the services:
'GET/Service/all'

./manager.py info --all
--2 service found
'''
json
{
	Service: foobar
	Port: 7373
	Maintainer: abc@foo.nl
	Labels:
	-groups:apis
	-team:it
	Service: barbaz
	Port: 80
	Maintainer: def@foo.nl
	Labels:
	-groups:apps
}
'''
--if you pass multiple labels, it should show all the ones that match that criteria.
--./manager.py info --labels groups:apis
--1 service found
'''
json
{
	Service: foobar
	Port: 7373
	Maintainer: abc@foo.nl
	Labels:
	-groups:apis
	-team:it
}
'''

##Delete Service
***Defination***
---./manager.py delete --name foobar
'DELETE/Service/name'
***Response***
--'404 Not Found' if the service not exists
--Service 'foobar' deleted


