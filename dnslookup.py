import dns.resolver

def dns_lookup(domain_name, record_types=['A']):
    resolver = dns.resolver.Resolver()
    results = {}
    
    try:
        for record_type in record_types:
            answers = resolver.resolve(domain_name, record_type)
            if record_type == 'MX':
                results['MX'] = [(rdata.preference, rdata.exchange.to_text()) for rdata in answers]
            elif record_type == 'AAAA' or record_type == 'A':
                results[record_type] = [rdata.address for rdata in answers]
            elif record_type == 'TXT':
                results['TXT'] = [rdata.strings for rdata in answers]
            elif record_type == 'CNAME' or record_type == 'NS' or record_type == 'PTR':
                results[record_type] = [rdata.to_text() for rdata in answers]
            elif record_type == 'SRV':
                results['SRV'] = [(rdata.priority, rdata.weight, rdata.port, rdata.target.to_text()) for rdata in answers]
        return results
    except dns.resolver.NoAnswer:
        return f"No {', '.join(record_types)} records found for {domain_name}"
    except dns.resolver.NXDOMAIN:
        return f"{domain_name} does not exist"
    except dns.exception.Timeout:
        return "DNS query timed out"

if __name__ == "__main__":
    print("Record type commands:")
    print("- A (IPv4 address)")
    print("- AAAA (IPv6 address)")
    print("- MX (Mail Exchange)")
    print("- TXT (Text)")
    print("- CNAME (Canonical Name)")
    print("- NS (Name Server)")
    print("- PTR (Pointer)")
    print("- SRV (Service)")

    user_input = input("Enter the domain name followed by optional record type commands (e.g., google.com -txt -A): ").strip()

    input_parts = user_input.split()
    domain_name = input_parts[0]

    record_type_commands = [part.upper() for part in input_parts[1:]]

    record_types = ['A'] if not record_type_commands else []

    for command in record_type_commands:
        if command in ['-A', '-AAAA', '-MX', '-TXT', '-CNAME', '-NS', '-PTR', '-SRV']:
            record_types.append(command[1:])

    result = dns_lookup(domain_name, record_types)

    if isinstance(result, dict):
        for record_type, records in result.items():
            if record_type == 'MX':
                print("MX records:")
                for preference, exchange in records:
                    print(f"Preference {preference}: {exchange}")
            elif record_type == 'SRV':
                print("SRV records:")
                for priority, weight, port, target in records:
                    print(f"Priority: {priority}, Weight: {weight}, Port: {port}, Target: {target}")
            else:
                print(f"{record_type} records:")
                for item in records:
                    print(item)
    else:
        print(result)

