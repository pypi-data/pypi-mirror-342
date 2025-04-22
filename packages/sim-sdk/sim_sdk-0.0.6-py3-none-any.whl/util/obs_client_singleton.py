from obs import ObsClient


class ObsClientSingleton:
    _instance = None

    @staticmethod
    def get_instance(ak, sk, endpoint):
        if ObsClientSingleton._instance is None:
            ObsClientSingleton._instance = ObsClient(access_key_id=ak, secret_access_key=sk, server=endpoint)
        return ObsClientSingleton._instance