def sudo(filename):
  from os import getenv as env
  import json
  file = open(filename,"w")
  json_obj = {}
  json_obj["type"] = env("type")
  json_obj["project_id"] = env("project_id")
  json_obj["private_key_id"] = env("private_key_id")
  json_obj["private_key"] = env("private_key")
  json_obj["client_email"] = env("client_email")
  json_obj["client_id"] = env("client_id")
  json_obj["auth_uri"] = env("auth_uri")
  json_obj["token_uri"] = env("token_uri")
  json_obj["auth_provider_x509_cert_url"] = env("auth_provider_x509_cert_url")
  json_obj["client_x509_cert_url"] = env("client_x509_cert_url")
  file.write(json.dumps(json_obj, indent = 4))
  file.close()
  return