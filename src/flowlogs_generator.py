import random
import time
import os
from datetime import datetime

class FlowLogsGenerator:
    def __init__(self):
       
        self.VERSION = 2 
        self.ACCOUNT_ID = "123456789012"  
        self.ACTIONS = ["ACCEPT", "REJECT"]
        self.LOG_STATUSES = ["OK", "FAILED"]
        self.PROTOCOLS = {
            "6": "tcp",   
            "17": "udp",  
            "1": "icmp"   
        }
        
    def generate_random_ip(self):
        """Generate a random IP address."""
        return ".".join(str(random.randint(0, 255)) for _ in range(4))
    
    def generate_eni_id(self):
        """Generate a random ENI ID."""
        chars = "abcdef0123456789"
        return f"eni-{''.join(random.choice(chars) for _ in range(8))}"
    
    def generate_log_entry(self):
        """Generate a single flow log entry."""
        current_time = int(time.time())
        start_time = current_time - random.randint(0, 3600)
        end_time = start_time + random.randint(1, 3600)
        
        protocol = random.choice(list(self.PROTOCOLS.keys()))
        dst_port = random.randint(1, 65535)
        src_port = random.randint(1, 65535)
        
        return f"{self.VERSION} {self.ACCOUNT_ID} {self.generate_eni_id()} " \
               f"{self.generate_random_ip()} {self.generate_random_ip()} " \
               f"{dst_port} {src_port} {protocol} " \
               f"{random.randint(1, 1000)} {random.randint(1000, 20000)} " \
               f"{start_time} {end_time} " \
               f"{random.choice(self.ACTIONS)} {random.choice(self.LOG_STATUSES)}"

def get_file_size_mb(file_path):
    """Get the size of a file in megabytes."""
    return os.path.getsize(file_path) / (1024 * 1024)

def generate_flow_logs(target_size_mb=20, output_file="flow_logs.txt"):
    """
    Generate flow logs until the file reaches approximately the target size in MB.
    
    Args:
        target_size_mb (int): Target file size in megabytes
        output_file (str): Output file name
    """
    generator = FlowLogsGenerator()
    batch_size = 10000  
    entries_generated = 0
    
    try:
        with open(output_file, 'w') as f:
            while True:
                
                for _ in range(batch_size):
                    log_entry = generator.generate_log_entry()
                    f.write(log_entry + '\n')
                    entries_generated += 1
                
                
                current_size_mb = get_file_size_mb(output_file)
                if current_size_mb >= target_size_mb:
                    break
                
                
                if entries_generated % 50000 == 0:
                    print(f"Generated {entries_generated} entries, current size: {current_size_mb:.2f}MB")
        
        final_size = get_file_size_mb(output_file)
        print(f"\nFinished generating flow logs:")
        print(f"Total entries: {entries_generated}")
        print(f"Final file size: {final_size:.2f}MB")
        print(f"Output file: {output_file}")
        
    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    # Generate approximately 20MB of flow logs
    generate_flow_logs(target_size_mb=20)