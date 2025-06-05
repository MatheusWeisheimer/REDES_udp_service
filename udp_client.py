import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import socket
import struct
import os

def read_doubles_from_file(filepath):
    with open(filepath, 'rb') as f:
        content = f.read(1024)
    try:
        lines = content.decode('utf-8').splitlines()
    except UnicodeDecodeError:
        lines = content.decode('latin1').splitlines()
    doubles = []
    for line in lines:
        try:
            doubles.append(float(line.strip()))
        except ValueError:
            continue
    return doubles

class UDPClientGUI:
    def __init__(self, master):
        self.master = master
        master.title("UDP Client GUI")

        self.filepath = None

        tk.Label(master, text="Server IP:").grid(row=0, column=0, sticky='e')
        self.ip_entry = tk.Entry(master)
        self.ip_entry.insert(0, "127.0.0.1")
        self.ip_entry.grid(row=0, column=1, sticky='w')

        tk.Button(master, text="Select .txt File", command=self.select_file).grid(row=1, column=0, columnspan=2, pady=5)

        self.sum_var = tk.IntVar()
        self.avg_var = tk.IntVar()
        self.minmax_var = tk.IntVar()
        tk.Checkbutton(master, text="Sum", variable=self.sum_var).grid(row=2, column=0, sticky='w')
        tk.Checkbutton(master, text="Average", variable=self.avg_var).grid(row=2, column=1, sticky='w')
        tk.Checkbutton(master, text="Min/Max", variable=self.minmax_var).grid(row=2, column=2, sticky='w')

        tk.Button(master, text="Send", command=self.send_request).grid(row=3, column=0, columnspan=3, pady=5)

        self.result_box = scrolledtext.ScrolledText(master, width=50, height=15)
        self.result_box.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

    def select_file(self):
        self.filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.filepath:
            self.result_box.insert('1.0', f"Selected file: {self.filepath}\n")

    def send_request(self):
        ip = self.ip_entry.get().strip()
        if not ip:
            messagebox.showerror("Error", "Please enter the server IP address.")
            return
        if not self.filepath or not os.path.isfile(self.filepath):
            messagebox.showerror("Error", "Please select a valid .txt file.")
            return
        flags = (self.sum_var.get(), self.avg_var.get(), self.minmax_var.get())
        if not any(flags):
            messagebox.showerror("Error", "Please select at least one operation.")
            return

        doubles = read_doubles_from_file(self.filepath)
        if not doubles:
            messagebox.showerror("Error", "No valid doubles found in file.")
            return

        data = struct.pack('3B', *flags) + struct.pack(f'{len(doubles)}d', *doubles)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.settimeout(2)
            sock.sendto(data, (ip, 2022))
            expected = 0
            if flags[0]: expected += 1
            if flags[1]: expected += 1
            if flags[2]: expected += 2
            response, _ = sock.recvfrom(4096)
            results = struct.unpack(f'{expected}d', response)
            result_strs = []
            idx = 0
            if flags[0]:
                result_strs.append(f"Sum: {results[idx]}")
                idx += 1
            if flags[1]:
                result_strs.append(f"Average: {results[idx]}")
                idx += 1
            if flags[2]:
                result_strs.append(f"Min: {results[idx]}, Max: {results[idx+1]}")
                idx += 2
            self.result_box.insert('1.0', f"Response: {', '.join(result_strs)}\n")
        except Exception as e:
            self.result_box.insert('1.0', f"Error: {e}\n")
        finally:
            sock.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = UDPClientGUI(root)
    root.mainloop()