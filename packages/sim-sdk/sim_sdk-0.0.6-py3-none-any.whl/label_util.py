import es_util
from data_deal_util import query_data_all

# -----  原始数据  -----  #
# 根据id查询原始数据标签
def selectSourceDataLabelById(id):
    return es_util.selectById("source_data_index", id)

# 根据idList批量查询原始数据标签
def selectSourceDataLabelByIdList(idList):
    return es_util.selectByIdList("source_data_index", idList)

# 保存原始数据标签 (insert or update)
def saveSourceDataLabel(id, doc):
    es_util.save("source_data_index", doc, id)

# 批量新增原始数据标签
def insertBatchSourceDataLabel(idList, docList):
    es_util.saveBatch("source_data_index", docList, idList)

# 原始数据标签新增或修改清洗状态
def setQualifiedById(id, value):
    doc = es_util.selectById("source_data_index", id)
    if "clean_info" not in doc["data_info"].keys():
        doc["data_info"]["clean_info"] = {}
    doc["data_info"]["clean_info"]["qualified"] = value
    es_util.save("source_data_index", doc, id)


# -----  场景数据  -----  #
# 根据id查询场景数据标签
def selectSceneDataLabelById(id):
    return es_util.selectById("dig_index", id)

# 根据idList批量查询场景数据标签
def selectSceneDataLabelByIdList(idList):
    return es_util.selectByIdList("dig_index", idList)

# 保存场景数据标签 (insert or update)
def saveSceneDataLabel(id, doc):
    es_util.save("dig_index", doc, id)

# 批量新增场景数据标签
def insertBatchSceneDataLabel(idList, docList):
    es_util.saveBatch("dig_index", docList, idList)

# 校验dig_info(挖掘算子自定义标签)
def verify_dig_info(doc_list):
    error_index_list, error_msg_map = verify_label(doc_list, "data_info.dig_info")
    return error_index_list, error_msg_map


# -----  切片数据  -----  #
# 根据id查询切片数据标签
def selectSplitDataLabelById(id):
    return es_util.selectById("split_index", id)

# 根据idList批量查询切片数据标签
def selectSplitDataLabelByIdList(idList):
    return es_util.selectByIdList("split_index", idList)

# 保存切片数据标签 (insert or update)
def saveSplitDataLabel(id, doc):
    es_util.save("split_index", doc, id)

# 批量新增切片数据标签
def insertBatchSplitDataLabel(idList, docList):
    es_util.saveBatch("split_index", docList, idList)

# -----  评测数据  -----  #
# 根据id查询评测数据标签
def selectEvaluateDataLabelById(id):
    return es_util.selectById("evaluate_index", id)

# 根据idList批量查询评测数据标签
def selectEvaluateDataLabelByIdList(idList):
    return es_util.selectByIdList("evaluate_index", idList)

# 保存评测数据标签 (insert or update)
def saveEvaluateDataLabel(id, doc):
    es_util.save("evaluate_index", doc, id)

# 批量新增评测数据标签
def insertBatchEvaluateDataLabel(idList, docList):
    es_util.saveBatch("evaluate_index", docList, idList)

# -----  通用  -----  #
# 获得mysql中的标签管理信息{fullName: datacenter_dataset_label_info}
def getLabel(prefix = None):
    sql = f"select id, key_name, parent_id, value_type, enum_value, status from datacenter_dataset_label"
    result = query_data_all(sql)
    id_row_map = {}
    for row in result:
        id_row_map[row['id']] = row
        row["full_name"] = row["key_name"]
    for row in result:
        parent_id = row['parent_id']
        while parent_id != 0:
            parent = id_row_map[parent_id]
            row["full_name"] = f'{parent["key_name"]}.{row["full_name"]}'
            parent_id = parent['parent_id']

    if prefix != None:
        map = {}
        for row in result:
            if row['full_name'].startswith(prefix):
                map[row['full_name']] = row
        return map
    else:
        map = {}
        for row in result:
            map[row['full_name']] = row
        return map

# 提取子标签
def extract_sub_label(doc_list, prefix = None):
    sub_doc_list = []
    if prefix != None:
        prefix_arr = prefix.split(".")
        for doc in doc_list:
            pass_flag = False
            for p in prefix_arr:
                # 如果文档为空，退出
                if doc == None:
                    pass_flag = True
                    break
                # 如果文档类型不为dict
                if type(doc) != dict:
                    raise Exception("prefix should be a dictionary, but got {}".format(type(doc)))
                if p in doc.keys():
                    doc = doc[p]
                else:
                    pass_flag = True
                    break
            if not pass_flag:
                sub_doc_list.append(doc)
    else:
        sub_doc_list = doc_list
    return sub_doc_list

# 校验label
def verify_label(doc_list, prefix = None):
    # 1.从标签管理表获取前缀为prefix的的标签类型
    label_info = getLabel(prefix)
    # 2.获取prefix层级下的子数据
    sub_doc_list = extract_sub_label(doc_list, prefix)
    # 3.展开标签
    return_list = []
    index = 0
    for doc in sub_doc_list:
        get_label_full_name_and_value(prefix, doc, return_list, index)
        index = index + 1
    # 4.校验每一个值
    error_msg_map = {}
    for r in return_list:
        error_msg = set()
        if r[0] not in label_info.keys():
            error_msg.add(f"{r[0]}标签不存在")
            if r[2] not in error_msg_map.keys():
                error_msg_map[r[2]] = set()
            error_msg_map[r[2]].update(error_msg)
            continue
        info = label_info[r[0]]
        if info["status"] == 0:
            error_msg.add(f"{r[0]}标签已禁用")
            if r[2] not in error_msg_map.keys():
                error_msg_map[r[2]] = set()
            error_msg_map[r[2]].update(error_msg)
            continue
        value_type = int(info["value_type"])
        value = r[1]
        if value_type == 0:
            if value != None and type(value) != dict:
                error_msg.add(f"{r[0]}标签{type(value)}类型错误，应为object")
        elif value_type == 1:
            if value != None and type(value) != list:
                error_msg.add(f"{r[0]}标签{type(value)}类型错误，应为list")
        elif value_type == 2:
            if value == None:
                continue
            else:
                try:
                    t = str(value)
                except Exception as e:
                    error_msg.add(f"{r[0]}标签{value}类型错误，应为string")
        elif value_type == 3:
            if value == None:
                continue
            else:
                try:
                    t = int(value)
                except Exception as e:
                    error_msg.add(f"{r[0]}标签{value}类型错误，应为int")
        elif value_type == 4:
            if value == None:
                continue
            else:
                try:
                    t = float(value)
                except Exception as e:
                    error_msg.add(f"{r[0]}标签{value}类型错误，应为double")
        elif value_type == 5:
            if value == None:
                continue
            else:
                try:
                    t = bool(value)
                except Exception as e:
                    error_msg.add(f"{r[0]}标签{value}类型错误，应为bool")
        elif value_type == 6:
            if value == None:
                continue
            else:
                try:
                    t = str(value)
                except Exception as e:
                    error_msg.add(f"{r[0]}标签{value}类型错误，应为enum(string)")
                    if r[2] not in error_msg_map.keys():
                        error_msg_map[r[2]] = set()
                    error_msg_map[r[2]].update(error_msg)
                    continue
                t = str(value)
                enum_value = info["enum_value"]
                if t not in enum_value.split(","):
                    error_msg.add(f"{r[0]}标签{t}枚举值错误，应为{enum_value}")
        elif value_type == 7:
            if value == None:
                continue
            else:
                try:
                    t = int(value)
                except Exception as e:
                    error_msg.add(f"{r[0]}标签{value}类型错误，应为timestamp(int)")
                    if r[2] not in error_msg_map.keys():
                        error_msg_map[r[2]] = set()
                    error_msg_map[r[2]].update(error_msg)
                    continue
                t = int(value)
                if t < 1000000000000:
                    error_msg.add(f"{r[0]}标签{t}过小，应大于1000000000000")
                if t > 9000000000000:
                    error_msg.add(f"{r[0]}标签{t}过大，应小于9000000000000")
        if len(error_msg) > 0:
            if r[2] not in error_msg_map.keys():
                error_msg_map[r[2]] = set()
            error_msg_map[r[2]].update(error_msg)
    error_index_list = []
    for i in range(len(sub_doc_list)):
        if i in error_msg_map.keys():
            error_index_list.append(i)
    return error_index_list, error_msg_map


# 递归，获得标签的全称和值,结果保存在return_list中，[(fullName, value)]
def get_label_full_name_and_value(name, doc, return_list, index):
    if doc == None:
        return_list.append((name, None, index))
    elif type(doc) == dict:
        return_list.append((name, {}, index))
        for key, value in doc.items():
            get_label_full_name_and_value(f"{name}.{key}", value, return_list, index)
    elif type(doc) == list:
        return_list.append((name, [], index))
        for item in doc:
            get_label_full_name_and_value(f"{name}.item", item, return_list, index)
    else:
        return_list.append((name, doc, index))