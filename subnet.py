def create_decimal(list):
    decimal_list = []
    for i in list:
        decimal = int(i, 2)
        decimal_list.append(decimal)
    joined = ".".join([str(x) for x in decimal_list])
    return joined

def create_string(list):
    decimal_list = []
    for i in list:
        decimal = int(i, 2)
        decimal_list.append(decimal)
    joined = ".".join([str(x) for x in decimal_list])
    return joined

oct_count = 1
ip = []
ip_bin = []
while oct_count < 5:
    octet = int(input(f"{oct_count} octet: "))
    if octet < 255:
        ip.append(octet)
        octet = format(octet, '08b')
        ip_bin.append(octet)
        oct_count += 1
    else:
        print("Octets can't be above 255. Please try again!")

show_ip = f'{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}'
show_ip_bin = f'{ip_bin[0]}.{ip_bin[1]}.{ip_bin[2]}.{ip_bin[3]}'

print(f'IP address: {show_ip} or {show_ip_bin}')

network_bits = int(input("Enter subnet mask [24, 1, 2...]: /"))
host_bits = 32 - network_bits
print(f'Network bits: {network_bits}')
print(f'Host bits: {host_bits}')

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
full_mask_bin = ".".join([str(x) for x in full_list])

print(f'{mask_ip_form} or {mask_ip_decimal}')

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
            ending += "1" # if a zero, then 
    starting_ip.append(starting)
    ending_ip.append(ending)

decimal_starting = create_decimal(starting_ip)
decimal_ending = create_decimal(ending_ip)
joined_starting_ip = ".".join([str(x) for x in starting_ip])
joined_ending_ip = ".".join([str(x) for x in ending_ip])

print(f'your IP: {show_ip}')
print(f'starting IP: {joined_starting_ip} or {decimal_starting}')
print(f'ending IP: {joined_ending_ip} or {decimal_ending}')

# Fix the usable IP address
