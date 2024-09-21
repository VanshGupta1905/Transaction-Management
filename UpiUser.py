import Transaction

class UPIUser:
    def __init__(self, name, phone_number, upi_id):
        self.name = name
        self.phone_number = phone_number
        self.upi_id = upi_id
        self.linked_bank_accounts = []
        self.transaction_history = []
        self.daily_limit = 0
        self.pending_requests = []
        self.bank_info = self.extract_bank_info(upi_id)
        self.is_verified = False


    def is_valid_upi_id(self, upi_id):
        # Basic validation: alphanumeric, @, and minimum length
        return (len(upi_id) >= 5 and 
                '@' in upi_id and 
                upi_id.replace('@', '').isalnum())

    def extract_bank_info(self, upi_id):
        # UPI ID format: username@bankhandle
        bankname, bank_handle = upi_id.split('@')
        # In a real system, you'd have a mapping of bank handles to actual bank information
        return {"bank_handle": bank_handle}


    def send_money(self, recipient_upi_id, amount):
        # This would connect to NPCI to process the transaction via IMPS
        return self.Transaction.route_payment_through_imps(recipient_upi_id, amount)

    def request_money(self, from_upi_id, amount, description=""):
        request = {
            "from_upi_id": from_upi_id,
            "to_upi_id": self.upi_id,
            "amount": amount,
            "description": description,
            "status": "pending"
        }
        self.pending_requests.append(request)
        return request

    def approve_request(self, request_id):
        for request in self.pending_requests:
            if request["id"] == request_id:
                request["status"] = "approved"

                # Here we would trigger the actual money transfer
                self.Transaction.route_payment_through_imps(request.to_upi_id, request.amount)
                
                return True
        return False
    
    def reject_request(self, request_id):
        for request in self.pending_requests:
            if request["id"] == request_id:
                request["status"] = "rejected"
                return True
        return False
    def get_pending_requests(self):
        return [req for req in self.pending_requests if req["status"] == "pending"]

    def check_balance(self):
        # Check the balance of the linked bank account
        balance = self.simulate_balance_check()
        return {"upi_id": self.upi_id, "balance": balance}
    

    def simulate_balance_check(self):
        # This is a placeholder. In reality, it would involve:
        # 1. Sending a request to NPCI
        # 2. NPCI forwarding the request to the user's bank
        # 3. Bank responding with the balance
        # 4. NPCI relaying the balance back to the UPI system
        return 10000.00  # Simulated balance

    def view_transaction_history(self):
        return self.transaction_history

