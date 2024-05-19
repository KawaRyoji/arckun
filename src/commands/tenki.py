from typing import Any, override

import discord
import requests
import tabulate

from .core import Command, Response

codes = [
    {
        "prefecture": "道北",
        "cities": [
            {"city": "稚内", "id": "011000"},
            {"city": "旭川", "id": "012010"},
            {"city": "留萌", "id": "012020"},
        ],
    },
    {
        "prefecture": "道東",
        "cities": [
            {"city": "網走", "id": "013010"},
            {"city": "北見", "id": "013020"},
            {"city": "紋別", "id": "013030"},
            {"city": "根室", "id": "014010"},
            {"city": "釧路", "id": "014020"},
            {"city": "帯広", "id": "014030"},
        ],
    },
    {
        "prefecture": "道央",
        "cities": [
            {"city": "札幌", "id": "016010"},
            {"city": "岩見沢", "id": "016020"},
            {"city": "倶知安", "id": "016030"},
            {"city": "室蘭", "id": "015010"},
            {"city": "浦河", "id": "015020"},
        ],
    },
    {
        "prefecture": "道南",
        "cities": [{"city": "函館", "id": "017010"}, {"city": "江差", "id": "017020"}],
    },
    {
        "prefecture": "青森県",
        "cities": [
            {"city": "青森", "id": "020010"},
            {"city": "むつ", "id": "020020"},
            {"city": "八戸", "id": "020030"},
        ],
    },
    {
        "prefecture": "岩手県",
        "cities": [
            {"city": "盛岡", "id": "030010"},
            {"city": "宮古", "id": "030020"},
            {"city": "大船渡", "id": "030030"},
        ],
    },
    {
        "prefecture": "宮城県",
        "cities": [{"city": "仙台", "id": "040010"}, {"city": "白石", "id": "040020"}],
    },
    {
        "prefecture": "秋田県",
        "cities": [{"city": "秋田", "id": "050010"}, {"city": "横手", "id": "050020"}],
    },
    {
        "prefecture": "山形県",
        "cities": [
            {"city": "山形", "id": "060010"},
            {"city": "米沢", "id": "060020"},
            {"city": "酒田", "id": "060030"},
            {"city": "新庄", "id": "060040"},
        ],
    },
    {
        "prefecture": "福島県",
        "cities": [
            {"city": "福島", "id": "070010"},
            {"city": "小名浜", "id": "070020"},
            {"city": "若松", "id": "070030"},
        ],
    },
    {
        "prefecture": "茨城県",
        "cities": [{"city": "水戸", "id": "080010"}, {"city": "土浦", "id": "080020"}],
    },
    {
        "prefecture": "栃木県",
        "cities": [
            {"city": "宇都宮", "id": "090010"},
            {"city": "大田原", "id": "090020"},
        ],
    },
    {
        "prefecture": "群馬県",
        "cities": [
            {"city": "前橋", "id": "100010"},
            {"city": "みなかみ", "id": "100020"},
        ],
    },
    {
        "prefecture": "埼玉県",
        "cities": [
            {"city": "さいたま", "id": "110010"},
            {"city": "熊谷", "id": "110020"},
            {"city": "秩父", "id": "110030"},
        ],
    },
    {
        "prefecture": "千葉県",
        "cities": [
            {"city": "千葉", "id": "120010"},
            {"city": "銚子", "id": "120020"},
            {"city": "館山", "id": "120030"},
        ],
    },
    {
        "prefecture": "東京都",
        "cities": [
            {"city": "東京", "id": "130010"},
            {"city": "大島", "id": "130020"},
            {"city": "八丈島", "id": "130030"},
            {"city": "父島", "id": "130040"},
        ],
    },
    {
        "prefecture": "神奈川県",
        "cities": [
            {"city": "横浜", "id": "140010"},
            {"city": "小田原", "id": "140020"},
        ],
    },
    {
        "prefecture": "新潟県",
        "cities": [
            {"city": "新潟", "id": "150010"},
            {"city": "長岡", "id": "150020"},
            {"city": "高田", "id": "150030"},
            {"city": "相川", "id": "150040"},
        ],
    },
    {
        "prefecture": "富山県",
        "cities": [{"city": "富山", "id": "160010"}, {"city": "伏木", "id": "160020"}],
    },
    {
        "prefecture": "石川県",
        "cities": [{"city": "金沢", "id": "170010"}, {"city": "輪島", "id": "170020"}],
    },
    {
        "prefecture": "福井県",
        "cities": [{"city": "福井", "id": "180010"}, {"city": "敦賀", "id": "180020"}],
    },
    {
        "prefecture": "山梨県",
        "cities": [
            {"city": "甲府", "id": "190010"},
            {"city": "河口湖", "id": "190020"},
        ],
    },
    {
        "prefecture": "長野県",
        "cities": [
            {"city": "長野", "id": "200010"},
            {"city": "松本", "id": "200020"},
            {"city": "飯田", "id": "200030"},
        ],
    },
    {
        "prefecture": "岐阜県",
        "cities": [{"city": "岐阜", "id": "210010"}, {"city": "高山", "id": "210020"}],
    },
    {
        "prefecture": "静岡県",
        "cities": [
            {"city": "静岡", "id": "220010"},
            {"city": "網代", "id": "220020"},
            {"city": "三島", "id": "220030"},
            {"city": "浜松", "id": "220040"},
        ],
    },
    {
        "prefecture": "愛知県",
        "cities": [
            {"city": "名古屋", "id": "230010"},
            {"city": "豊橋", "id": "230020"},
        ],
    },
    {
        "prefecture": "三重県",
        "cities": [{"city": "津", "id": "240010"}, {"city": "尾鷲", "id": "240020"}],
    },
    {
        "prefecture": "滋賀県",
        "cities": [{"city": "大津", "id": "250010"}, {"city": "彦根", "id": "250020"}],
    },
    {
        "prefecture": "京都府",
        "cities": [{"city": "京都", "id": "260010"}, {"city": "舞鶴", "id": "260020"}],
    },
    {"prefecture": "大阪府", "cities": [{"city": "大阪", "id": "270000"}]},
    {
        "prefecture": "兵庫県",
        "cities": [{"city": "神戸", "id": "280010"}, {"city": "豊岡", "id": "280020"}],
    },
    {
        "prefecture": "奈良県",
        "cities": [{"city": "奈良", "id": "290010"}, {"city": "風屋", "id": "290020"}],
    },
    {
        "prefecture": "和歌山県",
        "cities": [
            {"city": "和歌山", "id": "300010"},
            {"city": "潮岬", "id": "300020"},
        ],
    },
    {
        "prefecture": "鳥取県",
        "cities": [{"city": "鳥取", "id": "310010"}, {"city": "米子", "id": "310020"}],
    },
    {
        "prefecture": "島根県",
        "cities": [
            {"city": "松江", "id": "320010"},
            {"city": "浜田", "id": "320020"},
            {"city": "西郷", "id": "320030"},
        ],
    },
    {
        "prefecture": "岡山県",
        "cities": [{"city": "岡山", "id": "330010"}, {"city": "津山", "id": "330020"}],
    },
    {
        "prefecture": "広島県",
        "cities": [{"city": "広島", "id": "340010"}, {"city": "庄原", "id": "340020"}],
    },
    {
        "prefecture": "山口県",
        "cities": [
            {"city": "下関", "id": "350010"},
            {"city": "山口", "id": "350020"},
            {"city": "柳井", "id": "350030"},
            {"city": "萩", "id": "350040"},
        ],
    },
    {
        "prefecture": "徳島県",
        "cities": [
            {"city": "徳島", "id": "360010"},
            {"city": "日和佐", "id": "360020"},
        ],
    },
    {"prefecture": "香川県", "cities": [{"city": "高松", "id": "370000"}]},
    {
        "prefecture": "愛媛県",
        "cities": [
            {"city": "松山", "id": "380010"},
            {"city": "新居浜", "id": "380020"},
            {"city": "宇和島", "id": "380030"},
        ],
    },
    {
        "prefecture": "高知県",
        "cities": [
            {"city": "高知", "id": "390010"},
            {"city": "室戸岬", "id": "390020"},
            {"city": "清水", "id": "390030"},
        ],
    },
    {
        "prefecture": "福岡県",
        "cities": [
            {"city": "福岡", "id": "400010"},
            {"city": "八幡", "id": "400020"},
            {"city": "飯塚", "id": "400030"},
            {"city": "久留米", "id": "400040"},
        ],
    },
    {
        "prefecture": "佐賀県",
        "cities": [
            {"city": "佐賀", "id": "410010"},
            {"city": "伊万里", "id": "410020"},
        ],
    },
    {
        "prefecture": "長崎県",
        "cities": [
            {"city": "長崎", "id": "420010"},
            {"city": "佐世保", "id": "420020"},
            {"city": "厳原", "id": "420030"},
            {"city": "福江", "id": "420040"},
        ],
    },
    {
        "prefecture": "熊本県",
        "cities": [
            {"city": "熊本", "id": "430010"},
            {"city": "阿蘇乙姫", "id": "430020"},
            {"city": "牛深", "id": "430030"},
            {"city": "人吉", "id": "430040"},
        ],
    },
    {
        "prefecture": "大分県",
        "cities": [
            {"city": "大分", "id": "440010"},
            {"city": "中津", "id": "440020"},
            {"city": "日田", "id": "440030"},
            {"city": "佐伯", "id": "440040"},
        ],
    },
    {
        "prefecture": "宮崎県",
        "cities": [
            {"city": "宮崎", "id": "450010"},
            {"city": "延岡", "id": "450020"},
            {"city": "都城", "id": "450030"},
            {"city": "高千穂", "id": "450040"},
        ],
    },
    {
        "prefecture": "鹿児島県",
        "cities": [
            {"city": "鹿児島", "id": "460010"},
            {"city": "鹿屋", "id": "460020"},
            {"city": "種子島", "id": "460030"},
            {"city": "名瀬", "id": "460040"},
        ],
    },
    {
        "prefecture": "沖縄県",
        "cities": [
            {"city": "那覇", "id": "471010"},
            {"city": "名護", "id": "471020"},
            {"city": "久米島", "id": "471030"},
            {"city": "南大東", "id": "472000"},
            {"city": "宮古島", "id": "473000"},
            {"city": "石垣島", "id": "474010"},
            {"city": "与那国島", "id": "474020"},
        ],
    },
]


def format_prefecture(prefecture: str) -> str:
    if prefecture == "東京":
        return prefecture + "都"
    elif prefecture == "大阪" or prefecture == "京都":
        return prefecture + "府"
    elif (
        prefecture == "道北"
        or prefecture == "道南"
        or prefecture == "道央"
        or prefecture == "道東"
        or prefecture.endswith("県")
    ):
        return prefecture
    else:
        return prefecture + "県"


def get_cities(prefecture: str) -> list[dict[str, str]] | None:
    f_prefecture = format_prefecture(prefecture)
    maybe_prefecture = list(filter(lambda x: x["prefecture"] == f_prefecture, codes))

    if len(maybe_prefecture) == 0:
        return None
    else:
        return maybe_prefecture[0]["cities"]


def format_response(response: dict[str, Any]) -> str:
    today = response["forecasts"][0]
    tomorrow = response["forecasts"][1]
    after_tomorrow = response["forecasts"][2]

    temp = lambda res: "N" if res is None else res
    table = tabulate.tabulate(
        tabular_data=[
            [today["telop"], tomorrow["telop"], after_tomorrow["telop"]],
            [
                f"{temp(today['temperature']['min']['celsius'])}-{temp(today['temperature']['max']['celsius'])}",
                f"{temp(tomorrow['temperature']['min']['celsius'])}-{temp(tomorrow['temperature']['max']['celsius'])}",
                f"{temp(after_tomorrow['temperature']['min']['celsius'])}-{temp(after_tomorrow['temperature']['max']['celsius'])}",
            ],
        ],
        headers=[
            f"今日({today['date'][5:]})",
            f"明日({tomorrow['date'][5:]})",
            f"明後日({after_tomorrow['date'][5:]})",
        ],
    )
    return "\n".join(
        [
            "### " + response["title"] + "([詳細な天気](" + response["link"] + "))",
            str(table),
        ]
    )


class Tenki(Command):
    @override
    def exec(self, source_message: discord.Message, *args: str) -> Response:
        if len(args) < 1:
            return Response.failure(self)("引数が足りないよ。")

        todouhuken = args[0]

        maybe_cities = get_cities(todouhuken)
        if maybe_cities is None:
            return Response(todouhuken + "は日本に存在しないよ。")

        cities = maybe_cities

        responses = list(
            map(
                lambda city: requests.get(
                    "https://weather.tsukumijima.net/api/forecast/city/" + city["id"]
                ).json(),
                cities,
            )
        )
        return Response("\n".join(list(map(format_response, responses))))
