import enum


class AnswerType(enum.IntEnum):
    OK = 1,
    NOT_FOUND = 2,
    ONLY_ONE = 3,
    MANUAL = 4
