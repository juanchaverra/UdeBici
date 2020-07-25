import os, uuid, sys
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core._match_conditions import MatchConditions
from azure.storage.filedatalake._models import ContentSettings, FileProperties

# Conectarse a la cuenta
try:
    global service_client
    service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
        "https", 'datalakeudea'),
        credential='KYbkkoQvPCNWHfWmS3EFxt2GVIdGFwfDLluo8scL3hhLSWHZpG3ExayCa6yz4v66mItMKhcbW9lNTEVfYbP1yQ==')
except Exception as e:
    print(e)


# Subir un archivo a un directorio Tip si es muy grande cambiar append_data por upload_data
def upload_file_to_directory(cedula):
    try:
        file_system_client = service_client.get_file_system_client(file_system="registro")
        directory_client = file_system_client.get_directory_client("Fotos")
        content_settings = ContentSettings(content_type='image/jpeg')
        file_client = directory_client.get_file_client(str(cedula) + ".jpeg")
        file_client.create_file(content_settings)
        local_file = open("Fotos/" + str(cedula) + ".jpeg", 'rb')
        file_contents = local_file.read()
        file_client.upload_data(data=file_contents, overwrite=True)

        file_client.set_http_headers(content_settings)
    except Exception as e:
        print(e)


def download_file_from_directory(cedula):
    try:
        file_system_client = service_client.get_file_system_client(file_system="registro")
        directory_client = file_system_client.get_directory_client("Fotos")
        local_file = open("Des/"+str(cedula) + ".jpeg", 'wb')
        file_client = directory_client.get_file_client(str(cedula)+".jpeg")
        download = file_client.download_file()
        downloaded_bytes = download.readall()
        local_file.write(downloaded_bytes)
        local_file.close()
        return True
    except Exception as e:
        print(e)
        return False


def delete_file_from_directory(cedula):
    try:
        file_system_client = service_client.get_file_system_client(file_system="registro")
        directory_client = file_system_client.get_directory_client("Fotos")
        file_client = directory_client.get_file_client(str(cedula)+".jpeg")
        file_client.delete_file()
    except Exception as e:
      print(e)


cc = 987451325
upload_file_to_directory(cc)
#download_file_from_directory(cc)