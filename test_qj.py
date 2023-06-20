#!/usr/bin/env python3

from libfb.py import testutil

from .lib import _jskey, find


class TestJSKey(testutil.BaseFacebookTestCase):
    def test_plain(self):
        self.assertEquals(_jskey("foo"), ".foo")

    def test_punctuated(self):
        self.assertEquals(_jskey("I'm a string!"), """["I'm a string!"]""")

    def test_numeric(self):
        self.assertEquals(_jskey("123"), """["123"]""")

    def test_alphanumeric(self):
        self.assertEquals(_jskey("abc123"), ".abc123")


class TestFind(testutil.BaseFacebookTestCase):
    def setUp(self):
        testutil.BaseFacebookTestCase.setUp(self)
        self.struct = {
            "cakes": {
                "sweet": {
                    "Extreme Chocolate": {
                        "variations": ["Moist", "Sugary", "Lovely", "This is delicious"]
                    }
                },
                "savoury": {"Extreme Carrot": {"variations": ["Lovely"]}},
            }
        }

    def test_basic(self):
        self.assertEquals(
            find("This is delicious", self.struct),
            [('.cakes.sweet["Extreme Chocolate"].variations[3]', "This is delicious")],
        )

    def test_multiple(self):
        self.assertEquals(
            find("Lovely", self.struct),
            [
                ('.cakes.sweet["Extreme Chocolate"].variations[2]', "Lovely"),
                ('.cakes.savoury["Extreme Carrot"].variations[0]', "Lovely"),
            ],
        )
