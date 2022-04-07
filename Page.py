from Parser import K_VALUE


class Page:
    def __init__(
        self, ID: int, value: int, timeOfAccess: int, K_VALUE: int
    ) -> None:
        self._ID: int = ID
        self._value: int = value

        # TODO make another class for only _LAST and _HIST
        self._LAST: int = timeOfAccess

        # HIST is an array of size K_VALUE
        self._HIST: list[int] = [timeOfAccess] + [0] * (K_VALUE - 1)

    # getters
    @property
    def ID(self):
        return self._ID

    @property
    def value(self):
        return self._value

    @property
    def LAST(self):
        return self._LAST

    @property
    def HIST(self):
        return self._HIST

    @ID.setter
    def ID(self, ID):
        self._ID = ID

    @value.setter
    def value(self, value):
        self._value = value

    @LAST.setter
    def LAST(self, timeStamp):
        self._LAST = timeStamp

    def __lt__(self, other):
        return self._HIST[K_VALUE - 1] < other._HIST[K_VALUE - 1]

    def __cmp__(self, other):
        if self._HIST[K_VALUE - 1] < other._HIST[K_VALUE - 1]:
            return -1
        elif self._HIST[K_VALUE - 1] > other._HIST[K_VALUE - 1]:
            return 1
        else:
            return 0

    def update(self, timeStamp: int):
        lcp: int = self._LAST - self._HIST[0]
        for index in self._HIST[1:]:
            self._HIST[index] = self._HIST[index - 1] + lcp
        self._LAST = timeStamp
        self._HIST[0] = timeStamp
