from minio import Minio


class MinioClientSingleton:
    _instance = None

    @staticmethod
    def get_instance(endpoint, access_key, secret_key):
        if MinioClientSingleton._instance is None:
            MinioClientSingleton._instance = Minio(
                endpoint,
                access_key=access_key,
                secret_key=secret_key,
                secure=False
            )
        return MinioClientSingleton._instance