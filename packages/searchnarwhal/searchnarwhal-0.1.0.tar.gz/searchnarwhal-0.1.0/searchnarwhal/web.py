# web.py
from tkinter import Tk

def run_browser():
    # Import Browser here to avoid circular import issues
    from searchnarwhal.browser import Browser  # Import inside the function
    root = Tk()
    root.title("SearchNarwhal")
    root.geometry("1024x768")
    app = Browser(root)
    app.pack(fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    run_browser()

