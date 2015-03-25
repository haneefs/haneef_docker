# Work in Progress

import os
from keystoneclient.v3 import client as v3client
import logging
import requests
import json


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_admin_client(username=None, password=None,
                     user_domainname=None, projectname=None,
                     project_domainname=None, auth_url=None):
      
        # Used for creating the ADMIN user
        OS_PASSWORD = password or os.environ['OS_PASSWORD']
        OS_USERNAME = username or os.environ['OS_USERNAME']
        # This will vary according to the entity:
        # the IdP or the SP
        OS_AUTH_URL = auth_url or os.environ.get('OS_AUTH_URL')
        OS_PROJECT_NAME = projectname or os.environ.get('OS_PROJECT_NAME')
        OS_PROJECT_DOMAIN_NAME = project_domainname or os.environ.get('OS_PROJECT_DOMAIN_NAME')
        
      
        return v3client.Client(auth_url=OS_AUTH_URL,
                             username=OS_USERNAME,
                             password=OS_PASSWORD,
                             project_name=OS_PROJECT_NAME,
                             project_domain_name=OS_PROJECT_DOMAIN_NAME)
    


def get_admintoken_client(token=None, auth_url=None):
      
        # Used for creating the ADMIN user        
        OS_AUTH_URL = auth_url or os.environ['OS_URL']
        OS_TOKEN = token or os.environ['OS_TOKEN']
       

        return v3client.Client(endpoint=OS_AUTH_URL,
                             token=OS_TOKEN)



rules = [  
{
    "local": [
        {
            "user": {
                "name": "{0}"
            }
        },
        {
            "group": {
                "id": "replace_it_with_group_id"
            }
        }
    ],
    "remote": [
        {
            "type": "openstack_user",
            "any_one_of": [
                "user1",
                "admin"
            ]
        }
    ]
}
]


def send_request(method, headers, url, data=None):
    """Keystoneclient doesn't implement service providers.
    So use request api to diretly make api call
    """
    logger.info("Sending request to the url %s", url)
    if data:
        logger.info("Request content  %s", data)
    response = None
    if method == "GET":
        response  = requests.get(url, headers=headers)
    if method == "PUT" :
        response  = requests.put(url, headers=headers, data=data)
    if  method == "POST":
        response  = requests.post(url, headers=headers, data=data, verify=False, allow_redirects=False)
    
    return response
    


def generate_token_json(token, sp_name):
        return {
            "auth": {
                "identity": {
                    "methods": [
                        "token"
                    ],
                    "token": {
                        "id": token
                    }
                },
                "scope": {
                    "service_provider": {
                        "id": sp_name
                    }
                }
            }
        }


def create_or_find(fn, **kwargs):
      
    val = None  
    try:        
        val = fn.create(**kwargs)
    except:
        try:
            val = fn.find(**kwargs)
        except Exception as e:
            logger.error(e)
        
    return val

def provision_idp_with_sp(client, sp_name, idp_name, sp_url ):    
    
    headers = {"X-Auth-Token" : client.auth_ref.auth_token,
               "Content-Type" : "application/json"}

    sp_auth_url = "%s/OS-FEDERATION/identity_providers/%s/protocols/saml2/auth" %(client.auth_url, idp_name)
    
    
    body = { "auth_url" : sp_auth_url,
             "enabled" : True,
             "sp_url": sp_url
           }
    
    rest_url = "%s//OS-FEDERATION/service_providers/%s" %(client.auth_url, sp_name)
    
    response = send_request("GET",  headers, rest_url )
    if not response or response.status_code != 200:
                     
        data=json.dumps({"service_provider" : body})
        response = send_request("PUT",  headers,  rest_url, data = data)
    logger.info(response.text)

def provision_sp_for_idp(idpname, client):
    
    
    domain_name = idpname + "_domain"
    kwargs = { "name": domain_name}
    
    logger.info("Creating or finding domain with name  %s" , kwargs["name"])
    domain = create_or_find(client.domains, **kwargs)
    
    
    project_name = idpname + "_project"
    kwargs = { "name": project_name, "domain" : domain}
    
    logger.info("Creating or finding project with name  %s" , kwargs["name"])
    project = create_or_find(client.projects, **kwargs)
 
    group_name = idpname + "_group"
    kwargs = { "name": group_name, "domain" : domain}
    
    logger.info("Creating or finding groups with name  %s" , kwargs["name"])
    group = create_or_find(client.groups, **kwargs)
    
            
    role_name = idpname + "_role"
    kwargs = { "name": role_name}
        
    logger.info("Creating or finding roles with name  %s" , kwargs["name"])
    role = create_or_find(client.roles, **kwargs)
  
    logger.info("Granting role to the project")  
    client.roles.grant(role, group=group, project=project)    
      
                
    kwargs = { "id": idpname, "enabled" : True}
        
    logger.info("Creating or finding idp with id  %s" , kwargs["id"])
    idp = create_or_find(client.federation.identity_providers, **kwargs)
      
            
    
    idp_mapping_id = idpname + "_mapping"        
    rules[0]["local"][1]["group"]["id"] = group.id        
    kwargs = { "mapping_id": idp_mapping_id, "rules" : rules}
    
    logger.info("Creating mapping with id  %s for the idp " , idp_mapping_id)
    mapping = create_or_find(client.federation.mappings, **kwargs)
          
      
        
    protocol_id = "saml2" 
    kwargs = { "protocol_id": protocol_id, "identity_provider" : idp,
              "mapping" : mapping}
        
    logger.info("Creating protocol %s for the idp %s" % ("saml2" , idpname))
    protocol = create_or_find(client.federation.protocols, **kwargs)
      
            
   

def get_client():
     client = get_admin_client(username="admin", projectname="admin",
                              user_domainname="Default", project_domainname="Default",
                              password="password", auth_url="http://localhost:35357/v3")
     return client

def get_client_with_unscoped_token():
     client = get_admin_client(username="admin", user_domainname="Default",
                              password="password", auth_url="http://localhost:35357/v3")
     return client

def generate_saml_asssertion(auth_token, sp_name):
    body = generate_token_json(auth_token,sp_name )
    
    headers = {"Content-Type" : "application/json"}

    url = "%s/auth/OS-FEDERATION/saml2" %(client.auth_url)
    
    response = send_request("POST", headers, url, data = json.dumps(body))
    logger.info(response.text)
    
    return response.text
    
    
def trasform_assertion_to_ecp(assertion):
        TEMPLATE = """<soap11:Envelope
        xmlns:soap11="http://schemas.xmlsoap.org/soap/envelope/"><soap11:Header><ecp:RelayState  
        xmlns:ecp="urn:oasis:names:tc:SAML:2.0:profiles:SSO:ecp"
        soap11:actor="http://schemas.xmlsoap.org/soap/actor/next"
        soap11:mustUnderstand="1">ss:mem:f88cd8ad5aeee3456e74900b306b5ed54ec9fb23c614f9fa7
3ece1c97ec004ed</ecp:RelayState><samlec:GeneratedKey  
        xmlns:samlec="urn:ietf:params:xml:ns:samlec"
        soap11:actor="http://schemas.xmlsoap.org/soap/actor/next">yvYbdh49qSJ7LqjFv+rfB8SR
97hPWMwQkL0KKOgSkhY=</samlec:GeneratedKey></soap11:Header>  
        <soap11:Body>%(response)s</soap11:Body></soap11:Envelope>"""

        assertion = '\n'.join(assertion.split('\n')[1:])
        assertion = assertion.replace('\n', '')
        ecp_assertion = TEMPLATE % {'response': assertion}
        
        return ecp_assertion


def exchange_assertion(sp_url, ecp_assertion):
        """Send assertion to a Keystone SP and get token."""
        
        headers={'Content-Type': 'application/vnd.paos+xml',
                # "Host": "keystone.sp:80"
                }
        
        return send_request("POST", headers, sp_url, data = ecp_assertion)
        
def handle_http_302_ecp_redirect(response):
        location = os.environ.get('OS_SP_AUTH')
        # We are not following the redirect URL, but the one at OS_SP_AUTH,
        # for our example is
        # http://keystone.sp/v3/OS-FEDERATION/identity_providers/kestone-idp/protocols/saml2/auth
        #return self.auth_session.request(location, method, authenticated=False, **kwargs)
        return send_request("GET", response.headers, "http://localhost:35357/v3/OS-FEDERATION/identity_providers/ks_idp1/protocols/saml2/auth" )
        
if __name__ == "__main__":
    client = get_client()
    
    idp_name = "ks_idp1"
    sp_name  = "ks_sp1"
    
    #provision_sp_for_idp(idp_name, client)
    #provision_idp_with_sp(client, sp_name, idp_name, "http://localhost:35357/Shibboleth.sso/SAML2/ECP")
    
  #  generate_saml_asssertion(client.auth_ref.auth_token, sp_name)
    #client = get_client_with_unscoped_token()
    #logger.info(client.auth_ref.auth_token)
    
    assertion = generate_saml_asssertion(client.auth_ref.auth_token, sp_name)
    ecp_assertion = trasform_assertion_to_ecp(assertion)
    
    #exchange_assertion("https://keystone.rndd.aw1.hpcloud.net:35357/Shibboleth.sso/SAML2/ECP", ecp_assertion)
    response = exchange_assertion("http://localhost:35357/Shibboleth.sso/SAML2/ECP", ecp_assertion)
    response = handle_http_302_ecp_redirect(response)
    print response.text
    
