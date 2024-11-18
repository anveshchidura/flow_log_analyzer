import csv
import os
from typing import Dict, Tuple, Set, Optional


class LookupTableParser:
    def __init__(self, filename: str):
        """Initialize with lookup table filename."""
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Lookup table file not found: {filename}")
            
        self.filename = filename
        self.unique_tags: Set[str] = set()

    def _validate_port(self, port_str: str) -> Optional[str]:
        """Validate port number."""
        try:
            port = int(port_str.strip())
            if 0 <= port <= 65535:
                return str(port)
        except ValueError:
            pass
        return None

    def _normalize_protocol(self, protocol: str) -> Optional[str]:
        """Normalize protocol string."""
        protocol = protocol.strip().lower()
        protocol_map = {
            'tcp': 'tcp',
            'udp': 'udp',
            'icmp': 'icmp',
            '6': 'tcp',
            '17': 'udp',
            '1': 'icmp'
        }
        return protocol_map.get(protocol)

    def _clean_row(self, row: Dict[str, str]) -> Dict[str, str]:
        """Clean whitespace from all fields in a row."""
        return {key: value.strip() if value else "" for key, value in row.items()}

    def parse_lookup_table(self) -> Dict[Tuple[str, str], str]:
        """Parse lookup table CSV file."""
        lookup_map: Dict[Tuple[str, str], str] = {}
        
        try:
            with open(self.filename, 'r', encoding='ascii') as f:
              
                csv_data = f.readlines()
                if not csv_data:
                    raise ValueError("Empty CSV file")
                
                
                headers = [h.strip().lower() for h in csv_data[0].split(',')]
                cleaned_data = [csv_data[0].strip()] + [line.strip() for line in csv_data[1:] if line.strip()]
                
                reader = csv.DictReader(cleaned_data, fieldnames=headers)
                next(reader)  
                
                required_fields = {'dstport', 'protocol', 'tag'}
                if not required_fields.issubset(set(headers)):
                    missing = required_fields - set(headers)
                    raise ValueError(f"Missing required columns: {', '.join(missing)}")
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        
                        clean_row = self._clean_row(row)
                        
                        
                        if not any(clean_row.values()):
                            continue
                        
                        
                        port = self._validate_port(clean_row['dstport'])
                        if port is None:
                            print(f"Warning: Row {row_num} - Invalid port number")
                            continue
                            
                        protocol = self._normalize_protocol(clean_row['protocol'])
                        if protocol is None:
                            print(f"Warning: Row {row_num} - Invalid protocol")
                            continue
                            
                        
                        tag = clean_row['tag'].lower()
                        if not tag:
                            print(f"Warning: Row {row_num} - Empty tag")
                            continue
                            
                        
                        key = (port, protocol)
                        lookup_map[key] = tag
                        self.unique_tags.add(tag)
                        
                    except Exception as e:
                        print(f"Warning: Error processing row {row_num}: {str(e)}")
                        continue
                        
        except UnicodeDecodeError:
            raise ValueError("Lookup table must be ASCII encoded")
        except Exception as e:
            raise RuntimeError(f"Error processing lookup table: {str(e)}")
            
        if not lookup_map:
            raise ValueError("No valid entries found in lookup table")
            
        return lookup_map

    def get_unique_tags(self) -> Set[str]:
        """Return set of unique tags (all lowercase)."""
        return self.unique_tags


def create_parser(filename: str) -> LookupTableParser:
    """Factory function to create a LookupTableParser instance."""
    return LookupTableParser(filename)