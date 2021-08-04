import pandas as pd
import numpy as np

cp_trans = {
    '北京市': ('北京市'),
    '天津市': ('天津市'),
    '河北省': ('石家庄市', '唐山市', '邯郸市', '张家口市', '保定市', '沧州市', '秦皇岛市', '邢台市', '廊坊市', '承德市', '衡水市'),
    '山西省': ('阳泉市', '长治市', '晋城市', '朔州市', '忻州市', '晋中市', '吕梁市', '临汾市', '运城市', '大同市', '太原市'),
    '内蒙古自治区': ('呼伦贝尔市', '兴安盟', '通辽市', '锡林郭勒盟', '乌兰察布市', '鄂尔多斯市', '巴彦淖尔市', '阿拉善盟', '呼和浩特市', '包头市', '乌海市', '赤峰市'),
    '辽宁省': ('沈阳市', '大连市', '鞍山市', '抚顺市', '本溪市', '丹东市', '锦州市', '营口市', '阜新市', '辽阳市', '铁岭市', '朝阳市', '盘锦市', '葫芦岛市'),
    '吉林省': ('长春市', '吉林市', '四平市', '辽源市', '通化市', '白山市', '白城市', '松原市', '延边朝鲜族自治州', '长白山管委会'),
    '黑龙江省': ('哈尔滨市', '齐齐哈尔市', '牡丹江市', '佳木斯市', '鸡西市', '鹤岗市', '双鸭山市', '七台河市', '黑河市', '伊春市', '大庆市', '大兴安岭地区', '绥化市'),
    '上海市': ('上海市'),
    '江苏省': ('南京市', '无锡市', '徐州市', '常州市', '苏州市', '南通市', '连云港市', '淮安市', '盐城市', '扬州市', '镇江市', '泰州市', '宿迁市'),
    '浙江省': ('杭州市', '嘉兴市', '湖州市', '舟山市', '金华市', '绍兴市', '温州市', '台州市', '丽水市', '衢州市', '宁波市'),
    '安徽省': ('宣城市', '宿州市', '滁州市', '池州市', '阜阳市', '六安市', '合肥市', '蚌埠市', '淮南市', '铜陵市', '马鞍山市', '淮北市', '芜湖市', '安庆市', '黄山市', '亳州市'),
    '福建省': ('福州市', '三明市', '南平市', '宁德市', '莆田市', '泉州市', '漳州市', '龙岩市', '厦门市', '平潭综合实验区'),
    '江西省': ('南昌市', '景德镇市', '萍乡市', '九江市', '新余市', '鹰潭市', '赣州市', '宜春市', '上饶市', '吉安市', '抚州市'),
    '山东省': ('青岛市', '莱芜市', '济南市', '淄博市', '枣庄市', '烟台市', '潍坊市', '济宁市', '临沂市', '泰安市', '聊城市', '菏泽市', '德州市', '滨州市', '东营市', '威海市', '日照市'),
    '河南省': ('郑州市', '开封市', '洛阳市', '平顶山市', '安阳市', '濮阳市', '新乡市', '焦作市', '鹤壁市', '许昌市', '漯河市', '三门峡市', '南阳市', '商丘市', '信阳市', '周口市', '驻马店市', '济源市'),
    '湖北省': ('武汉市', '黄石市', '十堰市', '荆州市', '宜昌市', '襄阳市', '鄂州市', '荆门市', '孝感市', '黄冈市', '咸宁市', '恩施土家族苗族自治州', '随州市', '仙桃市', '天门市', '潜江市', '神农架林区'),
    '湖南省': ('长沙市', '株洲市', '湘潭市', '衡阳市', '邵阳市', '岳阳市', '常德市', '张家界市', '益阳市', '永州市', '郴州市', '娄底市', '怀化市', '湘西土家族苗族自治州'),
    '广东省': ('广州市', '深圳市', '珠海市', '汕头市', '佛山市', '韶关市', '河源市', '梅州市', '惠州市', '汕尾市', '东莞市', '中山市', '江门市', '阳江市', '湛江市', '茂名市', '肇庆市', '清远市', '潮州市', '揭阳市', '云浮市'),
    '广西壮族自治区': ('南宁市', '柳州市', '桂林市', '梧州市', '北海市', '防城港市', '钦州市', '贵港市', '玉林市', '贺州市', '百色市', '河池市', '来宾市', '崇左市'),
    '海南省': ('海口市', '三亚市', '三沙市', '儋州市'),
    '重庆市': ('重庆市'),
    '四川省': ('成都市', '自贡市', '攀枝花市', '泸州市', '德阳市', '绵阳市', '广元市', '遂宁市', '内江市', '乐山市', '南充市', '宜宾市', '广安市', '达州市', '资阳市', '眉山市', '巴中市', '雅安市', '阿坝藏族羌族自治州', '甘孜藏族自治州', '凉山彝族自治州'),
    '贵州省': ('贵阳市', '六盘水市', '遵义市', '安顺市', '黔南布依族苗族自治州', '黔东南苗族侗族自治州', '毕节市', '铜仁市', '黔西南布依族苗族自治州'),
    '云南省': ('昆明市', '昭通市', '昆明市', '曲靖市', '玉溪市', '红河哈尼族彝族自治州', '文山壮族苗族自治州', '普洱市', '西双版纳傣族自治州', '楚雄彝族自治州', '大理白族自治州', '保山市', '德宏傣族景颇族自治州', '丽江市', '怒江傈僳族自治州', '迪庆藏族自治州', '临沧市'),
    '西藏自治区': ('拉萨市', '日喀则市', '昌都市', '林芝市', '山南市', '那曲市', '阿里地区'),
    '陕西省': ('西安市', '铜川市', '宝鸡市', '咸阳市', '渭南市', '汉中市', '安康市', '商洛市', '延安市', '榆林市'),
    '甘肃省': ('兰州市', '嘉峪关市', '金昌市', '白银市', '天水市', '酒泉市', '张掖市', '武威市', '定西市', '陇南市', '平凉市', '庆阳市', '临夏回族自治州', '甘南藏族自治州'),
    '青海省': ('西宁市', '海东市', '海西蒙古族藏族自治州', '海南藏族自治州', '海北藏族自治州', '黄南藏族自治州', '玉树藏族自治州', '果洛藏族自治州'),
    '宁夏回族自治区': ('银川市', '石嘴山市', '吴忠市', '中卫市', '固原市'),
    '新疆维吾尔自治区': ('乌鲁木齐市', '克拉玛依市', '石河子市', '伊犁哈萨克自治州', '塔城地区', '阿勒泰地区', '博尔塔拉蒙古自治州', '昌吉回族自治州', '巴音郭楞蒙古自治州', '阿克苏地区', '克孜勒苏柯尔克孜自治州', '喀什地区', '和田地区', '吐鲁番市', '哈密市', '阿拉尔市', '图木舒克市', '五家渠市', '北屯市', '铁门关市', '双河市', '可克达拉市', '昆玉市', '胡杨河市', '新星市'),
}


def inverse_dic(dictionary):
    new_dic = {}
    for k, v in dictionary.items():
        new_dic[v] = k
    return new_dic


def ptwoc(prov):
    for province in cp_trans.keys():
        if (prov[0: 2] == province[0: 2]) or (prov[0: 3] == province[0: 3]):
            return cp_trans[province]


def ctwop(city):
    dictionary = inverse_dic(cp_trans)
    for targets, trash in dictionary.items():
        if targets == trash:
            if (city[0: 2] == targets[0: 2]) or (city[0: 3] == targets[0: 3]):
                return dictionary[targets]
        else:
            for target in targets:
                if (city[0: 2] == target[0: 2]) or (city[0: 3] == target[0: 3]):
                    return dictionary[targets]


def add_pro(column):
    col_len = len(column)
    provinces = []
    for i in range(col_len):
        prov = ctwop(column[i])
        provinces.append(prov)
    newarray = pd.DataFrame(provinces)
    return newarray
