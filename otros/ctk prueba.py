import customtkinter as ctk

# Create the main window
app = ctk.CTk()
app.geometry("400x300")

# Create a CTkFrame with rounded corners
rounded_frame = ctk.CTkFrame(app, width=200, height=150, corner_radius=20)
rounded_frame.pack(pady=20)

# Add a label inside the frame
label = ctk.CTkLabel(rounded_frame, text="This is a rounded frame!")
label.pack(pady=20,padx=20)

app.mainloop()