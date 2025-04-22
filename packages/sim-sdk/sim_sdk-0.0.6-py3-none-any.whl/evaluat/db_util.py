from data_deal_util import query_data_all, execute_sql, executemany_sql, insert_and_get_id

import es_util


def update_task_4_start(task_id, state):
    # 更新任务
    sql_list = []
    args_list = []

    update_sql = "UPDATE datacenter_logsim_evaluat_task SET start_time=NOW(), state=%s WHERE id = %s"
    update_values = (state, task_id)

    sql_list.append(update_sql)
    args_list.append(update_values)

    execute_sql(sql_list, args_list)


def update_task_4_failed(task_id, state):
    # 更新任务
    sql_list = []
    args_list = []

    update_sql = "UPDATE datacenter_logsim_evaluat_task SET end_time=NOW(), state=%s WHERE id = %s"
    update_values = (state, task_id)

    sql_list.append(update_sql)
    args_list.append(update_values)

    execute_sql(sql_list, args_list)


def update_task_4_success(task_id, state):
    # 更新任务
    sql_list = []
    args_list = []

    update_sql = "UPDATE datacenter_logsim_evaluat_task SET end_time=NOW(), state=%s WHERE id = %s"
    update_values = (state, task_id)

    sql_list.append(update_sql)
    args_list.append(update_values)

    execute_sql(sql_list, args_list)


def update_logsim_eval_task_dataset(id, state):
    # 更新任务
    sql_list = []
    args_list = []

    sql = "update datacenter_logsim_evaluat_task_dataset set state = %s where id = %s"
    params = (state, id,)

    sql_list.append(sql)
    args_list.append(params)

    execute_sql(sql_list, args_list)


def update_logsim_eval_task_dataset_by_task_id(task_id, state):
    # 更新任务
    sql_list = []
    args_list = []

    sql = "update datacenter_logsim_evaluat_task_dataset set state = %s where task_id = %s"
    params = (state, task_id,)

    sql_list.append(sql)
    args_list.append(params)

    execute_sql(sql_list, args_list)

def get_model(model_id):
    sql = "select * from datacenter_logsim_model where id = %s"
    params = (model_id,)

    result = query_data_all(sql, params)

    return result


def get_logsim_task(task_id):
    sql = "select * from datacenter_logsim_task where id = %s"
    params = (task_id,)

    result = query_data_all(sql, params)

    return result


def get_evaluate_task(task_id):
    sql = "select * from datacenter_logsim_evaluat_task where id = %s"
    params = (task_id,)

    result = query_data_all(sql, params)

    return result


def get_evaluate_main_task(batch_no):
    sql = "select * from datacenter_logsim_evaluat_main_task where batch_no = %s"
    params = (batch_no,)

    result = query_data_all(sql, params)

    return result

def get_evaluate_main_tas_by_id(id):
    sql = "select * from datacenter_logsim_evaluat_main_task where id = %s"
    params = (id,)

    result = query_data_all(sql, params)

    return result


def get_logsim_task_result(task_id_list):
    sql = f"select * from datacenter_logsim_task_result where id in ({task_id_list})"
    dataset_list = query_data_all(sql)

    return dataset_list


def get_logsim_son_task_by_main_task_id(main_task_id_list):
    sql = f"select * from datacenter_logsim_task where parent_task_id in ({main_task_id_list})"
    task_list = query_data_all(sql)

    return task_list


def get_logsim_task_dataset(id):
    """
    获取回灌任务数据集信息
    :param task_id: 回灌任务id
    :return:    回灌数据集列表
    """
    sql = "SELECT * FROM datacenter_logsim_task_dataset WHERE id=%s"
    param = (id,)
    return query_data_all(sql, args=param)


def get_source_data(dataset_id_list):
    """
        获取源数据列表
        dataset_id_list: 数据集id列表 1,2,3,4
        """

    sql = f"select * from datacenter_source_data where id in ({dataset_id_list}) ORDER BY raw_time"
    dataset_list = query_data_all(sql)

    return dataset_list

def get_source_data_by_id(dataset_id):
    """
        获取源数据
        dataset_id: 数据集id
        """

    sql = f"select * from datacenter_source_data where id = {dataset_id}"
    dataset_list = query_data_all(sql)

    return dataset_list[0]

def get_split_data(dataset_id_list):
    """
        获取切片数据列表
        dataset_id_list: 数据集id列表 1,2,3,4
        """

    sql = f"select * from datacenter_split_data where id in ({dataset_id_list})"
    dataset_list = query_data_all(sql)

    return dataset_list

def get_dig_data(dataset_id_list):
    """
        获取场景数据列表
        dataset_id_list: 数据集id列表 1,2,3,4
        """

    sql = f"select * from datacenter_dig_detail where id in ({dataset_id_list})"
    dataset_list = query_data_all(sql)

    return dataset_list

def get_dig_data_by_data_id(data_id):
    """
        获取场景数据列表
        data_id_list: 数据集id列表 1,2,3,4
        """
    data_ids = [data_id]  # 转换为单元素列表

    quoted_ids = ", ".join(f"'{id}'" for id in data_ids)
    sql = f"SELECT * FROM datacenter_dig_detail WHERE data_id IN ({quoted_ids})"
    dataset_list = query_data_all(sql)

    return dataset_list

def get_dig_data_by_id(dataset_id):
    """
        获取场景数据
        dataset_id: 数据集id
        """

    sql = f"select * from datacenter_dig_detail where id = {dataset_id}"
    dataset_list = query_data_all(sql)

    return dataset_list[0]

def get_logsim_task_result_by_id(dataset_id_list):
    """
        获取回灌结果数据列表
        dataset_id_list: 回灌结果表主键id 1,2,3,4
        """

    sql = f"select * from datacenter_logsim_task_result where id in ({dataset_id_list})"
    dataset_list = query_data_all(sql)

    return dataset_list

def get_logsim_task_result_by(main_task_id, data_id):
    """
        获取回灌结果数据列表
        dataset_id_list: 回灌结果表主键id 1,2,3,4
        """

    sql = f"""
        select b.*
        from datacenter_logsim_task_dataset a join datacenter_logsim_task_result b on b.parent_id = a.id
        where a.task_id in (select id from datacenter_logsim_task where parent_task_id = %s) and a.data_id = %s
    """
    params = (main_task_id,data_id, )
    return query_data_all(sql, params)

def get_dataset(dataset_id_list):
    """
    获取数据集列表
    dataset_id_list: 数据集id列表 1,2,3,4
    """
    sql = f"select * from datacenter_dataset where id in ({dataset_id_list})"
    dataset_list = query_data_all(sql)

    return dataset_list


def get_vehicle(plate_no):
    sql = "select * from datacenter_vehicle where plate_number = %s"
    params = (plate_no,)
    return query_data_all(sql, params)


def get_vehicle_by_id(id):
    sql = "select * from datacenter_vehicle where id = %s"
    params = (id,)
    return query_data_all(sql, params)


def save_evaluate_task(logsim_task, logsim_task_id, task_name, bc_name, op_file_name, config_str, state,
                       argo_task_name, batch_no, main_task_id):
    model_id = None
    model_type = None
    if logsim_task is not None:
        model_id = logsim_task["model_id"]
        model_type = logsim_task["model_type"]


    sql = ("insert into datacenter_logsim_evaluat_task (task_name, start_time, logsim_task_id, "
           "logsim_model_id, state, bc_name, op_file_name, config_str, model_type, argo_task_name, "
           "batch_no, parent_task_id, creater, create_time, updater, update_time) "
           "values (%s, NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, NOW())")
    params = (task_name, logsim_task_id, model_id, state, bc_name, op_file_name, config_str, model_type,
              argo_task_name, batch_no, main_task_id, 'admin', 'admin',)

    result = insert_and_get_id(sql, params)

    return result


def save_evaluate_main_task(logsim_task, logsim_task_id, task_name, bc_name, op_file_name, config_str, state, batch_no,
                            metric_json):
    model_id = None
    model_type = None
    if logsim_task is not None:
        model_id = logsim_task["model_id"]
        model_type = logsim_task["model_type"]


    sql = ("insert into datacenter_logsim_evaluat_main_task (task_name, start_time, logsim_task_id, "
           "logsim_model_id, state, bc_name, op_file_name, config_str, model_type, "
           "batch_no, metric_json, creater, create_time, updater, update_time) "
           "values (%s, NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, NOW())")
    params = (task_name, logsim_task_id, model_id, state, bc_name, op_file_name, config_str, model_type,
              batch_no, metric_json, 'admin', 'admin',)

    result = insert_and_get_id(sql, params)

    return result


def get_label_data():
    """
    获取标签列表
    """

    sql = "select * from datacenter_label_data"
    label_list = query_data_all(sql)

    return label_list


def save_evluate_task_dataset(task_dataset_list):
    insert_task_result_sql = ("INSERT INTO datacenter_logsim_evaluat_task_dataset (task_id, tag_name, dataset_id,"
           "source_data_ids, split_data_id, dataset_name, dataset_path, start_timestamp, end_timestamp,"
           "start_frame_no, end_frame_no, dataset_type, src_dataset_path, update_time, data_id) VALUES (%s, %s, %s, %s, %s, "
           "%s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s)")

    executemany_sql(insert_task_result_sql, task_dataset_list)


def delete_evluate_task_dataset(task_id):
    # 更新任务
    sql_list = []
    args_list = []

    sql = "delete from datacenter_logsim_evaluat_task_dataset where task_id = %s"
    params = (task_id,)

    sql_list.append(sql)
    args_list.append(params)

    execute_sql(sql_list, args_list)

def update_evluate_task_dataset(id, operator_result, state):
    # 更新任务
    sql_list = []
    args_list = []

    sql = "update datacenter_logsim_evaluat_task_dataset set operator_result = %s, state = %s where id = %s"
    params = (operator_result, state, id,)

    sql_list.append(sql)
    args_list.append(params)

    execute_sql(sql_list, args_list)


def update_evluate_task_dataset_middle_files(id, middle_files):
    # 更新任务
    sql_list = []
    args_list = []

    sql = "update datacenter_logsim_evaluat_task_dataset set middle_files = %s where id = %s"
    params = (middle_files, id,)

    sql_list.append(sql)
    args_list.append(params)

    execute_sql(sql_list, args_list)

def get_evluate_task_dataset(task_id):
    sql = "select * from datacenter_logsim_evaluat_task_dataset where task_id = %s"
    params = (task_id,)
    return query_data_all(sql, params)

def save_qtest_task_result(evaluat_task_id, evaluat_task_dataset_id, tag_region, tag_day_night, miles,
                           tag_car_load, tag_road, start_time, end_time, evaluat_result):

    sql = ("insert into datacenter_qtest_evaluat_result ("
           "evaluat_task_id, "
           "evaluat_task_dataset_id, "
           "tag_region, "
           "tag_day_night,"
           "miles,"
           "tag_car_load, "
           "tag_road, "
           "start_time,"
           "end_time, "
           "evaluat_result, "
           "create_time) "
           "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())")
    params = (evaluat_task_id,
              evaluat_task_dataset_id,
              tag_region,
              tag_day_night,
              miles,
              tag_car_load,
              tag_road,
              start_time,
              end_time,
              evaluat_result,)

    result = insert_and_get_id(sql, params)

    return result


def get_evaluat_target_set(set_id):

    sql = "select * from datacenter_logsim_evaluat_target_set where id = %s"
    params = (set_id,)
    result = query_data_all(sql, params)

    return result


def get_evaluat_target_str(set_id):

    sql = "SELECT * FROM datacenter_logsim_evaluat_target WHERE parent_id=%s"
    params = (set_id,)
    result_rows = query_data_all(sql, params)

    target_keys = [row['target_name'] for row in result_rows]
    target_key = ','.join(target_keys)

    return target_key


def query_dataset_label_by_id(source_data_id):
    index_name = 'dataset_label'

    # 查询当前标签
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"data_info.dataset_type": "dig"}},
                    {"match": {"basic_info.source_data_id": source_data_id}}
                ]
            }
        }
    }
    info, result_list = es_util.list(index_name, query)
    # if len(result_list) > 0:
    #     print(f"{source_data_id}的标签已存在")
    #     print(json.dumps(result_list, indent=4, ensure_ascii=False))
    #     return
    return result_list

