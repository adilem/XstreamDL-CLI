import re
import click


class X:
    '''
    每一个标签具有的通用性质
    - 标签名
    - 以期望的形式打印本身信息
    - 标签行去除 TAG_NAME: 部分
    '''
    def __init__(self, TAG_NAME: str = 'X'):
        self.TAG_NAME = TAG_NAME
        self.known_attrs = {}

    def __repr__(self):
        return f'{self.TAG_NAME}'

    def __strip(self, line: str):
        return line[len(self.TAG_NAME) + 1:]

    def get_tag_info(self, line: str):
        return self.__strip(line)

    def format_key(self, key: str):
        return key.replace('-', '_').lower()

    def convert_type(self, name: str, value: str, _type: type):
        self.__setattr__(self.format_key(name), _type(value))

    def regex_attrs(self, info: str) -> list:
        if info.endswith(',') is False:
            info += ','
        return re.findall('(.*?)=("[^"]*?"|[^,]*?),', info)

    def set_attrs_from_line(self, line: str):
        info = self.get_tag_info(line)
        for key, value in self.regex_attrs(info):
            value = value.strip('"')
            if key in self.known_attrs:
                if isinstance(self.known_attrs[key], str):
                    self.__setattr__(self.known_attrs[key], value)
                elif isinstance(self.known_attrs[key], type):
                    self.convert_type(key, value, self.known_attrs[key])
                else:
                    self.known_attrs[key](value)
            else:
                click.secho(f'unknown attr of {self.TAG_NAME}')
        return self