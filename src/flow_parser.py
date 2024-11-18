from typing import Iterator, Dict, Optional
import os

class FlowLogParser:
    def __init__(self, filename: str):
        """Initialize parser with flow log filename."""
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Flow log file not found: {filename}")
            
        self.filename = filename
        
        
        self.FIELDS = {
            'version': 0,
            'account': 1,
            'interface': 2,
            'srcip': 3,
            'dstip': 4,
            'srcport': 5,
            'dstport': 6,
            'protocol': 7,
            'packets': 8,
            'bytes': 9,
            'start': 10,
            'end': 11,
            'action': 12,
            'status': 13
        }
        
        
        self.PROTOCOL_MAP = {
            '6': 'tcp',
            '17': 'udp',
            '1': 'icmp'
        }

    def _validate_port(self, port_str: str) -> Optional[str]:
        """Validate port number."""
        try:
            port = int(port_str)
            if 0 <= port <= 65535:
                return str(port)
        except ValueError:
            pass
        return None

    def _parse_line(self, line: str, line_num: int) -> Optional[Dict[str, str]]:
        """Parse a single flow log line."""
        try:
            # Enhanced whitespace handling - clean up all fields
            fields = [field.strip() for field in line.strip().split()]
            
            # Basic validation
            if len(fields) < 14:
                print(f"Warning: Line {line_num} - Insufficient fields")
                return None

            # Version 2 check
            if fields[self.FIELDS['version']] != '2':
                print(f"Warning: Line {line_num} - Unsupported version")
                return None

            # Get destination port and validate
            dstport = self._validate_port(fields[self.FIELDS['dstport']])
            if dstport is None:
                print(f"Warning: Line {line_num} - Invalid destination port")
                return None

            # Get protocol and convert to lowercase name
            protocol = self.PROTOCOL_MAP.get(fields[self.FIELDS['protocol']])
            if protocol is None:
                print(f"Warning: Line {line_num} - Unsupported protocol")
                return None

            # Get action and convert to lowercase
            action = fields[self.FIELDS['action']].lower()  
            if action not in {'accept', 'reject'}:  
                print(f"Warning: Line {line_num} - Invalid action")
                return None

            return {
                'dstport': dstport,
                'protocol': protocol,  
                'action': action,      
                'line_num': line_num
            }

        except Exception as e:
            print(f"Warning: Line {line_num} - Error: {str(e)}")
            return None

    def parse_flows(self) -> Iterator[Dict[str, str]]:
        """Parse flow log entries."""
        try:
            with open(self.filename, 'r', encoding='ascii') as f:
                for line_num, line in enumerate(f, 1):
                    if not line.strip() or line.startswith('#'):  
                        continue
                        
                    flow_data = self._parse_line(line, line_num)
                    if flow_data:
                        yield flow_data

        except UnicodeDecodeError:
            raise ValueError("Flow log file must be ASCII encoded")
        except Exception as e:
            raise RuntimeError(f"Error processing flow log file: {str(e)}")


def create_parser(filename: str) -> FlowLogParser:
    """Factory function to create a FlowLogParser instance."""
    return FlowLogParser(filename)