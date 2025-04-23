import os

global ontario_taxes, federal_taxes, FEDERAL_BASIC_PERSONAL_AMOUNT, ONTARIO_BASIC_PERSONAL_AMOUNT, PROVINCIAL, FEDERAL, MAX_AMOUNT, TAX_RATE, AGGREGATE_TAX_BRACKETS, PROVINCIAL_MARGINAL_RATE, FEDERAL_MARGINAL_RATE

def setup()->None:
    """  """
    global ontario_taxes, federal_taxes, FEDERAL_BASIC_PERSONAL_AMOUNT, ONTARIO_BASIC_PERSONAL_AMOUNT, PROVINCIAL, FEDERAL, MAX_AMOUNT, TAX_RATE, AGGREGATE_TAX_BRACKETS
    PROVINCIAL = 0
    FEDERAL = 1
    MAX_AMOUNT = 0
    TAX_RATE = 1
    FEDERAL_BASIC_PERSONAL_AMOUNT = 16129
    ONTARIO_BASIC_PERSONAL_AMOUNT = 12747
    ontario_taxes = [[51446, 0.0505], [102894, 0.0915], [150000, 0.1116], [220000, 0.1216], [999999999, 0.1316]]
    federal_taxes = [[55867, 0.15], [111733, 0.205], [173205, 0.26], [246752, 0.29], [999999999, 0.33]]
    AGGREGATE_TAX_BRACKETS = get_tax_bracket_ranges()    
    return
    

def get_tax_bracket_ranges()->tuple:
    """  """
    global ontario_taxes, federal_taxes, PROVINCIAL, FEDERAL, MAX_AMOUNT, TAX_RATE, FEDERAL_BASIC_PERSONAL_AMOUNT, ONTARIO_BASIC_PERSONAL_AMOUNT
    tax_bracket_ranges = []
    tax_rate = []
    indices = [len(ontario_taxes) - 1, len(federal_taxes) - 1]
    while indices[PROVINCIAL] > -1 and indices[FEDERAL] > -1:
        amount = min([ontario_taxes[indices[PROVINCIAL]][MAX_AMOUNT], federal_taxes[indices[FEDERAL]][MAX_AMOUNT]])
        tax_bracket_ranges = [amount] + tax_bracket_ranges
        tax_rate = [federal_taxes[indices[FEDERAL]][TAX_RATE] + ontario_taxes[indices[PROVINCIAL]][TAX_RATE]] + tax_rate
        if amount == ontario_taxes[indices[PROVINCIAL]][MAX_AMOUNT]:
            indices[FEDERAL] -= 1
        else:
            indices[PROVINCIAL] -= 1
    amount = max(FEDERAL_BASIC_PERSONAL_AMOUNT, ONTARIO_BASIC_PERSONAL_AMOUNT)
    if amount == FEDERAL_BASIC_PERSONAL_AMOUNT:
        tax_bracket_ranges = [ONTARIO_BASIC_PERSONAL_AMOUNT, amount] + tax_bracket_ranges
        tax_rate = [0, ontario_taxes[0][TAX_RATE]] + tax_rate
    else:
        tax_bracket_ranges = [FEDERAL_BASIC_PERSONAL_AMOUNT, amount] + tax_bracket_ranges
        tax_rate = [0, federal_taxes[0][TAX_RATE]] + tax_rat
    """ DX
    for i in range(len(tax_bracket_ranges)):
        print("\t", tax_bracket_ranges[i], tax_rate[i], sep="\t")
    """
    return (tax_bracket_ranges, tax_rate)


def calc_taxes(gross_amount: float)->float:
    """  """
    global ontario_taxes, federal_taxes, PROVINCIAL, FEDERAL, MAX_AMOUNT, TAX_RATE, FEDERAL_BASIC_PERSONAL_AMOUNT, ONTARIO_BASIC_PERSONAL_AMOUNT, PROVINCIAL_MARGINAL_RATE, FEDERAL_MARGINAL_RATE
    provincial_tax = 0
    federal_tax = 0
    federal_bracket = 0
    provincial_bracket = 0
    while gross_amount > federal_taxes[federal_bracket][MAX_AMOUNT]:
        federal_bracket += 1
        if federal_bracket == len(federal_taxes):
            print("Error: Insufficient tax bracket data.")
            exit()
    while gross_amount > ontario_taxes[provincial_bracket][MAX_AMOUNT]:
        provincial_bracket += 1
        if provincial_bracket == len(ontario_taxes):
            print("Error: Insufficient tax bracket data.")
            exit()
    PROVINCIAL_MARGINAL_RATE = 100 * ontario_taxes[provincial_bracket][TAX_RATE]
    FEDERAL_MARGINAL_RATE = 100 * federal_taxes[federal_bracket][TAX_RATE]
    for index in range(provincial_bracket + 1):
        if not index:
            taxable_amount = ontario_taxes[index][MAX_AMOUNT] - ONTARIO_BASIC_PERSONAL_AMOUNT
            provincial_tax += taxable_amount * ontario_taxes[index][TAX_RATE]
        elif index == provincial_bracket:
            taxable_amount  = gross_amount - ontario_taxes[index - 1][MAX_AMOUNT]
            provincial_tax += taxable_amount * ontario_taxes[index][TAX_RATE]
        else:
            taxable_amount  = ontario_taxes[index][MAX_AMOUNT] - ontario_taxes[index - 1][MAX_AMOUNT]
            provincial_tax += taxable_amount * ontario_taxes[index][TAX_RATE]
    for index in range(federal_bracket + 1):
        if not index:
            taxable_amount = federal_taxes[index][MAX_AMOUNT] - FEDERAL_BASIC_PERSONAL_AMOUNT
            federal_tax += taxable_amount * federal_taxes[index][TAX_RATE]
        elif index == federal_bracket:
            taxable_amount  = gross_amount - federal_taxes[index - 1][MAX_AMOUNT]
            federal_tax += taxable_amount * federal_taxes[index][TAX_RATE]
        else:
            taxable_amount  = federal_taxes[index][MAX_AMOUNT] - federal_taxes[index - 1][MAX_AMOUNT]
            federal_tax += taxable_amount * federal_taxes[index][TAX_RATE]  
    return (provincial_tax, federal_tax)


def calc_reqd_gross(reqd_amount: float)->float:
    """  """
    global MAX_AMOUNT, TAX_RATE, AGGREGATE_TAX_BRACKETS
    remaining_amount = reqd_amount
    total_taxes = 0
    current_bracket = 0
    first_run = True
    while remaining_amount > 0:
        if current_bracket == len(AGGREGATE_TAX_BRACKETS[MAX_AMOUNT]):
            print("Error: Insufficient tax bracket data.")
            exit()
        current_max = 0
        if first_run:
            first_run = False
            current_max = AGGREGATE_TAX_BRACKETS[MAX_AMOUNT][current_bracket] * (1 - AGGREGATE_TAX_BRACKETS[TAX_RATE][current_bracket])
        else:
            current_max = (AGGREGATE_TAX_BRACKETS[MAX_AMOUNT][current_bracket] - AGGREGATE_TAX_BRACKETS[MAX_AMOUNT][current_bracket - 1]) * (1 - AGGREGATE_TAX_BRACKETS[TAX_RATE][current_bracket])
        if remaining_amount > current_max:
            remaining_amount -= current_max
            total_taxes += (current_max / (1 - AGGREGATE_TAX_BRACKETS[TAX_RATE][current_bracket])) * AGGREGATE_TAX_BRACKETS[TAX_RATE][current_bracket]
        else:
            gross_amount = remaining_amount / (1 - AGGREGATE_TAX_BRACKETS[TAX_RATE][current_bracket])
            total_taxes += gross_amount * AGGREGATE_TAX_BRACKETS[TAX_RATE][current_bracket]
            remaining_amount = 0
        current_bracket += 1
    return total_taxes + reqd_amount


def run()->None:
    """  """
    global ontario_taxes, federal_taxes, FEDERAL_BASIC_PERSONAL_AMOUNT, ONTARIO_BASIC_PERSONAL_AMOUNT, PROVINCIAL, FEDERAL, MAX_AMOUNT, TAX_RATE, AGGREGATE_TAX_BRACKETS, PROVINCIAL_MARGINAL_RATE, FEDERAL_MARGINAL_RATE
    
    while True:
        os.system("CLS")
        reqd_income = input('Enter req\'d income or exit: ').lower().replace(" ", "")
        if reqd_income == "q" or reqd_income == "x" or reqd_income == "quit" or reqd_income == "exit":
            exit()
        else:
            try:
                reqd_income = float(reqd_income)
            except:
                os.system("CLS")
                print(reqd_income, " is not a valid entry.")
                input("Press <ENTER> to continue")
                continue
        pre_tax_income = calc_reqd_gross(reqd_income)
        total_taxes = pre_tax_income - reqd_income
        provincial_tax = 0
        federal_tax = 0
        (provincial_tax, federal_tax) = calc_taxes(pre_tax_income)
        print(PROVINCIAL_MARGINAL_RATE, FEDERAL_MARGINAL_RATE)
        overall_marginal_rate = max([PROVINCIAL_MARGINAL_RATE, FEDERAL_MARGINAL_RATE])
        net_income = pre_tax_income - (provincial_tax + federal_tax)
        os.system("CLS")
        print("Required (pre-tax) Income is:\t\t$", f"{pre_tax_income:.{2}f}")
        print("\n\tProvincial Taxes:\t\t$", f"{provincial_tax:.{2}f}")
        print("\t    Mean Prov. Tax Rate:\t", f"{100*provincial_tax/pre_tax_income:.{2}f}", "%")
        print("\t    Marginal Prov. Tax Rate:\t", f"{PROVINCIAL_MARGINAL_RATE:.{2}f}", "%")
        print("\n\tFederal Taxes:\t\t\t$", f"{federal_tax:.{2}f}")
        print("\t    Mean Fed. Tax Rate:\t\t", f"{100*federal_tax/pre_tax_income:.{2}f}", "%")
        print("\t    Marginal Fed. Tax Rate:\t", f"{FEDERAL_MARGINAL_RATE:.{2}f}", "%")
        print("\n\tTotal Taxes:\t\t\t$", f"{total_taxes:.{2}f}")
        print("\t    Mean Tax Rate:\t\t", f"{100*total_taxes/pre_tax_income:.{2}f}", "%")
        print("\t    Marginal Tax Rate:\t\t", f"{overall_marginal_rate:.{2}f}", "%")
        print("\nNet Income:\t$", f"{reqd_income:.{2}f}")
        print("\n\n\n")
        input("Press <ENTER> to continue...")    



if __name__ == "__main__":
    global ontario_taxes, federal_taxes, FEDERAL_BASIC_PERSONAL_AMOUNT, ONTARIO_BASIC_PERSONAL_AMOUNT, PROVINCIAL, FEDERAL, MAX_AMOUNT, TAX_RATE, AGGREGATE_TAX_BRACKETS, PROVINCIAL_MARGINAL_RATE, FEDERAL_MARGINAL_RATE
    
    setup()
    run()