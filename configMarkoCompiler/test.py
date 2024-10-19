import unittest
from unittest.mock import patch, mock_open

TEST_CONFIG = [
    r"#define STUFF \"i3-nagbar -t warning -m 'Hotkey not available!';\" mode \"notAvailable\"     ",
    r"set     $var1 Value1",
    r"    set $var2 Value2",
    r"    set $var3 'var2 is $var2'",
    r"    set $var4 '\$var4 is $var3'",
    r"    bindsym $var1 $var2",
    r"bindsym --release Print exec \"$(date --rfc-3339=seconds)\".png",
    r"fxx STUFF"
]


class TestConfigSubstitution(unittest.TestCase):
    def test_resolve_makros(self):
        from configMarkoCompiler import resolve_makros
        lines = resolve_makros(TEST_CONFIG)
        self.assertEqual(len(lines), 7)
        self.assertEqual(lines[0], r"set     $var1 Value1")
        self.assertEqual(lines[1], r"    set $var2 Value2")
        self.assertEqual(lines[2], r"    set $var3 'var2 is $var2'")
        self.assertEqual(lines[3], r"    set $var4 '\$var4 is $var3'")
        self.assertEqual(lines[4], r"    bindsym $var1 $var2")
        self.assertEqual(lines[5], r"bindsym --release Print exec \"$(date --rfc-3339=seconds)\".png")
        self.assertEqual(lines[6], r"fxx \"i3-nagbar -t warning -m 'Hotkey not available!';\" mode \"notAvailable\"")

    def test_replace_variables(self):
        from configMarkoCompiler import replace_variables
        lines = replace_variables(TEST_CONFIG)
        self.assertEqual(len(lines), 8)
        self.assertEqual(lines[0], r"#define STUFF \"i3-nagbar -t warning -m 'Hotkey not available!';\" mode \"notAvailable\"     ")
        self.assertEqual(lines[1], r"set     $var1 Value1")
        self.assertEqual(lines[2], r"    set $var2 Value2")
        self.assertEqual(lines[3], r"    set $var3 'var2 is Value2'")
        self.assertEqual(
            lines[4],
            r"    set $var4 '\$var4 is 'var2 is Value2''"
        )
        self.assertEqual(lines[5], r"    bindsym Value1 Value2")
        self.assertEqual(lines[6], r"bindsym --release Print exec \"$(date --rfc-3339=seconds)\".png")
        self.assertEqual(lines[7], r"fxx STUFF")


if __name__ == '__main__':
    unittest.main()
