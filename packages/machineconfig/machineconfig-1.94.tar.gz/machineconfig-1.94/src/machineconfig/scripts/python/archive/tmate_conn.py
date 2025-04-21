import argparse
import configparser
from pathlib import Path
import random
import string
import os


def get_conn_string(sess_name: str) -> str:
    creds = configparser.ConfigParser()
    creds.read(Path.home().joinpath('dotfiles/creds/tmate/creds.ini'))
    sess_name = creds['sessions_names'][sess_name]
    user_name = creds['keys']['username']
    return f"{user_name}/{sess_name}@sgp1.tmate.io"


def main():
    print(f"""
╔{'═' * 60}╗
║ 🔌 Tmate Connection Manager
╚{'═' * 60}╝
""")
    
    parser = argparse.ArgumentParser(description='Tmate launcher')
    parser.add_argument("sess_name", help="session name", default=random.choices(list(string.digits + string.ascii_letters), k=20))
    args = parser.parse_args()
    
    print(f"🔍 Looking up session: {args.sess_name}")
    conn_string = get_conn_string(args.sess_name)
    
    print(f"""
╭{'─' * 60}╮
│ 🔗 Connection String: ssh {conn_string}
╰{'─' * 60}╯
""")
    
    print("🚀 Connecting to tmate session...")
    os.system(f"ssh {conn_string}")
    
    print("✅ Connection closed")


if __name__ == '__main__':
    main()
