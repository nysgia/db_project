import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import PhotoImage
import sqlite3
import pygame  
from datetime import datetime
from PIL import Image, ImageTk
font2 = ("Comic Sans MS", 12, "bold")
font1 = ("Comic Sans MS", 20)
font3= ("Comic Sans MS", 16)
font4= ("Comic Sans MS", 10)
color1= '#112e0b'
color2 = '#05d7ff'
color3='#65e7ff'
color4='#f4baf0'
color5='#280b2e'
skouro='#44b62b'
anoixto='#bef9a2'
class CRUDApp:
    def __init__(self, root):
        
        self.root = root
        self.root.title("CRUD App")
        self.root.geometry("1600x900")   
        self.my_tree = None   
        self.sort_column = None
        self.sort_descending = False
        pygame.mixer.init()
        self.play_music()  
        self.root.maxsize(1920, 1080) 
        self.volume_scale=0    
        self.style=ttk.Style()
        self.style.theme_use("clam")
        self.style.configure('TButton',
                             background=color1,
                             foreground=color4,
                             padding=(10, 5), 
                             bordercolor=color1, 
                             font=font3)
        self.style.configure('Treeview',  
                             foreground=color4,
                            fieldbackground=color1,
                          roewheight=25,
                          font=font4 
                         )
        self.style.configure("labelz.TLabel", background=color1, foreground=color4, font=("Comic Sans MS", 14))
        self.style.configure("title.TLabel", background=color1, foreground=color4, font=("Comic Sans MS", 20))
        self.style.configure("vol.TLabel", background=color5, foreground=color4, font=("Comic Sans MS", 14))

        self.style.map('Treeview',
                       background=[('selected', '#87cefa')], foreground = [('selected', 'black')])
        self.style.map('TButton',
                       foreground=[('active', color5)])
        pygame.mixer.music.set_volume(0) 
        self.current_volume = pygame.mixer.music.get_volume() 
        self.init_database() 
        self.crud_frame = tk.Frame(self.root, bd=2, relief=tk.SOLID) 
        self.crud_frame.pack(side="top", fill="both", expand=True)  
        self.table_names = self.get_table_names()

        self.table_var = tk.StringVar()
        self.table_var.set(self.table_names[0] if self.table_names else "")

        table_dropdown = ttk.Combobox(self.crud_frame, 
                                      textvariable=self.table_var, 
                                      values=self.table_names, 
                                      font=font2)
        table_dropdown.grid(row=0, column=0, padx=10, pady=10)
         
        action_button = ttk.Button(self.crud_frame, 
                                  text="Select", 
                                  command=self.switch_table)
        action_button.grid(row=0, column=1, padx=10, pady=10)

        add_button = ttk.Button(self.crud_frame, 
                               text="Add",  
                               command=self.add_data)
        add_button.grid(row=0, column=5, padx=10, pady=10)

        action_button = ttk.Button(self.crud_frame,  
                                  text="Search" ,
                                  command=self.search_data)
        action_button.grid(row=0, column=2, padx=10, pady=10)
        
        delete_button = ttk.Button(self.crud_frame, 
                                  text="Delete",  
                                  command=self.delete_data)
        delete_button.grid(row=0, column=3, padx=10, pady=10)

        update_button = ttk.Button(self.crud_frame, 
                                  text="Update",
                                  command=self.update_data)
        update_button.grid(row=0, column=4, padx=10, pady=10)

        has_not_paid= ttk.Button(self.crud_frame, 
                                  text="💀",
                                  command=self.display_unpaid_reservations)
        has_not_paid.grid(row=0, column=6, padx=10, pady=10)

        self.fields_frame = tk.Frame(self.root, bd=2, relief=tk.SOLID)  
        self.fields_frame.pack(side="top", fill="both", expand=True)
        self.fields_frame.pack_propagate(False)  

        for i in range(3):
            self.fields_frame.grid_rowconfigure(i, weight=0)
            self.fields_frame.grid_columnconfigure(i, weight=0)  
        self.img_og=Image.open('map.png').resize((650,280))
        self.img_tk=ImageTk.PhotoImage(self.img_og)

        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(side="bottom", 
                              fill="both", 
                              expand=True)
        
        custom_sql_label = ttk.Label(self.root, 
                                    text="Custom SQL Query", 
                                    style="title.TLabel")
        custom_sql_label.pack(side="top", pady=10)

        self.custom_sql_entry = tk.Entry(self.root, 
                                         font=font2,
                                         width=100)
        self.custom_sql_entry.pack(side="top", pady=25, padx=10, expand=True)

        custom_sql_button = ttk.Button(self.root, 
                                      text="Execute", 
                                      command=self.execute_custom_query)
        custom_sql_button.pack(side="top", pady=10)    

        self.speaker_button = tk.Button(self.crud_frame, 
                                        command=self.toggle_music, 
                                        text="🔊", 
                                        font=("Helvetica", 20))
        self.speaker_button.place(relx=0.99, rely=0.9, anchor="se")

        # Volume Bar
        self.volume_label = ttk.Label(self.crud_frame, 
                                     text=f"Volume: {float(self.current_volume * 100)}", 
                                     style="vol.TLabel")
        self.volume_label.place(relx=0.94, rely=0.85, anchor="se")
        

        self.volume_scale = ttk.Scale(self.crud_frame, 
                                      from_=0, to=100, 
                                      orient="horizontal", 
                                      command=self.set_volume ) 
        self.volume_scale.place(relx=0.94, rely=1, anchor="e")
        self.volume_scale.set(float(self.current_volume*100)) 
        self.crud_frame.configure(bg=color5)   
        self.fields_frame.configure(bg=color1)
        self.table_frame.configure(bg=color1)
        self.root.config(bg=color1)
    def execute_custom_query(self):
        selected_table = self.table_var.get()
        custom_query = self.custom_sql_entry.get()

        try: 
            self.cursor.execute(custom_query)
            self.conn.commit()
 
            if custom_query.strip().upper().startswith("SELECT"):
                result = self.cursor.fetchall()
 
                result_window = tk.Toplevel(self.root)
                result_window.title("Query Result")

                tree = ttk.Treeview(result_window)
 
                if result:
                    columns = [desc[0] for desc in self.cursor.description]
                    tree['columns'] = columns
                    for col in columns:
                        tree.heading(col, text=col)
 
                    for row in result:
                        tree.insert("", tk.END, values=row)

                tree.pack(fill="both", expand=True)
            else: 
                self.switch_table()

            messagebox.showinfo("Success", "Custom query executed successfully.")
        except sqlite3.Error as e: 
            messagebox.showerror("Error", f"Error executing custom query:\n{str(e)}")
    def play_music(self):
        
        pygame.mixer.music.load("resources/music/soundtrack.mp3")
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(float(15) / 100.0)
    def set_volume(self, value):
         
        volume = float(value) / 100.0
        pygame.mixer.music.set_volume(volume)
        self.volume_label.config(text=f"Volume: {int(float(value))}")
    def toggle_music(self):
        current_volume = pygame.mixer.music.get_volume()  
        if current_volume == 0.0:  
            self.volume_scale.set(15)   
            self.speaker_button.config(text="🔊")  
        else:    
            self.volume_scale.set(0)  
            self.speaker_button.config(text="🔇")  
    def delete_data(self):
        selected_table = self.table_var.get() 
        selected_item = self.my_tree.selection() 
        first_attribute_name = self.get_first_attribute_name(selected_table)
 
        if selected_item:
            selected_row_id = str(self.my_tree.item(selected_item[0])['values'][0])   
            if selected_table: 
                delete_query = f"DELETE FROM {selected_table} WHERE {first_attribute_name} = ?;"
                self.cursor.execute(delete_query, (selected_row_id,))
                self.conn.commit()
 
                self.switch_table()
            else: 
                messagebox.showwarning("Warning", "Please select a table before deleting.")
        else: 
            messagebox.showwarning("Warning", "Please select a row before deleting.")
    def add_data(self):
        selected_table = self.table_var.get()
        attribute_names = [label.cget("text") for label in self.fields_frame.winfo_children() if isinstance(label, ttk.Label)]
 
        data_to_insert = [entry.get() for entry in self.fields_frame.winfo_children() if isinstance(entry, tk.Entry)]
 
        if all(data_to_insert): 
            placeholders = ', '.join(['?' for _ in attribute_names])
            insert_query = f"INSERT INTO {selected_table} ({', '.join(attribute_names)}) VALUES ({placeholders});"
            self.cursor.execute(insert_query, tuple(data_to_insert))
            self.conn.commit()
 
            self.switch_table()
        else: 
            messagebox.showwarning("Warning", "Please fill in all fields before adding data.")
    def update_data(self):
        selected_table = self.table_var.get()
        selected_item = self.my_tree.selection()
        first_attribute_name = self.get_first_attribute_name(selected_table)

        if selected_item:
            selected_row_id = str(self.my_tree.item(selected_item[0])['values'][0])
            attribute_names = [label.cget("text") for label in self.fields_frame.winfo_children() if isinstance(label, ttk.Label)]
            data_to_update = [entry.get() for entry in self.fields_frame.winfo_children() if isinstance(entry, tk.Entry)]
 
            set_values = [f"{attribute} = ?" for attribute, value in zip(attribute_names, data_to_update) if value]
            if set_values:
                set_clause = ', '.join(set_values)
                update_query = f"UPDATE {selected_table} SET {set_clause} WHERE {first_attribute_name} = ?;"
                self.cursor.execute(update_query, tuple([value for value in data_to_update if value] + [selected_row_id]))
                self.conn.commit()

                self.switch_table()
            else:
                messagebox.showwarning("Warning", "Please fill in at least one field before updating data.")
        else:
            messagebox.showwarning("Warning", "Please select a row before updating.")
    def search_data(self):
        selected_table = self.table_var.get()
        attribute_names = [label.cget("text") for label in self.fields_frame.winfo_children() if isinstance(label, ttk.Label)]
        data_to_search = [entry.get() for entry in self.fields_frame.winfo_children() if isinstance(entry, tk.Entry)]
         
        filled_attributes = [attribute for attribute, value in zip(attribute_names, data_to_search) if value]

        if len(filled_attributes) == 1:
            search_attribute = filled_attributes[0]
            search_value = data_to_search[attribute_names.index(search_attribute)] 

            search_query = f"SELECT * FROM {selected_table} WHERE {search_attribute} = ?;"

            try:
                self.cursor.execute(search_query, (search_value,))
                result = self.cursor.fetchall()

                if result: 
                    result_window = tk.Toplevel(self.root)
                    result_window.title("Search Result")

                    tree = ttk.Treeview(result_window, style="Treeview")
 
                    columns = [desc[0] for desc in self.cursor.description]
                    tree['columns'] = columns
                    for col in columns:
                        tree.column(col, anchor="center")
                        tree.heading(col, text=col, anchor=tk.N)
                        tree.tag_configure("evenrow", background=color1, font=font2)
                        tree.tag_configure("oddrow", background=color5, font=font2)
 
                    for row_index, row in enumerate(result):
                        tags = ("evenrow",) if row_index % 2 == 0 else ("oddrow",)
                        tree.insert("", tk.END, values=row, tags=tags)

                    tree.pack(fill="both", expand=True)
                else:
                    messagebox.showinfo("Search Result", "No results found.")
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error executing search query:\n{str(e)}")
    def init_database(self): 
        self.conn = sqlite3.connect("camping_org.db")
        self.cursor = self.conn.cursor() 
    def get_first_attribute_name(self, table_name): 
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        table_info = self.cursor.fetchone()
 
        if table_info:
            first_attribute_name = table_info[1]
            return first_attribute_name
        else:
            return None
    def get_table_names(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [table[0] for table in self.cursor.fetchall()]
    def switch_table(self):
        selected_table = self.table_var.get()

        self.cursor.execute(f"PRAGMA table_info({selected_table});")
        table_info = self.cursor.fetchall()
        attribute_names = [info[1] for info in table_info]
 
        for widget in self.fields_frame.winfo_children():
            widget.destroy()

        for widget in self.table_frame.winfo_children():
            widget.destroy()
 
        for index, attribute in enumerate(attribute_names):
            label = ttk.Label(self.fields_frame, text=attribute,style="labelz.TLabel")
            label.grid(row=index, column=0, padx=5, pady=5)

            entry = tk.Entry(self.fields_frame,
                                         width=50,font=font2)
            entry.grid(row=index, column=1, padx=5, pady=5)
         
        image_label = tk.Label(self.fields_frame, image=self.img_tk)
        image_label.place(relx=0.5, rely=0.5, anchor="w")

        tree_scroll = tk.Scrollbar(self.table_frame)
        tree_scroll.pack(side="right", fill="y")
        self.my_tree = ttk.Treeview(self.table_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        self.my_tree.pack(fill="both", expand=True)

        self.my_tree['columns'] = tuple(attribute_names)

        self.my_tree.column("#0", width=0, stretch="no")
        self.calculate_and_update_cost()
        for attribute in attribute_names:
            self.my_tree.column(attribute, anchor="center")
            self.my_tree.heading(attribute, text=attribute, anchor=tk.N)
            self.my_tree.heading(attribute, command=lambda col=attribute: self.sort_tree(col))
 
        self.cursor.execute(f"SELECT * FROM {selected_table};")
        data = self.cursor.fetchall()
        
        self.my_tree.tag_configure("evenrow", background=color1, font=font2)   
        self.my_tree.tag_configure("oddrow", background=color5,font=font2)    

        for row_index, row in enumerate(data):
            tags = ("evenrow",) if row_index % 2 == 0 else ("oddrow",)
            if selected_table == 'camperEq':
                self.my_tree.insert("", tk.END, values=row, tags=tags)
            else:

                self.my_tree.insert("", tk.END, values=row, tags=tags)  
    def display_unpaid_reservations(self):
        try:
            self.cursor.execute("SELECT reservationID, camperID, totalcost,checkout FROM reservation")
            reservations = self.cursor.fetchall()
            
            unpaid_data = []

            for reservation in reservations:
                reservationID, camperID, total_cost,checkout = reservation

                self.cursor.execute("SELECT SUM(amount) FROM payment WHERE reservationID = ?", (reservationID,))
                payment_amount_result = self.cursor.fetchone()
                payment_amount = payment_amount_result[0] if payment_amount_result[0] is not None else 0

                if payment_amount < total_cost:
                    self.cursor.execute("SELECT fname,lname FROM camper WHERE camperID = ?", (camperID,))
                    remaining_name = self.cursor.fetchone() 
                    full_name = remaining_name[0] + " " + remaining_name[1]
                    remaining_amount = total_cost - payment_amount
                    unpaid_data.append((full_name,reservationID, remaining_amount,checkout))
            
            if unpaid_data: 
                result_window = tk.Toplevel(self.root)
                result_window.title("Has not paid")

                tree = ttk.Treeview(result_window, style="Treeview") 
                tree['columns'] = ("Name", "reservationID", "Remaining Amount", "Since")

# Set the column headings
                for col in range(4):
                    tree.heading(tree['columns'][col], text=tree['columns'][col], anchor=tk.N)

                # Configure and add tags for alternate row colors
                for col in range(4):
                    tree.column(tree['columns'][col], anchor="center")
                    tree.tag_configure("evenrow", background=color1, font=font2)
                    tree.tag_configure("oddrow", background=color5, font=font2)

                i = 0
                for row in unpaid_data:
                    tags = ("evenrow",) if i % 2 == 0 else ("oddrow",)
                    tree.insert("", tk.END, values=row, tags=tags)
                    i += 1

                tree.pack(fill="both", expand=True)
            else:
                messagebox.showinfo("No Unpaid Reservations", "All reservations are fully paid.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error retrieving unpaid reservations:\n{str(e)}")
  
    def sort_tree(self, column): 
        data = [(self.my_tree.set(child, column), child) for child in self.my_tree.get_children('')]

        data.sort(reverse=self.sort_descending)
        for index, item in enumerate(data):
            self.my_tree.move(item[1], '', index)
 
        self.sort_descending = not self.sort_descending      
    def calculate_and_update_cost(self):
        self.cursor.execute("SELECT reservationID, camperID, checkin, checkout, campsiteID FROM reservation")
        reservations = self.cursor.fetchall()
        for reservation in reservations:
            reservationID, camperID, checkin, checkout, campsiteID = reservation
             
            self.cursor.execute("SELECT dailyprice FROM campsite WHERE campsiteID = ?", (campsiteID,))
            campsite_result = self.cursor.fetchone()

            if campsite_result is not None:
                dailyprice = campsite_result[0]
 
                checkin_date = datetime.strptime(checkin, '%d/%m/%y')
                checkout_date = datetime.strptime(checkout, '%d/%m/%y')
                days_stayed = (checkout_date - checkin_date).days
 
                stay_cost = days_stayed * dailyprice  
                self.cursor.execute("SELECT activityID FROM activityRes WHERE reservationID = ?", (reservationID,))
                activities_done = self.cursor.fetchall() 
                total_activity_cost = 0
                items_cost = 0
                for activity_id in activities_done:
                    self.cursor.execute("SELECT cost FROM activity WHERE activityID =?", activity_id)
                    activity_cost = self.cursor.fetchone()
                    if activity_cost is not None:
                        total_activity_cost += activity_cost[0]
                    else:
                        print(f"Error: Activity with ID {activity_id} not found in the activity table.")
                total_cost = stay_cost + total_activity_cost

                self.cursor.execute("SELECT equipmentID FROM camperEq WHERE camperID = ?", (camperID,))
                eq_used = self.cursor.fetchall()  
                for eq in eq_used:
                     
                    self.cursor.execute("SELECT cost FROM equipment WHERE equipmentID = ?", (eq[0],))
                    item_price=self.cursor.fetchone()
                    
                    items_cost += item_price[0]
                

                total_cost = total_cost + items_cost 
                self.cursor.execute("UPDATE reservation SET totalcost = ? WHERE reservationID = ?", (total_cost, reservationID))
                self.conn.commit()

            else:
                print(f"Error: No campsite found for reservationID {reservationID}.")         
   
if __name__ == "__main__":
    root = tk.Tk()
    app = CRUDApp(root)
    root.mainloop()