import tkinter as tk
from tkinter import messagebox, ttk
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import threading
import webbrowser

class Game:
    def __init__(self, root):
        self.root = root
        self.root.geometry("680x680")
        self.root.title("Article Search App - Dark Theme")
        self.root.resizable(True, True)

        #Dark Theme
        self.BG_DARK = "#1e1e1e"     
        self.BG_PANEL = "#252526"      
        self.BG_ENTRY = "#3c3c3c"       
        self.FG_TEXT = "#e0e0e0"        
        self.ACCENT_GREEN = "#4caf50" 
        self.ACCENT_HOVER = "#45a049"   

        
        self.root.configure(bg=self.BG_DARK)

        
        self.setup_styles()

        
        self.label_title = tk.Label(
            root, 
            text="Enter Your Search", 
            font=("Arial", 16, "bold"),
            bg=self.BG_DARK,
            fg="#ffffff"
        )
        self.label_title.pack(pady=15)        

        
        self.frame_search = tk.Frame(root, bg=self.BG_DARK)
        self.frame_search.pack(pady=5)

        self.entry_task = tk.Entry(
            self.frame_search, 
            font=("Times New Roman", 12), 
            width=35,
            bg=self.BG_ENTRY,
            fg="#ffffff",
            insertbackground="magenta", 
            relief="flat",
            bd=5
        )
        self.entry_task.pack(side="left", padx=5)
        self.entry_task.focus()
        self.entry_task.bind("<Return>", lambda event: self.start_search())

        self.btn_add = tk.Button(
            self.frame_search, 
            text="🔍 Search", 
            font=("Arial", 10, "bold"),
            bg=self.ACCENT_GREEN, 
            fg="white", 
            activebackground=self.ACCENT_HOVER,
            activeforeground="white",
            relief="flat",
            padx=10,
            pady=3,
            command=self.start_search
        )
        self.btn_add.pack(side="left", padx=5)

        
        self.frame_results = tk.Frame(root, bg=self.BG_DARK)
        self.frame_results.pack(fill="both", expand=True, padx=15, pady=15)

        # Text Widget
        self.text_results = tk.Text(
            self.frame_results, 
            wrap="word", 
            font=("Arial", 10),
            bg=self.BG_ENTRY,
            fg=self.FG_TEXT,
            insertbackground="white",
            selectbackground="#04395e", 
            selectforeground="#ffffff",
            relief="flat",
            bd=8
        )
        self.text_results.pack(side="left", fill="both", expand=True)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.frame_results, command=self.text_results.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.text_results.config(yscrollcommand=self.scrollbar.set)

        self.text_results.tag_config("title", font=("Arial", 11, "bold"), foreground="#4fc3f7")
        self.text_results.tag_config("summary", font=("Arial", 9, "italic"), foreground="#cccccc")
        self.text_results.tag_config("link", font=("Arial", 9, "underline"), foreground="#81c784")
        self.text_results.tag_config("separator", foreground="#555555")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TScrollbar", 
                        background="#333333", 
                        troughcolor=self.BG_DARK, 
                        bordercolor=self.BG_DARK, 
                        arrowcolor="#ffffff")

    def start_search(self):
        query = self.entry_task.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Stop messing and enter a valid entry")
            return

        self.btn_add.config(state="disabled", text="Searching...")
        self.text_results.delete("1.0", tk.END)
        self.text_results.insert(tk.END, "Fetching top 5 articles, please wait...\n")

        threading.Thread(target=self.fetch_arxiv_data, args=(query,), daemon=True).start()

    def fetch_arxiv_data(self, query):
        try:
            encoded_query = urllib.parse.quote(query)
            url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results=5&sortBy=relevance&sortOrder=descending"

            response = urllib.request.urlopen(url)
            xml_data = response.read()

            root = ET.fromstring(xml_data)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            entries = root.findall('atom:entry', ns)

            self.root.after(0, lambda: self.display_results(entries))

        except Exception as e:
            self.root.after(0, lambda: self.show_error(str(e)))

    def display_results(self, entries):
        self.text_results.delete("1.0", tk.END)
        self.btn_add.config(state="normal", text="🔍 Search")

        if not entries:
            self.text_results.insert(tk.END, "No articles found for your query. Sorry... Please try a search engine instead.")
            return

        for i, entry in enumerate(entries, 1):
            title = entry.find('atom:title', {'atom': 'http://www.w3.org/2005/Atom'}).text.strip().replace('\n', ' ')
            summary = entry.find('atom:summary', {'atom': 'http://www.w3.org/2005/Atom'}).text.strip().replace('\n', ' ')
            link = entry.find('atom:id', {'atom': 'http://www.w3.org/2005/Atom'}).text.strip()

            
            self.text_results.insert(tk.END, f"{i}. {title}\n", "title")

            
            self.text_results.insert(tk.END, f"Summary: {summary[:250]}...\n", "summary")

            # Link (works)
            tag_name = f"link_{i}"
            self.text_results.insert(tk.END, f"Link: {link}\n", ("link", tag_name))
            
            self.text_results.tag_bind(tag_name, "<Button-1>", lambda event, url=link: webbrowser.open(url))
            self.text_results.tag_bind(tag_name, "<Enter>", lambda event: self.text_results.config(cursor="hand2"))
            self.text_results.tag_bind(tag_name, "<Leave>", lambda event: self.text_results.config(cursor=""))

            
            self.text_results.insert(tk.END, "\n" + "─"*70 + "\n\n", "separator")

    def show_error(self, error_msg):
        self.text_results.delete("1.0", tk.END)
        self.text_results.insert(tk.END, f"An error occurred: {error_msg}")
        self.btn_add.config(state="normal", text="🔍 Search")


if __name__ == "__main__":
    root = tk.Tk()
    app = Game(root)
    root.mainloop()