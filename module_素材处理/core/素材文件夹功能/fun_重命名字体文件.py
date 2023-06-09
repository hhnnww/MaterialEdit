import re
from pathlib import Path

import fontTools.ttLib
from fontTools.ttLib import TTFont

from module_素材处理.core.setting import FONT_SUFFIX


class FontPathReName:
    def __init__(self, in_path: Path, tb_name: str):
        self.in_path = in_path
        self.tb_name = tb_name

    @staticmethod
    def is_chinese(string):
        for ch in string:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    def fun_获取文件名(self, font_path: Path):
        font_name = ''
        font_weight = ''
        name_list = []

        with TTFont(font_path) as font:

            names = font['name'].names
            for nt in names:
                if nt.nameID == 4 or nt.nameID == 1:
                    name_list.append(str(nt))
                elif nt.nameID == 2:
                    font_weight = str(nt)

        for string_text in name_list:
            if self.is_chinese(string_text):
                font_name = string_text

        if font_name == '':
            name_list.sort(key=lambda k: len(k), reverse=True)
            font_name = name_list[0]

        if font_weight != '' and '字体子系未定义' not in font_weight:
            font_name = font_name + '_' + font_weight

        return font_name

    @staticmethod
    def fun_文件名转STEM(font_name: str):
        replace_text = (
            ('-', '_'),
            ('?', '_'),
            ('.', '_'),
            (':', '_'),
            ('<', ''),
            ('>', ''),
            (' ', '_'),
        )
        for rep in replace_text:
            font_name = font_name.replace(rep[0], rep[1])

        font_name = re.sub(r'_+', '_', font_name)

        if font_name[0] == '_':
            font_name = font_name[1:]

        font_name = ''.join(x for x in font_name if x.isprintable())

        return font_name.lower()

    def fun_所有字体文件(self):
        all_file = []
        for in_file in self.in_path.rglob('*'):
            if in_file.is_file() and in_file.suffix.lower() in FONT_SUFFIX:
                all_file.append(in_file)

        all_file.sort(key=lambda k: k.suffix.lower())

        return all_file

    def main(self):
        bad_file = []
        for in_file in self.fun_所有字体文件():
            try:
                font_name = self.fun_获取文件名(in_file)
            except fontTools.ttLib.TTLibError:
                print(f'错误的字体文件{in_file}')
                bad_file.append(in_file)
                pass
            else:
                font_stem = self.tb_name + '_' + self.fun_文件名转STEM(font_name)

                if in_file.stem == font_stem:
                    continue

                try:
                    new_name = in_file.with_stem(font_stem)
                except ValueError:
                    print('无法修改文件名')
                else:
                    if new_name.exists() is False:
                        print(f'修改名字:{in_file.as_posix()}\t-->\t{new_name.as_posix()}')

                        try:
                            in_file.rename(new_name)
                        except:
                            pass

        for bf in bad_file:
            print(bf)
