def route_payment_through_imps(self, recipient_upi_id, amount):
        # Step will be 
        # 1. Extracting recipient's bank info from their UPI ID
        # 2. Connecting to NPCI
        # 3. NPCI would route the transaction through IMPS to the recipient's bank
        recipient_bank = self.extract_bank_info(recipient_upi_id)
        # Simulate IMPS transaction
        print(f"Routing ₹{amount} to {recipient_upi_id} via IMPS")
        print(f"From bank: {self.bank_info['bank_handle']}")
        print(f"To bank: {recipient_bank['bank_handle']}")
        return True

