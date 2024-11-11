import ssl
import socket
import smtplib
import argparse
from datetime import datetime
from email.mime.text import MIMEText
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
                    issuer = dict(x[0] for x in cert['issuer'])['commonName']
                    days_left = (expiration_date - datetime.utcnow()).days
                    return "Valid", expiration_date.strftime("%Y-%m-%d"), days_left, issuer
                else:
                    return "No Certificate", "N/A", "N/A", "N/A"
    except ssl.SSLCertVerificationError:
        return "Invalid Certificate", "N/A", "N/A", "N/A"
    except Exception as e:
        return f"Error: {str(e)}", "N/A", "N/A", "N/A"

# Function to check SSL certificates for multiple sites
def check_ssl_certificates(sites, email=None):
    results = []
    for site in sites:
        hostname, port = site['hostname'], site['port']
        status, expires, days_left, issuer = get_certificate_info(hostname, port)
        results.append({
            "Website Name": hostname,
            "Status": status,
            "Expires": expires,
            "Days Left": days_left,
            "Issuer": issuer
        })

        # Send an email if days_left is 7 or less and email is provided
        if email and isinstance(days_left, int) and days_left <= 7:
            send_expiration_notice(email, hostname, expires, days_left, issuer)

    return results

# Function to parse FQDN:port from input list
def parse_sites_from_input(input_list):
    sites = []
    for entry in input_list:
        try:
            hostname, port = entry.split(':')
            sites.append({"hostname": hostname, "port": int(port)})
        except ValueError:
            print(f"Invalid format for entry '{entry}'. Expected format is FQDN:port")
    return sites

# Function to send an email notification
def send_expiration_notice(email, hostname, expires, days_left, issuer):
    smtp_server = "smtp.example.com"  # Replace with your SMTP server
    smtp_port = 587                   # Replace with your SMTP server's port
    smtp_user = "your_email@example.com"  # Replace with your SMTP email
    smtp_password = "your_password"       # Replace with your SMTP password

    subject = f"SSL Certificate Expiration Notice for {hostname}"
    body = f"""
    Attention,

    The SSL certificate for {hostname} is set to expire in {days_left} days on {expires}.
    Issuer: {issuer}

    Please take necessary action to renew it before it expires.

    Regards,
    SSL Checker
    """
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, email, msg.as_string())
            print(f"Expiration notice sent to {email} for {hostname}.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Main function for command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Check SSL certificate expiry for websites.")
    parser.add_argument("-w", "--website", help="Specify a single website with format FQDN:port (e.g., example.com:443)")
    parser.add_argument("-f", "--file", help="Specify a text file containing FQDN:port entries, one per line")
    parser.add_argument("-e", "--email", help="Email address to send expiration notices if certificate expires within 7 days")
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
    ssl_results = check_ssl_certificates(sites, email=args.email)
    print(tabulate(ssl_results, headers="keys", tablefmt="pretty"))

if __name__ == "__main__":
    main()
