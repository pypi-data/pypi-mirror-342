# searchnarwhal/browser.py

import os
import tkinter as tk
from tkinterweb import HtmlFrame
from tkinter import messagebox
from . import localres  # Absolute import
from . import download

print ("SearchNarwhal Browser Engine 1.0")
print ("Origanlly Developed by Zohan Haque")
print ("Browser is starting.")
print (" ")

class Browser(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.html = HtmlFrame(self)
        self.html.pack(fill="both", expand=True)

        # Path to resources
        self.resource_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Navigation history
        self.history = []
        self.history_index = -1

        # Buttons for navigation
        self.nav_frame = tk.Frame(self)
        self.nav_frame.pack(fill="x")

        self.back_button = tk.Button(self.nav_frame, text="Back", command=self.go_back)
        self.back_button.pack(side="left", padx=5, pady=5)

        self.forward_button = tk.Button(self.nav_frame, text="Forward", command=self.go_forward)
        self.forward_button.pack(side="left", padx=5, pady=5)

        self.reload_button = tk.Button(self.nav_frame, text="Reload", command=self.reload_page)
        self.reload_button.pack(side="left", padx=5, pady=5)

        # Initialize navigation
        self.load_newtab()

    def load_url(self, url):
        if url.startswith("http://") or url.startswith("https://"):
            try:
                self.html.load_website(url)
                self.add_to_history(url)
            except:
                self.load_error_page("err_internet_disconnected.html")
        elif url.startswith("localres:"):
            local_path = localres.convert_to_path(url)
            if os.path.exists(local_path):
                self.html.load_file(local_path)
                self.add_to_history(url)
            else:
                self.load_error_page("notvalidurl.html")
        elif url.strip() == "":
            self.load_newtab()
        else:
            self.load_error_page("unknown.html")

    def load_newtab(self):
        path = os.path.join(self.resource_dir, "newtab.html")
        self._safe_load_file(path)
        self.add_to_history("newtab.html")

    def load_error_page(self, filename):
        path = os.path.join(self.resource_dir, filename)
        self._safe_load_file(path)

    def _safe_load_file(self, path):
        if os.path.exists(path):
            self.html.load_file(path)
        else:
            self.html.set_content(f"<h1>Error</h1><p>Missing resource: {os.path.basename(path)}</p>")

    def add_to_history(self, url):
        if self.history_index != len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        self.history.append(url)
        self.history_index += 1
        self.update_navigation_buttons()

    def go_back(self):
        if self.history_index > 0:
            self.history_index -= 1
            url = self.history[self.history_index]
            self.load_url(url)
        self.update_navigation_buttons()

    def go_forward(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            url = self.history[self.history_index]
            self.load_url(url)
        self.update_navigation_buttons()

    def reload_page(self):
        current_url = self.history[self.history_index]
        self.load_url(current_url)

    def update_navigation_buttons(self):
        if self.history_index > 0:
            self.back_button.config(state="normal")
        else:
            self.back_button.config(state="disabled")

        if self.history_index < len(self.history) - 1:
            self.forward_button.config(state="normal")
        else:
            self.forward_button.config(state="disabled")

    def get_html_frame(self):
        return self.html

    def download_file(self, url):
        download.download(url)
        messagebox.showinfo("Download", f"Download started for {url}")
