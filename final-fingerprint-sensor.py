import tkinter as tk
from tkinter import messagebox, filedialog
import cv2
import os
import numpy as np
import pymongo
from pymongo import MongoClient
from PIL import Image
from io import BytesIO

# MongoDB connection setup
client = MongoClient(
    "",#Paste your connection link to MongoDB databse
    ssl=True,
    tlsAllowInvalidCertificates=True  # Use for testing only, as it disables SSL certificate verification
)
db = client["atm"]  # Database name
collection = db["users"]  # Collection name to store the images and user data

# Create main window
h = tk.Tk()
h.title("Service Bank")
h.geometry("655x655")
h.maxsize(width=650, height=650)
h.minsize(width=600, height=600)

def set_background(window, bg_image_path=None, bg_color=None):
    """
    Sets a background image or color for a Tkinter window.
    :param window: Tkinter window (root or Toplevel)
    :param bg_image_path: Path to the background image file
    :param bg_color: Background color (if no image is provided)
    """
    if bg_image_path:
        try:
            # Load and set the background image
            bg_image = Image.open(bg_image_path)
            bg_image = bg_image.resize((650, 650), Image.ANTIALIAS)  # Resize the image to match the window size
            bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(window, image=bg_photo)
            bg_label.image = bg_photo  # Keep a reference to prevent garbage collection
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load background image.\n{e}")
    elif bg_color:
        # Set the background color
        window.configure(bg=bg_color)

# Apply background to the main window
set_background(h, bg_image_path="bg-t1.jpg")  # Replace with your actual image path


# Registration form
def shyam():
    top = tk.Toplevel()
    top.maxsize(width=650, height=650)
    top.minsize(width=640, height=600)
    head = tk.Label(top, text="Welcome to Registration Form", bg="green", fg="white", font=("", 26)).pack()
 
    # Variables to store user data
    image_path = ""
    
    def submit():
        if en.get() == "" or en2.get() == "":
            messagebox.showwarning("Warning", "Blank Invalid")
        else:
            v = en.get()
            g = int(v)

            v2 = en2.get()
            g2 = str(v2)

            if v == "" or v2 == "":
                messagebox.showwarning("Warning", "Not filled properly")
            else:
                ko = messagebox.showinfo("Info", "Congratulations, you are registered")
                if ko == True:
                    print("hello")
                else:
                    top.destroy()

    # Create input fields
    en = tk.Entry(top, bd=2)
    en.place(x=160, y=150)
    pin = tk.Label(top, text="Enter your new pin:")
    pin.place(x=20, y=150)

    en2 = tk.Entry(top, bd=2)
    en2.place(x=160, y=200)
    pin = tk.Label(top, text="Enter your new name:")
    pin.place(x=20, y=200)

    def select_image():
        nonlocal image_path
        filetypes = (("JPEG files", "*.jpg"), ("PNG files", "*.png"),("BMP files", "*.bmp"), ("All files", "*.*"))
        image_path = filedialog.askopenfilename(title="Select Image", filetypes=filetypes)
        if image_path:
            image_label.config(text="Selected Image: " + image_path)
        else:
            image_label.config(text="No image selected.")

    def save_image():
        if image_path:
            # Open the image and convert it to binary data
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()

            # Insert the image and user info into MongoDB
            document = {
                "name": en2.get(),
                "pin": en.get(),
                "image": image_data  # Store the image as binary data
            }
            collection.insert_one(document)
            messagebox.showinfo(title="Success!", message="Image saved to MongoDB.")

            # Optional: Trigger submit after saving the image
            submit1()
        else:
            messagebox.showerror(title="Error", message="No image selected.")

    select_image_button = tk.Button(top, text="Select Fingerprint", command=select_image)
    select_image_button.place(x=150, y=250)
    image_label = tk.Label(top)
    image_label.pack()

    save_image_button = tk.Button(top, text="Save", command=save_image)
    save_image_button.place(x=280, y=250)

    def submit1():
        su = tk.Button(top, text="SUBMIT", fg="green", command=submit)
        su.place(x=9, y=250)


def depo():
    top2 = tk.Toplevel()
    top2.maxsize(width=650, height=650)
    top2.minsize(width=640, height=600)
    head2 = tk.Label(top2, text="Welcome to Cash Deposit", bg="orange", fg="black", font=("", 26)).pack()

    ent_pin = tk.Entry(top2, bd=2)
    ent_pin.place(x=160, y=150)

    textho = tk.Label(top2, fg="green")
    textho.place(x=170, y=400)

    def upload_file():
        # Select the fingerprint image to upload
        img1_path = filedialog.askopenfilename(title="Select the fingerprint image file",
                                                filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if not img1_path:
            messagebox.showerror("Error", "No image selected.")
            return

        img1 = cv2.imread(img1_path)
        pin = ent_pin.get()
        match_found = False

        # Retrieve the user based on the PIN
        user = collection.find_one({"pin": pin})
        if user:
            stored_image_data = user.get("image")
            if stored_image_data:
                # Convert the stored binary data to an image
                nparr = np.frombuffer(stored_image_data, np.uint8)
                stored_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                # Compare the uploaded image (img1) with the stored image (stored_img)
                if img1.shape == stored_img.shape:
                    difference = cv2.subtract(img1, stored_img)
                    result = cv2.countNonZero(cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY))

                    if result == 0:
                        match_found = True
                        messagebox.showinfo("Image Matched", "Fingerprint matched successfully!")
                        deposit_amount(user)  # Proceed to deposit amount
                    else:
                        messagebox.showerror("Error", "Fingerprint does not match.")
                else:
                    messagebox.showerror("Error", "Fingerprint image size mismatch.")
            else:
                messagebox.showerror("Error", "No fingerprint image found for this PIN.")
        else:
            messagebox.showerror("Error", "Invalid PIN. Please try again.")

        if not match_found:
            messagebox.showerror("Error", "Authentication failed.")

    def deposit_amount(user):
        # Function to deposit amount after successful authentication
        ent_amount = tk.Entry(top2, bd=2)
        ent_amount.place(x=160, y=200)

        amount_label = tk.Label(top2, text="Enter Amount:")
        amount_label.place(x=20, y=200)

        def process_deposit():
            try:
                deposit_value = int(ent_amount.get())
                if deposit_value <= 0:
                    messagebox.showerror("Error", "Amount must be greater than zero.")
                    return

                # Update the user's balance in MongoDB
                new_balance = user.get("balance", 0) + deposit_value
                collection.update_one({"pin": user["pin"]}, {"$set": {"balance": new_balance}})
                textho.config(text=f"Deposit successful!\nNew Balance: {new_balance} Rupees")
                messagebox.showinfo("Success", "Amount deposited successfully!")
            except ValueError:
                messagebox.showerror("Error", "Invalid amount entered. Please enter a valid number.")

        submit_button = tk.Button(top2, text="Deposit", fg="green", command=process_deposit)
        submit_button.place(x=20, y=250)

    # PIN Entry
    pin_label = tk.Label(top2, text="Enter your PIN:")
    pin_label.place(x=20, y=150)

    # Upload Fingerprint Button
    upload_button = tk.Button(top2, text="Upload Fingerprint", width=20, command=upload_file)
    upload_button.place(x=20, y=300)

bt_deposit = tk.Button(text="Cash Deposit", bd=5, command=depo)
bt_deposit.place(x=450, y=110)


def cash():
    top3 = tk.Toplevel()
    top3.maxsize(width=650, height=650)
    top3.minsize(width=640, height=600)
    head2 = tk.Label(top3, text="Welcome to CASH Withdrawal", bg="purple", fg="white", font=("", 26)).pack()

    ent_pin = tk.Entry(top3, bd=2)
    ent_pin.place(x=160, y=150)

    textho4 = tk.Label(top3, fg="green")
    textho4.place(x=170, y=400)

    def upload_filew():
        # Select the fingerprint image to upload
        img1_path = filedialog.askopenfilename(title="Select the fingerprint image file",
                                                filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if not img1_path:
            messagebox.showerror("Error", "No image selected.")
            return

        img1 = cv2.imread(img1_path)
        pin = ent_pin.get()
        match_found = False

        # Retrieve the user based on the PIN
        user = collection.find_one({"pin": pin})
        if user:
            stored_image_data = user.get("image")
            if stored_image_data:
                # Convert the stored binary data to an image
                nparr = np.frombuffer(stored_image_data, np.uint8)
                stored_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                # Compare the uploaded image (img1) with the stored image (stored_img)
                if img1.shape == stored_img.shape:
                    difference = cv2.subtract(img1, stored_img)
                    result = cv2.countNonZero(cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY))

                    if result == 0:
                        match_found = True
                        messagebox.showinfo("Image Matched", "Fingerprint matched successfully!")
                        withdraw_amount(user)  # Proceed to withdraw amount
                    else:
                        messagebox.showerror("Error", "Fingerprint does not match.")
                else:
                    messagebox.showerror("Error", "Fingerprint image size mismatch.")
            else:
                messagebox.showerror("Error", "No fingerprint image found for this PIN.")
        else:
            messagebox.showerror("Error", "Invalid PIN. Please try again.")

        if not match_found:
            messagebox.showerror("Error", "Authentication failed.")

    def withdraw_amount(user):
        # Function to withdraw amount after successful authentication
        ent_amount = tk.Entry(top3, bd=2)
        ent_amount.place(x=200, y=200)

        amount_label = tk.Label(top3, text="Enter Withdrawal Amount:")
        amount_label.place(x=20, y=200)

        def process_withdrawal():
            try:
                withdraw_value = int(ent_amount.get())
                current_balance = user.get("balance", 0)

                if withdraw_value <= 0:
                    messagebox.showerror("Error", "Amount must be greater than zero.")
                elif withdraw_value > current_balance:
                    messagebox.showerror("Error", "Insufficient balance.")
                else:
                    # Deduct the withdrawal amount from the balance
                    new_balance = current_balance - withdraw_value
                    collection.update_one({"pin": user["pin"]}, {"$set": {"balance": new_balance}})
                    textho4.config(text=f"Withdrawal successful!\nNew Balance: {new_balance} Rupees")
                    messagebox.showinfo("Success", "Amount withdrawn successfully!")
            except ValueError:
                messagebox.showerror("Error", "Invalid amount entered. Please enter a valid number.")

        submit_button = tk.Button(top3, text="Withdraw", fg="green", command=process_withdrawal)
        submit_button.place(x=20, y=250)

    # PIN Entry
    pin_label = tk.Label(top3, text="Enter your PIN:")
    pin_label.place(x=20, y=150)

    # Upload Fingerprint Button
    upload_button = tk.Button(top3, text="Upload Fingerprint", width=20, command=upload_filew)
    upload_button.place(x=20, y=300)
bt_withdraw = tk.Button(text="Cash Withdrawal", bd=5, command=cash)
bt_withdraw.place(x=20, y=160)


# Balance check form
def check_balance_form():
    top4 = tk.Toplevel()
    top4.maxsize(width=650, height=650)
    top4.minsize(width=640, height=600)
    head2 = tk.Label(top4, text="Welcome to Balance Check Service", bg="pink", fg="white", font=("", 26)).pack()

    ent7 = tk.Entry(top4, bd=2)
    ent7.place(x=160, y=150)

    def upload_fileb():
        # Select the fingerprint image to upload
        img1_path = filedialog.askopenfilename(title="Select the first image file", filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
        img1 = cv2.imread(img1_path)
        match_found = False

        # Get the PIN entered by the user
        pin = ent7.get()

        # Retrieve the stored fingerprint image from MongoDB
        user = collection.find_one({"pin": pin})
        if user:
            stored_image_data = user.get("image")
            if stored_image_data:
                # Convert the stored binary data to an image
                nparr = np.frombuffer(stored_image_data, np.uint8)
                stored_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                # Compare the uploaded image (img1) with the stored image (stored_img)
                if img1.shape == stored_img.shape:
                    difference = cv2.subtract(img1, stored_img)
                    result = cv2.countNonZero(cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY))

                    if result == 0:
                        messagebox.showinfo("Image Matched", "Fingerprint matched successfully!")
                        print("The images are completely identical")
                        match_found = True

                        # Image matched, now check the balance
                        check_balance(user)  # Pass the user document to the check_balance function
                    else:
                        messagebox.showerror("Error", "Fingerprint does not match.")
                else:
                    messagebox.showerror("Error", "Fingerprint image size mismatch.")
            else:
                messagebox.showerror("Error", "No fingerprint image found in the database.")
        else:
            messagebox.showerror("Error", "Invalid PIN. Please try again.")

    def check_balance(user):
        # Extract balance from the user document
        balance = user.get("balance", 0)
        textho3.config(text=f"Welcome back Mr. {user['name']}\nYour balance: {balance} Rupees")

    b1 = tk.Button(top4, text='Upload Fingerprint', width=20, command=upload_fileb)
    b1.place(x=20, y=300)

    pinvalue2 = tk.Label(top4, text="Enter your PIN:")
    pinvalue2.place(x=20, y=150)

    textho3 = tk.Label(top4, fg="green")
    textho3.place(x=170, y=400)

# Header Section
header = tk.Frame(h)
header.pack(side=tk.TOP)
tk.Label(header, text="Welcome to the ATM Service", fg="white", font=("arial", 33), bg="blue").pack()

# Add Buttons or Other UI Elements
bt_register = tk.Button(h, text="Register", bd=5, command=shyam)
bt_register.place(x=20, y=100)


bt_balance_check = tk.Button(text="Check Balance", bd=5, command=check_balance_form)
bt_balance_check.place(x=450, y=160)

h.mainloop()
