from collections import defaultdict

class Utils:

    # Method to get the protocol name based on the protocol number
    def get_protocol_name(protocol_number):
        iana_protocol_map = {
            1: 'ICMP',
            2: 'IGMP',
            6: 'TCP',
            17: 'UDP',
            41: 'IPv6 Encapsulation',
            50: 'ESP',
            51: 'AH',
            58: 'ICMPv6',
            89: 'OSPF',
            132: 'SCTP',
            136: 'UDPLite',
        }
        protocol_number = int(protocol_number)
        protocol_name = iana_protocol_map.get(protocol_number, 'Untagged')  
        return protocol_name

# Main class to handle flow log parsing and tagging
class FlowLogParser:
    def __init__(self, lookup_file, flow_log_file, output_file):
        self.lookup_file = lookup_file
        self.flow_log_file = flow_log_file
        self.output_file = output_file
        self.lookup_cache = {}
        self.port_protocol_counts = defaultdict(int)
        self.tag_counts = defaultdict(int)
        self.untagged_count = 0

    # Main method to load the lookup table, parse logs, and process them
    def parse(self):
        self.load_lookup_table()
        flow_logs = self.parse_flow_logs()
        self.process_logs(flow_logs)

    def load_lookup_table(self):
        with open(self.lookup_file, mode='r') as file:
            # Skip the header
            next(file)
            for row in file:
                # To remove any leading or trailing whitespaces and split the row by comma
                row = row.strip().split(",")
                if(len(row) == 3):
                    dstport, protocol, tag = row
                    print(dstport, protocol, tag)
                    self.lookup_cache[(int(dstport), protocol)] = tag
                else:
                    print("Invalid row in lookup table: ", row)

    # Parse the flow log file and extract relevant fields
    def parse_flow_logs(self):
        flow_logs = []
        with open(self.flow_log_file, mode='r') as file:
            for line in file:
                data = line.split()
                # Check to make sure we have all the required fields
                if len(data) >= 13: 
                    flow_logs.append({
                        'dst_port': int(data[5]),
                        'src_port': int(data[6]),
                        'protocol': Utils.get_protocol_name(data[7])
                    })
                else:
                    print("Invalid flow log entry: ", line)
        return flow_logs

    # Method to get the tag based on port and protocol from the lookup table
    def getTag(self, dst_port, protocol):
        tag = 'Untagged'
        for port, proto in self.lookup_cache:
            if dst_port == port and protocol.lower() == proto.lower():
                tag = self.lookup_cache[(port, proto)]
                break
        return tag

    def process_logs(self, flow_logs):
        for log in flow_logs:
            dst_port = log['dst_port']
            src_port = log['src_port']
            protocol = log['protocol']
            # Identify the tag for the port/protocol combination
            tag = self.getTag(dst_port, protocol)
            
            # Update the counts
            if tag == 'Untagged':
                self.untagged_count += 1
            else:
                self.tag_counts[tag] += 1

            # Update the port/protocol counts
            self.port_protocol_counts[(dst_port, protocol)] += 1
            # Considering the source port as well if needed, uncomment the below line
            #self.port_protocol_counts[(src_port, protocol)] += 1

    def generate_output_file(self):
        with open(self.output_file, mode='w') as file:
            file.write("Tag Counts:\n")
            file.write("Tag,Count\n")
            for tag, count in self.tag_counts.items():
                file.write(f"{tag},{count}\n")
            file.write(f"Untagged,{self.untagged_count}\n\n")
            
            file.write("Port/Protocol Combination Counts:\n")
            file.write("Port,Protocol,Count\n")
            for (port, protocol), count in self.port_protocol_counts.items():
                file.write(f"{port},{protocol},{count}\n")

if __name__ == "__main__":
    parser = FlowLogParser('lookup_table.csv', 'flow_logs.txt', 'output_results.txt')
    parser.parse()
    parser.generate_output_file()