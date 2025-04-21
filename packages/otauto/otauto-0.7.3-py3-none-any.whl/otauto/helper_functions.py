def set_merge_dicts(dict_a, dict_b):
    """
    合并两个字典，如果有相同的键，则以 dict_a 的值为准
    :param dict_a: 第一个字典
    :param dict_b: 第二个字典
    :return: 合并后的字典
    """
    merged_dict = {}
    # 先处理 dict_a
    for key in dict_a:
        if key not in merged_dict:
            merged_dict[key] = {}
        merged_dict[key].update(dict_a[key])
    # 再处理 dict_b
    for key in dict_b:
        if key not in merged_dict:
            merged_dict[key] = {}
        # 更新 dict_b 的键，如果存在相同的键，则以 dict_a 的值为准
        for subkey, value in dict_b[key].items():
            if subkey not in merged_dict[key]:  # 只有当子键不存在时才添加
                merged_dict[key][subkey] = value
    return merged_dict

def 变量名():
    """
    队伍相关:
    res_team_status:组队状态
    res_team_information:队伍信息
    res_team_number:队伍番号
    res_team_size:队伍人数
    res_captain:队长
    res_team_member:队员
    功能相关:
    res_target_image:目标图片
    res_screenshot_image:截图图片
    res_text:文字
    res_image:图片
    res_color:颜色
    res_coordinates:坐标
    res_scope:范围
    result:结果
    ls_result:列表结果
    dic_result:字典结果

    流程相关:
    function:功能
    res_responsibilities:职责
    res_status_code:状态码
    res_serial_number:序列号
    res_friend_request:好友申请
    counter:计数器
    flag:标志位
    res_task:任务
    ls_task_keyword:任务关键字列表
    ls_exception_code:异常代码
    res_game_interface:游戏界面
    ls_progress:进度器列表
    res_mission_location:任务地点
    res_battle_status:战斗状态
    res_other_interfaces:其他界面
    res_current_time:当前时间
    res_binding:绑定
    res_level:等级
    res_location:地点
    res_equipment_number:设备编号
    res_changes:改动
    res_not_choosing:不选择
    res_exception:异常
    main_line:主线
    res_delay_time:延迟时间
    res_time_difference:时间差
    """
    pass