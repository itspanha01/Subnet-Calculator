import customtkinter as ctk

class SubnetCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Font configuration
        self.main_font = "Space Grotesk"
        self.code_font = "Consolas" # For IP addresses/Numbers
        self.ascii_font = "Courier" # REQUIRED for ASCII alignment

        # Window Configuration
        self.title("Subnet Calculator v1.1")
        self.geometry("600x750")
        ctk.set_appearance_mode("dark")
        
        # --- ASCII Header ---
        self.ascii_art = """
▄█████ ▄▄ ▄▄ ▄▄▄▄  ▄▄  ▄▄ ▄▄▄▄▄ ▄▄▄▄▄▄ 
▀▀▀▄▄▄ ██ ██ ██▄██ ███▄██ ██▄▄    ██   
█████▀ ▀███▀ ██▄█▀ ██ ▀██ ██▄▄▄   ██    v1.1
        """
        
        self.header_label = ctk.CTkLabel(
            self, 
            text=self.ascii_art, 
            font=(self.ascii_font, 12, "bold"),
            text_color="#39e600",
            justify="left"
        )
        self.header_label.pack(pady=(10, 0))

        self.sub_text = ctk.CTkLabel(
            self, 
            text="Subnet mask calculator in the terminal.\nGithub: itspanha01",
            font=(self.main_font, 12, "bold"),
            text_color="gray"
        )
        self.sub_text.pack(pady=(0, 20))

        # --- Input Section ---
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=10, padx=30, fill="x")

        self.ip_entry = ctk.CTkEntry(
            self.input_frame, 
            placeholder_text="IP Address (e.g. 192.168.1.1)", 
            height=40,
            font=(self.main_font, 14)
        )
        self.ip_entry.grid(row=0, column=0, pady=15, padx=10, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=3)

        self.mask_entry = ctk.CTkEntry(
            self.input_frame, 
            placeholder_text="/24", 
            width=80, 
            height=40,
            font=(self.main_font, 14)
        )
        self.mask_entry.grid(row=0, column=1, pady=15, padx=10)

        self.calc_button = ctk.CTkButton(
            self, 
            text="CALCULATE", 
            command=self.perform_calculation,
            fg_color="#39e600",
            text_color="black",
            hover_color="#2eb300",
            font=(self.main_font, 16, "bold"),
            height=45
        )
        self.calc_button.pack(pady=10)

        # --- Table Section ---
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(pady=20, padx=30, fill="both", expand=True)
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(1, weight=1)

        self.results = {}
        fields = [
            ("Target IP", "target"),
            ("Subnet Mask", "mask"),
            ("Network Bits", "n_bits"),
            ("Host Bits", "h_bits"),
            ("Total Hosts", "t_hosts"),
            ("Usable Hosts", "u_hosts"),
            ("Network ID", "n_id"),
            ("Broadcast", "b_cast"),
            ("Usable Range", "range")
        ]

        for i, (label_text, key) in enumerate(fields):
            lbl = ctk.CTkLabel(
                self.table_frame, 
                text=label_text, 
                font=(self.main_font, 14, "bold"), 
                text_color="#39e600", 
                anchor="w"
            )
            lbl.grid(row=i, column=0, padx=20, pady=8, sticky="w")

            val = ctk.CTkLabel(
                self.table_frame, 
                text="--", 
                font=(self.code_font, 14), 
                anchor="e"
            )
            val.grid(row=i, column=1, padx=20, pady=8, sticky="e")
            self.results[key] = val

    def create_decimal(self, bit_list):
        return ".".join([str(int(i, 2)) for i in bit_list])

    def perform_calculation(self):
        try:
            ip_input = self.ip_entry.get().strip()
            mask_input = self.mask_entry.get().strip().replace("/", "")
            
            if not ip_input: return

            ip_parts = ip_input.split('.')
            ip_bin = [format(int(x), '08b') for x in ip_parts]
            n_bits = int(mask_input)
            
            h_bits = 32 - n_bits
            t_hosts = 2**h_bits
            u_hosts = max(0, t_hosts - 2)
            
            mask_str = ("1" * n_bits) + ("0" * h_bits)
            mask_bin = [mask_str[i:i+8] for i in range(0, 32, 8)]

            net_id_bin, bcast_bin = [], []
            for i in range(4):
                n_oct, b_oct = "", ""
                for b_ip, b_mask in zip(ip_bin[i], mask_bin[i]):
                    n_oct += "1" if b_ip == "1" and b_mask == "1" else "0"
                    b_oct += b_ip if b_mask == "1" else "1"
                net_id_bin.append(n_oct)
                bcast_bin.append(b_oct)

            u_start, u_end = net_id_bin[:], bcast_bin[:]
            if u_hosts > 0:
                u_start[3] = format(int(u_start[3], 2) + 1, '08b')
                u_end[3] = format(int(u_end[3], 2) - 1, '08b')
                range_text = f"{self.create_decimal(u_start)} - {self.create_decimal(u_end)}"
            else:
                range_text = "N/A"

            # Update Labels
            self.results["target"].configure(text=f"{ip_input}/{n_bits}", text_color="white")
            self.results["mask"].configure(text=self.create_decimal(mask_bin))
            self.results["n_bits"].configure(text=str(n_bits))
            self.results["h_bits"].configure(text=str(h_bits))
            self.results["t_hosts"].configure(text=f"{t_hosts:,}")
            self.results["u_hosts"].configure(text=f"{u_hosts:,}")
            self.results["n_id"].configure(text=self.create_decimal(net_id_bin))
            self.results["b_cast"].configure(text=self.create_decimal(bcast_bin))
            self.results["range"].configure(text=range_text, text_color="yellow")

        except Exception:
            self.results["target"].configure(text="Input Error!", text_color="red")

if __name__ == "__main__":
    app = SubnetCalculator()
    app.mainloop()