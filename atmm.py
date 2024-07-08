import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as pdf_canvas
from datetime import datetime

class ATM:
    def __init__(self, root):
        # Initialize the ATM with its main window
        self.root = root
        root.geometry("800x600")  # Set window size
        self.root.title("Pythondex ATM")  # Set window title
        self.user = {'card_number': '12345678', 'pin': 1234, 'balance': 1000, 'transaction_history': []}

        # Load and resize the background image
        try:
            original_image = Image.open("background.jpg")
            resized_image = original_image.resize((800, 600), Image.LANCZOS)
            self.background_image = ImageTk.PhotoImage(resized_image)
        except Exception as e:
            # Show error message if background image fails to load
            messagebox.showerror("Error", f"Failed to load background image: {e}")
            self.root.destroy()  # Close the window if image load fails
            return
        
        # Create a Canvas widget to hold the background image
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        
        # Set the background image on the canvas
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        # Add the company name label at the top
        self.company_name_label = tk.Label(root, text="AVINASH ATM", font=("Helvetica", 24, "bold"), bg="lightblue")
        self.canvas.create_window(400, 50, window=self.company_name_label)  # Centered at the top

        # Add card number input label and entry field
        self.card_number_label = tk.Label(root, text="Enter your card number:", bg="lightblue")
        self.card_number_label_window = self.canvas.create_window(400, 120, window=self.card_number_label)  # Left-aligned
        self.card_number_entry = tk.Entry(root)
        self.card_number_entry_window = self.canvas.create_window(400, 150, window=self.card_number_entry)  # Left-aligned

        # Add PIN input label and entry field
        self.pin_label = tk.Label(root, text="Enter your four-digit pin:", bg="lightblue")
        self.pin_label_window = self.canvas.create_window(400, 200, window=self.pin_label)  # Left-aligned
        self.pin_entry = tk.Entry(root, show="*")
        self.pin_entry_window = self.canvas.create_window(400, 230, window=self.pin_entry)  # Left-aligned

        # Add Login button to authenticate user
        self.login_button = tk.Button(root, text="Login", command=self.check_credentials)
        self.login_button_window = self.canvas.create_window(400, 280, window=self.login_button)  # Left-aligned

    def check_credentials(self):
        # Validate user credentials upon login button press
        card_number = self.card_number_entry.get()
        try:
            pin = int(self.pin_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid 4-digit pin")
            return

        # Check if entered credentials match stored user data
        if card_number == self.user['card_number'] and pin == self.user['pin']:
            # If credentials are correct, clear login UI elements and show ATM options
            self.canvas.delete(self.card_number_label_window)
            self.canvas.delete(self.card_number_entry_window)
            self.canvas.delete(self.pin_label_window)
            self.canvas.delete(self.pin_entry_window)
            self.canvas.delete(self.login_button_window)

            # Display user's balance and ATM options
            self.balance_label = tk.Label(root, text=f"Total balance: {self.user['balance']} Rupees", bg="lightblue")
            self.canvas.create_window(400, 150, window=self.balance_label)  # Left-aligned

            self.withdraw_button = tk.Button(root, text="Withdraw Cash", command=self.withdraw_cash, bg="white", fg="blue")
            self.canvas.create_window(200, 200, window=self.withdraw_button)  # Left-aligned

            self.deposit_button = tk.Button(root, text="Deposit Cash", command=self.deposit_cash, bg="white", fg="blue")
            self.canvas.create_window(200, 250, window=self.deposit_button)  # Left-aligned

            self.balance_button = tk.Button(root, text="Balance Enquiry", command=self.balance_enquiry, bg="white", fg="blue")
            self.canvas.create_window(600, 200, window=self.balance_button)  # Left-aligned

            self.mini_statement_button = tk.Button(root, text="Mini Statement", command=self.mini_statement, bg="white", fg="blue")
            self.canvas.create_window(600, 250, window=self.mini_statement_button)  # Left-aligned

            self.transaction_history_button = tk.Button(root, text="Transaction History", command=self.transaction_history, bg="blue", fg="white")
            self.canvas.create_window(400, 350, window=self.transaction_history_button)  # Left-aligned

            self.quit_button = tk.Button(root, text="Quit", command=self.quit_atm, bg="blue", fg="white")
            self.canvas.create_window(500, 350, window=self.quit_button)  # Centered at the bottom
        else:
            # Display error message if credentials are incorrect
            messagebox.showerror("Error", "Entered wrong card number or pin")

    def quit_atm(self):
        # Confirm and quit the ATM application
        confirm_quit = messagebox.askyesno("Quit Confirmation", "Are you sure you want to quit?")
        if confirm_quit:
            messagebox.showinfo("Thank You", "Thanks for visiting the Avinash ATM")
            self.root.quit()

    def withdraw_cash(self):
        # Open window to withdraw cash
        amount_window = tk.Toplevel(self.root)
        amount_window.geometry("400x200")
        amount_window.title("Withdraw Cash")

        amount_label = tk.Label(amount_window, text="Enter the amount of money you want to withdraw:")
        amount_label.pack()

        amount_entry = tk.Entry(amount_window)
        amount_entry.pack()

        def withdraw_amount():
            # Process withdrawal amount entered by user
            try:
                amount = int(amount_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount")
                return

            # Check if sufficient balance is available for withdrawal
            if amount > self.user['balance']:
                messagebox.showerror("Error", "You don't have sufficient balance to make this withdrawal")
            else:
                # Deduct amount from balance, record transaction, and update balance display
                self.user['balance'] -= amount
                self.user['transaction_history'].append((datetime.now(), f"Withdrawal of {amount} Rupees"))
                self.balance_label['text'] = f"Total balance: {self.user['balance']} Rupees"
                messagebox.showinfo("Success", f"{amount} Rupees successfully withdrawn")
                amount_window.destroy()  # Close the window after successful withdrawal

        withdraw_button = tk.Button(amount_window, text="Withdraw", command=withdraw_amount)
        withdraw_button.pack()

    def deposit_cash(self):
        # Open window to deposit cash
        amount_window = tk.Toplevel(self.root)
        amount_window.geometry("400x200")
        amount_window.title("Deposit Cash")

        amount_label = tk.Label(amount_window, text="Enter the amount of money you want to deposit:")
        amount_label.pack()

        amount_entry = tk.Entry(amount_window)
        amount_entry.pack()

        def deposit_amount():
            # Process deposit amount entered by user
            try:
                amount = int(amount_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount")
                return

            # Add deposited amount to balance, record transaction, and update balance display
            self.user['balance'] += amount
            self.user['transaction_history'].append((datetime.now(), f"Deposit of {amount} Rupees"))
            self.balance_label['text'] = f"Total balance: {self.user['balance']} Rupees"
            messagebox.showinfo("Success", f"{amount} Rupees successfully deposited")
            amount_window.destroy()  # Close the window after successful deposit

        deposit_button = tk.Button(amount_window, text="Deposit", command=deposit_amount)
        deposit_button.pack()

    def balance_enquiry(self):
        # Display current balance of the user
        messagebox.showinfo("Balance Enquiry", f"Total balance: {self.user['balance']} Rupees")

    def mini_statement(self):
        # Display mini statement showing last 5 transactions
        last_transactions = "\n".join(f"{i+1}. {transaction[1]} - {transaction[0].strftime('%Y-%m-%d %H:%M:%S')}" for i, transaction in enumerate(self.user['transaction_history'][-5:]))
        messagebox.showinfo("Mini Statement", f"Last 5 transactions:\n{last_transactions}")

    def transaction_history(self):
        # Display detailed transaction history
        history_window = tk.Toplevel(self.root)
        history_window.geometry("600x420")
        history_window.title("Transaction History")

        history_text = tk.Text(history_window)
        history_text.pack()

        # Populate transaction history in text format
        for i, transaction in enumerate(self.user['transaction_history']):
            serial_number = i + 1
            transaction_date = transaction[0].strftime('%Y-%m-%d %H:%M:%S')
            transaction_info = f"{serial_number}. {transaction[1]} - {transaction_date}"
            history_text.insert(tk.END, transaction_info + "\n")

        # Add button to download transaction history as PDF
        def download_pdf():
            pdf_file = "transaction_history.pdf"
            c = pdf_canvas.Canvas(pdf_file, pagesize=letter)
            c.setFont("Helvetica", 12)
            y = 750
            for i, transaction in enumerate(self.user['transaction_history']):
                serial_number = i + 1
                transaction_date = transaction[0].strftime('%Y-%m-%d %H:%M:%S')
                transaction_text = f"{serial_number}. {transaction[1]} - {transaction_date}"
                c.drawString(100, y, transaction_text)
                y -= 20
            c.save()
            messagebox.showinfo("Download PDF", f"PDF saved as {pdf_file}")
            history_window.destroy()  # Close the transaction history window after PDF download

        download_button = tk.Button(history_window, text="Download PDF", command=download_pdf)
        download_button.pack()

# Main program starts here
root = tk.Tk()  # Create the main window
atm = ATM(root)  # Initialize the ATM application
root.mainloop()  # Start the main event loop
