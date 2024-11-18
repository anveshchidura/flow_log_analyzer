from collections import defaultdict
from typing import Dict, List, Tuple, DefaultDict
from .flow_parser import FlowLogParser
from .lookup_parser import LookupTableParser


class FlowAnalyzer:
    def __init__(self, flow_parser: FlowLogParser, lookup_parser: LookupTableParser):
        """Initialize analyzer with parsers."""
        self.flow_parser = flow_parser
        self.lookup_parser = lookup_parser
        self.tag_counts: DefaultDict[str, int] = defaultdict(int)
        self.port_proto_counts: DefaultDict[Tuple[str, str], int] = defaultdict(int)
        self.lookup_map: Dict[Tuple[str, str], str] = {}
        self.processed_flows = 0
        
    def _get_tag(self, dstport: str, protocol: str) -> str:
        """Get tag for given port/protocol combination."""
        key = (dstport, protocol)
        return self.lookup_map.get(key, 'untagged')
        
    def analyze(self) -> None:
        """Analyze flow logs and generate statistics."""
        self.lookup_map = self.lookup_parser.parse_lookup_table()
        
        for flow in self.flow_parser.parse_flows():
            dstport = flow['dstport']
            protocol = flow['protocol']
            
            key = (dstport, protocol)
            self.port_proto_counts[key] += 1
            
            tag = self._get_tag(dstport, protocol)
            self.tag_counts[tag] += 1
            
            self.processed_flows += 1
            
    def get_tag_counts(self) -> List[Tuple[str, int]]:
        """Get sorted tag counts."""
        return sorted(
            self.tag_counts.items(),
            key=lambda x: (-x[1], x[0])  
        )
        
    def get_port_protocol_counts(self) -> List[Tuple[Tuple[str, str], int]]:
        """Get sorted port/protocol counts."""
        return sorted(
            self.port_proto_counts.items(),
            key=lambda x: (int(x[0][0]), x[0][1])  
        )
        
    def get_statistics(self) -> Dict[str, int]:
        """Get summary statistics."""
        return {
            'total_flows': self.processed_flows,
            'tagged_flows': self.processed_flows - self.tag_counts.get('untagged', 0),
            'untagged_flows': self.tag_counts.get('untagged', 0),
            'unique_tags': len(self.tag_counts) - (1 if 'untagged' in self.tag_counts else 0)
        }


def create_analyzer(flow_parser: FlowLogParser, lookup_parser: LookupTableParser) -> FlowAnalyzer:
    """Factory function to create a FlowAnalyzer instance."""
    return FlowAnalyzer(flow_parser, lookup_parser)