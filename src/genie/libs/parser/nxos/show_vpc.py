import re


from genie.metaparser import MetaParser


class ShowVpcSchema(MetaParser):

    schema = {
        'vpc':{
            'vpc-domain-id': int,
            'vpc-peer-status': str,
            'vpc-peer-keepalive-status': str,
            'vpc-per-vlan-peer-consistency': str,
            'vpc-peer-consistency-status': str,
            'vpc-type-2-consistency-status': str,
            'vpc-role': str,
            'num-of-vpcs': int,
            'peer-gateway': str,
            'dual-active-excluded-vlans': str,
            'vpc-graceful-consistency-check-status': str,
            'vpc-auto-recovery-status': str,
            'vpc-delay-restore-status': str,
            'vpc-delay-restore-svi-status': str,
            'operational-l3-peer': str
        }
    }


class ShowVpc(ShowVpcSchema):
    
    cli_command = 'show vpc'

    def cli(self, cmd= cli_command, output=None):
        if output is None:
            out = self.device.execute(cmd)
        else:
            out = output

        regexp_dict = {
            # vPC domain id                     : 10
            'vpc-domain-id': {
                'regexp': r'^vPC\sdomain\sid\s*?:\s(\d*?)$',
                'expected_state': None
            },
            # Peer status                       : peer adjacency formed ok
            'vpc-peer-status': {
                'regexp': r'Peer\sstatus\s*?:\s(.+?)$',
                'expected_state': 'peer adjacency formed ok'
            },
            # vPC keep-alive status             : peer is alive
            'vpc-peer-keepalive-status': {
                'regexp': r'vPC\skeep-alive\sstatus\s*?:\s(.+?)$',
                'expected_state': 'peer is alive'
            },
            # Per-vlan consistency status       : success
            'vpc-per-vlan-peer-consistency': {
                'regexp': r'Per-vlan\s(?:in)?consistency\sstatus\s*?:\s(.+?)$',
                'expected_state': 'success'
            },
            # Configuration consistency status  : success
            'vpc-peer-consistency-status': {
                'regexp': r'Configuration\s(?:in)?consistency\s(?:reason|status)\s*?:\s(.+?)$',
                'expected_state': 'success'
            },
            # Type-2 consistency status         : success
            'vpc-type-2-consistency-status': {
                'regexp': r'Type-2\s(?:in)?consistency\s(?:reason|status)\s*?:\s(.+?)$',
                'expected_state': 'success'
            },
            # vPC role                          : primary
            'vpc-role': {
                'regexp': r'vPC\srole\s*?:\s(.+?)$',
                'expected_state': None
            },
            # Number of vPCs configured         : 0
            'num-of-vpcs': {
                'regexp': r'Number\sof\svPCs\sconfigured\s*?:\s(.+?)$',
                'expected_state': None
            },
            # Peer Gateway                      : Enabled
            'peer-gateway': {
                'regexp': r'Peer\sGateway\s*?:\s(.+?)$',
                'expected_state': None
            },
            # Dual-active excluded VLANs        : -
            'dual-active-excluded-vlans': {
                'regexp': r'Dual-active\sexcluded\sVLANs\s*?:\s(.+?)$',
                'expected_state': None
            },
            # Graceful Consistency Check        : Enabled
            'vpc-graceful-consistency-check-status': {
                'regexp': r'Graceful\sConsistency\sCheck\s*?:\s(.+?)$',
                'expected_state': None
            },
            # Auto-recovery status              : Enabled, timer is off.(timeout = 240s)
            'vpc-auto-recovery-status': {
                'regexp': r'Auto-recovery\sstatus\s*?:\s(.+?)$',
                'expected_state': None
            },
            # Delay-restore status              : Timer is off.(timeout = 30s)
            'vpc-delay-restore-status': {
                'regexp': r'Delay-restore\sstatus\s*?:\s(.+?)$',
                'expected_state': None
            },
            # Delay-restore SVI status          : Timer is off.(timeout = 10s)
            'vpc-delay-restore-svi-status': {
                'regexp': r'Delay-restore\sSVI\sstatus\s*?:\s(.+?)$',
                'expected_state': None
            },
            # Operational Layer3 Peer-router    : Disabled
            'operational-l3-peer': {
                'regexp': r'Operational\sLayer3\sPeer-router\s*?:\s(.+?)$',
                'expected_state': None
            }
        }

        result_dict = {}
        for line in out.splitlines():
            line = line.strip()
            for option, value in regexp_dict.items():
                p = re.compile(value['regexp'])
                m = p.match(line)
                if m:
                    if 'vpc' not in result_dict.keys():
                        result_dict['vpc'] = {}
                    if value['expected_state'] and value['expected_state'] == m.group(1):
                        result_dict['vpc'][option] = 'success'
                    elif value['expected_state']:
                        result_dict['vpc'][option] = 'failed'
                    else:
                        if str(m.group(1)).isdigit():
                            result_dict['vpc'][option] = int(m.group(1))
                        else:
                            result_dict['vpc'][option] = m.group(1)
                    break
        
        return result_dict
