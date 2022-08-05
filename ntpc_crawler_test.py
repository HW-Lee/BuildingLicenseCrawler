from ntpc_crawler import analyze_key_value_table, analyze_row_column_table

class TestTableAnalyzer:
    def test_analyze_key_value_table(self):
        xmlstr = "" \
            "<?xml version=\"1.0\" ?>\n" \
            "<table>\n" \
            "    <caption class=\"tb_title\">設計人</caption>\n" \
            "    <tbody>\n" \
            "        <tr>\n" \
            "            <th>設計人</th>\n" \
            "            <td colspan=\"3\">李兆嘉</td>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <th>事務所名稱</th>\n" \
            "            <td colspan=\"3\">李兆嘉建築師事務所</td>\n" \
            "        </tr>\n" \
            "        <tr class=\"tr_hidden\">\n" \
            "            <td width=\"20%\"/>\n" \
            "            <td width=\"30%\"/>\n" \
            "            <td width=\"20%\"/>\n" \
            "            <td width=\"30%\"/>\n" \
            "        </tr>\n" \
            "    </tbody>\n" \
            "</table>\n"

        assert analyze_key_value_table(xmlstr=xmlstr) == {
            "設計人": {
                "設計人": "李兆嘉",
                "事務所名稱": "李兆嘉建築師事務所"
            }
        }

        xmlstr = "" \
            "<?xml version=\"1.0\" ?>\n" \
            "<table>\n" \
            "    <caption class=\"tb_title\">基地概要</caption>\n" \
            "    <tbody>\n" \
            "        <tr>\n" \
            "            <th>使用分區</th>\n" \
            "            <td colspan=\"3\">第一種住宅區</td>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <th>騎樓地面積</th>\n" \
            "            <td>0㎡</td>\n" \
            "\n" \
            "            <th>其他面積</th>\n" \
            "            <td>6684.89㎡</td>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <th>退縮地面積</th>\n" \
            "            <td>0㎡</td>\n" \
            "\n" \
            "            <th>基地面積合計</th>\n" \
            "            <td>6684.89㎡</td>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <td class=\"tb_title\" colspan=\"4\" style=\"line-height: 5px;\">建築概要</td>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <th>層棟戶數</th>\n" \
            "            <td>2幢4棟地上7層 地下3層 共210戶</td>\n" \
            "\n" \
            "            <th>法定空地面積</th>\n" \
            "            <td>4823.19㎡</td>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <th>設計建蔽率</th>\n" \
            "            <td>27.85％</td>\n" \
            "\n" \
            "            <th>總樓地板面積</th>\n" \
            "            <td>21347.25㎡</td>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <th>設計容積率</th>\n" \
            "            <td>155.99％</td>\n" \
            "\n" \
            "            <th>建物高度</th>\n" \
            "            <td>21.6Ｍ</td>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <th>建造類別</th>\n" \
            "            <td>新建</td>\n" \
            "\n" \
            "            <th>構造種類</th>\n" \
            "            <td>鋼筋混凝土構造</td>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <th>防空避難面積</th>\n" \
            "            <td colspan=\"3\">地上0㎡，地下--㎡</td>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <th>總設計停車輛數</th>\n" \
            "            <td>180</td>\n" \
            "\n" \
            "            <th>法定停車輛數</th>\n" \
            "            <td>83</td>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <th>自行增設停車輛數</th>\n" \
            "            <td>97</td>\n" \
            "\n" \
            "            <th>鼓勵停車輛數</th>\n" \
            "            <td>0</td>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <th>工程造價</th>\n" \
            "            <td colspan=\"3\">246129122元</td>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <th>發照日期</th>\n" \
            "            <td colspan=\"3\">民國110年12月08日</td>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <td class=\"tb_title\" colspan=\"4\" style=\"line-height: 5px;\">雜項</td>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <th>雜項工作物</th>\n" \
            "            <td colspan=\"3\">詳雜項工作物概要表</td>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <td class=\"tb_title\" colspan=\"4\" style=\"line-height: 5px;\">其他</td>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <th>核准日期    </th>\n" \
            "            <td>民國110年11月15日</td>\n" \
            "\n" \
            "            <th>規定竣工日期</th>\n" \
            "            <td>自開工日起 65 個月內竣工</td>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <th>開工日期    </th>\n" \
            "            <td>--</td>\n" \
            "\n" \
            "            <th>實際竣工日期</th>\n" \
            "            <td>--</td>\n" \
            "        </tr>\n" \
            "        <tr class=\"tr_hidden\">\n" \
            "            <td width=\"18%\"/>\n" \
            "            <td width=\"32%\"/>\n" \
            "            <td width=\"20%\"/>\n" \
            "            <td width=\"30%\"/>\n" \
            "        </tr>\n" \
            "    </tbody>\n" \
            "</table>\n"

        assert analyze_key_value_table(xmlstr=xmlstr) == {
            "基地概要": {
                "使用分區": "第一種住宅區",
                "騎樓地面積": "0㎡",
                "其他面積": "6684.89㎡",
                "退縮地面積": "0㎡",
                "基地面積合計": "6684.89㎡",
            },
            "建築概要": {
                "層棟戶數": "2幢4棟地上7層 地下3層 共210戶",
                "法定空地面積": "4823.19㎡",
                "設計建蔽率": "27.85％",
                "總樓地板面積": "21347.25㎡",
                "設計容積率": "155.99％",
                "建物高度": "21.6Ｍ",
                "建造類別": "新建",
                "構造種類": "鋼筋混凝土構造",
                "防空避難面積": "地上0㎡，地下--㎡",
                "總設計停車輛數": "180",
                "法定停車輛數": "83",
                "自行增設停車輛數": "97",
                "鼓勵停車輛數": "0",
                "工程造價": "246129122元",
                "發照日期": "民國110年12月08日",
            },
            "雜項": {
                "雜項工作物": "詳雜項工作物概要表",
            },
            "其他": {
                "核准日期": "民國110年11月15日",
                "規定竣工日期": "自開工日起 65 個月內竣工",
                "開工日期": "--",
                "實際竣工日期": "--",
            },
        }

        xmlstr = "" \
            "<?xml version=\"1.0\" ?>\n" \
            "<table>\n" \
            "    <caption class=\"tb_title\">相關執照</caption>\n" \
            "    <tbody>\n" \
            "        <tr>\n" \
            "            <th>執照字號</th>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <td>\n" \
            "                <a href=\"bm_detail.jsp?ri1=110&amp;ri2=1&amp;ri3=00600&amp;ri4=00&amp;ri5=11010060000I30\">110淡建字第00600號</a>\n" \
            "            </td>\n" \
            "        </tr>\n" \
            "        <tr class=\"tr_hidden\">\n" \
            "            <td width=\"100%\"/>\n" \
            "        </tr>\n" \
            "    </tbody>\n" \
            "</table>\n"

        assert analyze_key_value_table(xmlstr=xmlstr) == {
            "相關執照": {
                "執照字號": "110淡建字第00600號",
            }
        }

    def test_analyze_row_column_table(self):
        xmlstr = "" \
            "<?xml version=\"1.0\" ?>\n" \
            "<table>\n" \
            "    <caption class=\"tb_title\">樓層</caption>\n" \
            "    <tbody>\n" \
            "        <tr>\n" \
            "            <th>棟別</th>\n" \
            "            <th>層別</th>\n" \
            "            <th>樓層高度</th>\n" \
            "            <th>申請面積</th>\n" \
            "            <th>陽台面積</th>\n" \
            "            <th>露台面積</th>\n" \
            "            <th>使用類組</th>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <td>--</td>\n" \
            "            <td>地下001層</td>\n" \
            "            <td>4Ｍ</td>\n" \
            "            <td>2615.69㎡</td>\n" \
            "            <td>0</td>\n" \
            "            <td>0</td>\n" \
            "            <td>停車空間</td>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <td>--</td>\n" \
            "            <td>地下002層</td>\n" \
            "            <td>3.1Ｍ</td>\n" \
            "            <td>2587.07㎡</td>\n" \
            "            <td>0</td>\n" \
            "            <td>0</td>\n" \
            "            <td>停車空間</td>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <td>--</td>\n" \
            "            <td>地上001層</td>\n" \
            "            <td>3.6Ｍ</td>\n" \
            "            <td>1813.19㎡</td>\n" \
            "            <td>0</td>\n" \
            "            <td>0</td>\n" \
            "            <td>梯廳、管委會使用空間、H2集合住宅</td>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <td>--</td>\n" \
            "            <td>地上002層</td>\n" \
            "            <td>3Ｍ</td>\n" \
            "            <td>1845.96㎡</td>\n" \
            "            <td>157.89</td>\n" \
            "            <td>0</td>\n" \
            "            <td>H2集合住宅</td>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <td>--</td>\n" \
            "            <td>突出物001層</td>\n" \
            "            <td>3.1Ｍ</td>\n" \
            "            <td>229.68㎡</td>\n" \
            "            <td>0</td>\n" \
            "            <td>0</td>\n" \
            "            <td>樓梯間、機房</td>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <td>--</td>\n" \
            "            <td>突出物002層</td>\n" \
            "            <td>2.9Ｍ</td>\n" \
            "            <td>229.68㎡</td>\n" \
            "            <td>0</td>\n" \
            "            <td>0</td>\n" \
            "            <td>水錶室</td>\n" \
            "        </tr>\n" \
            "        <tr class=\"tr_hidden\">\n" \
            "            <td width=\"10%\"/>\n" \
            "            <td width=\"20%\"/>\n" \
            "            <td width=\"16%\"/>\n" \
            "            <td width=\"16%\"/>\n" \
            "            <td width=\"10%\"/>\n" \
            "            <td width=\"10%\"/>\n" \
            "            <td width=\"20%\"/>\n" \
            "        </tr>\n" \
            "    </tbody>\n" \
            "</table>\n"

        assert analyze_row_column_table(xmlstr=xmlstr) == {
            "樓層": {
                "棟別": [
                    "--",
                    "--",
                    "--",
                    "--",
                    "--",
                    "--",
                ],
                "層別": [
                    "地下001層",
                    "地下002層",
                    "地上001層",
                    "地上002層",
                    "突出物001層",
                    "突出物002層",
                ],
                "樓層高度": [
                    "4Ｍ",
                    "3.1Ｍ",
                    "3.6Ｍ",
                    "3Ｍ",
                    "3.1Ｍ",
                    "2.9Ｍ",
                ],
                "申請面積": [
                    "2615.69㎡",
                    "2587.07㎡",
                    "1813.19㎡",
                    "1845.96㎡",
                    "229.68㎡",
                    "229.68㎡",
                ],
                "陽台面積": [
                    "0",
                    "0",
                    "0",
                    "157.89",
                    "0",
                    "0",
                ],
                "露台面積": [
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                ],
                "使用類組": [
                    "停車空間",
                    "停車空間",
                    "梯廳、管委會使用空間、H2集合住宅",
                    "H2集合住宅",
                    "樓梯間、機房",
                    "水錶室",
                ],
            },
        }

        xmlstr = "" \
            "<?xml version=\"1.0\" ?>\n" \
            "<table>\n" \
            "    <caption class=\"tb_title\">起造人變更記錄</caption>\n" \
            "    <tbody>\n" \
            "        <tr>\n" \
            "            <th>變更日期</th>\n" \
            "            <td colspan=\"3\">民國111年05月11日</td>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <th>變更內容</th>\n" \
            "            <td colspan=\"3\">2幢2棟1層S1戶   僑OO設股份有限公司負責人:李勇志</td>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <th>變更日期</th>\n" \
            "            <td colspan=\"3\">民國111年05月11日</td>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <th>變更內容</th>\n" \
            "            <td colspan=\"3\">2幢2棟2層A1戶   僑OO設股份有限公司負責人:李勇志</td>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <th>變更日期</th>\n" \
            "            <td colspan=\"3\">民國111年05月11日</td>\n" \
            "        </tr>\n" \
            "        <tr>\n" \
            "            <th>變更內容</th>\n" \
            "            <td colspan=\"3\">2幢2棟3層A1戶   僑OO設股份有限公司負責人:李勇志</td>\n" \
            "        </tr>\n" \
            "        <tr class=\"tr_hidden\">\n" \
            "            <td width=\"20%\"/>\n" \
            "            <td width=\"30%\"/>\n" \
            "            <td width=\"20%\"/>\n" \
            "            <td width=\"30%\"/>\n" \
            "        </tr>\n" \
            "    </tbody>\n" \
            "</table>\n"

        assert analyze_row_column_table(xmlstr=xmlstr) == {
            "起造人變更記錄": {
                "變更日期": [
                    "民國111年05月11日",
                    "民國111年05月11日",
                    "民國111年05月11日",
                ],
                "變更內容": [
                    "2幢2棟1層S1戶   僑OO設股份有限公司負責人:李勇志",
                    "2幢2棟2層A1戶   僑OO設股份有限公司負責人:李勇志",
                    "2幢2棟3層A1戶   僑OO設股份有限公司負責人:李勇志",
                ],
            }
        }
