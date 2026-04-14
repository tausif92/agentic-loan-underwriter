def calculate_dti(income: float, loan_amount: float) -> dict:
    dti = loan_amount / income
    return {
        "dti": round(dti, 2)
    }
