import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from src.flow_parser import create_parser as create_flow_parser
from src.lookup_parser import create_parser as create_lookup_parser
from src.analyzer import create_analyzer


def main() -> int:
    """Main entry point for the analyzer."""
    try:
        
        if len(sys.argv) != 3:
            print("Usage: python main.py <flow_log_file> <lookup_table_file>", file=sys.stderr)
            return 1

       
        flow_log_path = os.path.abspath(sys.argv[1])
        lookup_path = os.path.abspath(sys.argv[2])
        
        
        tag_output = os.path.join(current_dir, "tag_counts.csv")
        port_output = os.path.join(current_dir, "port_protocol_counts.csv")

        
        if not os.path.exists(flow_log_path):
            print(f"Flow log file not found: {flow_log_path}", file=sys.stderr)
            return 1
        if not os.path.exists(lookup_path):
            print(f"Lookup table file not found: {lookup_path}", file=sys.stderr)
            return 1

        # Create parsers and analyzer
        flow_parser = create_flow_parser(flow_log_path)
        lookup_parser = create_lookup_parser(lookup_path)
        analyzer = create_analyzer(flow_parser, lookup_parser)
        
        # Run analysis
        analyzer.analyze()
        
        # Write tag counts
        try:
            with open(tag_output, 'w', encoding='ascii') as f:
                f.write("Tag,Count\n")
                for tag, count in analyzer.get_tag_counts():
                    f.write(f"{tag},{count}\n")
        except Exception as e:
            print(f"Error writing tag counts: {str(e)}", file=sys.stderr)
            return 1

        # Write port/protocol counts
        try:
            with open(port_output, 'w', encoding='ascii') as f:
                f.write("Port,Protocol,Count\n")
                for (port, protocol), count in analyzer.get_port_protocol_counts():
                    f.write(f"{port},{protocol},{count}\n")
        except Exception as e:
            print(f"Error writing port/protocol counts: {str(e)}", file=sys.stderr)
            return 1

        print(f"Tag counts written to: {tag_output}")
        print(f"Port/protocol counts written to: {port_output}")
        return 0
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())