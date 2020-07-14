# main search engine

import tkinter as tk
from PIL import ImageTk, Image
from retriever import initialize, search
import webbrowser
from urllib.request import urlopen
from bs4 import BeautifulSoup

class Engine:
    def __init__(self, width, height):
        self.width = width
        self.master = tk.Tk()
        self.master.title("Search Engine")
        self.master.geometry(f"{width}x{height}")

        logo = ImageTk.PhotoImage(Image.open("logo.png"))
        panel = tk.Label(self.master, image=logo)
        panel.place(relx = 0.5, rely = 0.2, anchor=tk.CENTER)
        
        query = tk.Entry(self.master)
        query.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        
        search_button = tk.Button(self.master, text = "Search", command=lambda q=query: self.retrieve(query.get()))
        search_button.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

        self.result = tk.Label(self.master)
        self.q = tk.Label(self.master)
        self.master.mainloop()

    def retrieve(self, query):
        results = search(query)
        # display results
        self.displayResults(query, results)

    def getPageTitle(self, url):
        soup = BeautifulSoup(urlopen(url), 'lxml')
        return soup.title.string

    def displayResults(self, query, results):
        if len(results) == 0:
            q = tk.Label(self.master, text=f"No results found for {query}", width = self.width)
            q.place(relx=0.5, rely = 0.4, anchor = tk.N)
            y = 0.45
            for i in range(5):
                self.result = tk.Label(self.master, text=f"  \n  ", width = self.width)
                self.result.place(relx=0.5, rely = y, anchor = tk.N)
                y += .1
        else:
            self.q = tk.Label(self.master, text=f"Found {len(results)} results for {query}, here are the top 5 results:", width=self.width)
            self.q.place(relx=0.5, rely = 0.4, anchor = tk.N)
            y = 0.45
            for x in range(0,5):
                try:
                    pageTitle = self.getPageTitle(results[x])
                    self.result = tk.Label(self.master, text=f"{pageTitle}\n{results[x]}", width = self.width)
                except:
                    self.result = tk.Label(self.master, text=f"  \n  ", width = self.width)
                finally:
                    self.result.place(relx=0.5, rely = y, anchor = tk.N)
                    y += .1

if __name__ == "__main__":
    initialize()
    e = Engine(800,600)