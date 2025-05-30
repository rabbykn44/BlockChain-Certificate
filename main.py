from tkinter import Tk, Text, Label, Button, filedialog, simpledialog, messagebox
from tkinter.ttk import Style, Frame
from hashlib import sha256
import os
import pickle

# Assuming Block and Blockchain classes are implemented separately
from Block import *
from Blockchain import *

# Initialize Blockchain
blockchain = Blockchain()

# Load blockchain from file if exists
if os.path.exists('blockchain_contract.txt') and os.path.getsize('blockchain_contract.txt') > 0:
    try:
        with open('blockchain_contract.txt', 'rb') as file:
            blockchain = pickle.load(file)
    except pickle.UnpicklingError:
        print("Error loading blockchain file. Starting with a new blockchain.")
        blockchain = Blockchain()
else:
    print("No existing blockchain file found. Starting with a new blockchain.")

def save_certificate():
    """Function to save a certificate into the blockchain."""
    text_display.delete('1.0', 'end')
    file_path = filedialog.askopenfilename(title="Select Certificate File", filetypes=[("All Files", "*.*")])

    if not file_path:
        text_display.insert('end', "No file selected for saving.\n")
        return

    with open(file_path, "rb") as f:
        file_data = f.read()

    digital_signature = sha256(file_data).hexdigest()

    # Get user details
    roll_no = simpledialog.askstring("Input", "Enter Roll Number:")
    if not roll_no:
        text_display.insert('end', "Roll Number is required.\n")
        return
    student_name = simpledialog.askstring("Input", "Enter Student Name:")
    if not student_name:
        text_display.insert('end', "Student Name is required.\n")
        return
    contact_no = simpledialog.askstring("Input", "Enter Contact Number:")
    if not contact_no:
        text_display.insert('end', "Contact Number is required.\n")
        return

    # Add data to blockchain
    data = f"{roll_no}#{student_name}#{contact_no}#{digital_signature}"
    blockchain.add_new_transaction(data)
    blockchain.mine_block()

    # Save blockchain to file
    with open('blockchain_contract.txt', 'wb') as file:
        pickle.dump(blockchain, file)

    text_display.insert('end', "Certificate saved to the blockchain.\n")
    text_display.insert('end', f"Digital Signature: {digital_signature}\n")

def validate_certificate():
    """Function to validate a certificate."""
    text_display.delete('1.0', 'end')
    file_path = filedialog.askopenfilename(title="Select Certificate File", filetypes=[("All Files", "*.*")])

    if not file_path:
        text_display.insert('end', "No file selected for validation.\n")
        return

    with open(file_path, "rb") as f:
        file_data = f.read()

    digital_signature = sha256(file_data).hexdigest()
    validation_successful = False

    for block in blockchain.chain[1:]:  # Skip the genesis block
        for transaction in block.transactions:
            parts = transaction.split("#")
            if parts[-1] == digital_signature:
                text_display.insert('end', "Certificate verification successful!\n")
                text_display.insert('end', "Details:\n")
                text_display.insert('end', f"Roll No: {parts[0]}\n")
                text_display.insert('end', f"Student Name: {parts[1]}\n")
                text_display.insert('end', f"Contact No: {parts[2]}\n")
                text_display.insert('end', f"Digital Signature: {parts[3]}\n")
                validation_successful = True
                break

        if validation_successful:
            break

    if not validation_successful:
        text_display.insert('end', "Certificate Verification failed.\n")
        text_display.insert('end', "The certificate may have been tampered with or does not exist in the blockchain.\n")

# Create Main Window
main = Tk()
main.title("Blockchain-Based Certificate Validation")
main.geometry("800x600")

# Style
style = Style()
style.configure('TButton', font=('Helvetica', 12), padding=5)
style.configure('TLabel', font=('Helvetica', 14))

# GUI Components
header_label = Label(main, text="Blockchain-Based Certificate Verification", font=('Helvetica', 18, 'bold'), bg='lightblue')
header_label.pack(fill='x', pady=10)

frame = Frame(main)
frame.pack(pady=20)

text_display = Text(main, height=20, width=80, wrap='word', font=('Courier', 12))
text_display.pack(pady=10)

save_button = Button(frame, text="Save Certificate", command=save_certificate, width=20)
save_button.grid(row=0, column=0, padx=10)

validate_button = Button(frame, text="Varification Certificate", command=validate_certificate, width=20)
validate_button.grid(row=0, column=1, padx=10)

exit_button = Button(frame, text="Exit", command=main.quit, width=20)
exit_button.grid(row=0, column=2, padx=10)

# Run the application
main.mainloop()
