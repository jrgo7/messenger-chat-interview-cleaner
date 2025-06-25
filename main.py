import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.minsize(400, 300)
        self.init_main_widgets()
        self.init_menu()

        self.INTERVIEWER = 0
        self.INTERVIEWEE = 1
        self.interviewer_match = {"\nInterviewer:"}
        self.interviewee_match = {"\nInterviewee:"}
        self.delete_match = {"Edited"}

    def init_main_widgets(self):
        ttk.Label(text="Messenger Interview Find and Replacer").pack()

        btn_frame = ttk.Frame()
        btn_frame.pack(side=tk.LEFT, fill=tk.X, anchor="n")
        ttk.Button(
            master=btn_frame, text="Select file...", command=self.ask_transcript
        ).pack(fill=tk.X)
        ttk.Button(
            master=btn_frame, text="Process transcript", command=self.process_transcript
        ).pack(fill=tk.X)
        ttk.Button(
            master=btn_frame, text="Save as...", command=self.save_as
        ).pack(fill=tk.X)

        self.list_items = tk.Variable()
        self.listbox = tk.Listbox(listvariable=self.list_items)
        self.listbox.bind("<Button-3>", self.right_click_select)
        self.listbox.pack(expand=True, fill=tk.BOTH, anchor="n")

        self.set_common_padding()

    def right_click_select(self, event):
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(self.listbox.nearest(event.y))
        self.listbox.activate(self.listbox.nearest(event.y))

    def set_common_padding(self, padx=10, pady=10):
        for child in self.winfo_children():
            child.pack_configure(padx=padx, pady=pady)

    def init_menu(self):
        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(
            label='Mark as "Interviewer:"', command=self.mark_as_interviewer
        )
        self.popup_menu.add_command(
            label='Mark as "Interviewee:"', command=self.mark_as_interviewee
        )
        self.popup_menu.add_command(
            label="Mark for deletion", command=self.mark_for_deletion
        )
        self.popup_menu.add_command(label="Unmark", command=self.unmark)
        self.bind("<Button-3>", self.popup)

    def popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def ask_transcript(self):
        file_name = filedialog.askopenfilename()
        with open(file_name, mode='r', encoding='utf-8') as file_pointer:
            lines = list(map(lambda line: line.strip("\n"), file_pointer.readlines()))
        self.list_items.set(lines)
        self.display_lines()

    def save_as(self):
        file_name = filedialog.asksaveasfilename()
        lines = self.list_items.get()
        with open(file_name, mode='w', encoding='utf-8') as file_pointer:
            file_pointer.write("\n".join(lines))

    def display_lines(self):
        for i, line in enumerate(self.list_items.get()):
            if line in self.interviewer_match:
                self.listbox.itemconfig(i, bg="blue", fg="white")
            elif line in self.interviewee_match:
                self.listbox.itemconfig(i, bg="green", fg="white")
            elif line in self.delete_match:
                self.listbox.itemconfig(i, bg="red", fg="white")
            else:
                self.listbox.itemconfig(i, bg="white", fg="black")

    def get_line_selected(self):
        lines = self.list_items.get()
        index = self.listbox.curselection()[0]
        return lines[index]

    def mark_as_interviewer(self):
        self.interviewer_match.add(self.get_line_selected())
        self.display_lines()

    def mark_as_interviewee(self):
        self.interviewee_match.add(self.get_line_selected())
        self.display_lines()

    def mark_for_deletion(self):
        self.delete_match.add(self.get_line_selected())
        self.display_lines()

    def unmark(self):
        try:
            self.interviewer_match.remove(self.get_line_selected())
        finally:
            pass
        try:
            self.interviewee_match.remove(self.get_line_selected())
        finally:
            pass
        try:
            self.delete_match.remove(self.get_line_selected())
        finally:
            pass
        self.display_lines()

    def process_transcript(self):
        print(f"{self.interviewee_match = }\n{self.interviewer_match = }")
        filtered_lines = []
        mode = None
        for line in self.list_items.get():
            if line in self.delete_match:
                continue
            elif line in self.interviewer_match:
                if mode != self.INTERVIEWER:
                    filtered_lines.append("\nInterviewer:")
                    mode = self.INTERVIEWER
            elif line in self.interviewee_match:
                if mode != self.INTERVIEWEE:
                    filtered_lines.append("\nInterviewee:")
                    mode = self.INTERVIEWEE
            elif line:
                filtered_lines.append(line)
        self.listbox.selection_clear(0, tk.END)
        self.list_items.set(filtered_lines)
        self.display_lines()


app = App()
app.title("Hello")
app.mainloop()
