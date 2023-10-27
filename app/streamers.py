import pymongo
from app.streamer import Streamer
from logging import getLogger, DEBUG, NullHandler

class Streamers:
    def __init__(self):
        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.setLevel(DEBUG)
        self._logger.propagate = True
        self.streamers = {
            "ホロライブ" : Streamer("HL0000", "ホロライブ", "hololive", ["bland","jp"], "hololive.jpg", "@hololive"),

            "ときのそら" : Streamer("HL0001", "ときのそら", "hololive", ["gen0","jp"], "tokino_sora.jpg", "@TokinoSora"),
            "ロボ子さん" : Streamer("HL0002", "ロボ子さん", "hololive", ["gen0","jp"], "robokosan.jpg", "@Robocosan"),
            "さくらみこ" : Streamer("HL0003", "さくらみこ", "hololive", ["gen0","jp"], "sakura_miko.jpg", "@SakuraMiko"),
            "星街すいせい" : Streamer("HL0004", "星街すいせい", "hololive", ["gen0","jp"], "hoshimachi_suisei.jpg", "@HoshimachiSuisei"),
            "AZKi" : Streamer("HL0005", "AZKi", "hololive", ["gen0","jp"], "azki.jpg", "@AZKi"),

            "夜空メル" : Streamer("HL0101", "夜空メル", "hololive", ["gen1","jp"], "yozora_mel.jpg", "@YozoraMel"),
            "アキ・ローゼンタール" : Streamer("HL0102", "アキ・ローゼンタール", "hololive", ["gen1","jp"], "aki_rosenthal.jpg", "@AkiRosenthal"),
            "赤井はあと" : Streamer("HL0103", "赤井はあと", "hololive", ["gen1","jp"], "haachama.jpg", "@AkaiHaato"),
            "白上フブキ" : Streamer("HL0104", "白上フブキ", "hololive", ["gen1","gamers","jp"], "shirakami_fubuki.jpg", "@ShirakamiFubuki"),
            "夏色まつり" : Streamer("HL0105", "夏色まつり", "hololive", ["gen1","jp"], "natsuiro_matsuri.jpg", "@NatsuiroMatsuri"),

            "湊あくあ" : Streamer("HL0201", "湊あくあ", "hololive", ["gen2","jp"], "minato_aqua.jpg", "@MinatoAqua"),
            "紫咲シオン" : Streamer("HL0202", "紫咲シオン", "hololive", ["gen2","jp"], "murasaki_shion.jpg", "@MurasakiShion"),
            "百鬼あやめ" : Streamer("HL0203", "百鬼あやめ", "hololive", ["gen2","jp"], "nakiri_ayame.jpg", "@NakiriAyame"),
            "癒月ちょこ" : Streamer("HL0204", "癒月ちょこ", "hololive", ["gen2","jp"], "yuzuki_choco.jpg", "@YuzukiChoco"),
            "大空スバル" : Streamer("HL0205", "大空スバル", "hololive", ["gen2","jp"], "oozora_subaru.jpg", "@OozoraSubaru"),

            "大神ミオ" : Streamer("HL0G02", "大神ミオ", "hololive", ["gamers","jp"], "ookami_mio.jpg", "@OokamiMio"),
            "猫又おかゆ" : Streamer("HL0G03", "猫又おかゆ", "hololive", ["gamers","jp"], "nekomata_okayu.jpg", "@NekomataOkayu"),
            "戌神ころね" : Streamer("HL0G04", "戌神ころね", "hololive", ["gamers","jp"], "inugami_korone.jpg", "@InugamiKorone"),

            "兎田ぺこら" : Streamer("HL0301", "兎田ぺこら", "hololive", ["gen3","jp"], "usada_pekora.jpg", "@usadapekora"),
            "潤羽るしあ" : Streamer("HL0302", "潤羽るしあ", "hololive", ["gen3","jp"], "uruha_rushia.jpg", "@hololive", True),
            "不知火フレア" : Streamer("HL0303", "不知火フレア", "hololive", ["gen3","jp"], "shiranui_flare.jpg", "@ShiranuiFlare"),
            "白銀ノエル" : Streamer("HL0304", "白銀ノエル", "hololive", ["gen3","jp"], "shirogane_noel.jpg", "@ShiroganeNoel"),
            "宝鐘マリン" : Streamer("HL0305", "宝鐘マリン", "hololive", ["gen3","jp"], "housyou_marine.jpg", "@HoushouMarine"),

            "天音かなた" : Streamer("HL0401", "天音かなた", "hololive", ["gen4","jp"], "amane_kanata.jpg", "@AmaneKanata"),
            "桐生ココ" : Streamer("HL0402", "桐生ココ", "hololive", ["gen4","jp"], "kiryu_coco.jpg", "@KiryuCoco", True),
            "角巻わため" : Streamer("HL0403", "角巻わため", "hololive", ["gen4","jp"], "tsunomaki_watame.jpg", "@TsunomakiWatame"),
            "常闇トワ" : Streamer("HL0404", "常闇トワ", "hololive", ["gen4","jp"], "tokoyami_towa.jpg", "@TokoyamiTowa"),
            "姫森ルーナ" : Streamer("HL0405", "姫森ルーナ", "hololive", ["gen4","jp"], "himemori_luna.jpg", "@HimemoriLuna"),

            "獅白ぼたん" : Streamer("HL0501", "獅白ぼたん", "hololive", ["gen5","jp"], "shishiro_botan.jpg", "@ShishiroBotan"),
            "雪花ラミィ" : Streamer("HL0502", "雪花ラミィ", "hololive", ["gen5","jp"], "yukihana_lamy.jpg", "@YukihanaLamy"),
            "尾丸ポルカ" : Streamer("HL0503", "尾丸ポルカ", "hololive", ["gen5","jp"], "omaru_polka.jpg", "@OmaruPolka"),
            "桃鈴ねね" : Streamer("HL0504", "桃鈴ねね", "hololive", ["gen5","jp"], "momosuzu_nene.jpg", "@MomosuzuNene"),
            "魔乃アロエ" : Streamer("HL0505", "魔乃アロエ", "hololive", ["gen5","jp"], "mano_aloe.jpg", "@hololive", True),

            "ラプラス" : Streamer("HL0601", "ラプラス・ダークネス", "hololive", ["gen6","jp"], "laplus_darknesss.jpg", "@LaplusDarknesss"),
            "鷹嶺ルイ" : Streamer("HL0602", "鷹嶺ルイ", "hololive", ["gen6","jp"], "takane_lui.jpg", "@TakaneLui"),
            "博衣こより" : Streamer("HL0603", "博衣こより", "hololive", ["gen6","jp"], "hakui_koyori.jpg", "@HakuiKoyori"),
            "沙花叉クロヱ" : Streamer("HL0604", "沙花叉クロヱ", "hololive", ["gen6","jp"], "sakamata_chloe.jpg", "@SakamataChloe"),
            "風真いろは" : Streamer("HL0605", "風真いろは", "hololive", ["gen6","jp"], "kazama_iroha.jpg", "@kazamairoha"),

            "hololive DEV_IS" : Streamer("HLDI00", "hololive DEV_IS", "hololive", ["bland","jp"], "hololive_dev_is.jpg", "@hololiveDEV_IS"),
            "火威青" : Streamer("HLDI01", "火威青", "hololive", ["dev_is","jp"], "hiodoshi_ao.jpg", "@HiodoshiAo"),
            "儒烏風亭らでん" : Streamer("HLDI02", "儒烏風亭らでん", "hololive", ["dev_is","jp"], "juufuutei_raden.jpg", "@JuufuuteiRaden"),
            "一条莉々華" : Streamer("HLDI03", "一条莉々華", "hololive", ["dev_is","jp"], "otonose_kanade.jpg", "@OtonoseKanade"),
            "音乃瀬奏" : Streamer("HLDI04", "音乃瀬奏", "hololive", ["dev_is","jp"], "ichijou_ririka.jpg", "@IchijouRirika"),
            "轟はじめ" : Streamer("HLDI05", "轟はじめ", "hololive", ["dev_is","jp"], "todoroki_hajime.jpg", "@TodorokiHajime"),

            "Risu" : Streamer("HLID01", "Ayunda Risu", "hololive_id", ["gen1","id"], "ayunda_risu.jpg", "@AyundaRisu"),
            "Moona" : Streamer("HLID02", "Moona Hoshinova", "hololive_id", ["gen1","id"], "moona_hoshinova.jpg", "@MoonaHoshinova"),
            "Iofi" : Streamer("HLID03", "Airani Iofifteen", "hololive_id", ["gen1","id"], "airani_iofifteen.jpg", "@AiraniIofifteen"),

            "Ollie" : Streamer("HLID04", "Kureiji Ollie", "hololive_id", ["gen2","id"], "kureiji_ollie.jpg", "@KureijiOllie"),
            "Anya" : Streamer("HLID05", "Anya Melfissa", "hololive_id", ["gen2","id"], "anya_melfissa.jpg", "@AnyaMelfissa"),
            "Reine" : Streamer("HLID06", "Pavolia Reine", "hololive_id", ["gen2","id"], "pavolia_reine.jpg", "@PavoliaReine"),

            "Zeta" : Streamer("HLID07", "Vestia Zeta", "hololive_id", ["gen3","id"], "vestia_zeta.jpg", "@VestiaZeta"),
            "Kaela" : Streamer("HLID08", "Kaela Kovalskia", "hololive_id", ["gen3","id"], "kaela_kovalskia.jpg", "@KaelaKovalskia"),
            "Kobo" : Streamer("HLID09", "Kobo Kanaeru", "hololive_id", ["gen3","id"], "kobo_kanaeru.jpg", "@KoboKanaeru"),

            "Calli" : Streamer("HLEN01", "Mori Calliope", "hololive_en", ["gen1","en"], "mori_calliope.jpg", "@MoriCalliope"),
            "Kiara" : Streamer("HLEN02", "Takanashi Kiara", "hololive_en", ["gen1","en"], "takanashi_kiara.jpg", "@TakanashiKiara"),
            "Ina" : Streamer("HLEN03", "Ninomae Ina'nis", "hololive_en", ["gen1","en"], "ninomae_ina'nis.jpg", "@NinomaeInanis"),
            "Gura" : Streamer("HLEN04", "Gawr Gura", "hololive_en", ["gen1","en"], "gawr_gura.jpg", "@GawrGura"),
            "Amelia" : Streamer("HLEN05", "Watson Amelia", "hololive_en", ["gen1","en"], "watson_amelia.jpg", "@WatsonAmelia"),

            "IRyS" : Streamer("HLEN06", "IRyS", "hololive_en", ["hope","gen2","en"], "irys.jpg", "@IRyS"),
            "Fauna" : Streamer("HLEN07", "Ceres Fauna", "hololive_en", ["gen2","en"], "ceres_fauna.jpg", "@CeresFauna"),
            "Kronii" : Streamer("HLEN08", "Ouro Kronii", "hololive_en", ["gen2","en"], "ouro_kronii.jpg", "@OuroKronii"),
            "Mumei" : Streamer("HLEN09", "Nanashi Mumei", "hololive_en", ["gen2","en"], "nanashi_mumei.jpg", "@NanashiMumei"),
            "Baelz" : Streamer("HLEN10", "Hakos Baelz", "hololive_en", ["gen2","en"], "hakos_baelz.jpg", "@HakosBaelz"),
            "Sana" : Streamer("HLEN11", "Tsukumo Sana", "hololive_en", ["gen2","en"], "tsukumo_sana.jpg", "@TsukumoSana", True),

            "Shiori" : Streamer("HLEN12", "Shiori Novella", "hololive_en", ["gen3","en"], "shiori_novella.jpg", "@ShioriNovella"),
            "Bijou" : Streamer("HLEN13", "Koseki Bijou", "hololive_en", ["gen3","en"], "koseki_bijou.jpg", "@KosekiBijou"),
            "Nerissa" : Streamer("HLEN14", "Nerissa Ravencroft", "hololive_en", ["gen3","en"], "nerissa_ravencroft.jpg", "@NerissaRavencroft"),
            "FUWAMOCO" : Streamer("HLEN15", "FUWAMOCO", "hololive_en", ["gen3","en"], "fuwamoco.jpg", "@FUWAMOCOch"),
        }

    def get_streamer_by_name(self, name: str) -> Streamer:
        return self.streamers.get(name, None)

    def save_to_mongodb(self, uri: str, db_name: str, collection_name: str):
        client = pymongo.MongoClient(uri)
        db = client[db_name]
        collection = db[collection_name]
        for _, streamer in self.streamers.items():
            data = streamer.to_dict()
            collection.replace_one({"code": streamer.code}, data, upsert=True)
