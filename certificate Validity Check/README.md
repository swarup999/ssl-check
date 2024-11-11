# SSL Check Script

This script checks the SSL certificate status of websites, reporting whether the certificate is valid or expired. It also provides the expiry date and the number of days left before expiration.

## Usage
First Clone the repository 
```bash
git clone https://github.com/swarup999/ssl-check.git
```
Download all the dependencies form `requirements.txt` file 
```bash
pip install -r requirements.txt
```

### Single Website Check
To check the SSL certificate of a single website, save the script as `ssl_check.py` and run it from the command line with the following command:

```bash
python ssl-check.py -w example.com:443
```

Multiple Websites from a File
To check multiple websites from a file, use the -f option. The file should contain one Fully Qualified Domain Name (FQDN) with port per line:
```bash
python ssl-check.py -f websites.txt
```

The `websites.txt` file should have the following format
```bash
example.com:443
expired.badssl.com:443
self-signed.badssl.com:443
```
Here is the example output
```bash
+------------------------+---------------------+------------+-----------+
|      Website Name      |       Status        |  Expires   | Days Left |
+------------------------+---------------------+------------+-----------+
|      example.com       |        Valid        | 2025-03-01 |    110    |
|   expired.badssl.com   | Invalid Certificate |    N/A     |    N/A    |
| self-signed.badssl.com | Invalid Certificate |    N/A     |    N/A    |
+------------------------+---------------------+------------+-----------+
```

