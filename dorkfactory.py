#!/usr/bin/env python3
import os
import sys
import argparse
import platform
from enum import Enum
from typing import List, Dict, Set, Optional

try:
    from colorama import init, Fore, Back, Style, just_fix_windows_console
    init(autoreset=True)
    if platform.system() == "Windows":
        just_fix_windows_console()
    COLORS_ENABLED = True
except ImportError:
    class Fore:
        BLACK = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Back:
        BLACK = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ""
    COLORS_ENABLED = False

class SearchEngine(Enum):
    GOOGLE = "google"
    YANDEX = "yandex"
    BOTH = "both"

class Category(Enum):
    PANELS_AUTH = "Panels & Auth"
    SENSITIVE_FILES = "Sensitive Files"
    ERRORS_DEBUG = "Errors & Debug"
    APIS_ENDPOINTS = "APIs & Endpoints"
    OSINT = "OSINT"
    VULNERABILITIES = "Vulnerabilities"
    BACKUPS = "Backups & Logs"
    CONFIG_FILES = "Configuration Files"
    DIRECTORIES = "Directory Listings"
    DATABASE = "Database Dumps"

class Profile(Enum):
    BUGBOUNTY = "bugbounty"
    OSINT_COMPANY = "osint-company"
    CTF = "ctf"
    WEBAPP_BASIC = "webapp-basic"
    FULL_SCOPE = "full-scope"

class DorkFactory:
    def __init__(self):
        self.targets = []
        self.exclusions = []
        self.engine = SearchEngine.GOOGLE
        self.categories = set()
        self.advanced_options = {
            'exclude_subdomains': False,
            'strict_queries': False,
            'reduce_noise': False,
            'disable_colors': False,
            'no_banner': False
        }
        self.profile = None
        self.silent = False
        self.export_path = None
        
        self.dork_templates = {
            Category.PANELS_AUTH: [
                "site:{target} intitle:\"login\" | \"admin\" | \"dashboard\"",
                "site:{target} inurl:login | admin | wp-admin | administrator",
                "site:{target} \"index of /admin\"",
                "site:{target} \"admin panel\" | \"control panel\"",
                "site:{target} filetype:php inurl:login"
            ],
            Category.SENSITIVE_FILES: [
                "site:{target} ext:env | ext:yml | ext:yaml | ext:config",
                "site:{target} \"SECRET_KEY\" | \"API_KEY\" | \"PASSWORD\"",
                "site:{target} filetype:sql | filetype:db | filetype:mdb",
                "site:{target} \"robots.txt\" \"disallow:\"",
                "site:{target} \"phpinfo()\" \"PHP Version\""
            ],
            Category.ERRORS_DEBUG: [
                "site:{target} \"error\" | \"exception\" | \"stack trace\"",
                "site:{target} \"debug\" | \"testing\" | \"staging\"",
                "site:{target} \"internal server error\" | \"500 error\"",
                "site:{target} \"syntax error\" | \"mysql_fetch\""
            ],
            Category.APIS_ENDPOINTS: [
                "site:{target} inurl:api | endpoint | graphql | rest",
                "site:{target} \"swagger\" | \"openapi\" | \"postman\"",
                "site:{target} \"api/v1\" | \"api/v2\" | \"v1/api\"",
                "site:{target} filetype:json | filetype:xml inurl:api"
            ],
            Category.OSINT: [
                "site:{target} \"@example.com\" | \"contact\" | \"about\"",
                "site:{target} filetype:pdf | filetype:doc | filetype:docx",
                "site:{target} \"employee\" | \"team\" | \"careers\"",
                "site:{target} \"confidential\" | \"internal\" | \"private\""
            ],
            Category.VULNERABILITIES: [
                "site:{target} \"wp-content\" \"vulnerable\"",
                "site:{target} \"sql injection\" | \"xss\" | \"csrf\"",
                "site:{target} \"cve-\" | \"security update\"",
                "site:{target} \"unauthorized access\" | \"breach\""
            ],
            Category.BACKUPS: [
                "site:{target} ext:bak | ext:old | ext:backup",
                "site:{target} \"backup\" | \"dump\" | \"archive\"",
                "site:{target} \"*.tar.gz\" | \"*.zip\" | \"*.rar\"",
                "site:{target} \"database backup\" | \"db dump\""
            ],
            Category.CONFIG_FILES: [
                "site:{target} filetype:ini | filetype:cfg | filetype:conf",
                "site:{target} \".git/config\" | \".env.example\"",
                "site:{target} \"config.php\" | \"settings.py\"",
                "site:{target} \"docker-compose.yml\" | \"dockerfile\""
            ],
            Category.DIRECTORIES: [
                "site:{target} \"index of /\" \"parent directory\"",
                "site:{target} intitle:\"index of\"",
                "site:{target} \"directory listing\"",
                "site:{target} inurl:/uploads/ | /files/ | /assets/"
            ],
            Category.DATABASE: [
                "site:{target} \"mysql dump\" | \"pg_dump\"",
                "site:{target} \"db.sql\" | \"database.sql\"",
                "site:{target} \"INSERT INTO\" | \"CREATE TABLE\"",
                "site:{target} filetype:sql \"-- Dump\""
            ]
        }
        
        self.profile_configs = {
            Profile.BUGBOUNTY: {
                'engines': [SearchEngine.GOOGLE, SearchEngine.YANDEX],
                'categories': [
                    Category.PANELS_AUTH,
                    Category.SENSITIVE_FILES,
                    Category.APIS_ENDPOINTS,
                    Category.VULNERABILITIES,
                    Category.CONFIG_FILES
                ],
                'strict_queries': True,
                'reduce_noise': True
            },
            Profile.OSINT_COMPANY: {
                'engines': [SearchEngine.GOOGLE],
                'categories': [
                    Category.OSINT,
                    Category.SENSITIVE_FILES,
                    Category.APIS_ENDPOINTS
                ],
                'strict_queries': False,
                'reduce_noise': False
            },
            Profile.CTF: {
                'engines': [SearchEngine.GOOGLE],
                'categories': [
                    Category.PANELS_AUTH,
                    Category.SENSITIVE_FILES,
                    Category.BACKUPS,
                    Category.CONFIG_FILES,
                    Category.DIRECTORIES
                ],
                'strict_queries': True,
                'reduce_noise': False
            },
            Profile.WEBAPP_BASIC: {
                'engines': [SearchEngine.GOOGLE],
                'categories': [
                    Category.PANELS_AUTH,
                    Category.SENSITIVE_FILES,
                    Category.ERRORS_DEBUG
                ],
                'strict_queries': False,
                'reduce_noise': False
            },
            Profile.FULL_SCOPE: {
                'engines': [SearchEngine.GOOGLE, SearchEngine.YANDEX],
                'categories': list(Category),
                'strict_queries': False,
                'reduce_noise': False
            }
        }

    def clear_screen(self):
        os.system('cls' if platform.system() == 'Windows' else 'clear')

    def print_banner(self):
        if self.advanced_options['no_banner'] or self.silent:
            return
            
        banner_lines = [
            "⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
            "⠀⠀⠀⢀⣴⣾⣦⣀⣀⣠⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
            "⠀⠀⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
            "⠀⠀⠀⢀⣾⣿⡿⠋⠁⠈⠙⢿⣿⣷⣶⣶⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
            "⠀⢸⣿⣿⣿⣿⡇⠀⠀⠀⠀⢸⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
            "⠀⠘⠛⠛⠻⣿⣷⣤⣀⣀⣴⣿⣿⠏⢀⣀⠀⠀⠀⠀⣾⣿⣿⡇⠀⠀⠀⠀⣀⠀",
            "⠀⠀⠀⠀⠀⣾⣿⣿⡿⠿⢿⣿⣿⣷⣿⣿⣧⠀⣀⣀⣿⣿⣿⣇⣀⡀⠀⣼⣿⠀",
            "⠀⠀⠀⠀⠸⠿⣿⡿⠀⠀⠀⠻⠿⠋⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀ 88888888ba,                          88",
            "⠀⠀⠀⠀⠀⠀⠀⠁⢀⣴⣤⣀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀ 88      `\"8b                         88",
            "⠀⠀⠀⠀⠀⠀⠀⠀⠺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀ 88        `8b                        88",
            "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⣿⣿⣿⣿⣿⠀ 88         88  ,adPPYba,  8b,dPPYba, 88   ,d8",
            "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀ ⠈⢻⣿⣿⣿⠀ 88         88 a8\"     \"8a 88P'   \"Y8 88 ,a8\"",
            "⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀ ⣿⣿⣿⠀ 88         8P 8b       d8 88         8888[",
            "⠀⠀⠀⠀⠀⠀⠘⠛⠛⠻⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⠀ 88      .a8P  \"8a,   ,a8\" 88         88`\"Yba,",
            "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠛⠛⠛⠛⠛⠛⠛⠛⠂⠀⠀⠀⠀⠒⠛⠛⠛⠛⠀ 88888888Y\"'    `\"YbbdP\"'  88         88   `Y8a",
            "",
            "   88888888888",
            "   88                              ,d",
            "   88                              88",
            "   88aaaaa ,adPPYYba,  ,adPPYba, MM88MMM ,adPPYba,  8b,dPPYba, 8b       d8",
            "   88\"\"\"\"\" \"\"     `Y8 a8\"     \"\"   88   a8\"     \"8a 88P'   \"Y8 `8b     d8'",
            "   88      ,adPPPPP88 8b           88   8b       d8 88          `8b   d8'",
            "   88      88,    ,88 \"8a,   ,aa   88,  \"8a,   ,a8\" 88           `8b,d8'",
            "   88      `\"8bbdP\"Y8  `\"Ybbd8\"'   \"Y888 `\"YbbdP\"'  88             Y88'",
            "                                                                   d8'",
            f"       {Fore.YELLOW}By URDev | https://github.com/urdev4ever | v2.6{Fore.CYAN}            d8'{Style.RESET_ALL}"
        ]
        
        for line in banner_lines:
            print(f"{Fore.CYAN}{line}{Style.RESET_ALL}")

    def print_main_menu(self):
        """Print the exact main menu with colors"""
        print(f"{Fore.CYAN}{Style.BRIGHT}╔═══════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}{Style.BRIGHT}║                          D O R K   F A C T O R Y                          ║")
        print(f"{Fore.CYAN}{Style.BRIGHT}╠═══════════════════════════════════════════════════════════════════════════╣")
        print(f"{Fore.CYAN}{Style.BRIGHT}║{Style.RESET_ALL}   Passive Recon Query Generator By URDev                                  {Fore.CYAN}{Style.BRIGHT}║")
        print(f"{Fore.CYAN}{Style.BRIGHT}║{Style.RESET_ALL}                                                                           {Fore.CYAN}{Style.BRIGHT}║")
        print(f"{Fore.CYAN}{Style.BRIGHT}║{Style.RESET_ALL}   {Fore.YELLOW}[1]{Style.RESET_ALL} Set Target                                                          {Fore.CYAN}{Style.BRIGHT}║")
        print(f"{Fore.CYAN}{Style.BRIGHT}║{Style.RESET_ALL}   {Fore.YELLOW}[2]{Style.RESET_ALL} Select Search Engine                                                {Fore.CYAN}{Style.BRIGHT}║")
        print(f"{Fore.CYAN}{Style.BRIGHT}║{Style.RESET_ALL}   {Fore.YELLOW}[3]{Style.RESET_ALL} Select Recon Categories                                             {Fore.CYAN}{Style.BRIGHT}║")
        print(f"{Fore.CYAN}{Style.BRIGHT}║{Style.RESET_ALL}   {Fore.YELLOW}[4]{Style.RESET_ALL} Use Profile                                                         {Fore.CYAN}{Style.BRIGHT}║")
        print(f"{Fore.CYAN}{Style.BRIGHT}║{Style.RESET_ALL}   {Fore.YELLOW}[5]{Style.RESET_ALL} Advanced Options                                                    {Fore.CYAN}{Style.BRIGHT}║")
        print(f"{Fore.CYAN}{Style.BRIGHT}║{Style.RESET_ALL}   {Fore.YELLOW}[6]{Style.RESET_ALL} Generate Dorks                                                      {Fore.CYAN}{Style.BRIGHT}║")
        print(f"{Fore.CYAN}{Style.BRIGHT}║{Style.RESET_ALL}   {Fore.YELLOW}[7]{Style.RESET_ALL} Show Current Configuration                                          {Fore.CYAN}{Style.BRIGHT}║")
        print(f"{Fore.CYAN}{Style.BRIGHT}║{Style.RESET_ALL}                                                                           {Fore.CYAN}{Style.BRIGHT}║")
        print(f"{Fore.CYAN}{Style.BRIGHT}║{Style.RESET_ALL}   {Fore.YELLOW}[H]{Style.RESET_ALL} Help        {Fore.YELLOW}[Q]{Style.RESET_ALL} Quit                                                {Fore.CYAN}{Style.BRIGHT}║")
        print(f"{Fore.CYAN}{Style.BRIGHT}║{Style.RESET_ALL}                                                                           {Fore.CYAN}{Style.BRIGHT}║")
        print(f"{Fore.CYAN}{Style.BRIGHT}╚═══════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")

    def print_header(self, title: str):
        if self.silent:
            return
            
        width = 77
        print(f"{Fore.CYAN}{Style.BRIGHT}╔{'═' * (width - 2)}╗")
        print(f"{Fore.CYAN}{Style.BRIGHT}║{title.center(width - 2)}║")
        print(f"{Fore.CYAN}{Style.BRIGHT}╚{'═' * (width - 2)}╝{Style.RESET_ALL}")

    def print_menu(self, title: str, options: List[str], selected: Set[int] = None):
        if selected is None:
            selected = set()
            
        self.print_header(title)
        print()
        
        for i, option in enumerate(options, 1):
            prefix = f"{Fore.GREEN}[✓]{Style.RESET_ALL}" if i in selected else "[ ]"
            print(f"  {Fore.YELLOW}[{i}]{Style.RESET_ALL} {prefix} {option}")
        print()

    def get_input(self, prompt: str, default: str = "") -> str:
        if self.silent:
            return default
            
        prompt_text = f"{Fore.GREEN}{prompt}{Style.RESET_ALL}"
        if default:
            prompt_text += f" [{default}]"
        prompt_text += f"\n{Fore.CYAN}>{Style.RESET_ALL} "
        
        try:
            user_input = input(prompt_text).strip()
            return user_input if user_input else default
        except (KeyboardInterrupt, EOFError):
            print(f"\n{Fore.RED}Exiting...{Style.RESET_ALL}")
            sys.exit(0)

    def get_multi_input(self, prompt: str) -> List[str]:
        if self.silent:
            return []
            
        print(f"{Fore.GREEN}{prompt}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}(Press Enter on empty line to finish){Style.RESET_ALL}")
        
        inputs = []
        i = 1
        while True:
            try:
                user_input = input(f"{Fore.CYAN}[{i}]>{Style.RESET_ALL} ").strip()
                if not user_input:
                    break
                inputs.append(user_input)
                i += 1
            except (KeyboardInterrupt, EOFError):
                print(f"\n{Fore.RED}Exiting...{Style.RESET_ALL}")
                sys.exit(0)
        return inputs

    def set_targets_interactive(self):
        self.clear_screen()
        self.print_header("Set Target(s)")
        print(f"{Fore.YELLOW}Enter target domains (supports wildcards like *.example.com):{Style.RESET_ALL}")
        print()
        
        self.targets = self.get_multi_input("Enter target domain(s):")
        
        if not self.targets:
            print(f"{Fore.RED}No targets specified!{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            return False
            
        print()
        exclusions_input = self.get_input("Enter domains to exclude (comma-separated, optional):")
        if exclusions_input:
            self.exclusions = [x.strip() for x in exclusions_input.split(',')]
            
        return True

    def select_engine_interactive(self):
        self.clear_screen()
        engines = ["Google", "Yandex", "Both"]
        self.print_menu("Select Search Engine", engines)
        
        while True:
            choice = self.get_input("Select engine (1-3):")
            try:
                choice_int = int(choice)
                if 1 <= choice_int <= 3:
                    if choice_int == 1:
                        self.engine = SearchEngine.GOOGLE
                    elif choice_int == 2:
                        self.engine = SearchEngine.YANDEX
                    else:
                        self.engine = SearchEngine.BOTH
                    return True
            except ValueError:
                pass
            print(f"{Fore.RED}Invalid choice! Please enter 1, 2, or 3.{Style.RESET_ALL}")

    def select_categories_interactive(self):
        self.clear_screen()
        categories = [cat.value for cat in Category]
        selected = set()
        
        while True:
            self.clear_screen()
            self.print_menu("Select Recon Categories", categories, selected)
            print(f"{Fore.YELLOW}Enter numbers to toggle selection (comma-separated){Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Enter 'all' to select all, 'none' to clear, 'done' to finish{Style.RESET_ALL}")
            
            choice = self.get_input("Your choice:").lower()
            
            if choice == 'done':
                if selected:
                    self.categories = {list(Category)[i-1] for i in selected}
                    return True
                else:
                    print(f"{Fore.RED}Please select at least one category!{Style.RESET_ALL}")
                    input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            elif choice == 'all':
                selected = set(range(1, len(categories) + 1))
            elif choice == 'none':
                selected = set()
            else:
                try:
                    numbers = [int(x.strip()) for x in choice.split(',')]
                    valid_numbers = [n for n in numbers if 1 <= n <= len(categories)]
                    
                    for num in valid_numbers:
                        if num in selected:
                            selected.remove(num)
                        else:
                            selected.add(num)
                except ValueError:
                    print(f"{Fore.RED}Invalid input!{Style.RESET_ALL}")
                    input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

    def select_profile_interactive(self):
        self.clear_screen()
        profiles = [
            "Bug Bounty (comprehensive)",
            "OSINT Company (focused)",
            "CTF (challenge-oriented)",
            "Web App Basic (lightweight)",
            "Full Scope (all categories)",
            "Custom (manual selection)"
        ]
        
        self.print_menu("Use Profile", profiles)
        
        while True:
            choice = self.get_input("Select profile (1-6, Enter to skip):")
            if not choice:
                return True
                
            try:
                choice_int = int(choice)
                if 1 <= choice_int <= 6:
                    if choice_int == 1:
                        self.profile = Profile.BUGBOUNTY
                    elif choice_int == 2:
                        self.profile = Profile.OSINT_COMPANY
                    elif choice_int == 3:
                        self.profile = Profile.CTF
                    elif choice_int == 4:
                        self.profile = Profile.WEBAPP_BASIC
                    elif choice_int == 5:
                        self.profile = Profile.FULL_SCOPE
                    else:
                        self.profile = None
                        return True
                        
                    config = self.profile_configs[self.profile]
                    self.categories = set(config['categories'])
                    if len(config['engines']) == 1:
                        self.engine = config['engines'][0]
                    else:
                        self.engine = SearchEngine.BOTH
                    self.advanced_options['strict_queries'] = config['strict_queries']
                    self.advanced_options['reduce_noise'] = config['reduce_noise']
                    
                    print(f"{Fore.GREEN}Profile '{self.profile.value}' applied!{Style.RESET_ALL}")
                    input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    return True
            except ValueError:
                pass
            print(f"{Fore.RED}Invalid choice! Please enter 1-6.{Style.RESET_ALL}")

    def advanced_options_interactive(self):
        self.clear_screen()
        options = [
            "Exclude subdomains",
            "Strict queries (more precise)",
            "Reduce noise (filter common results)",
            "Disable colors",
            "No banner"
        ]
        
        selected = set()
        for i, opt in enumerate(options, 1):
            key = opt.lower().replace(' ', '_').replace('(', '').replace(')', '')
            if key in self.advanced_options and self.advanced_options[key]:
                selected.add(i)
        
        while True:
            self.clear_screen()
            self.print_menu("Advanced Options", options, selected)
            print(f"{Fore.YELLOW}Toggle options with numbers (comma-separated), 'done' to finish{Style.RESET_ALL}")
            
            choice = self.get_input("Your choice:").lower()
            
            if choice == 'done':
                self.advanced_options['exclude_subdomains'] = 1 in selected
                self.advanced_options['strict_queries'] = 2 in selected
                self.advanced_options['reduce_noise'] = 3 in selected
                self.advanced_options['disable_colors'] = 4 in selected
                self.advanced_options['no_banner'] = 5 in selected
                
                if self.advanced_options['disable_colors']:
                    global COLORS_ENABLED
                    COLORS_ENABLED = False
                    
                return True
            else:
                try:
                    numbers = [int(x.strip()) for x in choice.split(',')]
                    valid_numbers = [n for n in numbers if 1 <= n <= len(options)]
                    
                    for num in valid_numbers:
                        if num in selected:
                            selected.remove(num)
                        else:
                            selected.add(num)
                except ValueError:
                    print(f"{Fore.RED}Invalid input!{Style.RESET_ALL}")
                    input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

    def show_status(self):
        self.clear_screen()
        self.print_header("Current Configuration")
        print()
        
        print(f"{Fore.YELLOW}Targets:{Style.RESET_ALL}")
        for target in self.targets:
            print(f"  {Fore.GREEN}•{Style.RESET_ALL} {target}")
        if self.exclusions:
            print(f"{Fore.YELLOW}Exclusions:{Style.RESET_ALL}")
            for excl in self.exclusions:
                print(f"  {Fore.RED}•{Style.RESET_ALL} {excl}")
        print()
        
        print(f"{Fore.YELLOW}Search Engine:{Style.RESET_ALL} {Fore.CYAN}{self.engine.value}{Style.RESET_ALL}")
        print()
        
        print(f"{Fore.YELLOW}Categories:{Style.RESET_ALL}")
        for cat in self.categories:
            print(f"  {Fore.GREEN}✓{Style.RESET_ALL} {cat.value}")
        print()
        
        if self.profile:
            print(f"{Fore.YELLOW}Profile:{Style.RESET_ALL} {Fore.MAGENTA}{self.profile.value}{Style.RESET_ALL}")
            print()
            
        print(f"{Fore.YELLOW}Advanced Options:{Style.RESET_ALL}")
        for key, value in self.advanced_options.items():
            status = f"{Fore.GREEN}ON{Style.RESET_ALL}" if value else f"{Fore.RED}OFF{Style.RESET_ALL}"
            print(f"  {key.replace('_', ' ').title()}: {status}")
        print()

    def generate_dorks(self) -> Dict[Category, List[str]]:
        all_dorks = {}
        
        for category in self.categories:
            category_dorks = []
            templates = self.dork_templates.get(category, [])
            
            for template in templates:
                for target in self.targets:
                    if self.exclusions and any(excl in target for excl in self.exclusions):
                        continue
                        
                    dork = template
                    if self.advanced_options['exclude_subdomains']:
                        dork = dork.replace('site:{target}', f'site:{target} -site:*.{target}')
                    else:
                        dork = dork.replace('{target}', target)
                    
                    if self.advanced_options['strict_queries']:
                        dork = f'"{dork}"'
                        
                    if self.advanced_options['reduce_noise']:
                        noise_terms = ['-forum', '-blog', '-news', '-articles']
                        dork += ' ' + ' '.join(noise_terms)
                    
                    category_dorks.append(dork)
            
            if category_dorks:
                all_dorks[category] = category_dorks
        
        return all_dorks

    def format_dork_url(self, dork: str, engine: SearchEngine) -> str:
        if engine == SearchEngine.GOOGLE:
            base_url = "https://www.google.com/search"
            params = {"q": dork, "hl": "en"}
        elif engine == SearchEngine.YANDEX:
            base_url = "https://yandex.com/search"
            params = {"text": dork, "lr": "10267"}
        else:
            return ""
            
        param_str = '&'.join([f"{k}={v}" for k, v in params.items()])
        return f"{base_url}?{param_str}"

    def display_results(self, dorks: Dict[Category, List[str]]):
        self.clear_screen()
        
        if not self.advanced_options['no_banner']:
            self.print_banner()
            
        self.print_header("Generated Dorks")
        print()
        
        if not dorks:
            print(f"{Fore.RED}No dorks generated! Please check your configuration.{Style.RESET_ALL}")
            return
            
        engines_to_show = []
        if self.engine == SearchEngine.BOTH:
            engines_to_show = [SearchEngine.GOOGLE, SearchEngine.YANDEX]
        else:
            engines_to_show = [self.engine]
        
        for category, category_dorks in dorks.items():
            if not category_dorks:
                continue
                
            category_name = category.value
            width = 60
            print(f"{Fore.MAGENTA}{Style.BRIGHT}╔{'═' * (width - 2)}╗")
            print(f"{Fore.MAGENTA}{Style.BRIGHT}║{category_name.center(width - 2)}║")
            print(f"{Fore.MAGENTA}{Style.BRIGHT}╚{'═' * (width - 2)}╝{Style.RESET_ALL}")
            print()
            
            for i, dork in enumerate(category_dorks[:20], 1):
                dork_num = f"[{i:02d}]"
                print(f"{Fore.YELLOW}{dork_num}{Style.RESET_ALL} {dork}")
                
                for engine in engines_to_show:
                    url = self.format_dork_url(dork, engine)
                    if url:
                        engine_name = engine.value.title()
                        print(f"{Fore.CYAN}     ↳ {engine_name}: {url}{Style.RESET_ALL}")
                print()
            
            if len(category_dorks) > 20:
                print(f"{Fore.YELLOW}... and {len(category_dorks) - 20} more dorks{Style.RESET_ALL}")
                print()
        
        total_dorks = sum(len(d) for d in dorks.values())
        print(f"{Fore.GREEN}{Style.BRIGHT}✓ Generated {total_dorks} dorks across {len(dorks)} categories{Style.RESET_ALL}")
        print()
        
        if not self.silent:
            export_choice = self.get_input("Export to file? (y/N):").lower()
            if export_choice == 'y':
                filename = self.get_input("Filename (default: dorks.txt):", "dorks.txt")
                self.export_dorks(dorks, filename)

    def export_dorks(self, dorks: Dict[Category, List[str]], filename: str):
        try:
            with open(filename, 'w') as f:
                f.write("# Dork Factory Export\n")
                f.write(f"# Targets: {', '.join(self.targets)}\n")
                f.write(f"# Engine: {self.engine.value}\n")
                f.write(f"# Profile: {self.profile.value if self.profile else 'Custom'}\n")
                f.write("#\n\n")
                
                for category, category_dorks in dorks.items():
                    f.write(f"## {category.value}\n")
                    for dork in category_dorks:
                        f.write(f"{dork}\n")
                        for engine in ([SearchEngine.GOOGLE, SearchEngine.YANDEX] 
                                     if self.engine == SearchEngine.BOTH else [self.engine]):
                            url = self.format_dork_url(dork, engine)
                            if url:
                                f.write(f"# {engine.value}: {url}\n")
                    f.write("\n")
                    
            print(f"{Fore.GREEN}Dorks exported to {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error exporting: {e}{Style.RESET_ALL}")

    def main_menu(self):
        while True:
            self.clear_screen()
            if not self.advanced_options['no_banner']:
                self.print_banner()
            
            # Print the exact menu
            self.print_main_menu()
            
            # Add status indicators below the menu if configured
            print()
            if self.targets:
                print(f"{Fore.GREEN}✓ Targets:{Style.RESET_ALL} {len(self.targets)} set")
            if self.categories:
                print(f"{Fore.GREEN}✓ Categories:{Style.RESET_ALL} {len(self.categories)} selected")
            if self.profile:
                print(f"{Fore.GREEN}✓ Profile:{Style.RESET_ALL} {self.profile.value}")
            if self.targets or self.categories or self.profile:
                print()
            
            # Get input outside the box
            choice = self.get_input("Select option:").upper()
            
            if choice == '1':
                self.set_targets_interactive()
            elif choice == '2':
                self.select_engine_interactive()
            elif choice == '3':
                self.select_categories_interactive()
            elif choice == '4':
                self.select_profile_interactive()
            elif choice == '5':
                self.advanced_options_interactive()
            elif choice == '6':
                if not self.targets:
                    print(f"{Fore.RED}Please set targets first!{Style.RESET_ALL}")
                    input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                elif not self.categories:
                    print(f"{Fore.RED}Please select categories first!{Style.RESET_ALL}")
                    input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                else:
                    dorks = self.generate_dorks()
                    self.display_results(dorks)
                    if not self.silent:
                        input(f"{Fore.YELLOW}Press Enter to return to main menu...{Style.RESET_ALL}")
            elif choice == '7':
                self.show_status()
                input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            elif choice == 'H':
                self.show_help()
                input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            elif choice == 'Q':
                print(f"{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
                sys.exit(0)
            else:
                print(f"{Fore.RED}Invalid option!{Style.RESET_ALL}")
                input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

    def show_help(self):
        self.clear_screen()
        self.print_header("Help & Information")
        print()
        
        help_text = f"""
{Fore.YELLOW}Dork Factory v2.6{Style.RESET_ALL}
{Fore.CYAN}A passive reconnaissance tool for generating search engine dorks.{Style.RESET_ALL}

{Fore.GREEN}Usage:{Style.RESET_ALL}
  Interactive mode: python dorkfactory.py
  Flag mode: python dorkfactory.py --target example.com --profile bugbounty

{Fore.GREEN}Interactive Mode:{Style.RESET_ALL}
  • Navigate using numbers and letters
  • Multi-select with comma-separated numbers
  • Press Enter on empty line to finish multi-input
  • Use 'all', 'none', 'done' in category selection

{Fore.GREEN}Profiles:{Style.RESET_ALL}
  • Bug Bounty: Comprehensive security testing
  • OSINT Company: Focused on information gathering
  • CTF: Challenge-oriented dorks
  • Web App Basic: Lightweight web app reconnaissance
  • Full Scope: All available categories

{Fore.GREEN}Safety Features:{Style.RESET_ALL}
  • No scanning or automated requests
  • No web scraping or crawling
  • Pure query generation only
  • Ethical use encouraged

{Fore.YELLOW}Note:{Style.RESET_ALL} Always comply with search engine terms of service
and applicable laws when using generated dorks.
"""
        print(help_text)

    def run_from_flags(self, args):
        if args.target:
            self.targets = args.target
        if args.exclude:
            self.exclusions = args.exclude
            
        if args.engine:
            if args.engine == 'google':
                self.engine = SearchEngine.GOOGLE
            elif args.engine == 'yandex':
                self.engine = SearchEngine.YANDEX
            elif args.engine == 'both':
                self.engine = SearchEngine.BOTH
                
        if args.profile:
            try:
                self.profile = Profile(args.profile)
                config = self.profile_configs[self.profile]
                self.categories = set(config['categories'])
                if len(config['engines']) == 1:
                    self.engine = config['engines'][0]
                else:
                    self.engine = SearchEngine.BOTH
                self.advanced_options['strict_queries'] = config['strict_queries']
                self.advanced_options['reduce_noise'] = config['reduce_noise']
            except ValueError:
                print(f"{Fore.RED}Invalid profile: {args.profile}{Style.RESET_ALL}")
                sys.exit(1)
                
        if args.category:
            selected_categories = []
            for cat_str in args.category:
                for cat in Category:
                    if cat_str.lower() in cat.value.lower().replace(' ', '').replace('&', ''):
                        selected_categories.append(cat)
            if selected_categories:
                self.categories = set(selected_categories)
                
        if args.no_banner:
            self.advanced_options['no_banner'] = True
        if args.silent:
            self.silent = True
        if args.no_color:
            self.advanced_options['disable_colors'] = True
            global COLORS_ENABLED
            COLORS_ENABLED = False
            
        if not self.targets:
            print(f"{Fore.RED}Error: Target(s) required!{Style.RESET_ALL}")
            print(f"Use --target or run in interactive mode")
            sys.exit(1)
            
        if not self.categories:
            print(f"{Fore.RED}Error: No categories selected!{Style.RESET_ALL}")
            print(f"Use --category, --profile, or run in interactive mode")
            sys.exit(1)
            
        dorks = self.generate_dorks()
        
        if args.silent:
            for category, category_dorks in dorks.items():
                for dork in category_dorks:
                    print(dork)
        else:
            self.display_results(dorks)
            
        if args.export:
            self.export_dorks(dorks, args.export)

def main():
    parser = argparse.ArgumentParser(
        description="Dork Factory - Passive Recon Query Generator",
        add_help=False
    )
    
    parser.add_argument("-h", "--help", action="store_true", help="Show help and exit")
    parser.add_argument("-i", "--interactive", action="store_true", help="Force interactive mode")
    parser.add_argument("-nb", "--no-banner", action="store_true", help="Disable banner")
    
    parser.add_argument("--target", nargs="+", help="Define target(s)")
    parser.add_argument("--exclude", nargs="+", help="Exclude domains")
    parser.add_argument("--engine", choices=["google", "yandex", "both"], help="Search engine")
    parser.add_argument("--category", nargs="+", help="Select categories")
    parser.add_argument("--profile", help="Use preset profile")
    parser.add_argument("--export", help="Export output to file")
    parser.add_argument("--silent", action="store_true", help="Minimal output")
    parser.add_argument("--no-color", action="store_true", help="Disable colors")
    
    args = parser.parse_args()
    
    df = DorkFactory()
    
    if args.help:
        df.show_help()
        sys.exit(0)
    
    core_flags = [
        args.target, args.engine, args.category, 
        args.profile, args.export, args.silent
    ]
    
    if args.interactive or not any(core_flags):
        df.main_menu()
    else:
        df.run_from_flags(args)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Interrupted by user{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)
