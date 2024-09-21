class BankAPI:
    bank_db = {
        "vansh.gupta@icici": "ICICI000123456789",
        "vanshika.gupta@hdfc": "HDFC000987654321",
    }

    @staticmethod
    def get_account_number(upi_id):
        return BankAPI.bank_db.get(upi_id)

class UPI:
    bank_mapping = {
        "icici": "ICICI Bank",
        "hdfc": "HDFC Bank",
    }

    @staticmethod
    def resolve_upi_id(upi_id):
        try:
            username, bank_handle = upi_id.split('@')
            bank_name = UPI.bank_mapping.get(bank_handle)
            if not bank_name:
                raise ValueError("Bank handle not found")
            
            account_number = BankAPI.get_account_number(upi_id)
            if not account_number:
                raise ValueError("UPI ID not found in bank database")

            return account_number
        except ValueError as e:
            print("Error resolving UPI ID")
            return None

# Example usage
upi_id = "vansh.gupta@icici"
account_number = UPI.resolve_upi_id(upi_id)
if account_number:
    print(f"Bank Account Number: {account_number}")
else:
    print("Invalid UPI ID or bank handle not found")