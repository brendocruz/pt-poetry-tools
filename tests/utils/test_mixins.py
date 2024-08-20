import re
from unittest import TestCase
from src.utils.mixins import ReprMixin


class ReprMixinMock(ReprMixin):
    def __init__(self, items: list[int]):
        self.items = items


class TestMixin(TestCase):
    def test_repr(self):
        instance = ReprMixinMock([1, 2, 3])
        pattern  = re.compile('^<.+>$')
        self.assertNotRegex(repr(instance), pattern)
