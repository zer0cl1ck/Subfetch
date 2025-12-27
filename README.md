# Subfetch

Subfetch is a Python-based subdomain enumeration tool designed to simplify the process of gathering subdomains from multiple sources. It integrates popular tools like Subfinder, Sublist3r, Findomain, and the Chaos API, and also fetches data from CRT.sh, allowing users to quickly discover valid subdomains for a given domain or a list of domains. The tool cleans and aggregates the results, removing duplicates, and saves them in an easy-to-read format. Subfetch was created to streamline reconnaissance for penetration testers, bug bounty hunters, and security enthusiasts, eliminating the need to run multiple tools individually and manually combine outputs. By providing a single unified interface, it helps users save time while ensuring comprehensive coverage across various subdomain sources. Its simplicity, efficiency, and integration with widely-used enumeration services make it an essential utility for anyone involved in web security research.

#Prerequisites

The following tools must be installed and available in your system PATH.

# Subfinder
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Sublist3r
sudo apt install sublist3r -y

# Findomain
wget https://github.com/Findomain/Findomain/releases/latest/download/findomain-linux -O /usr/local/bin/findomain
chmod +x /usr/local/bin/findomain

# Chaos CLI
go install github.com/projectdiscovery/chaos-client/cmd/chaos@latest

1. Set API key:
echo 'export CHAOS_API_KEY="your_api_key_here"' >> ~/.zshrc
source ~/.zshrc


#Usage


   Subdomain Enumeration Tool
   Developed by Keshav
=============================================

usage: subfetch.py [-h] [-d DOMAIN] [-f FILE]

Clean Subdomain Enumeration Tool

options:
  -h, --help           show this help message and exit
  -d, --domain DOMAIN  Single domain
  -f, --file FILE      File with domains




