"""
UCTE reader for UCTE standard:
UCTE data exchange format for load flow and three phase short circuit studies
Version 02 (coming into force:  2007.05.01)
"""

__author__ = "Denis Trputec"
__copyright__ = "HOPS 2020, UCTE reader"
__credits__ = ["Denis Trputec"]
__license__ = "HOPS d.o.o."
__app_name__ = "UCTE Reader"
__version__ = "1.0.1"
__maintainer__ = "Denis Trputec"
__email__ = "denis.trputec@hops.hr"
__status__ = "Completed"

from Node import Node
from Line import Line
from Transformer import Transformer
from TransformerRegulation import TransformerRegulation
from TransformerSpecParam import TransformerSpecParam

country_codes_list = [
    {'#': 1, 'country': 'A', 'name': 'Österreich (Austria)', 'country code nodes': 'O', 'country code': 'AT'},
    {'#': 2, 'country': 'AL', 'name': 'Shqiperia (Albania)', 'country code nodes': 'A', 'country code': 'AL'},
    {'#': 3, 'country': 'B', 'name': 'Belgique (Belgium)', 'country code nodes': 'B', 'country code': 'BE'},
    {'#': 4, 'country': 'BG', 'name': 'Bulgarija (Bulgaria)', 'country code nodes': 'V', 'country code': 'BG'},
    {'#': 5, 'country': 'BiH', 'name': 'Bosna i Hercegovina (Bosnia and Herzegovina)', 'country code nodes': 'W', 'country code': 'BA'},
    {'#': 6, 'country': 'BY', 'name': 'Belorussija (Belarus)', 'country code nodes': '3', 'country code': 'BY'},
    {'#': 7, 'country': 'CH', 'name': 'Schweiz (Switzerland)', 'country code nodes': 'S', 'country code': 'CH'},
    {'#': 8, 'country': 'CZ', 'name': 'Ceska Republika (Czech Republic)', 'country code nodes': 'C', 'country code': 'CZ'},
    {'#': 9, 'country': 'D', 'name': 'Deutschland (Germany)', 'country code nodes': 'D', 'country code': 'DE'},
    {'#': 10, 'country': 'DK', 'name': 'Danmark (Denmark)', 'country code nodes': 'K', 'country code': 'DK'},
    {'#': 11, 'country': 'E', 'name': 'Espana (Spain)', 'country code nodes': 'E', 'country code': 'ES'},
    {'#': 12, 'country': 'F', 'name': 'France (France)', 'country code nodes': 'F', 'country code': 'FR'},
    {'#': 13, 'country': 'GB', 'name': 'Great Britain (Great Britain)', 'country code nodes': '5', 'country code': 'GB'},
    {'#': 14, 'country': 'GR', 'name': 'Hellas (Greece)', 'country code nodes': 'G', 'country code': 'GR'},
    {'#': 15, 'country': 'H', 'name': 'Magyarorszag (Hungary)', 'country code nodes': 'M', 'country code': 'HU'},
    {'#': 16, 'country': 'HR', 'name': 'Hrvatska (Croatia)', 'country code nodes': 'H', 'country code': 'HR'},
    {'#': 17, 'country': 'I', 'name': 'Italia (Italy)', 'country code nodes': 'I', 'country code': 'IT'},
    {'#': 18, 'country': 'L', 'name': 'Luxembourg (Luxemburg)', 'country code nodes': '1', 'country code': 'LU'},
    {'#': 19, 'country': 'LT', 'name': 'Lietuva (Lithuania)', 'country code nodes': '6', 'country code': 'LT'},
    {'#': 20, 'country': 'MA', 'name': 'Maroc (Morocco)', 'country code nodes': '2', 'country code': 'MA'},
    {'#': 21, 'country': 'MD', 'name': 'Moldava (Moldavia)', 'country code nodes': '7', 'country code': 'MD'},
    {'#': 22, 'country': 'MK', 'name': 'Makedonija (FYROM)', 'country code nodes': 'Y', 'country code': 'MK'},
    {'#': 23, 'country': 'N', 'name': 'Norge (Norway)', 'country code nodes': '9', 'country code': 'NO'},
    {'#': 24, 'country': 'NL', 'name': 'Nederland (Netherlands)', 'country code nodes': 'N', 'country code': 'NL'},
    {'#': 25, 'country': 'P', 'name': 'Portugal (Portugal)', 'country code nodes': 'P', 'country code': 'PT'},
    {'#': 26, 'country': 'PL', 'name': 'Polska (Poland)', 'country code nodes': 'Z', 'country code': 'PL'},
    {'#': 27, 'country': 'RO', 'name': 'Romania (Romania)', 'country code nodes': 'R', 'country code': 'RO'},
    {'#': 28, 'country': 'RUS', 'name': 'Rossija (Russia)', 'country code nodes': '4', 'country code': 'RU'},
    {'#': 29, 'country': 'S', 'name': 'Sverige (Sweden)', 'country code nodes': '8', 'country code': 'SE'},
    {'#': 30, 'country': 'SK', 'name': 'Slovensko (Slovakia)', 'country code nodes': 'Q', 'country code': 'SK'},
    {'#': 31, 'country': 'SLO', 'name': 'Slovenija (Slovenia)', 'country code nodes': 'L', 'country code': 'SI'},
    {'#': 32, 'country': 'TR', 'name': 'Türkiye (Turkey)', 'country code nodes': 'T', 'country code': 'TR'},
    {'#': 33, 'country': 'UA', 'name': 'Ukraina (Ukraine)', 'country code nodes': 'U', 'country code': 'UA'},
    {'#': 34, 'country': 'MNE', 'name': 'Crna Gora (Montenegro)', 'country code nodes': '0', 'country code': 'ME'},
    {'#': 35, 'country': 'SRB', 'name': 'Srbija (Serbia)', 'country code nodes': 'J', 'country code': 'RS'},
    {'#': 36, 'country': '--', 'name': 'Fictitious border node', 'country code nodes': 'X', 'country code': 'XX'}
]


def read_lines(file_path, cls, first_line, last_line):
    # Open UCTE file
    with open(file_path) as handle:
        lines = handle.readlines()

    # Read only necessary par
    output = []
    flag_read = False
    for line in lines:
        if line == first_line:
            flag_read = True
            continue
        elif line == last_line:
            break
        elif flag_read:
            node = cls(line)
            output.append(node)

    return output


class Ucte:
    """
    file_name: name of file
    yyyymmdd: year, month and day
    HHMM: hour and minute
    TY: file type
    w: day of the week, starting with 1 for Monday
    cc: the ISO country-code for national datasets
    v: version number starting with 0
    """
    def __init__(self, file_path):
        """
        :param file_path: string (can be absolute or relatice path to uct file)
        """
        self.file_name = file_path.split('\\')[-1]
        self.yyyymmdd = self.file_name[0:8]
        self.HHMM = self.file_name[9:13]
        self.TY = self.file_name[14:16]
        self.w = self.file_name[16]
        self.cc = self.file_name[18:20]
        self.v = self.file_name.split('.')[0][20:]
        self.nodes = read_lines(file_path, Node, "##Z" + self.cc + "\n", "##ZXX\n")
        self.x_nodes = read_lines(file_path, Node, "##ZXX\n", "##L\n")
        self.lines = read_lines(file_path, Line, "##L\n", "##T\n")
        self.transformers = read_lines(file_path, Transformer, "##T\n", "##R\n")
        self.transformers_regulation = read_lines(file_path, TransformerRegulation, "##R\n", "##TT\n")
        self.transformers_spec_param = read_lines(file_path, TransformerSpecParam, "##TT\n", "##E\n")

    def get_year(self):
        """
        :return: integer
        """
        return int(self.yyyymmdd[0:4])

    def get_month(self):
        """
        :return: integer
        """
        return int(self.yyyymmdd[4:6])

    def get_day(self):
        """
        :return: integer
        """
        return int(self.yyyymmdd[6:8])

    def get_date_hr(self):
        """
        returns date in format: 'DD.MM.YYYY'
        :return: string
        """
        return self.yyyymmdd[6:8] + "." + self.yyyymmdd[4:6] + "." + self.yyyymmdd[0:4] + "."

    def get_date(self):
        """
        returns date in format: 'YYYY-MM-DD'.
        :return: string
        """
        return self.yyyymmdd[0:4] + "-" + self.yyyymmdd[4:6] + "-" + self.yyyymmdd[6:8]

    def get_file_type(self):
        """
        Returns name of file type instead of code
        :return: string
        """
        dictionary = {'FO': 'Forecast', 'SN': 'Snapshot', 'RE': 'Reference', 'LR': 'Long Term Reference'}
        return dictionary[self.TY]

    def get_day_of_week(self):
        """
        Returns day of the week instead of number
        :return: string
        """
        dictionary = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
        return dictionary[int(self.w)]

    def get_country_name_full(self):
        """
        Returns country name instead of country-code
        :return: string
        """
        for d in country_codes_list:
            if d['country code'] == self.cc:
                return d['name']

    def get_country_name(self):
        """
        Returns country name on English language
        :return: string
        """
        for d in country_codes_list:
            if d['country code'] == self.cc:
                return d['name'].split(' (')[1][:-1]

    def get_country_name_native(self):
        """
        Returns country name on native language
        :return: string
        """
        for d in country_codes_list:
            if d['country code'] == self.cc:
                return d['name'].split(' (')[0]


if __name__ == "__main__":
    file1 = "20200418_0930_FO6_HR1.uct"
    file2 = "20200401_2130_FO3_SI0.uct"
    file3 = "20200419_1430_SN7_HR0.uct"
    file4 = r"D:\Programiranje\Posao\UctReader\20200418_0930_FO6_HR1.uct"
    file_list = [file1, file2, file3, file4]

    for file in file_list:
        obj = Ucte(file)
        print(obj.file_name, len(obj.transformers_spec_param))
