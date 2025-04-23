class TextCase:
    simbol = ".-_/\ "
    kapital = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, text: str) -> None:
        self.text = self.explode(text)
        self.double_symbol = True

    def explode(self, text):
        r = []
        b = ""

        for t in text:
            if t in self.simbol:
                if len(b):
                    r.append(b)
                    b = ""
                r.append(t)
            elif t in self.kapital:
                if len(b):
                    r.append(b)
                    b = ""
                b = t
            else:
                b += t

        if len(b):
            r.append(b)
            b = ""

        return r

    def to_title_case(self):
        r = ""
        z = True
        for i in self.text:
            if i in self.simbol:
                if not z or self.double_symbol:
                    r += ""
                z = True
            else:
                if not z:
                    r += ""
                r += i.title()
                z = False
        return r

    def to_snake_case(self):
        r = ""
        z = True
        for i in self.text:
            if i in self.simbol:
                if not z or self.double_symbol:
                    r += "_"
                z = True
            else:
                if not z:
                    r += "_"
                r += i.lower()
                z = False
        return r

    def to_camel_case(self):
        r = ""
        z = True
        for i in self.text:
            if i in self.simbol:
                if not z or self.double_symbol:
                    r += ""
                z = True
            else:
                if not z:
                    r += ""
                r += i.title()
                z = False
        return r

    def to_path_case(self):
        r = ""
        z = True
        for i in self.text:
            if i in self.simbol:
                if not z or self.double_symbol:
                    r += "/"
                z = True
            else:
                if not z:
                    r += "/"
                r += i
                z = False
        return r

    def to_dot_case(self):
        r = ""
        z = True
        for i in self.text:
            if i in self.simbol:
                if not z or self.double_symbol:
                    r += "."
                z = True
            else:
                if not z:
                    r += "."
                r += i
                z = False
        return r

    def to_space_case(self):
        r = ""
        z = True
        for i in self.text:
            if i in self.simbol:
                if not z or self.double_symbol:
                    r += " "
                z = True
            else:
                if not z:
                    r += " "
                r += i
                z = False
        return r
