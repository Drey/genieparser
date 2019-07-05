# Python
import unittest
from unittest.mock import Mock

# ATS
from ats.topology import Device

# Metaparset
from genie.metaparser.util.exceptions import SchemaEmptyParserError, \
                                       SchemaMissingKeyError

# Parser
from genie.libs.parser.iosxe.show_vtp import ShowVtpStatus


# ============================================
# Parser for 'show vtp status'
# ============================================
class test_show_vtp_status(unittest.TestCase):
    
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}
    
    golden_parsed_output = {
        "vtp": {
        "pruning_mode": False,
        "device_id": "3820.5622.a580",
        "traps_generation": False,
        "updater_id": "192.168.234.1",
        "updater_interface": "Vl100",
        "updater_reason": "lowest numbered VLAN interface found",
        "configuration_revision": 55,
        "maximum_vlans": 1005,
        "md5_digest": '0x2D 0x35 0x38 0x3C 0x3D 0x55 0x62 0x66 0x67 0x70 '\
                      '0x72 0x74 0x9E 0xDD 0xDE 0xE9',
        "existing_vlans": 53,
        "enabled": True,
        "operating_mode": "server",
        "conf_last_modified_time": "12-5-17 09:35:46",
        "conf_last_modified_by": "192.168.234.1",
        "version": "1",
        "version_capable": [1,2,3],
        }

    }

    golden_output = {'execute.return_value': '''\
        VTP Version capable             : 1 to 3
        VTP version running             : 1
        VTP Domain Name                 : 
        VTP Pruning Mode                : Disabled
        VTP Traps Generation            : Disabled
        Device ID                       : 3820.5622.a580
        Configuration last modified by 192.168.234.1 at 12-5-17 09:35:46
        Local updater ID is 192.168.234.1 on interface Vl100 (lowest numbered VLAN interface found)

        Feature VLAN:
        --------------
        VTP Operating Mode                : Server
        Maximum VLANs supported locally   : 1005
        Number of existing VLANs          : 53
        Configuration Revision            : 55
        MD5 digest                        : 0x9E 0x35 0x3C 0x74 0xDD 0xE9 0x3D 0x62 
                                            0xDE 0x2D 0x66 0x67 0x70 0x72 0x55 0x38
    '''}


    def test_empty(self):
        self.device1 = Mock(**self.empty_output)
        obj = ShowVtpStatus(device=self.device1)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden(self):
        self.device = Mock(**self.golden_output)
        obj = ShowVtpStatus(device=self.device)
        parsed_output = obj.parse()
        self.maxDiff = None
        self.assertEqual(parsed_output,self.golden_parsed_output)


if __name__ == '__main__':
    unittest.main()