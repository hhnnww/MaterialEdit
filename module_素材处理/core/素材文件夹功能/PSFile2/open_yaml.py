from pathlib import Path
import yaml
from dataclasses import dataclass


def open_yml() -> dict:
    yml_path = Path(__file__).parent / 'replace_ad_name.yml'
    yml_text = yml_path.read_text(encoding='utf-8')

    yml = yaml.load(yml_text, Loader=yaml.FullLoader)
    return yml


@dataclass
class ADNameList:
    yaml_dict = open_yml()

    include_name_list = yaml_dict.get('include_name_list')
    is_name_list = yaml_dict.get('is_name_list')
    export_name_list = yaml_dict.get('export_name_list')


if __name__ == '__main__':
    ad_name_is = open_yml().get('include_name_list')
    layer_name = '千库网二维码'
    for ad_name in ad_name_is:
        if ad_name in layer_name:
            print(ad_name)
