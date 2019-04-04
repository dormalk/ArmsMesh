class GPS:
    def __init__(self):
        self.longitude = 12.12
        self.latitude = 34.12

    def collect(self):
        value = 'G:'
        value += str(self.latitude)
        value += ','
        value += str(self.longitude)
        return value

class ACC:
    def __init__(self):
        self.x = 1.12
        self.y = 3.12
        self.z = 5.00

    def collect(self):
        value = 'A:'
        value += str(self.x)
        value += ','
        value += str(self.y)
        value += ','
        value += str(self.z)
        return value


class PULSE:
    def __init__(self):
        self.value=120

    def collect(self):
        value = 'P:'
        value += str(self.value)
        return value


class EMARG:
    def __init__(self):
        self.value = False

    def collect(self):
        value = 'E:'
        value += str(self.value)
        return value