class TransformerSpecParam:
    def __init__(self, transformer_line):
        """
        :param transformer_line: line of uct file contaning line
        """
        self.line = transformer_line
        self.node1 = self.line[0:8]
        self.node2 = self.line[9:17]
        self.order_code = self.line[18]
        self.tap_postion = self.__get_tap_position()
        self.resistance_r = self.__get_resistance(0)
        self.resistance_x = self.__get_resistance(1)
        self.delta = self.__get_delta()
        self.angle = self.__get_angle()

    def __get_tap_position(self):
        """
        n'
        :return: integer
        """
        try:
            return int(self.line[22:25])
        except ValueError:
            return None

    def __get_resistance(self, index):
        """
        Pertaining to the rated voltage of the non-regulated winding 1 of the transformer
        :parameter: index = 0 for Resistance R at tap n’ (Ω) and index = 1 for Reactance X at tap n’ (Ω)
        :return: float
        """
        try:
            return float(self.line[26 + index * 7:32 + index * 7])
        except ValueError:
            return None

    def __get_delta(self):
        """
        ∆u at tap n’ (%)
        :return: float
        """
        try:
            return float(self.line[40:45])
        except ValueError:
            return None

    def __get_angle(self):
        """
        Phase shift angle α at tap n’ (°) (0° for phase regulation)
        :return: float
        """
        try:
            return float(self.line[46:51])
        except ValueError:
            return None


if __name__ == "__main__":
    line1 = "HSENJ 5  HSENJ 2  1 0  12  0.090    8.6 19.44 -10.5 "
    line2 = "HZERJA2  HZERJA1  1 0 -12  0.195   20.0 -9.79 -4.48 "
    line3 = "HZERJA2  HZERJA1  1 0 -12  0.195   20.0 -9.79 -4.48 "
    line4 = "HZERJA2  HZERJA1  1 0  11  0.195   15.6 11.52  6.12 "
    lines = [line1, line2, line3, line4]

    for line in lines:
        obj = TransformerSpecParam(line)
        print(obj.node1, obj.node2, obj.delta)
