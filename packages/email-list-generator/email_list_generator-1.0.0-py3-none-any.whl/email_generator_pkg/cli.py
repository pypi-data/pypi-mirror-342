from generator import EmailListGenerator
import argparse
from termcolor import cprint
import sys
import time

def show_banner():
    banner = """
    ███████╗███╗   ███╗ █████╗ ██╗██╗         ██████╗ ███████╗███╗   ██╗███████╗██████╗  █████╗ ████████╗ ██████╗ ██████╗ 
    ██╔════╝████╗ ████║██╔══██╗██║██║         ██╔══██╗██╔════╝████╗  ██║██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
    █████╗  ██╔████╔██║███████║██║██║         ██████╔╝█████╗  ██╔██╗ ██║█████╗  ██████╔╝███████║   ██║   ██║   ██║██████╔╝
    ██╔══╝  ██║╚██╔╝██║██╔══██║██║██║         ██╔══██╗██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗██╔══██║   ██║   ██║   ██║██╔══██╗
    ███████╗██║ ╚═╝ ██║██║  ██║██║███████╗    ██║  ██║███████╗██║ ╚████║███████╗██║  ██║██║  ██║   ██║   ╚██████╔╝██║  ██║
    ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
    
    Email List Generator Tool
    Version: 1.0
    Author: HackingRepo
    Github: https://github.com/HackingRepo
    Telegram: https://t.me/hacking_pentest
    Email: cs7778503@gmail.com
    """
    cprint(banner, "cyan")

def show_about():
    about_text = """
    Email List Generator Tool
    
    This tool is designed to generate potential email addresses based on target information.
    It can create email variations using:
    - Target's name
    - Family members' names
    - Favorite strings
    - Website domains
    
    The tool is intended for educational purposes and ethical security testing only.
    """
    cprint(about_text, "cyan")

def show_disclaimer():
    disclaimer = """
    DISCLAIMER:
    This tool is for educational purposes only.
    Attacking targets without permission is illegal and unethical in all countries.
    The author is not responsible for any misuse of this tool.
    """
    cprint(disclaimer, "red")

def show_progress(current, total, verbose=False):
    progress = (current / total) * 100
    if verbose:
        cprint(f"\rGenerating emails: {current}/{total} ({progress:.2f}%)", "yellow", end="")
    else:
        cprint(f"\rProgress: {progress:.2f}%", "yellow", end="")
    if current == total:
        print()  # New line after completion

def generate_emails(name=None, website=None, brother_name=None, sister_name=None, 
                   father_name=None, mother_name=None, favorite_string=None, verbose=False):
    total_items = sum(1 for x in [name, brother_name, sister_name, father_name, mother_name, favorite_string] if x)
    current_item = 0
    
    if name:
        current_item += 1
        show_progress(current_item, total_items, verbose)
        if verbose:
            cprint(f"\n[*] Generating emails for name: {name}", "blue")
        generator = EmailListGenerator(name=name, website=website)
        generator.generate_email()
    
    if brother_name:
        current_item += 1
        show_progress(current_item, total_items, verbose)
        if verbose:
            cprint(f"\n[*] Generating emails for brother: {brother_name}", "blue")
        generator = EmailListGenerator(brother_name=brother_name, website=website)
        generator.generate_email()
    
    if sister_name:
        current_item += 1
        show_progress(current_item, total_items, verbose)
        if verbose:
            cprint(f"\n[*] Generating emails for sister: {sister_name}", "blue")
        generator = EmailListGenerator(sister_name=sister_name, website=website)
        generator.generate_email()
    
    if father_name:
        current_item += 1
        show_progress(current_item, total_items, verbose)
        if verbose:
            cprint(f"\n[*] Generating emails for father: {father_name}", "blue")
        generator = EmailListGenerator(father_name=father_name, website=website)
        generator.generate_email()
    
    if mother_name:
        current_item += 1
        show_progress(current_item, total_items, verbose)
        if verbose:
            cprint(f"\n[*] Generating emails for mother: {mother_name}", "blue")
        generator = EmailListGenerator(mother_name=mother_name, website=website)
        generator.generate_email()
    
    if favorite_string:
        current_item += 1
        show_progress(current_item, total_items, verbose)
        if verbose:
            cprint(f"\n[*] Generating emails for favorite string: {favorite_string}", "blue")
        generator = EmailListGenerator(favorite_string=favorite_string, website=website)
        generator.generate_email()

if __name__ == "__main__":
    show_banner()
    parser = argparse.ArgumentParser(description="Generate Email List")
    parser.add_argument("-n", "--name", type=str, help="Target's name", required=True)
    parser.add_argument("-w", "--website", type=str, help="Target's website", required=False)
    parser.add_argument("-bn", "--brother_name", type=str, help="Brother's name", required=False)
    parser.add_argument("-sn", "--sister_name", type=str, help="Sister's name", required=False)
    parser.add_argument("-fn", "--father_name", type=str, help="Father's name", required=False)
    parser.add_argument("-mn", "--mother_name", type=str, help="Mother's name", required=False)
    parser.add_argument("-fs", "--favorite_string", type=str, help="Favorite string", required=False)
    parser.add_argument("-V", "--version", action="version", version="1.0")
    parser.add_argument("-a", "--about", action="store_true", help="About the tool")
    parser.add_argument("-d", "--disclaimer", action="store_true", help="Show disclaimer")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed progress information")
    args = parser.parse_args()

    if args.about:
        show_about()
        sys.exit(0)
    
    if args.disclaimer:
        show_disclaimer()
        sys.exit(0)

    if not args.name:
        cprint("[!] Please provide target's name", "red")
        sys.exit(255)

    if args.verbose:
        cprint("[*] Starting email generation in verbose mode", "blue")
        cprint(f"[*] Target name: {args.name}", "blue")
        if args.website:
            cprint(f"[*] Website: {args.website}", "blue")
        if args.brother_name:
            cprint(f"[*] Brother's name: {args.brother_name}", "blue")
        if args.sister_name:
            cprint(f"[*] Sister's name: {args.sister_name}", "blue")
        if args.father_name:
            cprint(f"[*] Father's name: {args.father_name}", "blue")
        if args.mother_name:
            cprint(f"[*] Mother's name: {args.mother_name}", "blue")
        if args.favorite_string:
            cprint(f"[*] Favorite string: {args.favorite_string}", "blue")

    generate_emails(
        name=args.name,
        website=args.website,
        brother_name=args.brother_name,
        sister_name=args.sister_name,
        father_name=args.father_name,
        mother_name=args.mother_name,
        favorite_string=args.favorite_string,
        verbose=args.verbose
    )
    
    cprint("\n[+] Email list has been generated in assets/email_list.txt", "green")
