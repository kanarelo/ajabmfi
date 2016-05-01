def post_disbursed_loans():
	loans = LoanAccount.objects.in_disbursement()

	for loan in loans:
		disburse_loan(loan)