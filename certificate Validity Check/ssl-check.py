import ssl
import socket
import argparse
from datetime import datetime
from tabulate import tabulate

# Function to get SSL certificate information
def get_certificate_info(hostname, port):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                if cert:
                    expiration_date = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
                    days_left = (expiration_date - datetime.utcnow()).days
                    return "Valid", expiration_date.strftime("%Y-%m-%d"), days_left
                else:
                    return "No Certificate", "N/A", "N/A"
    except ssl.SSLCertVerificationError:
        return "Invalid Certificate", "N/A", "N/A"
    except Exception as e:
        return f"Error: {str(e)}", "N/A", "N/A"

# Main function to check multiple websites
def check_ssl_certificates(sites):
    results = []
    for site in sites:
        hostname, port = site['hostname'], site['port']
        status, expires, days_left = get_certificate_info(hostname, port)
        results.append({
            "Website Name": hostname,
            "Status": status,
            "Expires": expires,
            "Days Left": days_left
        })
    return results

# Function to parse FQDN:port from user input or file
def parse_sites_from_input(input_list):
    sites = []
    for entry in input_list:
        try:
            hostname, port = entry.split(':')
            sites.append({"hostname": hostname, "port": int(port)})
        except ValueError:
            print(f"Invalid format for entry '{entry}'. Expected format is FQDN:port")
    return sites

# Main entry point for command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Check SSL certificate expiry for websites.")
    parser.add_argument("-w", "--website", help="Specify a single website with format FQDN:port (e.g., example.com:443)")
    parser.add_argument("-f", "--file", help="Specify a text file containing FQDN:port entries, one per line")
    args = parser.parse_args()

    sites = []

    # Parse website from -w flag
    if args.website:
        sites += parse_sites_from_input([args.website])

    # Parse websites from file provided by -f flag
    if args.file:
        try:
            with open(args.file, "r") as file:
                file_sites = [line.strip() for line in file.readlines()]
                sites += parse_sites_from_input(file_sites)
        except FileNotFoundError:
            print(f"File '{args.file}' not found.")
            return

    # Check if there are any sites to process
    if not sites:
        print("No valid sites provided. Use -w to specify a website or -f to specify a file.")
        return

    # Run the check and print the results in a table format
    ssl_results = check_ssl_certificates(sites)
    print(tabulate(ssl_results, headers="keys", tablefmt="pretty"))

if __name__ == "__main__":
    main()
