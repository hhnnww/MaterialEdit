import json
import random
from pathlib import Path

import zhconv


class GetShiJu:

    @staticmethod
    def fun_随机获取一个文件():
        json_dir = Path('./json')

        json_list = []
        for in_file in json_dir.iterdir():
            if in_file.is_file() and in_file.suffix.lower() == '.json':
                json_list.append(in_file)

        return random.choice(json_list)

    @staticmethod
    def fun_打开JSON(json_path: Path):
        return json.loads(json_path.read_text(encoding='utf-8'))

    @staticmethod
    def fun_构建诗句列表(json_text: list):
        shiju_list = []
        for json_content in json_text:
            parag = json_content['paragraphs']
            shiju_list.extend(parag)
        return shiju_list

    def main(self):
        js_file = self.fun_随机获取一个文件()
        print(f'抽取文件:{js_file}')

        js_text = self.fun_打开JSON(js_file)
        js_list = self.fun_构建诗句列表(js_text)
        shiju = random.choice(js_list)
        shiju = zhconv.convert(shiju, 'zh-hans')
        shiju_split = shiju.split('，')
        if len(shiju_split) > 0:
            shiju = shiju_split[0]

        return shiju


if __name__ == '__main__':
    jf = GetShiJu().main()
    print(jf)
