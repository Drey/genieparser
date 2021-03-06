# Python
import unittest
from unittest.mock import Mock

# ATS
from ats.topology import Device

# Metaparset
from genie.metaparser.util.exceptions import SchemaEmptyParserError, \
                                       SchemaMissingKeyError

from genie.libs.parser.iosxe.tests.test_show_archive import test_show_archive as test_show_archive_iosxe

# Parser
from genie.libs.parser.ios.show_archive import ShowArchive


# ============================================
# unit test for 'show archive'
# ============================================
class test_show_archive(test_show_archive_iosxe):

    def test_empty(self):
        self.device1 = Mock(**self.empty_output)
        obj = ShowArchive(device=self.device1)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden(self):
        self.device = Mock(**self.golden_output)
        obj = ShowArchive(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output)


class test_show_archive_ios(unittest.TestCase):
    
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output_1 = {
        'archive': {
            'total': 1,
            'most_recent_file': 'disk0:myconfig-1',
            '1': {
                'file': 'disk0:myconfig-1',
            }
        }
    }
    golden_output_1 = {'execute.return_value': '''\
    Router# show archive

     There are currently 1 archive configurations saved.
     The next archive file will be named disk0:myconfig-2
      Archive #  Name
        0
        1       disk0:myconfig-1 <- Most Recent
        2
        3
        4
        5
        6
        7
        8
        9
        10
        '''}

    def test_empty(self):
        self.device1 = Mock(**self.empty_output)
        obj = ShowArchive(device=self.device1)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden_1(self):
        self.device = Mock(**self.golden_output_1)
        obj = ShowArchive(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output_1)

if __name__ == '__main__':
    unittest.main()