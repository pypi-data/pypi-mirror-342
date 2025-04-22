"""
VisionFi CLI Color Guide
This script generates a visual guide of ANSI color codes that can be used in the VisionFi CLI.
It helps to select the exact colors for the VisionFi banner and UI elements.
"""

import os
from colorama import init, Fore, Back, Style

# Initialize colorama for cross-platform color support
init()

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(text):
    """Print a styled header."""
    width = 80
    print("\n" + "=" * width)
    print(f"{text.center(width)}")
    print("=" * width + "\n")

def show_basic_colors():
    """Show basic colorama colors."""
    print_header("BASIC COLORAMA COLORS")
    
    # Foreground colors
    print("FOREGROUND COLORS:")
    print(f"{Fore.BLACK}{Style.BRIGHT}Fore.BLACK + Style.BRIGHT{Style.RESET_ALL}")
    print(f"{Fore.RED}{Style.BRIGHT}Fore.RED + Style.BRIGHT{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{Style.BRIGHT}Fore.GREEN + Style.BRIGHT{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}Fore.YELLOW + Style.BRIGHT{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{Style.BRIGHT}Fore.BLUE + Style.BRIGHT{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{Style.BRIGHT}Fore.MAGENTA + Style.BRIGHT{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{Style.BRIGHT}Fore.CYAN + Style.BRIGHT{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Style.BRIGHT}Fore.WHITE + Style.BRIGHT{Style.RESET_ALL}")
    
    print("\nNORMAL INTENSITY:")
    print(f"{Fore.BLACK}Fore.BLACK{Style.RESET_ALL}")
    print(f"{Fore.RED}Fore.RED{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Fore.GREEN{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Fore.YELLOW{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Fore.BLUE{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}Fore.MAGENTA{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Fore.CYAN{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Fore.WHITE{Style.RESET_ALL}")
    
    print("\nDIM INTENSITY:")
    print(f"{Fore.BLACK}{Style.DIM}Fore.BLACK + Style.DIM{Style.RESET_ALL}")
    print(f"{Fore.RED}{Style.DIM}Fore.RED + Style.DIM{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{Style.DIM}Fore.GREEN + Style.DIM{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{Style.DIM}Fore.YELLOW + Style.DIM{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{Style.DIM}Fore.BLUE + Style.DIM{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{Style.DIM}Fore.MAGENTA + Style.DIM{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{Style.DIM}Fore.CYAN + Style.DIM{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Style.DIM}Fore.WHITE + Style.DIM{Style.RESET_ALL}")

def show_8bit_colors():
    """Show 8-bit ANSI color codes (256 colors) with black, white, red and blue focus."""
    print_header("8-BIT ANSI COLORS - BLACK, WHITE, RED & BLUE")
    
    # Black, white and gray variations
    print("BLACK, WHITE & GRAY VARIATIONS:")
    
    grayscale_colors = [
        (255, "Pure White"),
        (254, "Off White"),
        (250, "Light Gray"),
        (245, "Lighter Gray"),
        (240, "Medium Gray"),
        (235, "Dark Gray"),
        (232, "Darkest Gray"),
        (16, "Black")
    ]
    
    # Add red and blue variations
    print("\nRED VARIATIONS:")
    red_colors = [
        (196, "Bright Red"),
        (160, "Deep Red"),
        (124, "Dark Red"),
        (88, "Very Dark Red"),
        (52, "Darkest Red"),
        (203, "Light Red"),
        (210, "Pinkish Red")
    ]
    
    print("\nBLUE VARIATIONS:")
    blue_colors = [
        (21, "Blue"),
        (27, "Light Blue"),
        (33, "Cyan Blue"),
        (39, "Teal"),
        (20, "Deep Blue"),
        (19, "Dark Blue"),
        (17, "Navy Blue"),
        (45, "Light Cyan")
    ]
    
    # Display all grayscale variations
    for code, desc in grayscale_colors:
        print(f"\033[38;5;{code}m\\033[38;5;{code}m - {desc}{Style.RESET_ALL}")
    
    # Display all red variations
    for code, desc in red_colors:
        print(f"\033[38;5;{code}m\\033[38;5;{code}m - {desc}{Style.RESET_ALL}")
    
    # Display all blue variations
    for code, desc in blue_colors:
        print(f"\033[38;5;{code}m\\033[38;5;{code}m - {desc}{Style.RESET_ALL}")
    
    # Show examples of how the VisionFi text might look with black and white theme
    print("\nEXAMPLE TEXT SAMPLES WITH BLACK & WHITE THEME:")
    print("\033[38;5;255mVision\033[38;5;255mFi\033[0m - Pure White (255)")
    print("\033[38;5;250mVision\033[38;5;255mFi\033[0m - Light Gray (250) with White (255)")
    print("\033[38;5;240mVision\033[38;5;255mFi\033[0m - Medium Gray (240) with White (255)")
    
    # Show examples with red and blue accents
    print("\nEXAMPLE TEXT SAMPLES WITH ACCENT COLORS:")
    print("\033[38;5;255mVision\033[38;5;196mFi\033[0m - White with Bright Red (196)")
    print("\033[38;5;255mVision\033[38;5;21mFi\033[0m - White with Blue (21)")
    
    print("\nSee all colors? (y/n): ", end="")
    show_all = input().lower().startswith('y')
    
    if show_all:
        # Standard colors (0-15)
        print("\nSTANDARD COLORS (0-15):")
        for i in range(16):
            print(f"\033[38;5;{i}m\\033[38;5;{i}m{Style.RESET_ALL}", end=" ")
            if (i + 1) % 8 == 0:
                print()
        
        # 216 colors (16-231)
        print("\n\n216 COLORS (16-231):")
        for i in range(16, 232, 6):
            for j in range(6):
                code = i + j
                print(f"\033[38;5;{code}m{code}{Style.RESET_ALL}", end=" ")
            print()
        
        # Grayscale (232-255)
        print("\nGRAYSCALE (232-255):")
        for i in range(232, 256, 6):
            for j in range(min(6, 256 - i)):
                code = i + j
                print(f"\033[38;5;{code}m{code}{Style.RESET_ALL}", end=" ")
            print()

def show_rgb_colors():
    """Show RGB color codes examples with black, white, red and blue focus."""
    print_header("TRUE COLOR (RGB) EXAMPLES - BLACK, WHITE, RED & BLUE")
    
    # Black and white RGB values
    bw_colors = [
        ((255, 255, 255), "Pure White"),
        ((240, 240, 240), "Off White"),
        ((200, 200, 200), "Light Gray"),
        ((150, 150, 150), "Medium Gray"),
        ((100, 100, 100), "Dark Gray"),
        ((50, 50, 50), "Very Dark Gray"),
        ((0, 0, 0), "Black")
    ]
    
    # Red RGB values
    red_colors = [
        ((255, 0, 0), "Pure Red"),
        ((220, 20, 60), "Crimson"),
        ((178, 34, 34), "Firebrick"),
        ((139, 0, 0), "Dark Red"),
        ((255, 69, 0), "Red-Orange")
    ]
    
    # Blue RGB values
    blue_colors = [
        ((0, 0, 255), "Pure Blue"),
        ((30, 144, 255), "Dodger Blue"),
        ((0, 119, 190), "Medium Blue"),
        ((25, 25, 112), "Midnight Blue"),
        ((0, 104, 139), "Deep Sky Blue")
    ]
    
    print("BLACK & WHITE VARIATIONS:")
    for (r, g, b), desc in bw_colors:
        print(f"\033[38;2;{r};{g};{b}m\\033[38;2;{r};{g};{b}m - {desc}{Style.RESET_ALL}")
    
    print("\nRED VARIATIONS:")
    for (r, g, b), desc in red_colors:
        print(f"\033[38;2;{r};{g};{b}m\\033[38;2;{r};{g};{b}m - {desc}{Style.RESET_ALL}")
    
    print("\nBLUE VARIATIONS:")
    for (r, g, b), desc in blue_colors:
        print(f"\033[38;2;{r};{g};{b}m\\033[38;2;{r};{g};{b}m - {desc}{Style.RESET_ALL}")
    
    # Show examples of how the VisionFi text might look with black and white theme
    print("\nEXAMPLE TEXT SAMPLES WITH BLACK & WHITE THEME:")
    print("\033[38;2;255;255;255mVision\033[38;2;255;255;255mFi\033[0m - Pure White with White")
    print("\033[38;2;200;200;200mVision\033[38;2;255;255;255mFi\033[0m - Light Gray with White")
    
    # Show examples with red and blue
    print("\nEXAMPLE TEXT SAMPLES WITH ACCENT COLORS:")
    print("\033[38;2;255;255;255mVision\033[38;2;255;0;0mFi\033[0m - White with Pure Red")
    print("\033[38;2;255;255;255mVision\033[38;2;0;0;255mFi\033[0m - White with Pure Blue")
    print("\033[38;2;255;255;255mVision\033[38;2;220;20;60mFi\033[0m - White with Crimson")
    print("\033[38;2;255;255;255mVision\033[38;2;30;144;255mFi\033[0m - White with Dodger Blue")

def show_mixed_styles():
    """Show mixed styles for VisionFi text elements with black and white theme."""
    print_header("VISIONFI BRAND ELEMENTS - BLACK & WHITE THEME WITH ACCENTS")
    
    # Show different VisionFi logo color combinations with black and white focus
    print("VISIONFI LOGO COLOR COMBINATIONS:")
    print("\033[38;5;255mVision\033[38;5;255mFi\033[0m - All White (255)")
    print("\033[38;5;250mVision\033[38;5;255mFi\033[0m - Light Gray (250) with White (255)")
    print("\033[38;5;240mVision\033[38;5;255mFi\033[0m - Dark Gray (240) with White (255)")
    print("\033[38;5;232mVision\033[38;5;255mFi\033[0m - Black (232) with White (255)")
    
    # Show red and blue accent options
    print("\nRED AND BLUE ACCENT OPTIONS:")
    print("\033[38;5;255mVision\033[38;5;196mFi\033[0m - White with Bright Red (196)")
    print("\033[38;5;255mVision\033[38;5;160mFi\033[0m - White with Deep Red (160)")
    print("\033[38;5;255mVision\033[38;5;21mFi\033[0m - White with Blue (21)")
    print("\033[38;5;255mVision\033[38;5;27mFi\033[0m - White with Light Blue (27)")
    
    # Show UI elements with black and white theme
    print("\nUI ELEMENTS - BLACK & WHITE WITH ACCENTS:")
    print(f"\033[38;5;255m[1]\033[0m Menu Option - White (255)")
    print(f"\033[38;5;196m[2]\033[0m Menu Option - Bright Red (196)")
    print(f"\033[38;5;21m[3]\033[0m Menu Option - Blue (21)")
    print(f"\033[38;5;240m[4]\033[0m Menu Option - Dark Gray (240)")
    
    print("\nTEXT ELEMENTS:")
    print(f"\033[38;5;255m\033[1mHeading Text\033[0m - Bold White (255)")
    print(f"\033[38;5;250mSubheading Text\033[0m - Light Gray (250)")
    print(f"\033[38;5;196mWarning Text\033[0m - Bright Red (196)")
    print(f"\033[38;5;21mInfo Text\033[0m - Blue (21)")
    
    # VisionFi ASCII art representation (simplified)
    print("\nSIMPLIFIED VISION-FI BANNER WITH DIFFERENT COLOR OPTIONS:")
    ascii_art_sample = """
VVVVVV  iiii                      iiii                        FFFFFFFF  II
V::::V i::::i                    i::::i                      F::::::::F I::::I
V::::V  iiii                      iiii                      F::::::::F I::::I
V::::V                                                     F::::::FF  II:::II
 V:::V iiiii    sssss    iiiii    ooooo   nnnnnn          F:::::F      I:::I
  V:V i:::::i  ss:::::s  i:::::i oo:::oo  n:::::n         F:::::F      I:::I
   V:V i::::i ss:::::ss   i::::i o:::::o n:::::::n       F::::::FF    II:::II
    V  i::::i s::sss      i::::i o:::::o n:::::::n       F:::::::F    I::::I
       i::::i  s:s        i::::i o:::::o n:::::::n       F:::::::F    I::::I
       iiiiii   sssssss   iiiiii  ooooo   nnnnnnn        FFFFFFFFF    IIIIII
"""
    # Print the ASCII art sample with different gold colors
    print(f"\n\033[38;5;214m{ascii_art_sample}\033[0m")
    
def user_selection():
    """Let the user select preferred colors from the black and white theme with red and blue accents."""
    print_header("COLOR SELECTION - BLACK & WHITE THEME WITH ACCENTS")
    print("Now that you've seen the black, white, red, and blue color options, you can select your preferences.")
    print("For each element, enter the color code number or description.\n")
    
    elements = [
        "VisionFi Logo (Vision part)",
        "VisionFi Logo (Fi part)",
        "Menu brackets [ ]",
        "Headings",
        "Subheadings",
        "Error messages",
        "Info messages",
        "Border box"
    ]
    
    selections = {}
    
    for element in elements:
        print(f"\nPreferred color for {element}: ", end="")
        selection = input()
        selections[element] = selection
    
    print("\nYOUR SELECTIONS:")
    for element, color in selections.items():
        print(f"{element}: {color}")
    
    return selections

def main():
    """Main function to show the color guide."""
    clear_screen()
    print("VISIONFI CLI COLOR GUIDE")
    print("This tool helps you select the perfect colors for your VisionFi CLI.")
    print("Follow these steps to view color options and select your preferences.")
    print("\nPress Enter to continue...")
    input()
    
    show_basic_colors()
    print("\nPress Enter to continue to 8-bit colors...")
    input()
    
    show_8bit_colors()
    print("\nPress Enter to continue to RGB colors...")
    input()
    
    show_rgb_colors()
    print("\nPress Enter to continue to VisionFi brand elements...")
    input()
    
    show_mixed_styles()
    print("\nPress Enter to make your color selections...")
    input()
    
    selections = user_selection()
    
    print("\nThank you! Please share these color preferences with Claude to update the VisionFi CLI.")
    print("The selected colors will be used to update the banner.py file.\n")

if __name__ == "__main__":
    main()