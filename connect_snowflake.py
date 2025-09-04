import argparse
import snowflake.connector

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--account", required=True, help="Snowflake account identifier (e.g. xy12345.us-east-1)")
    parser.add_argument("--user", required=True, help="Snowflake service user name")
    parser.add_argument("--token", required=True, help="OIDC ID token from GitHub Actions")
    args = parser.parse_args()

    # Connect using Workload Identity Federation (OIDC)
    conn = snowflake.connector.connect(
        account=args.account,
        #user=args.user,
        authenticator="WORKLOAD_IDENTITY",
        workload_identity_provider="OIDC",
        token=args.token,
    )

    cur = conn.cursor()
    cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT();")
    print("Connection successful →", cur.fetchall())
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
