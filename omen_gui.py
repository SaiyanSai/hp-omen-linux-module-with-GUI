import tkinter as tk
from tkinter import colorchooser
import subprocess
import os

# Path based on the README.md documentation
ZONE_PATH = "/sys/devices/platform/hp-wmi/rgb_zones/"
# Four distinct zones as defined in the driver source
ZONES = ["zone00", "zone01", "zone02", "zone03"]

class OmenGui:
    def __init__(self, root):
        self.root = root
        self.root.title("HP Omen RGB Control")
        self.root.geometry("450x350")

        tk.Label(root, text="HP Omen Keyboard Zones", font=("Arial", 14, "bold")).pack(pady=15)

        for i, zone in enumerate(ZONES):
            frame = tk.Frame(root)
            # Fixed the typo: changed 'px' to 'padx'
            frame.pack(pady=5, fill=tk.X, padx=20)
            
            tk.Label(frame, text=f"Keyboard Zone {i}:", font=("Arial", 10)).pack(side=tk.LEFT)
            btn = tk.Button(frame, text="Select Color", width=15, 
                            command=lambda z=zone: self.set_color(z))
            btn.pack(side=tk.RIGHT)

        tk.Button(root, text="Set All Zones to Same Color", bg="#333", fg="white", 
                  font=("Arial", 10, "bold"), command=self.set_all).pack(pady=25)

    def apply_rgb(self, zone, hex_color):
        # Driver expects 24-bit hex RGB format
        hex_val = hex_color.replace("#", "")
        path = os.path.join(ZONE_PATH, zone)
        
        # Using sudo via bash -c to handle the redirection
        cmd = f"echo {hex_val} > {path}"
        try:
            subprocess.run(["sudo", "bash", "-c", cmd], check=True)
        except subprocess.CalledProcessError:
            print(f"Error: Could not write to {zone}. Check permissions.")

    def set_color(self, zone):
        with open(f'{zone_path}/{zone}', 'rt') as f:
            current = f.readline().strip().replace(' ', '').split(',')
        colors = [0, 0, 0]
        for c in current:
            colon = c.index(':') + 1
            if 'red' in c:
                colors[0] = int(c[colon:])
                continue
            if 'green' in c:
                colors[1] = int(c[colon:])
                continue
            if 'blue' in c:
                colors[2] = int(c[colon:])
                
        color = colorchooser.askcolor(title=f"Choose color for {zone}", color=tuple(colors))
        if color[1]:
            self.apply_rgb(zone, color[1])

    def set_all(self):
        color = colorchooser.askcolor(title="Choose color for ALL zones")
        if color[1]:
            for zone in ZONES:
                self.apply_rgb(zone, color[1])

if __name__ == "__main__":
    root = tk.Tk()
    if not os.path.exists(ZONE_PATH):
        tk.Label(root, text="Error: Driver path not found!\nIs the module loaded?", 
                 fg="red", font=("Arial", 12, "bold")).pack(pady=50)
    else:
        app = OmenGui(root)
    root.mainloop()