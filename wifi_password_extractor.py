import subprocess
import re

def print_banner():
    """Print the banner and description."""
    print("""
    ######################################
    #      Wi-Fi Password Extractor     #
    #       Extract saved Wi-Fi         #
    #          passwords on Windows     #
    ######################################
    """)

def get_saved_profiles():
    """Get all saved Wi-Fi profiles."""
    output = subprocess.check_output("netsh wlan show profiles", shell=True, encoding='utf-8', errors='ignore')
    profiles = re.findall(r"All User Profile\s*:\s*(.*)", output)
    return [p.strip() for p in profiles]

def get_wifi_password(profile):
    """Get the Wi-Fi password for a given profile."""
    try:
        output = subprocess.check_output(f"netsh wlan show profile name=\"{profile}\" key=clear", shell=True, encoding='utf-8', errors='ignore')
        password_line = re.search(r"Key Content\s*:\s(.*)", output)
        return password_line.group(1) if password_line else "N/A"
    except subprocess.CalledProcessError:
        return "Error"

def choose_profile(profiles):
    """Allow the user to choose a Wi-Fi profile."""
    print("\nPlease choose a Wi-Fi profile from the list:")
    for idx, profile in enumerate(profiles, 1):
        print(f"{idx}. {profile}")
    
    while True:
        try:
            choice = int(input("\nEnter the number of the profile you want to check: "))
            if 1 <= choice <= len(profiles):
                return profiles[choice - 1]
            else:
                print("Invalid choice. Please enter a number between 1 and", len(profiles))
        except ValueError:
            print("Please enter a valid number.")

def main():
    print_banner()

    profiles = get_saved_profiles()
    if not profiles:
        print("No Wi-Fi profiles found.")
        return

    chosen_profile = choose_profile(profiles)
    print(f"\nFetching password for: {chosen_profile}")
    
    password = get_wifi_password(chosen_profile)
    print(f"\nPassword for '{chosen_profile}': {password}")

if __name__ == "__main__":
    main()
