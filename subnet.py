import os
from rich.console import Console
from rich.rule import Rule
from rich.panel import Panel
from rich.tree import Tree
from rich.text import Text

console = Console()

os.system('cls')
print("""
▄█████ ▄▄ ▄▄ ▄▄▄▄  ▄▄  ▄▄ ▄▄▄▄▄ ▄▄▄▄▄▄ 
▀▀▀▄▄▄ ██ ██ ██▄██ ███▄██ ██▄▄    ██   
█████▀ ▀███▀ ██▄█▀ ██ ▀██ ██▄▄▄   ██    v1.0  
""")

def create_decimal(list):
    decimal_list = []
    for i in list:
        decimal = int(i, 2)
        decimal_list.append(decimal)
    joined = ".".join([str(x) for x in decimal_list])
    return joined

# IP input
oct_count = 1
ip = []
ip_bin = []
while oct_count < 5:
    octet = int(input(f"Enter octet {oct_count}: "))
    if octet < 255:
        ip.append(octet)
        octet = format(octet, '08b')
        ip_bin.append(octet)
        oct_count += 1
    else:
        print("Octets can't be above 255. Please try again!")

show_ip = f'{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}'
show_ip_bin = f'{ip_bin[0]}.{ip_bin[1]}.{ip_bin[2]}.{ip_bin[3]}'

network_bits = int(input("Enter subnet mask [24, 1, 2...]: /"))
host_bits = 32 - network_bits
total_hosts = 2**(host_bits)
usable_hosts = total_hosts - 2

mask_list = []
decimal_list = []

bit_form = "1" * network_bits + "0" * host_bits
for i in range(0, 32, 8):
    decimal = int(bit_form[i:i+8], 2)
    decimal_list.append(decimal)
    octet = int(bit_form[i:i+8])
    mask_list.append(octet)

# Turns all the strings into dot format
mask_ip_form = ".".join([f"{x:08}" for x in mask_list])
mask_ip_decimal = ".".join([str(x) for x in decimal_list])

starting_ip = []
ending_ip = []
split_ip_octets = show_ip_bin.split('.')
split_mask_octets = mask_ip_form.split('.')

for i in range(4):
    starting = ""
    ending = ""
    for ip_bits, mask_bits in zip(split_ip_octets[i], split_mask_octets[i]):
        if ip_bits == "1" and mask_bits == "1":
            starting += "1"
        else:
            starting += "0"
    for ip_bits, mask_bits in zip(split_ip_octets[i], split_mask_octets[i]):
        if mask_bits == "1": # if it's one, the ip stays the same
            ending += ip_bits
        else:
            ending += "1" # if a zero, then change that 0 into a 1
    starting_ip.append(starting)
    ending_ip.append(ending)

usable_start = starting_ip[:]
usable_end = ending_ip[:]
added_bit = int(usable_start[3], 2) + 1
usable_start[3] = format(added_bit, '08b')
removed_bit = int(usable_end[3], 2) - 1
usable_end[3] = format(removed_bit, '08b')

decimal_starting = create_decimal(starting_ip)
decimal_ending = create_decimal(ending_ip)
usable_start_ip = create_decimal(usable_start)
usable_end_ip = create_decimal(usable_end)
joined_starting_ip = ".".join([str(x) for x in starting_ip])
joined_ending_ip = ".".join([str(x) for x in ending_ip])
joined_usable_start = ".".join([str(x) for x in usable_start])
joined_usable_end= ".".join([str(x) for x in usable_end])

def display_output():
    summary = Text.assemble(                      
        ("Target IP: ", "bold green"), (f"{show_ip}/{network_bits}\n", "bold white"),
        ("Subnet Mask: ", "bold green"), (f"{mask_ip_decimal}\n", "bold white"),
        ("Network bits: ", "bold green"), (f"{network_bits}\n", "bold white"),
        ("Host bits: ", "bold green"), (f"{host_bits}\n", "bold white"),
        ("Total hosts: ", "bold green"), (f"{total_hosts}\n", "bold white"),
        ("Usable hosts: ", "bold green"), (f"{usable_hosts}\n", "bold white"),
        ("Network Address: ", "bold green"), (f"{decimal_starting}\n", "bold white"),
        ("Broadcast Address: ", "bold green"), (f"{decimal_ending}\n", "bold white"),
        ("Usable Range: ", "bold green"), (f"{usable_start_ip} — {usable_end_ip}", "bold yellow")
    )
    console.print(Panel(summary, border_style="dim", padding=(1, 2)))

# run the app
display_output()