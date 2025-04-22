import json
import re
import sys
import traceback
import requests
from pypinyin import lazy_pinyin, Style

from loguru import logger
import os
# 获取项目根目录
project_root = os.path.dirname(os.path.realpath(sys.argv[0]))
logs_dir = os.path.join(project_root, "logs")
# 如果日志目录不存在，则创建它
if not os.path.exists("logs"):
    os.makedirs("logs")
# 配置日志文件路径
logger.add("logs/{time:YYYY-MM-DD}.log", rotation="00:00",encoding="utf-8", level="DEBUG")

def datav_init_start(userinfo: dict, tokenid, login_id, service_url, yth_ip, customParams={}):
    if not tokenid:
        raise Exception("tokenid不能为空")
    if not login_id:
        raise Exception("login_id 不能为空")
    if not userinfo:
        raise Exception("用户信息不能为空")
    if not service_url:
        raise Exception("远程服务地址不能为空")
    user_id = userinfo.get("user_id")
    fiscal_year = userinfo.get("fiscal_year")
    mof_div_code = userinfo.get("mof_div_code")
    if not user_id or not fiscal_year or not mof_div_code:
        raise Exception("用户信息异常")
    url = f'{service_url}/get_datav_config?user_id={user_id}&fiscal_year={fiscal_year}&mof_div_code={mof_div_code}'
    response = requests.get(url, verify=False, headers={"loginid": login_id,"userinfo":json.dumps(userinfo)})
    if response.status_code == 200:
        res_json = json.loads(response.content)
        if res_json.get("state") == 'success':
            datav_configs = res_json.get("data")
            if datav_configs:
                for temp_datav_configs in datav_configs:
                    if not temp_datav_configs.get("data_sets"):
                        continue
                    menu_name = temp_datav_configs.get("menu_name")
                    excel_code = temp_datav_configs.get("excel_code")
                    authorization = temp_datav_configs.get("authorization")
                    datav_task_id = temp_datav_configs.get("datav_task_id")
                    deployed_excel_url = temp_datav_configs.get("deployed_excel_url")
                    data_url = temp_datav_configs.get("data_url")
                    data_sets = temp_datav_configs.get("data_sets")
                    data_count = datav_init_process(menu_name, tokenid, mof_div_code, fiscal_year, excel_code, user_id,
                                                    deployed_excel_url, data_url,
                                                    authorization, login_id,service_url,yth_ip,data_sets,customParams,user_info=userinfo)
                    param = {
                        "user_id":user_id,
                        "datav_task_id":datav_task_id,
                        "data_count":data_count,
                    }

                    try:
                        url = f'{service_url}/update_datav_execute_record'
                        response = requests.post(url, json=param, verify=False, headers={"loginid": login_id,"userinfo":json.dumps(userinfo)})
                    except Exception as e:
                        logger.info(traceback.format_exc(limit=None, chain=True))


def datav_init_process(menu_name: str, tokenid, mof_div_code, fiscal_year, excelCode, user_id, deployed_excel_url,
                       data_url,
                       authorization, login_id,service_url,yth_ip,data_sets=[],customParams={},user_info=None):
    try:
        return request_excel_cols_smart_report(excelCode, menu_name, tokenid, fiscal_year, mof_div_code, user_id, data_sets,
                                               deployed_excel_url, data_url, authorization,login_id,service_url,yth_ip,customParams,user_info)
    except Exception as e:
        error = traceback.format_exc(limit=None, chain=True)
        logger.info("datav########################################"+error)
        raise e


"""
智能报告迁移到模板库的爬数过程
或者说通用也可以
execelCode 从一体化获取的报表ID
menu_name 菜单名称
bas_dic_infos  需要爬取的报表ID
dicIdAndTableName 报表ID和报表名称的映射关系  如果没有表会根据映射关系的名称 去掉特殊字符和数字创建表 并且根据数据字段创建BAS_DIC_COLS表数据
后期给配上列名称后方可使用
"""


def request_excel_cols_smart_report(excelCode, menu_name, tokenid, fiscal_year, mof_div_code, user_id, data_sets,
                                    deployed_excel_url, data_url, authorization,login_id,service_url,yth_ip,customParams={},userinfo={}):
    request_excel_url = f"{yth_ip}{deployed_excel_url}?excelCode={excelCode}"
    # request_excel_url = f"http://223.223.190.114:10100/datav/v1/excel/deployed-excel?excelCode={excelCode}"
    session = requests.session()
    session.timeout = 60
    # 这块的tokenid没用，用的是Authorization这个验证
    headers = {
        "Authorization": authorization
    }
    try:
        response = session.get(request_excel_url, verify=False, headers=headers)
        excel_params = None
        if response.status_code == 200:
            res_json = json.loads(response.content)
            if str(res_json.get("code")) == "200":
                # 组装查询报表的查询参数
                styleString = res_json.get("data").get("styleString")
                searchList = json.loads(res_json.get("data").get("cfgString")).get("searchList")
                # logger.info(new_json)
                style_json = json.loads(styleString)
                # 统计所有报表的dataSetId
                ids = list(set([data.get("data_set_id") for data in data_sets]))
                logger.info("davav**********************"+str(ids))
                # 统计所有报表的dataSetId结束

                dicIdAndDataName = {item["data_set_id"]: item.get("data_name") for item in data_sets}
                dicIdAndTableName = {item["data_set_id"]: item.get("table_name") for item in data_sets}
                dicIdAndClassName = {item["data_set_id"]: item.get("class_name") for item in data_sets}
                dicIdAndColumnMapping = {item["data_set_id"]: item.get("column_mapping") for item in data_sets}

                data_count = 0
                for tepm_style_json in style_json:
                    formConfig = tepm_style_json.get("formConfig")
                    fields = list()
                    fieldIds = list()
                    parameterRequestInfos = list()
                    datasetId = None
                    temp_search_list = None
                    if not formConfig or not formConfig.items():
                        continue
                    for key, json_value in formConfig.items():
                        new_json = {}
                        sourceConfig = json_value.get('sourceConfig')
                        if datasetId is None or datasetId == '':
                            datasetId = sourceConfig.get('datasetId')
                            if datasetId not in ids:
                                continue
                        if not temp_search_list:
                            temp_search_list = [temp for temp in searchList if temp.get("datasetId") == datasetId]
                            logger.info("davav**********************"+str(temp_search_list))
                        fieldId = sourceConfig.get("fieldId")
                        if fieldId and fieldId not in fieldIds:
                            fieldIds.append(fieldId)
                            new_json['fieldId'] = fieldId
                            new_json['aggregateType'] = "" if sourceConfig.get(
                                "aggregateType") is None else sourceConfig.get("aggregateType")
                            new_json["sortType"] = "" if sourceConfig.get("sortType") is None else sourceConfig.get(
                                "sortType")
                            new_json["filterInfo"] = sourceConfig.get('filterInfo')
                            fields.append(new_json)
                    if datasetId not in ids:
                        continue
                    # 记录searchlist里有哪些参数
                    search_list_field = []
                    for single_searche in temp_search_list:
                        value = "null"
                        if single_searche.get("parameterKey") == 'mof_div':
                            value =mof_div_code
                        elif single_searche.get("parameterKey") == 'fiscal_year':
                            value = fiscal_year
                        elif single_searche.get("parameterKey") == 'pro_name':
                            # 不清楚为什么是999999
                            value = "999999"
                        search_list_field.append(single_searche.get("parameterKey"))
                        parameterRequestInfo = {
                            "parameterKey": single_searche.get("parameterKey"),
                            "type": "VALUE",
                            "value": value,
                            "apiRequestProperty": {}
                        }
                        parameterRequestInfos.append(parameterRequestInfo)
                    # 配置了默认参数时，需要将search_list没有的参数放进去
                    cur_parameterRequestInfos = [data.get("parameterRequestInfos") for data in data_sets if
                                                 data.get("data_set_id") == datasetId and data.get("parameterRequestInfos") is not None]
                    if cur_parameterRequestInfos and len(cur_parameterRequestInfos) > 0:
                        cur_parameterRequestInfos = json.loads(cur_parameterRequestInfos[0])
                        for param in cur_parameterRequestInfos:
                            # 当前变量
                            parameterKey = param.get("parameterKey")
                            if parameterKey in search_list_field:
                                continue
                            # 获取需要替换的变量
                            value = param.get("value")
                            replace_var = re.search(r'#.*#', value)
                            if replace_var is not None:
                                replace_var_str = replace_var.group()
                                field = replace_var_str[1:-1]
                                if customParams.get(field):
                                    value = value.replace(replace_var_str, str(customParams.get(field)))
                                    param["value"] = value
                                else:
                                    param["value"] = 'null'
                            parameterRequestInfos.append(param)
                    if datasetId is None or datasetId == '':
                        continue
                    excel_params = {"dataSetId": datasetId, "fields": fields,
                                    "parameterRequestInfos": parameterRequestInfos}
                    logger.info("davav**********************"+f"request_pay_bgt_detail_data --> excel_params--->{excel_params}", )
                    year, mof_div_code = fiscal_year, mof_div_code
                    params = build_request_data(excel_params, tokenid, year, mof_div_code)
                    logger.info("davav**********************"+f"request_pay_bgt_detail_data --> params--->{params}", )
                    # 请求数据
                    data_list = request_datas(params, year, mof_div_code, data_url, authorization,
                                              dicIdAndTableName.get(datasetId), dicIdAndClassName.get(datasetId),
                                              user_id,yth_ip,service_url,login_id)
                    logger.info("davav**********************"+f"request_datas --> data_list--->{len(data_list)}",)
                    entities = []
                    if data_list and len(data_list) > 0:
                        data_count += len(data_list)
                        # 第一步判断表是否存在
                        session = requests.session()
                        # 本来想写通用的接口，但是这里获取表名称有点疑问  之后再优化吧，不行把dicIdAndTableName写为必填参数
                        table_name = dicIdAndTableName.get(datasetId)
                        data_name = dicIdAndDataName.get(datasetId)
                        if not table_name:
                            table_name = str(data_name).replace("-", "") \
                                .replace("_", "") \
                                .replace("（", "") \
                                .replace("）", "") \
                                .replace("(", "") \
                                .replace(")", "")
                            digits = re.findall(r"\d", table_name)
                            for digit in digits:
                                table_name = table_name.replace(digit, '')
                            table_name = ''.join(lazy_pinyin(table_name, style=Style.FIRST_LETTER)).upper()
                        url = f'{service_url}/check_exists_dic_info_and_table_by_table_name?tableName={table_name}&mof_div_code={mof_div_code}&fiscal_year={fiscal_year}'
                        response = session.get(url, verify=False, headers={"loginid": login_id,"userinfo":json.dumps(userinfo)})
                        table_exists = False
                        bas_dic_info_exists = False
                        bas_dic_cols_exists = False
                        if response.status_code == 200:
                            res_json = json.loads(response.content)
                            if res_json.get("state") == 'success':
                                data = res_json.get("data")
                                table_exists = data.get("table")
                                bas_dic_cols_exists = data.get("dic_cols") is not None and len(data.get("dic_cols")) > 0
                                bas_dic_info_exists = data.get("dic_info") is not None and len(data.get("dic_info")) > 0
                        if not table_exists or not bas_dic_cols_exists or not bas_dic_info_exists:
                            # 开始调用创建表
                            logger.info("davav**********************"+"开始创建表")
                            param = {
                                "data": data_list[0],
                                "dict_name": data_name,
                                "dic_type": '5',
                                "dict_code": "999998",
                                "table_name": table_name,
                                "appguid": "ficsal",
                                "menu_name": menu_name,
                                "column_type": {},
                                "column_name": {},
                                "dic_id": datasetId,
                                "user_id":user_id,
                                "mof_div_code":mof_div_code,
                                "fiscal_year":fiscal_year
                            }
                            url = f'{service_url}/insert_info_and_cols_by_json_handler'
                            response = requests.post(url, json=param, verify=False, headers={"loginid": login_id,"userinfo":json.dumps(userinfo)})
                            if response.status_code == 200:
                                res_json = json.loads(response.content)
                                if res_json.get("state") == 'success':
                                    data = res_json.get("data")
                                    logger.info("davav**********************"+str(data))
                                else:
                                    raise Exception(res_json.get("msg"))
                        for data in data_list:
                            data["user_id"] = user_id
                            entities.append(data)
                        # 数据入库
                        biz_keys = []
                        columns = ', '.join(entities[0].keys())
                        # 字段情况不清楚，全部值为text # 数据入库
                        # 清除数据
                        params = {
                            "execute_type": "sql",
                            "executesql": f"delete from {table_name} where user_id = '{user_id}' and fiscal_year = '{fiscal_year}'"
                        }
                        requestServer(service_url,login_id,"execute_sql", params)
                        # 写入数据
                        insertParams = {
                            "execute_type": "batch_insert",
                            "datas": entities,
                            "table_name": table_name
                        }
                        requestServer(service_url,login_id,"execute_sql", insertParams)
                return data_count
            else:
                raise dataVException(res_json)
        else:
            # rm_sql = "delete from cur_fiscal_pay_process where 1=1"
            # params = {
            #     "execute_type": "sql",
            #     "executesql": rm_sql
            # }
            # requestServer("execute_sql", params)
            raise Exception(response.reason)
        return 0
    except Exception as e:
        # rm_sql = "delete from cur_fiscal_pay_process where 1=1"
        # params = {
        #     "execute_type": "sql",
        #     "executesql": rm_sql
        # }
        # requestServer("execute_sql", params)
        raise e

def dataVException(res_json):
    msg = res_json.get('msg') if res_json.get('msg') else res_json.get('errMsg')
    return Exception(msg)

def build_request_data(excel_params, tokenid, year, mof_div_code):
    default_dict = {
        "pageNum": 1,
        "pageSize": 20,
        "total": 0,
        "page": False,
        "filterExp": "",
        "dataSourceKey": year,
        "businessContext": {
            "token": tokenid
        },
        "enableRowReadableAuthority": False,
        "enableRowEditableAuthority": False,
        "enableColumnReadableAuthority": False,
        "enableColumnEditableAuthority": False
    }
    if excel_params:
        excel_params.update(default_dict)
    return excel_params


def request_datas(params, year, mof_div_code, data_url, authorization, table_name, class_name, user_id,yth_ip,service_url,login_id):
    bgt_detail_url = f"{yth_ip}{data_url}"
    # bgt_detail_url = f"http://223.223.190.114:10100/datav/v1/excel/data-displayed"
    session = requests.session()
    session.timeout = 60
    # 这块的tokenid没用，用的是Authorization这个验证
    headers = {
        "Authorization": authorization
    }
    try:
        response = session.post(bgt_detail_url, json=[params], verify=False, headers=headers)
        data_list = list()
        if response.status_code == 200:
            res_json = json.loads(response.content)
            if str(res_json.get("code")) == "200":
                detail_list = res_json.get("data")
                if detail_list and len(detail_list) > 0:
                    for data_json in detail_list:
                        rows_list = data_json.get("rows")
                        if rows_list and len(rows_list) > 0:
                            for rows in rows_list:
                                # 行转列处理
                                row_dict = {"fiscal_year": year, "mof_div_code": mof_div_code, "user_id": user_id}
                                for data_row in rows:
                                    field = data_row.get("fieldName").lower()
                                    # 上海不乐意改表、datav也不改，直接写死转换 把下划线都去掉
                                    if mof_div_code.startswith("31"):
                                        field = field.replace("_","")
                                    row_dict[field] = data_row.get("value")
                                if class_name:
                                    cls = globals()[class_name]
                                    row_dict = cls(**row_dict).__dict__
                                data_list.append(row_dict)
            else:
                raise dataVException(res_json)
        else:
            rm_sql = f"delete from {table_name} where 1=1"
            params = {
                "execute_type": rm_sql
            }
            requestServer(service_url,login_id,"execute_sql", params)
            raise Exception(response.reason)
        return data_list
    except Exception as e:
        rm_sql = f"delete from {table_name} where 1=1"
        params = {
            "execute_type": rm_sql
        }
        requestServer(service_url,login_id,"execute_sql", params)
        raise e


def requestServer(service_url,login_id,execute_sql, params):
    try:
        # remoteDBReqInfo = RemoteDBReqInfo(**params)
        url = f'{service_url}/' + execute_sql
        session = requests.session()
        # if not service_url:
        #     logger.info("davav**********************"+"远程请求地址service_url未配置 {}", service_url)
        # return remote_execute_sql(remoteDBReqInfo, None)
        response = session.post(url, json=params, verify=False, headers={"loginid": login_id})
        # logger.info("davav**********************"+"sx_request_basedata response {} ", response)
        if response.status_code == 200:
            res_json = json.loads(response.content)
            if res_json.get("state") == 'success':
                datas = res_json.get("data")
                return datas
            else:
                raise Exception(res_json.get("msg"))
        else:
            raise Exception(f"接口访问失败：{response},url is {url}")
    except Exception as e:
        error = traceback.format_exc(limit=None, chain=True)
        logger.info("datav#####################################调用远程保存接口失败 {}", error)

