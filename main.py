import numpy as np
from digitalsignalgenerator import DigitalSignalGenerator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext



class DigitalSignalGeneratorGUI:


    def __init__(self, root):
        self.root = root
        self.root.title("Digital Signal Generator")
        self.root.geometry("1400x900")
        self.root.configure(bg="#f0f0f0")

        self.generator = DigitalSignalGenerator()
        self.current_data = ""
        self.current_signal = None
        self.current_time = None
        self.current_scheme = None

        self.setup_ui()

    def setup_ui(self):


        title_frame = tk.Frame(self.root, bg="#2c3e50", pady=10)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(title_frame, text=" Digital Signal Generator ",
                               font=("Arial", 16, "bold"), bg="#2c3e50", fg="white")
        title_label.pack()


        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


        left_panel = ttk.LabelFrame(main_container, text="Input Controls", padding=10)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        ttk.Label(left_panel, text="Input Type:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=5)
        self.input_type = tk.StringVar(value="digital")
        ttk.Radiobutton(left_panel, text="Digital Input", variable=self.input_type,
                        value="digital", command=self.on_input_type_change).pack(anchor=tk.W)
        ttk.Radiobutton(left_panel, text="Analog Input (PCM/DM)", variable=self.input_type,
                        value="analog", command=self.on_input_type_change).pack(anchor=tk.W)

        self.binary_frame = ttk.Frame(left_panel)
        self.binary_frame.pack(fill=tk.X, pady=10)
        ttk.Label(self.binary_frame, text="Binary Data:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.binary_input = ttk.Entry(self.binary_frame, width=30, font=("Arial", 10))
        self.binary_input.pack(fill=tk.X, pady=5)
        self.binary_input.insert(0, "1100100100110")

        self.analog_frame = ttk.Frame(left_panel)
        ttk.Label(self.analog_frame, text="Modulation:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.modulation = tk.StringVar(value="pcm")
        ttk.Radiobutton(self.analog_frame, text="PCM (8-bit)", variable=self.modulation, value="pcm").pack(anchor=tk.W)
        ttk.Radiobutton(self.analog_frame, text="Delta Modulation", variable=self.modulation, value="dm").pack(
            anchor=tk.W)

        ttk.Label(self.analog_frame, text="Signal Type:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 0))
        self.signal_type = tk.StringVar(value="sine")
        ttk.Radiobutton(self.analog_frame, text="Sine Wave", variable=self.signal_type, value="sine").pack(anchor=tk.W)
        ttk.Radiobutton(self.analog_frame, text="Cosine Wave", variable=self.signal_type, value="cosine").pack(
            anchor=tk.W)
        ttk.Radiobutton(self.analog_frame, text="Square Wave", variable=self.signal_type, value="square").pack(
            anchor=tk.W)

        ttk.Label(left_panel, text="Line Encoding:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
        self.encoding_scheme = tk.StringVar(value="nrz_l")
        for text, value in [("NRZ-L", "nrz_l"), ("NRZ-I", "nrz_i"), ("Manchester", "manchester"),
                            ("Diff Manchester", "diff_manchester"), ("AMI", "ami")]:
            ttk.Radiobutton(left_panel, text=text, variable=self.encoding_scheme, value=value).pack(anchor=tk.W)

        self.scrambling_frame = ttk.LabelFrame(left_panel, text="Scrambling (AMI only)", padding=5)
        self.scrambling_frame.pack(fill=tk.X, pady=10)
        self.use_scrambling = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.scrambling_frame, text="Apply Scrambling", variable=self.use_scrambling).pack(anchor=tk.W)
        ttk.Label(self.scrambling_frame, text="Type:", font=("Arial", 9)).pack(anchor=tk.W)
        self.scrambling_type = tk.StringVar(value="b8zs")
        ttk.Radiobutton(self.scrambling_frame, text="B8ZS", variable=self.scrambling_type, value="b8zs").pack(
            anchor=tk.W, padx=20)
        ttk.Radiobutton(self.scrambling_frame, text="HDB3", variable=self.scrambling_type, value="hdb3").pack(
            anchor=tk.W, padx=20)

        button_frame = ttk.Frame(left_panel)
        button_frame.pack(fill=tk.X, pady=10)
        ttk.Button(button_frame, text="Generate Signal", command=self.generate_signal).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_all).pack(side=tk.LEFT, padx=5)


        right_panel = ttk.Frame(main_container)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.fig = Figure(figsize=(8, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


        bottom_panel = ttk.LabelFrame(self.root, text="Output & Analysis", padding=10)
        bottom_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.output_text = scrolledtext.ScrolledText(bottom_panel, height=8, font=("Courier", 9), wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True)


        decoder_frame = ttk.Frame(self.root)
        decoder_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(decoder_frame, text=" Decode Signal", command=self.decode_signal).pack(side=tk.LEFT, padx=5)

        main_container.columnconfigure(1, weight=1)
        main_container.rowconfigure(0, weight=1)

    def on_input_type_change(self):

        if self.input_type.get() == "digital":
            self.binary_frame.pack(fill=tk.X, pady=10)
            self.analog_frame.pack_forget()
        else:
            self.binary_frame.pack_forget()
            self.analog_frame.pack(fill=tk.X, pady=10)

    def generate_analog_signal(self):

        t = np.linspace(0, 2 * np.pi, 50)
        signal_type = self.signal_type.get()
        if signal_type == "sine":
            return np.sin(t)
        elif signal_type == "cosine":
            return np.cos(t)
        else:
            return np.sign(np.sin(t))

    def generate_signal(self):

        try:
            self.output_text.delete(1.0, tk.END)

            if self.input_type.get() == "digital":
                data = self.binary_input.get().strip()
                if not data or not all(c in '01' for c in data):
                    messagebox.showerror("Error", "Enter valid binary string!")
                    return
                self.current_data = data
            else:
                analog_signal = self.generate_analog_signal()
                self.current_data = self.generator.pcm_encode(analog_signal,
                                                              8) if self.modulation.get() == "pcm" else self.generator.delta_modulation(
                    analog_signal, 0.15)

            palindrome, start, length = self.generator.longest_palindrome_manacher(self.current_data)
            scheme = self.encoding_scheme.get()
            self.current_scheme = scheme

            scheme_map = {
                "nrz_l": ("NRZ-L", self.generator.nrz_l),
                "nrz_i": ("NRZ-I", self.generator.nrz_i),
                "manchester": ("Manchester", self.generator.manchester),
                "diff_manchester": ("Differential Manchester", self.generator.differential_manchester),
                "ami": ("AMI", self.generator.ami)
            }

            scheme_name, encoder = scheme_map[scheme]
            self.current_time, self.current_signal = encoder(self.current_data)

            scrambled_data = None
            if scheme == "ami" and self.use_scrambling.get():
                scrambled_data = self.generator.b8zs_scramble(
                    self.current_data) if self.scrambling_type.get() == "b8zs" else self.generator.hdb3_scramble(
                    self.current_data)

            output = f"{'=' * 60}\nSIGNAL GENERATION REPORT\n{'=' * 60}\n\n"
            output += f"Input Data: {self.current_data[:50]}{'...' if len(self.current_data) > 50 else ''}\n"
            output += f"Data Length: {len(self.current_data)} bits\n"
            output += f"Encoding: {scheme_name}\n\n"
            output += f"{'=' * 60}\nPALINDROME \n{'=' * 60}\n"


            if scrambled_data:
                output += f"{'=' * 60}\nSCRAMBLING\n{'=' * 60}\n"
                output += f"Type: {self.scrambling_type.get().upper()}\n"
                output += f"Data: {scrambled_data[:50]}{'...' if len(scrambled_data) > 50 else ''}\n\n"


            output += f"Mean: {np.mean(self.current_signal):.4f}, Std: {np.std(self.current_signal):.4f}\n\n"
            output += f"Click Decode button for decoding \n"

            self.output_text.insert(tk.END, output)
            self.plot_signal(scheme_name)
            messagebox.showinfo("Success", "Signal generated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

    def plot_signal(self, scheme_name):

        self.ax.clear()
        self.ax.plot(self.current_time, self.current_signal, linewidth=2, label="Signal")
        self.ax.set_title(f"{scheme_name} Encoding", fontsize=12, fontweight='bold')
        self.ax.set_xlabel("Time (bits)")
        self.ax.set_ylabel("Voltage")
        self.ax.grid(True, alpha=0.3)
        self.ax.set_ylim(-1.5, 1.5)

        for i in range(min(20, len(self.current_data))):
            bit = self.current_data[i]
            self.ax.text(i + 0.5, 1.3, bit, ha='center', fontsize=9,
                         bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))

        self.ax.legend(loc='upper right')
        self.fig.tight_layout()
        self.canvas.draw()

    def decode_signal(self):

        if self.current_signal is None:
            messagebox.showwarning("Warning", "Generate a signal first!")
            return

        try:
            decode_map = {
                "nrz_l": self.generator.decode_nrz_l,
                "nrz_i": self.generator.decode_nrz_i,
                "manchester": self.generator.decode_manchester,
                "diff_manchester": self.generator.decode_differential_manchester,
                "ami": self.generator.decode_ami
            }

            decoded = decode_map[self.current_scheme](self.current_signal)
            accuracy = sum(c1 == c2 for c1, c2 in zip(self.current_data, decoded)) / len(self.current_data) * 100

            current_output = self.output_text.get(1.0, tk.END)
            decode_report = f"\n{'=' * 60}\nDECODING \n{'=' * 60}\n"
            decode_report += f"Original:  {self.current_data[:50]}{'...' if len(self.current_data) > 50 else ''}\n"
            decode_report += f"Decoded:   {decoded[:50]}{'...' if len(decoded) > 50 else ''}\n"

            decode_report += f"Correct: {sum(c1 == c2 for c1, c2 in zip(self.current_data, decoded))}/{len(self.current_data)}\n"

            if accuracy == 100.0:
                decode_report += f" decode done successfully\n"

            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, current_output + decode_report)
            messagebox.showinfo("Decoding Complete", f"Success")

        except Exception as e:
            messagebox.showerror("Error", f"Decoding failed: {str(e)}")

    def clear_all(self):

        self.binary_input.delete(0, tk.END)
        self.binary_input.insert(0, "1100100100110")
        self.output_text.delete(1.0, tk.END)
        self.ax.clear()
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = DigitalSignalGeneratorGUI(root)
    root.mainloop()