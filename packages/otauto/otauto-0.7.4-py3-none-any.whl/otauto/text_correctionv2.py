import difflib
from loguru import logger
"""
更新日志:2024-10-21 09:20:47
替换符号
1.找出和基准文字高于相似度的识别文字
2.1次过滤关键字,keywords_filter,支持2次过滤关键词,keywords_filter_repeatedly,此功能暂时未启用
3.返回所有的结果,以字典的形式
"""
def process_text_comparison(str1:str, str2:str,con:float=0.6):
    """
    比较两个字符串的相似度
    str1 = "【阵营】【战斗】挑战义军精锐都"
    str2 = "挑战义军精锐【阵营]战斗】"
    res_tuple=process_text_comparison(str1, str2)
    print(res_tuple)


    :param str1: 文字,基准文字
    :param str2: 文字,识别出的文字
    :param con: 相似度阈值,默认为0.6
    :return:
    """


    # 将两个字符串转为集合
    set1 = set(str1)
    set2 = set(str2)

    # 求两个集合的交集，即两个字符串中的相同字
    same_chars = set1 & set2

    # 计算相似度
    similarity = len(same_chars) / (len(set1) + len(set2) - len(same_chars))
    if similarity>con:
        return str1,round(similarity,3)


def process_text_comparison_list(text_list: list, text_dict: dict, con: float = 0.6):
    """
    已弃用
    比较两个字符串的相似度
    :param text_list:
    :param text_dict:
    :param con:
    :return:
    """

    results = {}
    replaced_keys = set()
    for item in text_list:
        for key in text_dict.keys():
            s = difflib.SequenceMatcher(None, item, key)
            similarity = round(s.ratio(), 3)

            if similarity > con:
                if item not in results:
                    results[item] = [{key: text_dict[key]}, similarity]
                    replaced_keys.add(key)
                else:
                    if similarity > results[item][1]:
                        results[item] = [{key: text_dict[key]}, similarity]
                        replaced_keys.add(key)

    # 删除已替换的键
    for key in replaced_keys:
        del text_dict[key]

    return {"results":results, "text_dict":text_dict}


def process_text_comparison_dict(text_dict: dict, data_dict: dict, con: float = 0.6):
    results = {}
    replaced_keys = set()

    try:

        for text_key, text_value in text_dict.items():
            keywords = text_key.split("|")
            for data_key, data_value in data_dict.items():
                matching_keywords = [kw for kw in keywords if kw in data_key]
                keyword_similarity = len(matching_keywords) / len(keywords)
                value_similarity = difflib.SequenceMatcher(None, str(text_value), str(data_key)).ratio()
                if keyword_similarity > con and value_similarity > con:
                    replaced_keys.add(data_key)
                    if text_value not in results or keyword_similarity > results[text_value][1] or value_similarity > results[text_value][2]:
                        results[text_value] = [{data_key: data_value}, value_similarity]

        for key in replaced_keys:
            del data_dict[key]
    except Exception as e:
        logger.error(f"Error occurred while processing text comparison: {e}")

    return {"results": results, "text_dict": data_dict}


def data_filtering(data_dict):
    """
    识别出来有歧义的键值对2次过滤,主要区别未完成和完成
    a = {'寻找:武道灵(未完成)': [{'寻找:武道灵(未完成)': (1202, 274, 0.989, 4)}, 0.9523809523809523],
         '寻找:武道灵(完成)': [{'寻找:武道灵(未完成)': (1202, 274, 0.989, 4)}, 0.9],
         '【主线】为了爵位！': [{'【主线】为了爵位！': (1185, 258, 0.988)}, 1.0],
         '拥有:一个爵位(未完成)': [{'拥有:一个爵位(未完成)': (1200, 272, 0.977)}, 1.0],
         '交付人:苏三': [{'交付人:苏三': (1202, 290, 1.0)}, 1.0],
         '【阵营】【战斗】挑战义军精锐都': [{'【阵营】【战斗】挑战义军精锐都': (1185, 306, 0.995)}, 1.0],
         '打倒:义军精锐都尉(0/1)': [{'打倒:义军精锐都尉(0/1': (1203, 339, 0.997)}, 0.963],
         '【阵营】【后勤】探查刀魔': [{'【阵营】【后勤】探查刀魔': (1185, 354, 0.992)}, 1.0],
         '侦查:梨花唐3(未完成)': [{'侦查:梨花唐3(未完成)': (1203, 371, 0.978)}, 1.0],
        '侦查:梨花唐3(完成)': [{'侦查:梨花唐3(未完成)': (1203, 371, 0.978)}, 0.95],
         '完成:装备强化(未完成)': [{'完成:装备强化(朱完成)': (1201, 464, 0.854)}, 0.917]
         }
    same_keys_dict,diff_dict=data_filtering(a)
    print("Same Keys: ", same_keys_dict)
    print("Diff Dict: ", diff_dict, len(diff_dict))
    :param data_dict:
    :return:
    """
    same_keys = []
    diff_keys = []

    for key1, val1 in data_dict.items():
        if isinstance(val1[0], dict):
            for key2, val2 in data_dict.items():
                if key1 != key2:
                    if val1[0].keys() == val2[0].keys():
                        pair = {key1: val1, key2: val2}
                        if pair not in same_keys:
                            same_keys.append(pair)

    for key1, val1 in data_dict.items():
        if isinstance(val1[0], dict):
            keys_in_same = [k for pair in same_keys for k in pair]
            if key1 not in keys_in_same:
                for key2, val2 in data_dict.items():
                    if key1 != key2:
                        pair = {key1: val1, key2: val2}
                        if pair not in diff_keys:
                            diff_keys.append(pair)

    diff_dict = {}
    for pair in diff_keys:
        diff_dict.update(pair)

    for pair in same_keys:
        for key in pair:
            if key in diff_dict:
                del diff_dict[key]
    # same_keys_dict = {}
    # for pair in same_keys:
    #     same_keys_dict.update(pair)

    return same_keys, diff_dict


# def keywords_filter(data_dict, keywords):
#     """
#     比较关键词是否一致
#     res_dict={}
#     keywords_list = ['未完']
#     data_list=[{'寻找:武道灵(未完成)': [{'寻找:武道灵(未完成)': (1202, 274, 0.989, 4)}, 0.9523809523809523], '寻找:武道灵(完成)': [{'寻找:武道灵(未完成)': (1202, 274, 0.989, 4)}, 0.9]}, {'侦查:梨花唐3(未完成)': [{'侦查:梨花唐3(未完成)': (1203, 371, 0.978)}, 1.0], '侦查:梨花唐3(完成)': [{'侦查:梨花唐3(未完成)': (1203, 371, 0.978)}, 0.95]}]
#     for data in data_list:
#         d_dict = keywords_filter(data, keywords_list)
#         res_dict.update(d_dict)
#     print(res_dict)
#     :param data_dict:字典
#     :param keywords: 关键词列表
#     :return:
#     """
#     d_dict = {}  # 用于存储结果的新字典
#     for c_key, c_value in data_dict.items():
#         if isinstance(c_value, list) and len(c_value) > 0:  # 检查c_value是否为字典
#             if isinstance(c_value[0], dict):
#                  for sub_key, sub_value in c_value[0].items():  # 检查子字典
#                     for word in keywords:
#                         if word in sub_key and word in c_key: # 判断关键字
#                             d_dict[c_key] = c_value  # 保存键值对
#     return d_dict

def keywords_filter(data_dict, keywords):
    """
    根据关键词和可信度过滤字典中的键值对。
    :param data_dict: 字典
    :param keywords: 关键词列表
    :return: 包含符合条件的键值对的新字典
    """
    d_dict = {}  # 用于存储结果的新字典

    for c_key, c_value in data_dict.items():
        if isinstance(c_value, list) and len(c_value) > 0:  # 检查c_value是否为列表并且不为空
            if c_value[-1] == 1.0:
                d_dict[c_key] = c_value  # 如果最后一个元素是1.0，直接保留
            elif isinstance(c_value[0], dict):
                for sub_key, sub_value in c_value[0].items():  # 检查子字典
                    for word in keywords:
                        if word in sub_key and word in c_key:  # 判断关键字
                            d_dict[c_key] = c_value  # 保存键值对
                            break  # 找到匹配就可以停止继续检查这个c_value
    return d_dict

def keywords_filter_repeatedly(data_dict, keywords_1, keywords_2: list = None):
    """
    先根据关键词列表keywords_1过滤字典中的键值对，
    再根据关键词列表keywords_2再次过滤已过滤的结果。
    # 示例数据
    data_list = [{'打倒:豪猪王(已完成)': [{'打倒:豪猪(已完成)': (1202, 276, 0.996, 4)}, 0.9523809523809523],
        '打倒:豪猪(/5)': [{'打倒:豪猪(已完成)': (1202, 276, 0.996, 4)}, 0.7368421052631579]},
       {'打倒:豪猪王(已完成)': [{'打倒:豪猪(已完成)': (1202, 276, 0.996, 4)}, 0.9523809523809523],
        '打倒:豪猪(已完成)': [{'打倒:豪猪(已完成)': (1202, 276, 0.996, 4)}, 0.99]},
       {'打倒:豪猪(/5)': [{'打倒:豪猪(已完成)': (1202, 276, 0.996, 4)}, 0.7368421052631579],
        '打倒:豪猪(已完成)': [{'打倒:豪猪(已完成)': (1202, 276, 0.996, 4)}, 0.99]}]

    keywords_list_1 = ['完成']
    keywords_list_2 = ["猪("]
    # 处理示例数据
    res_dict = {}
    for data in data_list:
        d_dict = keywords_filter(data, keywords_list_1, keywords_list_2)
        res_dict.update(d_dict)
    print(res_dict)

    :param data_dict: 字典
    :param keywords_1: 第一次过滤的关键词列表
    :param keywords_2: 第二次过滤的关键词列表,默认为None
    :return: 包含符合条件的键值对的新字典
    """
    def filter_with_keywords(data, keywords):
        """
        根据关键词过滤数据字典的辅助函数。
        """
        filtered_dict = {}  # 用于存储过滤后的结果字典

        for c_key, c_value in data.items():
            if isinstance(c_value, list) and len(c_value) > 0:  # 检查c_value是否为列表并且不为空
                if c_value[-1] == 1.0:
                    filtered_dict[c_key] = c_value  # 如果最后一个元素是1.0，直接保留
                elif isinstance(c_value[0], dict):
                    for sub_key, sub_value in c_value[0].items():  # 检查子字典
                        for word in keywords:
                            if word in sub_key and word in c_key:  # 判断关键字
                                filtered_dict[c_key] = c_value  # 保存键值对
                                break  # 找到匹配就可以停止继续检查这个c_value
        return filtered_dict

    # 第一次过滤
    first_filtered = filter_with_keywords(data_dict, keywords_1)

    # 第二次过滤
    if keywords_2:
        second_filtered = filter_with_keywords(first_filtered, keywords_2)
        return second_filtered
    else:
        return first_filtered


def process_text_substitution(data_dict: dict,con: float = 0.6):
    """
    处理文本替换
    data_dict = {
    '【主线】为了爵位！': [{'【主线】为了爵位！': (1185, 258, 0.988)}, 1.0],
    '拥有:一个爵位(未完成)': [{'拥有:一个爵位(未完成)': (1200, 272, 0.977)}, 1.0],
    '交付人:苏三': [{'交付人:苏三': (1202, 290, 1.0)}, 1.0],
    '【阵营】【战斗】挑战义军精锐都': [{'【阵营】【战斗】挑战义军精锐都': (1185, 306, 0.995)}, 1.0],
    '打倒:义军精锐都尉(0/1)': [{'打倒:义军精锐都尉(0/1': (1203, 339, 0.997)}, 0.963],
    '【阵营】【后勤】探查刀魔': [{'【阵营】【后勤】探查刀魔': (1185, 354, 0.992)}, 1.0],
    '侦查:梨花唐3(未完成)': [{'侦查:梨花唐3(未完成)': (1203, 371, 0.978)}, 1.0],
    '完成:装备强化(未完成)': [{'完成:装备强化(朱完成)': (1201, 464, 0.854)}, 0.917]
    }
    res=process_text_substitution(data_dict)
    print(res)
    :param data_dict: 经过基准校队后的字典
    :param con: 置信度
    :return: {}
    """
    new_dict = {}
    for key, values in data_dict.items():
        for item in values[0].values():
            if item[2] > con:
                new_dict[key] = item
    return new_dict

def filter_dict(data_dict, standard_substrings):
    """
    过滤字典中值相同的项，保留含有标准子字符串的键
    standard_substrings_list = ["完成"]
    new_dict = filter_dict(b_dict, standard_substrings_list)
    print(new_dict)
    :param data_dict: 待处理的字典
    :param standard_substrings: 需要保留的子字符串列表
    :return: 过滤后的字典
    """
    new_dict = {}
    value_dict = {}  # 用于存储所有值相同的键
    for key, value in data_dict.items():
        if value not in value_dict:
            value_dict[value] = [key]
        else:
            value_dict[value].append(key)

    for value, keys in value_dict.items():
        # 如果standard_substrings中的任意一个子字符串在key中，优先保留
        preserved_key = next((key for key in keys for substring in standard_substrings if substring in key), keys[0])
        new_dict[preserved_key] = value
    return new_dict


def word_ocr(dic_word_ocr,word_standard_dict,keywords_list,con:float=0.6):
    """
    识别出来的文字替换成基准文字

    #文字基准字典
    word_standard_dict = {"乌部|未":"寻找:乌部神老(未完成)","精锐|义军":"【阵营】【战斗】挑战义军精锐","30级":"升到:30级(完成)","师":"抓获:歪嘴军师(完成)",
            "精锐|唐军":"【阵营】【战斗】挑战唐军精锐","唐军":"打倒:唐军精锐都尉(0/1)","敌军":"侦查:敌军粮车(完成)",
            "乌|部":"交付人:乌部神老",  "疑|犯":"打倒:疑犯(已完成)", "王捕":"交付人:王捕快","武":"寻找:武道灵(未完成)","道":"寻找:武道灵(完成)",
            "爵位":"爵位(完成)","为|爵":"【主线】为了爵位！","悬|赏":"【悬赏】悬赏任务",
        # "花|3":"侦查:梨花3(完成)","花|1":"侦查:梨花1(完成)","花|2":"侦查:梨花2(完成)","梨":"侦查:梨花1(未完成)","梨|花":"侦查:梨花2(未完成)","梨花":"侦查:梨花3(未完成)",
                          #"杂货":"杂货商(完成)",

            "拥有":"拥有:一个爵位(未完成)","苏":"交付人:苏三", "精锐":"【阵营】【战斗】挑战义军精锐都", "义军":"打倒:义军精锐都尉(0/1)",
            "刀魔":"【阵营】【后勤】探查刀魔", "强化":"完成:装备强化(未完成)", "交付":"【点击交付】",
            "名录":"寻物:名录(已完成)", "快":"寻找:王捕快:(未完成)", "捕":"寻找:王捕快:(完成)","悬":"悬赏任务(未完成)","完成:悬":"完成:悬赏任务(完成)",
            "疑犯":"打倒:疑犯(0/1)", "苏三":"寻找:苏三(未完成)","名":"寻物:名录(0/1)","猪王":"打倒:豪猪王(0/1)","豪":"豪猪王(已完成)",
            "宁|婉":"交付人:宁婉儿","技":"学习:技能(未完成)","狼|牙":"打倒:屠狼牙(0/1)","军师":"抓获:歪嘴军师(未完成)",
            "汉":"交付人:虬髯大汉","敌情":"【阵营】【后勤】探查敌情","通路":"【阵营】【后勤】探查通路","粮仓":"【阵营】【后勤】探查粮仓",
            "粮|车":"侦查:敌军粮车(未完成)",
            }

    # 过滤的关键字
    keywords_list = ['未完']

    #测试用的识别数据
    data_dict = {'【主线】伤': (1185, 258, 0.995), '升到：30级（完成）': (1202, 275, 0.977), '如何升到30级': (1204, 292, 0.98),
                 '交付人：小七': (1203, 308, 0.998), '【阵营】【战斗】挑战义军精锐都': (1186, 324, 0.996),
                 '尉': (1181, 340, 0.694),'寻找:武道灵(未完成)': (1202, 274, 0.989, 4),
                 '打倒：义军精锐都尉（0/1)': (1202, 354, 0.906), '【新手任务】玲珑的故事': (1186, 371, 0.998),
                 '完成：玲珑副本：未完成': (1203, 387, 0.958), '【新手任务】试炼场的试炼': (1186, 404, 0.998),
                 '完成：试炼场（未完成）': (1203, 420, 0.946), '【新手任务】装备强化之旅': (1186, 436, 0.998),
                 '完成：装备强化（未完成）': (1202, 452, 0.943), '【新手任务】金装的诱惑1': (1186, 468, 0.99),
                 '找人：': (1204, 484, 0.994), '名匠：未完成': (1246, 483, 0.913)}

    res = word_ocr(data_dict, word_standard_dict, keywords_list)
    print(res)

    :param dic_word_ocr: 识别出来的文字
    :param word_standard_dict: 基准文字
    :param con: 相似度
    :return: 替换过基准文字的字典
    """
    trans_table = str.maketrans(" （）：", " ():")#空格去除,替换()
    new_dic_word_ocr = {str(key).translate(trans_table): value for key, value in dic_word_ocr.items()}
    res_dict = process_text_comparison_dict(word_standard_dict, new_dic_word_ocr) #相似度比较
    logger.debug(f"文字筛选,初筛:{res_dict}")

    if res_dict:
        res_data_dict = {} #2次筛选结果
        res_text_dict={} # 需要替换成基准文字的字典
        res_text = res_dict["results"]#需要替换的文字

        if len(res_text) ==1:#结果有1个，或者没有结果，则直接返回
            res_text_dict=res_text

        if len(res_text) > 1:#结果有多个，则进行关键字筛选
            same_keys, diff_dict = data_filtering(res_text)
            logger.debug(f"文字关键字筛选,same_keys:{same_keys}, diff_dict:{diff_dict}" )
            # print("Diff Dict: ", diff_dict, len(diff_dict))
            if same_keys:
                for data in same_keys:
                    d_dict = keywords_filter(data, keywords_list)
                    res_data_dict.update(d_dict)
            res_text_dict={**res_data_dict,**diff_dict}

        res_dict_new = process_text_substitution(res_text_dict,con) #替换成基准文字
        results_dict= {**res_dict_new, **res_dict["text_dict"]}
        # results_dict_new=filter_dict(results_dict,standard_substrings_list) #过滤字典中值相同的项，保留含有标准子字符串的键
        return results_dict


#文字基准字典
basic_word_standard_dict = {"乌部|未":"寻找:乌部神老(未完成)","精锐|义军":"【阵营】【战斗】挑战义军精锐","30级":"升到:30级(完成)","师":"抓获:歪嘴军师(完成)",
        "精锐|唐军":"【阵营】【战斗】挑战唐军精锐","唐军":"打倒:唐军精锐都尉(0/1)","敌军":"侦查:敌军粮车(完成)",
        "乌|部":"交付人:乌部神老",  "疑|犯":"打倒:疑犯(已完成)", "王捕":"交付人:王捕快","武":"寻找:武道灵(未完成)","道":"寻找:武道灵(完成)",
        "爵位":"爵位(完成)","为|爵":"【主线】为了爵位！","悬|赏":"【悬赏】悬赏任务",
    # "花|3":"侦查:梨花3(完成)","花|1":"侦查:梨花1(完成)","花|2":"侦查:梨花2(完成)","梨":"侦查:梨花1(未完成)","梨|花":"侦查:梨花2(未完成)","梨花":"侦查:梨花3(未完成)",
                      #"杂货":"杂货商(完成)",

        "拥有":"拥有:一个爵位(未完成)","苏":"交付人:苏三", "义军":"打倒:义军精锐都尉(0/1)",
        "刀魔":"【阵营】【后勤】探查刀魔", "强化":"完成:装备强化(未完成)", "交付":"【点击交付】",
        "名录":"寻物:名录(已完成)", "快":"寻找:王捕快:(未完成)", "捕":"寻找:王捕快:(完成)","悬":"悬赏任务(未完成)","赏":"完成:悬赏任务(完成)",
        "苏三":"寻找:苏三(未完成)","名":"寻物:名录(0/1)","猪王":"打倒:豪猪王(0/1)","豪":"豪猪王(已完成)",
        "宁|婉":"交付人:宁婉儿","技":"学习:技能(未完成)","狼|牙":"打倒:屠狼牙(0/1)","军师":"抓获:歪嘴军师(未完成)",
        "汉":"交付人:虬髯大汉","敌情":"【阵营】【后勤】探查敌情","通路":"【阵营】【后勤】探查通路","粮仓":"【阵营】【后勤】探查粮仓",
        "粮|车":"侦查:敌军粮车(未完成)",
        }

# 过滤的关键字
basic_keywords_list = ["(未完成",'未完',"(完成","已完成","0/1","/2","/10","/5","(外)(未","(外)(完","/3","(1)","(2)","(3)","小王","小七","挑战"]

#todo,测试用的识别数据
# data_dict = {'【主线】伤': (1185, 258, 0.995), '升到：30级（完成）': (1202, 275, 0.977), '如何升到30级': (1204, 292, 0.98),
#              '交付人：小七': (1203, 308, 0.998), '【阵营】【战斗】挑战义军精锐都': (1186, 324, 0.996),
#              '尉': (1181, 340, 0.694),'寻找:武道灵(完成)': (1202, 274, 0.989, 4),
#              '打倒：义军精锐都尉（0/1)': (1202, 354, 0.906), '【新手任务】玲珑的故事': (1186, 371, 0.998),
#              '完成：玲珑副本：未完成': (1203, 387, 0.958), '【新手任务】试炼场的试炼': (1186, 404, 0.998),
#              '完成：试炼场（未完成）': (1203, 420, 0.946), '【新手任务】装备强化之旅': (1186, 436, 0.998),
#              '完成：装备强化（未完成）': (1202, 452, 0.943), '【新手任务】金装的诱惑1': (1186, 468, 0.99),
#              '找人：': (1204, 484, 0.994), '名匠：未完成': (1246, 483, 0.913)}
#
# res = word_ocr(data_dict, word_standard_dict, keywords_list)
# print(res)