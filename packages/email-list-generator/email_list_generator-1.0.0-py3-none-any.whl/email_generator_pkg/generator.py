from datetime import datetime
from termcolor import cprint
import json
import os

class EmailListGenerator:
    """
    Professional Email List Generator for Ethical Security Testing
    
    This class generates potential email addresses based on provided information.
    It supports multiple email domains and various name combinations.
    """
    
    def __init__(self, name: str | None = None, *, birth_date: str | None = None,
                 favorite_string: str | None = None, brother_name: str | None = None,
                 sister_name: str | None = None, father_name: str | None = None,
                 mother_name: str | None = None, company_name: str | None = None,
                 favorite_number: int | None = None, website: str | None = None) -> None:
        """
        Initialize the EmailListGenerator with target information.
        
        Args:
            name: Target's name
            birth_date: Target's birth date
            favorite_string: Target's favorite string
            brother_name: Brother's name
            sister_name: Sister's name
            father_name: Father's name
            mother_name: Mother's name
            company_name: Company name
            favorite_number: Favorite number
            website: Target's website
        """
        self.name = name
        self.birth_date = birth_date
        self.favorite_string = favorite_string
        self.brother_name = brother_name
        self.sister_name = sister_name
        self.father_name = father_name
        self.mother_name = mother_name
        self.company_name = company_name
        self.favorite_number = favorite_number
        self.website = website
        self.domains = self._load_domains()
        self.current_year = datetime.now().year

    def _load_domains(self) -> list:
        """Load email domains from JSON file."""
        try:
            with open('data/email_service.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            cprint("[!] Email domains file not found, using default domains", "red")
            return ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]

    def _generate_base_emails(self, base: str, file) -> None:
        """Generate base email variations for a given name."""
        # Basic email patterns
        for domain in self.domains:
            file.write(f"{base}@{domain}\n")
            if self.website:
                file.write(f"{base}@mail.{self.website}\n")

    def _generate_numbered_emails(self, base: str, file) -> None:
        """Generate numbered email variations."""
        for i in range(100):  # Reduced from 90009 for efficiency
            for domain in self.domains:
                file.write(f"{base}{i}@{domain}\n")
                if self.website:
                    file.write(f"{base}{i}@mail.{self.website}\n")

    def _generate_year_emails(self, base: str, file) -> None:
        """Generate year-based email variations."""
        for domain in self.domains:
            file.write(f"{base}{self.current_year}@{domain}\n")
            if self.website:
                file.write(f"{base}{self.current_year}@mail.{self.website}\n")

    def _generate_combined_emails(self, base: str, file) -> None:
        """Generate combined email variations."""
        for i in range(100):  # Reduced from 90009 for efficiency
            for domain in self.domains:
                file.write(f"{base}{self.current_year}{i}@{domain}\n")
                if self.website:
                    file.write(f"{base}{self.current_year}{i}@{self.website}\n")

    def _process_name(self, name: str, file) -> None:
        """Process a name and generate all email variations."""
        if not name:
            return
            
        # Generate all variations for the name
        self._generate_base_emails(name, file)
        self._generate_numbered_emails(name, file)
        self._generate_year_emails(name, file)
        self._generate_combined_emails(name, file)

    def generate_email(self) -> None:
        """Generate email list based on provided information."""
        try:
            # Ensure output directory exists
            os.makedirs('assets', exist_ok=True)
            
            with open('assets/email_list.txt', 'a+') as file:
                # Process each provided name
                self._process_name(self.name, file)
                self._process_name(self.brother_name, file)
                self._process_name(self.sister_name, file)
                self._process_name(self.father_name, file)
                self._process_name(self.mother_name, file)
                
                # Process favorite string if provided
                if self.favorite_string:
                    self._process_name(self.favorite_string, file)
                
                # Process company name if provided
                if self.company_name:
                    self._process_name(self.company_name, file)
            
            cprint("[+] Email list generation completed successfully", "green")
            
        except Exception as e:
            cprint(f"[!] Error generating email list: {str(e)}", "red")
            raise
        
