import customtkinter
from CTkDateEntry import CTkDateEntry  # Import the custom date entry widget

def get_date():
    print("Selected Date:", date_entry.get_date())

root = customtkinter.CTk()
root.geometry("400x200")

# Create the date entry widget
date_entry = CTkDateEntry(root, selectmode="day", year=2024, month=1, day=1)
date_entry.pack(pady=20)

# Button to retrieve the selected date
button = customtkinter.CTkButton(root, text="Get Date", command=get_date)
button.pack(pady=10)

root.mainloop()