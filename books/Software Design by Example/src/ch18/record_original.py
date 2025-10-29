class BasicRec:
    # These are class attributes
    MAX_NAME_LEN = 6     # length of name in chars
    TIMESTAMP_LEN = 8    # length of timestamp in chars
    MAX_READING = 10     # maximum reading value
    MAX_READING_LEN = 2  # length of reading in chars
    MAX_READINGS_NUM = 2 # maximum number of readings

    @staticmethod
    def key(record):
        assert isinstance(record, BasicRec)
        return record._name

    def __init__(self, name, timestamp, readings):
        assert 0 < len(name) <= self.MAX_NAME_LEN
        assert 0 <= len(readings) <= self.MAX_READINGS_NUM
        assert all((0 <= r <= self.MAX_READING) for r in readings)
        self._name = name
        self._timestamp = timestamp
        self._readings = readings
