import unittest
from pangu.particle.text.text import Text

class TestText(unittest.TestCase):

    def test_init_and_str(self):
        t = Text("hello")
        self.assertEqual(str(t), "hello")

    def test_len(self):
        t = Text("hello world")
        self.assertEqual(len(t), 11)

    def test_repr(self):
        t = Text("this is a long Text")
        r = repr(t)
        self.assertIn("Text(", r)
        self.assertIn("this is a ...", r)

    def test_add_Text(self):
        t1 = Text("hello ")
        t2 = Text("world")
        t3 = t1 + t2
        self.assertIsInstance(t3, Text)
        self.assertEqual(str(t3), "hello world")

    def test_add_str(self):
        t1 = Text("hello ")
        t2 = t1 + "world"
        self.assertIsInstance(t2, Text)
        self.assertEqual(str(t2), "hello world")

    def test_radd_str(self):
        t1 = Text("world")
        t2 = "hello " + t1
        self.assertIsInstance(t2, Text)
        self.assertEqual(str(t2), "hello world")

    def test_eq_and_ne(self):
        self.assertTrue(Text("abc") == "abc")
        self.assertTrue(Text("abc") == Text("abc"))
        self.assertTrue(Text("abc") != "def")
        self.assertTrue(Text("abc") != Text("def"))

    def test_upper_lower(self):
        t = Text("Hello")
        self.assertEqual(t.__upper__(), "HELLO")
        self.assertEqual(t.__lower__(), "hello")

    def test_as_upper_lower(self):
        t = Text("Hello")
        t.as_upper()
        self.assertEqual(str(t), "HELLO")
        t.as_lower()
        self.assertEqual(str(t), "hello")

    def test_encode(self):
        t = Text("hello")
        self.assertEqual(t.encode(), b"hello")

    def test_digest(self):
        t = Text("hello")
        t.as_digest("sha256")
        self.assertIsInstance(t.content, str)
        self.assertEqual(len(t.content), 64)

        t2 = Text("hello").to_digest("sha256")
        self.assertIsInstance(t2, Text)
        self.assertEqual(len(str(t2)), 64)

    def test_wildcard_match(self):
        t = Text("hello_world.py")
        self.assertTrue(t.wildcard_match("*.py"))
        self.assertFalse(t.wildcard_match("*.txt"))

if __name__ == "__main__":
    unittest.main()