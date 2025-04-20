def show_help():
    os.system('clear')
    help_message = f"""
{Fore.GREEN}+--------------------------------------------------+
{Fore.YELLOW}|              {Fore.RED}🔰SL Android Official ™             {Fore.YELLOW}|
{Fore.YELLOW}|           👨‍💻TOOL DEVELOPED BY IM COOL BOOY     {Fore.YELLOW}|
{Fore.CYAN}|                 📻 IM-COOL-BOOY-FM               {Fore.CYAN}|
{Fore.GREEN}+--------------------------------------------------+
{Fore.BLUE}   Usage:
{Fore.LIGHTCYAN_EX}     IM-COOL-BOOY-FM --help [options]

{Fore.BLUE}   Options:
{Fore.LIGHTCYAN_EX}     --help        ➡️       Show this help message and exit
{Fore.LIGHTCYAN_EX}     1️⃣            ➡️       Search for a Radio Station
{Fore.LIGHTCYAN_EX}     2️⃣            ➡️       Switch Channel
{Fore.LIGHTCYAN_EX}     3️⃣            ➡️       Stop Playing
{Fore.LIGHTCYAN_EX}     4️⃣            ➡️       View Station Details
{Fore.LIGHTCYAN_EX}     5️⃣            ➡️       Exit
{Fore.GREEN}+--------------------------------------------------+
    """
    print(help_message)

def main():
    player = None
    current_station = None
    station_number = None

    import sys
    if len(sys.argv) > 1 and sys.argv[1] in ('--help'):
        show_help()
        return
