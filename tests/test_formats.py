import unittest
from io import StringIO
from unittest.mock import patch

import crowsetta


class TestFormats(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_show(self, mock_stdout):
        # make sure calling formats.show() gives us back some string
        crowsetta.formats.show()
        what_printed = mock_stdout.getvalue()
        self.assertTrue(type(what_printed) == str)
        for format in crowsetta.formats._INSTALLED:
            # and that string should have the different formats in it somewhere
            self.assertTrue(format in what_printed)


if __name__ == '__main__':
    unittest.main()
