from entities.preinvoice_df import PreInvoice
import sys

# if len(sys.argv) > 1:
#     instruction = sys.argv[1]
#     file_path = instruction
# else:
#     file_path = r'./resources/Detalhes da pré-fatura LAST MILE NOV22-Q1.csv'

path_list = [
    r'./resources/Detalhes da pré-fatura LAST MILE DEZ22-Q1.csv',
    r'./resources/Detalhes da pré-fatura LAST MILE DEZ22-Q2.csv',
    r'./resources/Detalhes da pré-fatura LAST MILE JAN23-Q1.csv',
    r'./resources/Detalhes da pré-fatura LAST MILE JAN23-Q2.csv',
    r'./resources/Detalhes da pré-fatura LAST MILE FEV23-Q1.csv',
    r'./resources/Detalhes da pré-fatura LAST MILE FEV23-Q2.csv',
    r'./resources/Detalhes da pré-fatura LAST MILE MAR23-Q1.csv',
    r'./resources/Detalhes da pré-fatura LAST MILE MAR23-Q2.csv',
    r'./resources/Detalhes da pré-fatura LAST MILE ABR23-Q1.csv',
    r'./resources/Detalhes da pré-fatura LAST MILE ABR23-Q2.csv',
    r'./resources/Detalhes da pré-fatura LAST MILE MAI23-Q1.csv',
    r'./resources/Detalhes da pré-fatura LAST MILE MAI23-Q2.csv',
    r'./resources/Detalhes da pré-fatura LAST MILE JUN23-Q1.csv',
    r'./resources/Detalhes da pré-fatura LAST MILE JUN23-Q2.csv',
    r'./resources/Detalhes da pré-fatura LAST MILE JUL23-Q1.csv',
    r'./resources/Detalhes da pré-fatura LAST MILE JUL23-Q2.csv',
    r'./resources/Detalhes da pré-fatura LAST MILE AGO23-Q1.csv',
    r'./resources/Detalhes da pré-fatura LAST MILE AGO23-Q2.csv',
    r'./resources/Detalhes da pré-fatura LAST MILE SET23-Q1.csv',
    r'./resources/Detalhes da pré-fatura LAST MILE SET23-Q2.csv',
    r'./resources/Detalhes da pré-fatura LAST MILE OUT23-Q1.csv',
    r'./resources/Detalhes da pré-fatura LAST MILE OUT23-Q2.csv',
    r'./resources/Detalhes da pré-fatura LAST MILE NOV23-Q1.csv',
    r'./resources/Detalhes da pré-fatura LAST MILE NOV23-Q2.csv',
]

for file_path in path_list:
    preinvoice = PreInvoice()

    preinvoice.getPreInvoice_df(file_path=file_path)
