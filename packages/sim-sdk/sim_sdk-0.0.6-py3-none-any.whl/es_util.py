import json
import logging

import requests
from elasticsearch import Elasticsearch, helpers

from util import nacos_client

# 通过 get_config() 函数获取配置（懒加载）
current_config = nacos_client.get_config()

es_config = current_config.get('es_config')
sql_to_es_url = current_config.get('sql_to_es_url')

# 新增索引
def createIndex(index_name):
    if es_config[0].startswith("https"):
        es = Elasticsearch(es_config, verify_certs=True, ca_certs="CloudSearchService.cer")
    else:
        es = Elasticsearch(es_config)
    es.indices.create(index=index_name)

# 删除索引
def delIndex(index_name):
    if es_config[0].startswith("https"):
        es = Elasticsearch(es_config, verify_certs=True, ca_certs="CloudSearchService.cer")
    else:
        es = Elasticsearch(es_config)
    es.indices.delete(index=index_name, ignore=[400, 404])

# 保存文档 (insert, update)
def save(index_name, doc, id = None):
    if es_config[0].startswith("https"):
        es = Elasticsearch(es_config, verify_certs=True, ca_certs="CloudSearchService.cer")
    else:
        es = Elasticsearch(es_config)
    es.index(index=index_name, id=id, body=doc)

# 批量新增文档
def saveBatch(index_name, docList, idList):
    if es_config[0].startswith("https"):
        es = Elasticsearch(es_config, verify_certs=True, ca_certs="CloudSearchService.cer")
    else:
        es = Elasticsearch(es_config)
    if len(docList) != len(idList):
        raise Exception("文档和id长度不一致")
    documents = []
    for i in range(len(docList)):
        documents.append({
            "_index": index_name,
            "_id": idList[i],
            "_source": docList[i]
        })
    helpers.bulk(es, documents)

# 查询文档
def list(index_name, query, page_num = 0, page_size = 1000):
    if es_config[0].startswith("https"):
        es = Elasticsearch(es_config, verify_certs=True, ca_certs="CloudSearchService.cer")
    else:
        es = Elasticsearch(es_config)
    from_index = page_size * page_num
    response = es.search(index=index_name, body=query, from_=from_index, size=page_size)
    data = response['hits']['hits']
    result_list = []
    info = {
        "total": response['hits']['total']['value'],  # 文档总数
        "isLastPage": response['hits']['total']['value'] <= page_size * (page_num + 1)  # 当前页是否是末页
    }
    for item in data:
        result_list.append({
            'id': item['_id'],  # 文档id
            'source': item['_source']  # 文档
            # 内容
        })
    return info, result_list

# 根据id查询文档
def selectById(index_name, id):
    if es_config[0].startswith("https"):
        es = Elasticsearch(es_config, verify_certs=True, ca_certs="CloudSearchService.cer")
    else:
        es = Elasticsearch(es_config)
    response = es.get(index=index_name, id=id)
    doc = response['_source']
    return doc

# 根据idList查询文档
def selectByIdList(index_name, idList):
    if es_config[0].startswith("https"):
        es = Elasticsearch(es_config, verify_certs=True, ca_certs="CloudSearchService.cer")
    else:
        es = Elasticsearch(es_config)
    doc_map = {}
    for id in idList:
        response = es.get(index=index_name, id=id)
        doc = response['_source']
        doc_map[id] = doc
    return doc_map


# 根据sql获得es query
def sql2es(sql_str):
    body = {
        "sqlStr": sql_str
    }
    response = requests.post(sql_to_es_url, json=body)
    if response.status_code == 200 and json.loads(response.text)['code'] == 200:
        data = json.loads(json.loads(response.text)['data'])
        return data
    else:
        logging.info("请求失败：%s %s", response.status_code, response.text)
        raise Exception(response.text)

# 根据索引名称获得orderBy
def getIdKeyByIndexName(indexName):
    if indexName == "source_data_index":
        return "basic_info.source_data_id"
    elif indexName == "dig_index":
        return "data_info.dig_info.id"
    elif indexName == "split_index":
        return "data_info.split_info.id"
    elif indexName == "evaluate_index":
        return "evaluate_info.id"
    else:
        return None