from obs import ObsClient, CompletePart, CompleteMultipartUploadRequest
from minio import Minio

from util import nacos_client

current_config = nacos_client.get_config()

bucket_name = current_config.get('bucket_name')
endpoint = current_config.get('endpoint')
ak = current_config.get('ak')
sk = current_config.get('sk')

minio_endpoint = current_config.get('minio_endpoint')
minio_bucket_name = current_config.get('minio_bucket_name')
minio_access_key = current_config.get('minio_access_key')
minio_secret_key = current_config.get('minio_secret_key')
minio_conf = {
    'endpoint': minio_endpoint,
    'access_key': minio_access_key,
    'secret_key': minio_secret_key,
    'secure': False
}

deploy_model = current_config.get('deploy_model')

def upload(objectKey, filePath):
    if deploy_model == current_config.get('MODEL_CLOUD'):
        obsClient = ObsClient(access_key_id=ak, secret_access_key=sk, server=endpoint)
        resp = obsClient.putFile(bucket_name, objectKey, file_path=filePath)
        result = {}
        if resp.status < 300:
            result = {"result": "success", "url": f"{resp.body.objectUrl}"}
        else:
            print(f"[upload error]:{resp.errorCode} - {resp.errorMessage}")
            result = {"result": "error", "errorCode": f"{resp.errorCode}", "errorMessage": f"{resp.errorMessage}"}
        # 关闭obsClient
        obsClient.close()
        return result
    elif deploy_model == current_config.get('MODEL_LOCAL'):
        try:
            client = Minio(**minio_conf)
            resp = client.fput_object(bucket_name=minio_bucket_name, object_name=objectKey, file_path=filePath)
            result = {"result": "success", "url": f"{objectKey}"}
            return result
        except Exception as e:
            result = {"result": "error", "errorCode": "500", "errorMessage": f"error:upload:{e}"}
            return result

def download(objectKey, downloadPath):
    if deploy_model == current_config.get('MODEL_CLOUD'):
        obsClient = ObsClient(access_key_id=ak, secret_access_key=sk, server=endpoint)
        resp = obsClient.getObject(bucket_name, objectKey, downloadPath=downloadPath)
        result = {}
        if resp.status < 300:
            result = {"result": "success", "url": f"{resp.body.url}"}
        else:
            print(f"[download error]:{resp.errorCode} - {resp.errorMessage}")
            result = {"result": "error", "errorCode": f"{resp.errorCode}", "errorMessage": f"{resp.errorMessage}"}
        # 关闭obsClient
        obsClient.close()
        return result
    elif deploy_model == current_config.get('MODEL_LOCAL'):
        try:
            client = Minio(**minio_conf)
            resp = client.fget_object(minio_bucket_name, objectKey, downloadPath)
            result = {"result": "success", "url": f"{objectKey}"}
            return result
        except Exception as e:
            result = {"result": "error", "errorCode": "500", "errorMessage": f"error:download:{e}"}
            return result

def getListOfFiles(prefix):
    if deploy_model == current_config.get('MODEL_CLOUD'):
        obsClient = ObsClient(access_key_id=ak, secret_access_key=sk, server=endpoint)
        resp = obsClient.listObjects(bucket_name, prefix=prefix, delimiter='/')
        if resp.status < 300:
            files = []
            for content in resp.body.contents:
                files.append(content.get("key"))
            result = {"result": "success", "files": files}
        else:
            print(f"[getListOfFiles error]:{resp.errorCode} - {resp.errorMessage}")
            result = {"result": "error", "errorCode": f"{resp.errorCode}", "errorMessage": f"{resp.errorMessage}"}
        obsClient.close()
        return result
    elif deploy_model == current_config.get('MODEL_LOCAL'):
        try:
            client = Minio(**minio_conf)
            resp = client.list_objects(bucket_name=minio_bucket_name, prefix=prefix)
            files = []
            for obj in resp:
                files.append(obj.object_name)
            result = {"result": "success", "files": files}
            return result
        except Exception as e:
            result = {"result": "error", "errorCode": "500", "errorMessage": f"error:getListOfFiles:{e}"}
            return result
