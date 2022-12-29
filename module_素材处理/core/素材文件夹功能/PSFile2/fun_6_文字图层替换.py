def fun_文字图层替换内容(item):
    visible = item.Visible
    item.AllLocked = False

    keywords = [
        ('千图', '小夕'),
        ('包图', '小夕'),
        ('58pic', 'xiaoxisc'),
        ('58PIC', 'xiaoxisc'),
        ('千小图', '小夕夕'),
        ('摄图', '小夕'),
        ('699pic', 'xiaoxisc'),
        ('千/图', '小/夕'),
        ('baidu', 'xiaoxisc'),
        ('ibaotu', 'XiaoXi'),
        ('XIAO HUA', 'XiaoXi'),
        ('ibaotu', 'XiaoXi'),
        ('千库', '小夕'),
        ('千|图', '小|夕'),
        ('588ku', 'xiaoxisc'),
        ('qianku', 'xiaoxisc'),
        ('shetuwang', 'xiaoxiwang'),
        ('80053384', '12345677'),
        ('baotuwang', 'xiaoxiwang'),
        ('abaotu', 'xiaoxi'),
        ('BAOTUWANG', 'xiaoxisc'),
        ('abaotu', 'xiaoxisc'),
        ('iBaoTu', 'xiaoxi'),
        ('mige', 'xiaoxisc'),
        ('米鸽', '小夕'),
        ('51miz', 'xiaoxisc'),
        ('觅知', '小夕')
    ]

    for key in keywords:
        if key[0].lower() in str(item.textItem.Contents).lower():

            if 'bold' in str(item.textItem.Font).lower():
                item.TextItem.Font = "Alibaba_PuHuiTi_2_85_Bold"
            else:
                item.TextItem.Font = "Alibaba_PuHuiTi_2_55_Regular"

            item.TextItem.Contents = item.TextItem.Contents.replace(key[0], key[1])
            item.Name = item.TextItem.Contents

    item.Visible = visible
