import argparse
from smtp_checker.smtp_utils import check_smtp_connection

def main():
    parser = argparse.ArgumentParser(description="SMTP Checker CLI")
    parser.add_argument("host", help="SMTP server hostname")
    parser.add_argument("port", type=int, help="SMTP port")
    parser.add_argument("--security", choices=["none", "ssl", "tls"], default="tls", help="Security type")
    parser.add_argument("--username", help="SMTP username")
    parser.add_argument("--password", help="SMTP password")
    parser.add_argument("--from_email", help="Sender email address")
    parser.add_argument("--to_email", help="Recipient email address")

    args = parser.parse_args()

    result = check_smtp_connection(
        args.host, args.port, args.security,
        args.username, args.password,
        args.from_email, args.to_email
    )
    print(result)

if __name__ == "__main__":
    main()
