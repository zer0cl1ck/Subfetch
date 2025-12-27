#!/usr/bin/env python3

import argparse
import subprocess
import os
import sys
import re
import json
import urllib.request
import urllib.error

ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
DOMAIN_REGEX = re.compile(r'^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$')

CHAOS_API_KEY = os.getenv("CHAOS_API_KEY")

def banner():
    print("=" * 45)
    print("   Subdomain Enumeration Tool")
    print("   Developed by Keshav")
    print("=" * 45)
    print()

def tool_exists(tool):
    return subprocess.call(
        f"which {tool}",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ) == 0

def clean_output(text):
    text = ANSI_ESCAPE.sub('', text)
    results = set()

    for line in text.splitlines():
        line = line.strip().lower()
        if DOMAIN_REGEX.match(line):
            results.add(line)

    return results

def run_tool(cmd, tool_name, global_set):
    tool_binary = cmd.split()[0]

    if not tool_exists(tool_binary):
        print(f"[-] {tool_name}: not installed")
        return

    try:
        output = subprocess.check_output(
            cmd,
            shell=True,
            stderr=subprocess.DEVNULL,
            text=True
        )

        subs = clean_output(output)
        new = subs - global_set
        global_set.update(new)

        print(f"[+] {tool_name}: {len(subs)} found | Total: {len(global_set)}")

    except subprocess.CalledProcessError:
        print(f"[-] {tool_name}: error")

def run_crtsh(domain, global_set):
    print("[*] CRT.sh: querying certificates")

    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            raw = response.read().decode(errors="ignore")

        if not raw.startswith("["):
            print("[-] CRT.sh: no JSON data (blocked or empty)")
            return

        data = json.loads(raw)
        results = set()

        for entry in data:
            names = entry.get("name_value", "")
            for name in names.splitlines():
                name = name.strip().lower()
                if name.startswith("*."):
                    name = name[2:]
                if DOMAIN_REGEX.match(name):
                    results.add(name)

        if not results:
            print("[*] CRT.sh: no new subdomains")
            return

        new = results - global_set
        global_set.update(new)

        print(f"[+] CRT.sh: {len(results)} found | Total: {len(global_set)}")

    except (json.JSONDecodeError, urllib.error.HTTPError,
            urllib.error.URLError, TimeoutError):
        print("[-] CRT.sh: unavailable (rate-limited or blocked)")
    except Exception:
        print("[-] CRT.sh: unexpected error")

def enumerate_domain(domain, global_set):
    print(f"\n[>] Enumerating: {domain}\n")

    run_tool(f"subfinder -silent -d {domain}", "Subfinder", global_set)
    run_tool(f"sublist3r -d {domain} -n -o -", "Sublist3r", global_set)
    run_tool(f"findomain -t {domain} -q", "Findomain", global_set)

    if CHAOS_API_KEY:
        run_tool(
            f"chaos -d {domain} -key {CHAOS_API_KEY} -silent",
            "Chaos",
            global_set
        )
    else:
        print("[-] Chaos: API key not set (export CHAOS_API_KEY)")

    run_crtsh(domain, global_set)

def main():
    banner()

    parser = argparse.ArgumentParser(description="Clean Subdomain Enumeration Tool")
    parser.add_argument("-d", "--domain", help="Single domain")
    parser.add_argument("-f", "--file", help="File with domains")

    args = parser.parse_args()

    if not args.domain and not args.file:
        parser.print_help()
        sys.exit(1)

    domains = []

    if args.domain:
        domains.append(args.domain)

    if args.file:
        if not os.path.exists(args.file):
            print("File not found.")
            sys.exit(1)
        with open(args.file) as f:
            domains.extend(line.strip() for line in f if line.strip())

    all_subdomains = set()

    for domain in domains:
        enumerate_domain(domain, all_subdomains)

    with open("subdomains.txt", "w") as f:
        for sub in sorted(all_subdomains):
            f.write(sub + "\n")

    print(f"\n[✓] Enumeration completed")
    print(f"[✓] Total unique subdomains: {len(all_subdomains)}")
    print(f"[✓] Saved to subdomains.txt\n")

    for sub in sorted(all_subdomains):
        print(sub)

if __name__ == "__main__":
    main()
