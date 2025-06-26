import os
import re
import csv
import time
import math
import shutil
from pathlib import Path

# ANSI color codes for colorful UI
COLORS = {
    'HEADER': '\033[95m',
    'MENU': '\033[94m',
    'OPTION': '\033[96m',
    'INPUT': '\033[92m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'ENDC': '\033[0m',
    'BOLD': '\033[1m',
    'ACCENT': '\033[35m',
    'SUCCESS': '\033[32m',
    'ACCENT2': '\033[36m',
    'NOTICE': '\033[33m\033[5m',  # Yellow with blinking effect
    'PROGRESS': '\033[33m',       # Yellow for progress bars
    'TIMER': '\033[34m'           # Blue for timer
}

def clean_phone(phone):
    """Clean phone number: preserve + and digits only"""
    # Remove all non-digit characters except leading '+'
    return '+' + ''.join(filter(str.isdigit, phone[1:])) if phone.startswith('+') else phone

def generate_name(base_name, count):
    """Generate sequential names"""
    # Remove any existing numbers from base name
    clean_base = re.sub(r'\d+$', '', base_name).strip()
    return f"{clean_base} {count}"

def print_progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█'):
    """Display progress bar in terminal"""
    percent = f"{100 * (iteration / float(total)):.1f}"
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{COLORS["PROGRESS"]}{prefix} |{bar}| {percent}% {suffix}{COLORS["ENDC"]}', end='\r')
    # Print new line when complete
    if iteration == total: 
        print()

def simulate_processing_delay():
    """Simulate 3-second processing time for all files"""
    print(f"\n{COLORS['TIMER']}Simulating standard 3-second processing time...{COLORS['ENDC']}")
    for i in range(1, 4):
        print(f"{COLORS['TIMER']}Processing step {i}/3{COLORS['ENDC']}")
        time.sleep(1)

def csv_to_vcard(csv_path, output_dir, base_name):
    """Convert CSV file to vCard format with generated names"""
    contacts = []
    total_contacts = 0
    start_time = time.time()
    
    # First pass: count lines for progress bar
    with open(csv_path, 'r', encoding='utf-8') as f:
        total_lines = sum(1 for _ in f)
    
    print(f"{COLORS['PROGRESS']}Processing {Path(csv_path).name}...{COLORS['ENDC']}")
    
    # Second pass: process data
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if not row:  # Skip empty rows
                continue
                
            # Update progress bar every 10 lines or at start/end
            if i % 10 == 0 or i == total_lines - 1:
                elapsed = time.time() - start_time
                suffix = f"Time: {elapsed:.1f}s | {i+1}/{total_lines} lines"
                print_progress_bar(i + 1, total_lines, prefix='Progress:', suffix=suffix)
                
            # Extract phone number (first column)
            phone = row[0].strip()
            
            # Clean only if starts with '+' (as per your specification)
            if phone.startswith('+'):
                phone = clean_phone(phone)
                
            # Skip invalid phone numbers
            if len(phone) < 8 or not phone.startswith('+'):
                continue
                
            # Generate name with sequential numbering
            contact_name = generate_name(base_name, total_contacts + 1)
            
            contacts.append({
                'name': contact_name,
                'phone': phone
            })
            total_contacts += 1
    
    # Create output filename
    filename = Path(csv_path).stem + ".vcf"
    output_file = os.path.join(output_dir, filename)
    
    # Write to VCF file
    with open(output_file, 'w', encoding='utf-8') as vcf:
        for contact in contacts:
            vcf.write("BEGIN:VCARD\n")
            vcf.write("VERSION:3.0\n")
            vcf.write(f"FN:{contact['name']}\n")
            vcf.write(f"TEL;TYPE=CELL:{contact['phone']}\n")
            vcf.write("ORG:ACCsi Forex\n")
            vcf.write("NOTE:Educational Purpose Only | By Abdul Qadeer Gabol\n")
            vcf.write("END:VCARD\n")
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    return output_file, total_contacts, processing_time

def print_banner():
    """Print ACCsi Forex banner with educational warning"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{COLORS['ACCENT2']}{'='*60}")
    print(f"{COLORS['ACCENT']}███████╗ ██████╗ ██████╗ ███████╗██╗  ██╗")
    print(f"██╔════╝██╔═══██╗██╔══██╗██╔════╝╚██╗██╔╝")
    print(f"█████╗  ██║   ██║██████╔╝█████╗   ╚███╔╝ ")
    print(f"██╔══╝  ██║   ██║██╔══██╗██╔══╝   ██╔██╗ ")
    print(f"██║     ╚██████╔╝██║  ██║███████╗██╔╝ ██╗")
    print(f"╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝{COLORS['ENDC']}")
    print(f"{COLORS['ACCENT2']}{'='*60}{COLORS['ENDC']}")
    print(f"{COLORS['MENU']}        Professional Contact Refinement System")
    print(f"{COLORS['ACCENT2']}{'-'*60}{COLORS['ENDC']}")
    
    # Educational warning with blinking effect
    print(f"\n{COLORS['NOTICE']}╔{'═'*58}╗")
    print(f"║{'WARNING: FOR EDUCATIONAL PURPOSES ONLY':^58}║")
    print(f"║{'Developed by Abdul Qadeer Gabol':^58}║")
    print(f"╚{'═'*58}╝{COLORS['ENDC']}")
    time.sleep(2)  # Pause to ensure notice is seen

def batch_process_files(input_dir, output_dir, base_name):
    """Process all CSV files in directory"""
    try:
        csv_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.csv')]
    except FileNotFoundError:
        csv_files = []
        
    if not csv_files:
        print(f"\n{COLORS['WARNING']}No CSV files found in {input_dir}{COLORS['ENDC']}")
        return
        
    total_contacts = 0
    processed_files = 0
    total_time = 0
    
    print(f"\n{COLORS['SUCCESS']}Starting batch processing of {len(csv_files)} files...{COLORS['ENDC']}")
    
    # Simulate 3-second processing for standard files
    simulate_processing_delay()
    
    for i, filename in enumerate(csv_files):
        csv_path = os.path.join(input_dir, filename)
        output_file, contacts_in_file, proc_time = csv_to_vcard(csv_path, output_dir, base_name)
        total_contacts += contacts_in_file
        processed_files += 1
        total_time += proc_time
        print(f"{COLORS['SUCCESS']}  • Processed {filename}: {contacts_in_file} contacts in {proc_time:.2f} seconds{COLORS['ENDC']}")
    
    print(f"\n{COLORS['SUCCESS']}Batch processing complete!{COLORS['ENDC']}")
    print(f"{COLORS['SUCCESS']}Total files processed: {processed_files}{COLORS['ENDC']}")
    print(f"{COLORS['SUCCESS']}Total contacts created: {total_contacts}{COLORS['ENDC']}")
    print(f"{COLORS['SUCCESS']}Total processing time: {total_time:.2f} seconds{COLORS['ENDC']}")
    print(f"{COLORS['ACCENT']}Note: For educational purposes only | By Abdul Qadeer Gabol{COLORS['ENDC']}")
    input(f"\n{COLORS['INPUT']}Press Enter to continue...{COLORS['ENDC']}")

def export_contact_stats(output_dir):
    """Export contact statistics to a text file"""
    try:
        vcf_files = [f for f in os.listdir(output_dir) if f.lower().endswith('.vcf')]
        if not vcf_files:
            print(f"{COLORS['WARNING']}No VCF files found in output directory!{COLORS['ENDC']}")
            return
            
        stats_file = os.path.join(output_dir, "contact_statistics.txt")
        total_contacts = 0
        
        with open(stats_file, 'w') as f:
            f.write("ACCsi Forex Contact Statistics Report\n")
            f.write("====================================\n\n")
            f.write(f"Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Report by: Abdul Qadeer Gabol\n\n")
            
            f.write("File Breakdown:\n")
            f.write("--------------\n")
            for vcf in vcf_files:
                vcf_path = os.path.join(output_dir, vcf)
                with open(vcf_path, 'r') as vcf_file:
                    content = vcf_file.read()
                    contact_count = content.count('BEGIN:VCARD')
                    total_contacts += contact_count
                    f.write(f"{vcf}: {contact_count} contacts\n")
            
            f.write(f"\nTotal Contacts: {total_contacts}\n")
            f.write("\nEducational Purpose Only - ACCsi Forex\n")
        
        print(f"\n{COLORS['SUCCESS']}Statistics report exported to: {stats_file}{COLORS['ENDC']}")
        return True
    except Exception as e:
        print(f"{COLORS['FAIL']}Error generating report: {str(e)}{COLORS['ENDC']}")
        return False

def backup_directory(directory):
    """Create a backup of the directory"""
    try:
        backup_dir = f"{directory}_backup_{int(time.time())}"
        shutil.copytree(directory, backup_dir)
        print(f"\n{COLORS['SUCCESS']}Backup created at: {backup_dir}{COLORS['ENDC']}")
        return True
    except Exception as e:
        print(f"{COLORS['FAIL']}Backup failed: {str(e)}{COLORS['ENDC']}")
        return False

def main():
    # Create directories if they don't exist
    input_dir = "/storage/emulated/0/Qadeer/Csv/"
    output_dir = "/storage/emulated/0/Qadeer/Refined/"
    
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    while True:
        print_banner()
        print(f"{COLORS['MENU']}1.{COLORS['OPTION']} Process Single CSV File{COLORS['ENDC']}")
        print(f"{COLORS['MENU']}2.{COLORS['OPTION']} Batch Process All CSV Files{COLORS['ENDC']}")
        print(f"{COLORS['MENU']}3.{COLORS['OPTION']} View Directory Info{COLORS['ENDC']}")
        print(f"{COLORS['MENU']}4.{COLORS['OPTION']} Export Contact Statistics{COLORS['ENDC']}")
        print(f"{COLORS['MENU']}5.{COLORS['OPTION']} Backup Directory{COLORS['ENDC']}")
        print(f"{COLORS['MENU']}6.{COLORS['OPTION']} Exit{COLORS['ENDC']}")
        print(f"\n{COLORS['INPUT']}Input directory: {input_dir}{COLORS['ENDC']}")
        print(f"{COLORS['SUCCESS']}Output directory: {output_dir}{COLORS['ENDC']}")
        
        choice = input(f"\n{COLORS['INPUT']}Enter your choice: {COLORS['ENDC']}")
        
        if choice == '1':  # Process Single File
            # Find CSV files in input directory
            try:
                csv_files = [f for f in os.listdir(input_dir) 
                            if f.lower().endswith('.csv')]
            except FileNotFoundError:
                csv_files = []
                
            if not csv_files:
                print(f"\n{COLORS['WARNING']}No CSV files found in {input_dir}{COLORS['ENDC']}")
                input(f"\n{COLORS['INPUT']}Press Enter to continue...{COLORS['ENDC']}")
                continue
                
            print(f"\n{COLORS['MENU']}Available CSV files:{COLORS['ENDC']}")
            for i, f in enumerate(csv_files, 1):
                print(f"{COLORS['MENU']}{i}.{COLORS['OPTION']} {f}{COLORS['ENDC']}")
                
            try:
                file_choice = input(f"\n{COLORS['INPUT']}Select file number: {COLORS['ENDC']}")
                if not file_choice:
                    continue
                file_choice = int(file_choice)
                selected_file = csv_files[file_choice-1]
                csv_path = os.path.join(input_dir, selected_file)
            except (ValueError, IndexError):
                print(f"{COLORS['WARNING']}Invalid selection!{COLORS['ENDC']}")
                input(f"\n{COLORS['INPUT']}Press Enter to continue...{COLORS['ENDC']}")
                continue
            
            base_name = input(f"\n{COLORS['INPUT']}Enter base name for contacts (e.g. Trader): {COLORS['ENDC']}").strip()
            if not base_name:
                print(f"{COLORS['WARNING']}Base name cannot be empty!{COLORS['ENDC']}")
                input(f"\n{COLORS['INPUT']}Press Enter to continue...{COLORS['ENDC']}")
                continue
                
            # Simulate 3-second processing for standard files
            simulate_processing_delay()
            
            output_file, total_contacts, proc_time = csv_to_vcard(
                csv_path, output_dir, base_name
            )
            
            print(f"\n{COLORS['SUCCESS']}Successfully processed {total_contacts} contacts in {proc_time:.2f} seconds!{COLORS['ENDC']}")
            print(f"{COLORS['SUCCESS']}Output saved to: {output_file}{COLORS['ENDC']}")
            print(f"{COLORS['ACCENT']}Note: For educational purposes only | By Abdul Qadeer Gabol{COLORS['ENDC']}")
            input(f"\n{COLORS['INPUT']}Press Enter to continue...{COLORS['ENDC']}")
            
        elif choice == '2':  # Batch Process
            base_name = input(f"\n{COLORS['INPUT']}Enter base name for all contacts (e.g. Client): {COLORS['ENDC']}").strip()
            if not base_name:
                print(f"{COLORS['WARNING']}Base name cannot be empty!{COLORS['ENDC']}")
                input(f"\n{COLORS['INPUT']}Press Enter to continue...{COLORS['ENDC']}")
                continue
                
            # Confirm batch processing
            confirm = input(f"{COLORS['WARNING']}Process ALL CSV files? This cannot be undone. (y/n): {COLORS['ENDC']}").strip().lower()
            if confirm != 'y':
                print(f"{COLORS['SUCCESS']}Batch processing canceled.{COLORS['ENDC']}")
                time.sleep(1)
                continue
                
            batch_process_files(input_dir, output_dir, base_name)
            
        elif choice == '3':  # Directory Info
            print(f"\n{COLORS['SUCCESS']}=== Directory Information ===")
            print(f"{COLORS['INPUT']}Input directory: {input_dir}{COLORS['ENDC']}")
            
            try:
                csv_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.csv')]
                print(f"{COLORS['SUCCESS']}CSV files found: {len(csv_files)}{COLORS['ENDC']}")
                
                # Show file sizes
                total_size = 0
                for f in csv_files:
                    fp = os.path.join(input_dir, f)
                    size = os.path.getsize(fp)
                    total_size += size
                    print(f"  • {f}: {size/1024:.1f} KB")
                    
                print(f"\n{COLORS['SUCCESS']}Total CSV data: {total_size/1024:.1f} KB{COLORS['ENDC']}")
            except FileNotFoundError:
                print(f"{COLORS['WARNING']}Input directory not found!{COLORS['ENDC']}")
                
            print(f"\n{COLORS['INPUT']}Output directory: {output_dir}{COLORS['ENDC']}")
            try:
                vcf_files = [f for f in os.listdir(output_dir) if f.lower().endswith('.vcf')]
                print(f"{COLORS['SUCCESS']}VCF files found: {len(vcf_files)}{COLORS['ENDC']}")
                
                # Count total contacts in VCF files
                total_contacts = 0
                for f in vcf_files:
                    fp = os.path.join(output_dir, f)
                    with open(fp, 'r') as vcf:
                        content = vcf.read()
                        contacts = content.count('BEGIN:VCARD')
                        total_contacts += contacts
                        print(f"  • {f}: {contacts} contacts")
                
                print(f"\n{COLORS['SUCCESS']}Total contacts in output: {total_contacts}{COLORS['ENDC']}")
            except FileNotFoundError:
                print(f"{COLORS['WARNING']}Output directory not found!{COLORS['ENDC']}")
                
            input(f"\n{COLORS['INPUT']}Press Enter to continue...{COLORS['ENDC']}")
            
        elif choice == '4':  # Export Statistics
            print(f"\n{COLORS['SUCCESS']}Generating contact statistics report...{COLORS['ENDC']}")
            if export_contact_stats(output_dir):
                print(f"{COLORS['SUCCESS']}Statistics report created successfully!{COLORS['ENDC']}")
            input(f"\n{COLORS['INPUT']}Press Enter to continue...{COLORS['ENDC']}")
            
        elif choice == '5':  # Backup Directory
            print(f"\n{COLORS['SUCCESS']}Creating backup of output directory...{COLORS['ENDC']}")
            if backup_directory(output_dir):
                print(f"{COLORS['SUCCESS']}Backup completed successfully!{COLORS['ENDC']}")
            input(f"\n{COLORS['INPUT']}Press Enter to continue...{COLORS['ENDC']}")
            
        elif choice == '6':  # Exit
            print(f"\n{COLORS['SUCCESS']}Thank you for using ACCsi Forex Contact Refiner!{COLORS['ENDC']}")
            print(f"{COLORS['ACCENT']}Educational tool by Abdul Qadeer Gabol{COLORS['ENDC']}")
            break
            
        else:
            print(f"{COLORS['WARNING']}Invalid choice! Please enter 1-6.{COLORS['ENDC']}")
            input(f"\n{COLORS['INPUT']}Press Enter to continue...{COLORS['ENDC']}")

if __name__ == "__main__":
    main()
