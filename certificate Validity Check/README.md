# SSL Check Script

This script checks the SSL certificate status of websites, reporting whether the certificate is valid or expired. It also provides the expiry date and the number of days left before expiration.

## Usage

### Single Website Check
To check the SSL certificate of a single website, save the script as `ssl_check.py` and run it from the command line with the following command:

```bash
python ssl_check.py -w example.com:443
```

Multiple Websites from a File
To check multiple websites from a file, use the -f option. The file should contain one Fully Qualified Domain Name (FQDN) with port per line:
```bash
python ssl_check.py -f websites.txt
```

The `websites.txt` file should have the following format
`example.com:443
expired.badssl.com:443
self-signed.badssl.com:443
`
Here is the example output
![image](https://github.com/user-attachments/assets/62687fb1-404e-403f-b5ff-cbe772dee8e4)

