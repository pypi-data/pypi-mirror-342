import configparser
import os

class INIFileHandler:
    def __init__(self):
        """
        初始化INIFileHandler类,设置INI文件路径。
        """
        self.file_path = "config/config.ini" #这个是固定值
        # self.file_path=r"D:\pc_work\pc_script\config\config.ini"
        self.config = configparser.ConfigParser()
        self.config.read(self.file_path, encoding='utf-8')

    def check_section_exists(self, section_name):
        """
        检查INI文件中是否存在指定的节(section)。
        :param section_name: 要检查的节名
        :return: 如果节存在返回True,否则返回False
        """
        return self.config.has_section(section_name)

    def get_key_value(self, section_name, key_name):
        """
        从INI文件中获取指定节和键的值。
        :param section_name: 要获取值的节名
        :param key_name: 要获取值的键名
        :return: 如果键存在返回其值,否则返回None
        """
        if self.check_section_exists(section_name):
            if self.config.has_option(section_name, key_name):
                return self.config.get(section_name, key_name)
        return None

    def write_dict_to_ini(self, data_dict, section):
        """
        将字典数据写入INI文件里。
        :param data_dict: 要写入的数据字典
        :param section: 要写入的节(section)
        """
        if not section:
            raise ValueError("Section name cannot be empty or None.")

        # 如果路径存在,检查文件异常情况
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            # 移除空的节及内容
            with open(self.file_path, 'w', encoding='utf-8') as file:
                is_empty_section = False
                for line in lines:
                    if is_empty_section and line.strip() == '':
                        continue
                    if line.strip().startswith('[') and line.strip().endswith(']'):
                        is_empty_section = line.strip() == '[]'
                    else:
                        is_empty_section = False
                    file.write(line)

        # 读取现有的INI文件,若没有则会创建一个新的
        self.config.read(self.file_path, encoding='utf-8')

        if not self.config.has_section(section):
            self.config.add_section(section)

        for key, value in data_dict.items():
            self.config.set(section, key.strip(), str(value))

        with open(self.file_path, 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)

    def update_based_on_query(self, query_key, query_value, update_key, new_value):
        """
        根据查询键值对更新INI文件中的键值。
        如果没有要更新的键,则在符合条件的section中新增键值对。
        :param query_key: 查询的键
        :param query_value: 查询的值
        :param update_key: 要更新的键
        :param new_value: 新的值
        """
        updated = False

        # 遍历所有的section
        for section in self.config.sections():
            if self.config.has_option(section, query_key) and self.config[section][query_key] == query_value:
                if self.config.has_option(section, update_key):
                    self.config[section][update_key] = new_value
                    print(f"Key '{update_key}' updated successfully in section '{section}'")
                else:
                    self.config[section][update_key] = new_value
                    print(f"Added key '{update_key}' with value '{new_value}' in section '{section}'")
                updated = True

        if not updated:
            print(f'No matching key-value pair ({query_key}={query_value}) found in any section.')

        # 写回文件
        with open(self.file_path, 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)

    def find_other_key_value(self, known_key, known_value, target_key):
        """
        在INI文件中查找另一个键对应的值,基于已知的键值对。
        :param known_key: 已知的键
        :param known_value: 已知键对应的值
        :param target_key: 目标键
        :return: 目标键的值或None
        """
        for section in self.config.sections():
            if known_key in self.config[section] and self.config[section][known_key] == known_value:
                if target_key in self.config[section]:
                    return self.config[section][target_key]
        return None

    def get_section_items(self, section:str):
        """
        获取 INI 文件中指定节的所有键值对。
        :param section: 要查询的节名称
        :return: 节中的键值对
        :raises ValueError: 如果节不存在
        """
        if not self.check_section_exists(section):
            raise ValueError(f"节 '{section}' 不存在于文件 '{self.file_path}' 中")
        return dict(self.config.items(section))

    def get_multiple_sections_items(self, sections: list):
        """
        获取 INI 文件中多个节的所有键值对。
        :param sections: 要查询的节名称列表
        :return: 包含节名称及其键值对的字典
        :raises ValueError: 如果某个节不存在
        """
        result = {}
        for section in sections:
            if self.check_section_exists(section):
                result[section] = dict(self.config.items(section))
            else:
                raise ValueError(f"节 '{section}' 不存在于文件 '{self.file_path}' 中")
        return result

# 示例用法
# if __name__ == "__main__":
#     ini_handler = INIFileHandler()
#     # 你可以在这里调用类的方法进行测试


