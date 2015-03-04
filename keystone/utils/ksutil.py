#Work in Progress

import os

from keystoneclient.v3 import client as v3client



def get_admin_client(username=None, password=None,
                     user_domainname=None, projectname=None,
                     project_domainname=None, auth_url=None):
      
        # Used for creating the ADMIN user
        OS_PASSWORD = password or os.environ['OS_PASSWORD']
        OS_USERNAME = username or os.environ['OS_USERNAME']
        # This will vary according to the entity:
        # the IdP or the SP
        OS_AUTH_URL = auth_url or os.environ['OS_AUTH_URL']
        OS_PROJECT_NAME = projectname or os.environ['OS_PROJECT_NAME']
        OS_PROJECT_DOMAIN_NAME = project_domainname or os.environ['OS_PROJECT_DOMAIN_NAME']
        
      
        return v3client.Client(auth_url=OS_AUTH_URL,
                             username=OS_USERNAME,
                             password=OS_PASSWORD,
                             project_name=OS_PROJECT_NAME,
                             project_domain_name=OS_PROJECT_DOMAIN_NAME)
    


def get_admintoken_client(token=None, auth_url=None):
      
        # Used for creating the ADMIN user        
        OS_AUTH_URL = auth_url or os.environ['OS_AUTH_URL']
        OS_TOKEN    = token or os.environ['OS_TOKEN']
       

        return v3client.Client(auth_url=OS_AUTH_URL,
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


def provision_idp_with_sp(client, url):
    try:
         r = client.regions.create(id="keystone.sp", url=url)
    except:
         r = client.regions.find(id=id)
    

def provision_sp_for_idp(idpname, client):
    
    try:
        domain_name = idpname + "_domain"
        domain = client.domains.create(name=domain_name)
    except:
        domain = client.domains.find(name=domain_name)
    
    try:
        project_name = idpname + "_project"
        project = client.projects.create(name=project_name, domain=domain)
    except Exception:        
        project = client.projects.find(name=project_name, domain=domain)
    
    try:
        group_name = idpname + "_group"
        group = client.groups.create(name=group_name, domain=domain)
    except:
        group = client.groups.find(name=group_name, domain=domain)
        
    try:
        role_name = idpname + "_role"
        role = client.roles.create(name=role_name)
    except:
        role = client.roles.find(name=role_name)
        
    client.roles.grant(role, group=group, project=project)    
        
    try:
        idp = client.federation.identity_providers.create(id=idpname, enabled=True)
    except:
        idp = client.federation.identity_providers.find(id=idpname)
            
    try:
        idp_mapping_id = idpname + "_mapping"
        print rules[0]["local"][1]
        rules[0]["local"][1]["group"]["id"] = group.id
        mapping = client.federation.mappings.create(
            mapping_id=idp_mapping_id, rules=rules)
    except:
        mapping= client.federation.mappings.find(
            mapping_id=idp_mapping_id)
                
    try:
        protocol_id = "saml2" 
        protocol = client.federation.protocols.create(protocol_id=protocol_id,
                                               identity_provider=idp,
                                               mapping=mapping)
    except:
        protocol = client.federation.protocols.find(protocol_id=protocol_id)


def get_client():
     client = get_admin_client(username="admin", projectname="admin",
                              user_domainname="Default", project_domainname="Default",
                              password="admin", auth_url="http://localhost:35357/v3")
     return client


if __name__ == "__main__":
    client = get_client()
    
    provision_sp_for_idp("ks_idp1", client)
    #provision_idp_with_sp(client, "http://keystone.sp/Shibboleth.sso/SAML2/ECP")
