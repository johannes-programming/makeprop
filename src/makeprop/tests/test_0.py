import unittest

from makeprop.core import makeprop


class TestMakeprop(unittest.TestCase):
    def test_default_initialization(self):
        """Test initialization with default arguments."""
        prop = makeprop()
        self.assertIsNone(prop.var)
        self.assertFalse(prop.hasdeleter)
        self.assertIsNone(prop.deletervalue)

    def test_initialization_with_var(self):
        """Test initialization with a string variable."""
        prop = makeprop(var="test_var")
        self.assertEqual(prop.var, "test_var")
        self.assertFalse(prop.hasdeleter)
        self.assertIsNone(prop.deletervalue)

    def test_initialization_with_deleter(self):
        """Test initialization with deleter arguments."""
        prop = makeprop(var="test_var", delete="delete_value")
        self.assertEqual(prop.var, "test_var")
        self.assertTrue(prop.hasdeleter)
        self.assertEqual(prop.deletervalue, "delete_value")

    def test_call_without_deleter(self):
        """Test the __call__ method without a deleter."""

        class TestClass:
            @makeprop()
            def my_prop(self, value):
                return value * 2

        obj = TestClass()
        obj._my_prop = 10
        self.assertEqual(obj.my_prop, 10)

        obj.my_prop = 15
        self.assertEqual(obj._my_prop, 30)
        self.assertEqual(obj.my_prop, 30)

    def test_call_with_deleter(self):
        """Test the __call__ method with a deleter."""

        class TestClass:
            @makeprop(delete=None)
            def my_prop(self, value):
                if value is None:
                    return 0
                return value * 3

        obj = TestClass()
        obj._my_prop = 10
        self.assertEqual(obj.my_prop, 10)

        obj.my_prop = 5
        self.assertEqual(obj._my_prop, 15)
        self.assertEqual(obj.my_prop, 15)

        del obj.my_prop
        self.assertEqual(obj._my_prop, 0)


if __name__ == "__main__":
    unittest.main()
