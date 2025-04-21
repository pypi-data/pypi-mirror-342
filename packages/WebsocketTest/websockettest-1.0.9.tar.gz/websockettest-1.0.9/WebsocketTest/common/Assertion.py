
from datetime import datetime, timedelta,date
from WebsocketTest.common.assertUtils import *
import pytest


def iAssert(response, keys_values_str):
    """
    断言JSON响应中的键值对是否符合预期。

    :param response: JSON响应作为字典。
    :param keys_values_str: 键值对字符串，用逗号或顿号分隔。
    :return: 包含断言结果的字典。
    """
    # 处理输入字符串，提取键和值。
    key_value_map = get_key_value(keys_values_str, delimiter='\n', pair_delimiter='=',opt="not in")

    for key,value in key_value_map.items():
        expected_value = value
        actual_value = str(get_value(response, key))
        msg = f"【{key}】 expected【{expected_value}】, but got 【{actual_value}】"
        if expected_value == '1no1' or expected_value is None:
            # 对于期望值为 '1no1' 或 None 的情况，仅检查键是否存在。
            assert has_key(response, key),  f"key:{key}  is not exist, check path!" 
        else:
            # 需要校验值的情况。
            if expected_value.startswith('*') and expected_value.endswith('*'):
                assert re.search(expected_value[1:-1], actual_value),  msg
            elif expected_value.endswith('*'):
                assert re.match(expected_value[:-1], actual_value), msg
            elif expected_value.startswith('*'):
                assert re.search(expected_value[1:], actual_value), msg
            elif isinstance(expected_value, dict):
                assert actual_value != expected_value, msg
            elif expected_value.startswith('eval_'):
                except_value = expected_value[5:]
                assert str(eval(except_value)) == actual_value, msg
            elif expected_value.startswith('in('):
                # 处理以 in 开头的情况。or:a in(1||2||3)
                expected_value_list = expected_value[3:-1].split('||')
                assert actual_value in expected_value_list, msg 
            elif expected_value.startswith('language_'):
                # 检测文本 language 
                assert check_text_language(actual_value) == expected_value[9:], msg
            else:
                assert actual_value == expected_value, msg


def urlAssert(req, res, query_info):
    """
    比较请求和响应参数。
    :param req: 请求数据
    :param res: 响应数据
    :param query_info: 查询信息字符串
    :return: 响应数据对象
    """
    query_info_dic = get_key_value(query_info, delimiter='\n', pair_delimiter=':')
    url_path = query_info_dic["queryPath"]
    res_url = get_Urlparam_dic(get_value(res, url_path), json_fields = ['pers_param', 'user_defined_params'])
    req_res_keys_str = query_info_dic["queryCondit"]
    req_res_keys = get_key_value(req_res_keys_str)
    for req_key,res_key in req_res_keys.items():
        req_val = get_value(req,req_key.strip(), decode_funcs={"parameter.custom.custom_data.UserParams": decode_base64,"parameter.custom.custom_data.UserData": url_decode})
        res_val = get_value(res_url,res_key.strip())
        assert req_val == res_val, f"【请求参数: {req_key}】与【响应参数: {res_key}】 的值对比不一致，\n请求值为: 【{req_val}】\n响应值为:【{res_val}】"
    return res_url

def arrayAssert(response_json, query_info):
    """
    path对应数据是数组, 根据多个条件查找数组中匹配的元素。
    """
    query_info_dic = get_key_value(query_info, delimiter='\n', pair_delimiter=':')
    query_condit = query_info_dic["queryCondit"]
    query_path = query_info_dic["queryPath"]

    # 解析 查询条件，将其转换为字典形式
    condit_dit = get_key_value(query_condit, delimiter=',', pair_delimiter='=')

    try:
        # 获取返回消息中path对应的JSON 数据
        path_json = get_value(response_json, query_path)
    except KeyError as e:
        raise ValueError(f'{e}')

    # 查找所有匹配项
    index_list = list(find_matching_index(path_json, condit_dit))

    if not index_list:
        raise ValueError(f'未找到符合条件的元素：【{query_condit}】')
    else:
        # 假设我们只关心第一个匹配项
        return path_json[int(index_list[0])]

def Assert(request,response, case_suite):
        """执行断言"""
        if case_suite["UniversalAssert"]:  #通用断言，key=value
            iAssert(response, case_suite['UniversalAssert'])

        if case_suite["ArrayAssert"]: #数组断言，value=[{...},{...},{...},...],给出条件，找到匹配的{...},再在{...}中执行通用断言 key=value
            iAssert(arrayAssert(response, case_suite['ArrayAssert']), case_suite['ArrayAssert'])
            
        if case_suite["URLAssert"]:  #url查询参数断言，某些resquest key(a.b.c=xx）会传给res url,作为res_url的查询参数(http://...?c=xx)，断言value(a.b.c)=value(cc)
            _res = urlAssert(request, response, case_suite['URLAssert'])
            if get_key_value(case_suite['URLAssert'], delimiter='\n', pair_delimiter='=',opt="not in"):
                iAssert(_res, case_suite['URLAssert'])