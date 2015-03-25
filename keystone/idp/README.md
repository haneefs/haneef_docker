To build
docker build --tag haneef/keystone_idp .

Running keystone idp container

For interactive mode
docker run -ti -v /etc/keystone_idp:/etc/keystone  -v /var/log/keystone_idp:/var/log/keystone -p 35357:35357  --name keystone_idp haneef/keystone_idp  /bin/bash


Federation Setup k2K Federation:


IDP setup
  Configurations:
     saml section  ( certfile, keyfile, idp_entity_id, idp_sso_endpoint, idp_metadata_path)
     Also provider idp_org settings
  Using keystone-manage generate saml_idp_metatadata and store at idp_metadata_path    	
   

SP  setup
   Install shibbolobath
   Modify mod-wsgi setting to include federation path
   Add attribute map file /etc/shibboleth/attribute-map.xml

Create Domain, Create group, Create role, Create role assignments,
 Create IDP , Create mappings (rules),  Craeate protocl ( mapping ,protocl, and idp)


Federation Flows KS to KS
   1) Client gets teh token from IDP
   2) Rescope the token for the SP
   3) Posts the token to IDP /saml2 url and get an SAML assertion equivalent of the token
   4) Wraps the SAML Asserttion to ECP format
   5) Sends the ECP fomrat to SP ECP urL
   6) Client will get a HTTP redirect to SP auth URL ( These are the urls we registered when we regiser SP)
   7) Do a HTTP get on the redirected url to get Unscoped token for SP
   8) From the unscoped token get the /auth/projects and /auth/domains
   9) Rescope the unscoped token for any of the project or domain
   10) Now you can work with SP


Federation Flows ADFS:
  
Federation Flows KS to KS

Federation Flows WebSSO

