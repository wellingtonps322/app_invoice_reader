import pandas as pd
from IPython.display import display
from mysql.connector.errors import OperationalError

from tools.tools import Tools
from database.recorder import Recorder
from database.reader import Reader
from database.updater import Updater
from database.deleter import Deleter
from entities.preinvoice_discount import Discounts
from entities.preinvoice_payment import Payments
from entities.preinvoice_additional_payment import AdditionalPayments
from entities.driver import Driver
from entities.vehicle import Vehicle


class PreInvoice(Tools):

    def __init__(self) -> None:
        self.recorder = Recorder()
        self.reader = Reader()
        self.updater = Updater()
        self.discounts = Discounts(reader=self.reader)
        self.payments = Payments()
        self.additional_payments = AdditionalPayments(reader=self.reader)

    def getPreInvoice_df(self, file_path: str):
        try:
            print('GETTING INVOICE DATA')

            self.invoice = pd.read_csv(
                file_path, sep=';')
            self.invoice = self.invoice.dropna(how='all')
            self.invoice.reset_index(drop=True, inplace=True)
            self.invoice_header = self.invoice.loc[0]
            self.invoice_body = self.invoice.drop(0)
            self.invoice_body.reset_index(drop=True, inplace=True)
            self.invoice_body.columns = self.invoice_body.iloc[0]
            self.invoice_body = self.invoice_body.drop(0)
            self.invoice_body.reset_index(drop=True, inplace=True)

            preinvoice_information = {
                'id_invoice': self.invoice_header['ID pré-fatura'],
                'product': f'"{self.invoice_header['Produto']}"',
                'country': f'"{self.invoice_header['País']}"',
                'shipping_company': f'"{self.invoice_header['Transportadora']}"',
                'mille': f'"{self.invoice_header['Milha']}"',
                'period': f'"{self.invoice_header['Período']}"',
                'invoice_type': f'"{self.invoice_header['Tipo de pré-fatura']}"',
                'invoice_status': f'"{self.invoice_header['Status da pré-fatura']}"'
            }
            # Check if the previous invoice was inserted, if true authorize insertion, if false deny insertion
            self.recorder.setInvoiceInformation(invoice=preinvoice_information)

            for index_row, row in self.invoice_body.iterrows():
                # if index_row == 1643:
                #     print('Wait')

                # if row['ID da rota'] == '109195031':
                #     print('WAIT')

                preinvoice_row = {}

                # display(row)
                if 'Subtotal' in row['Descrição']:
                    continue

                if 'Total' in row['Descrição']:
                    continue

                # Checking if is discount
                if self.discounts.isDiscount(series_body=row):
                    preinvoice_row = self.discounts.getData(
                        series_body=row, preinvoice_header=self.invoice_header)

                if self.payments.isPayment(series_body=row):
                    preinvoice_row = self.payments.getData(
                        series_body=row, preinvoice_header=self.invoice_header)

                if self.additional_payments.isAddittionalPayment(series_body=row):
                    preinvoice_row = self.additional_payments.getData(
                        series_body=row, preinvoice_header=self.invoice_header)

                if preinvoice_row:
                    match preinvoice_row['data_type']:
                        case '"PAYMENT"':
                            vehicle_data = {
                                'license_plate': preinvoice_row['license_plate'],
                                'service_center': preinvoice_row['service_center'],
                                'last_route': preinvoice_row['start_date'],
                                'service_type': preinvoice_row['service_type'],
                                'driver': preinvoice_row['driver']
                            }
                            vehicle = Vehicle(
                                vehicle_data=vehicle_data, recorder=self.recorder, reader=self.reader, updater=self.updater)

                            vehicle.isVehicleExists()

                            driver_data = {
                                'id_driver': preinvoice_row['id_driver'],
                                'driver_name': preinvoice_row['driver'],
                                'service_center': preinvoice_row['service_center'],
                                'license_plate': preinvoice_row['license_plate'],
                                'last_route': preinvoice_row['start_date'],
                                'service_type': preinvoice_row['service_type'],
                            }
                            driver = Driver(
                                driver_data=driver_data, recorder=self.recorder, reader=self.reader, updater=self.updater)
                            driver.isDriverExists()

                            self.recorder.setInvoicePayment(
                                row_payment_dict=preinvoice_row)

                        case '"DISCOUNT"':

                            if self.areRouteInPaymentDB(route_number=preinvoice_row['id_route']):
                                self.recorder.setInvoiceDiscount(
                                    row_discount_dict=preinvoice_row)
                            else:
                                #! GENERATE A WINDOW ALERT AND SHOW DATA ROUTE AND DATA DRIVER
                                print(
                                    'ATENÇÃO: UM DESCONTO NÃO TEVE SUA ROTA IDENTIFICADA!\n POR FAVOR, FAZER UMA VERIFICAÇÃO MANUAL NA ABA: DESCONTOS SEM IDENTIFICAÇÃO')
                                self.recorder.setPreInvoiceDiscountsWithoutRoute(
                                    row_discount_dict=preinvoice_row)

                        case '"ADDITIONAL_PAYMENT"':

                            if self.areRouteInPaymentDB(route_number=preinvoice_row['id_route']):
                                self.recorder.setInvoiceAdditionalPayment(
                                    row_payment_dict=preinvoice_row)
                            else:
                                #! GENERATE A WINDOW ALERT
                                print(
                                    'ATENÇÃO: UM DESCONTO NÃO TEVE SUA ROTA IDENTIFICADA!\n POR FAVOR, FAZER UMA VERIFICAÇÃO MANUAL NA ABA: DESCONTOS SEM IDENTIFICAÇÃO')
                                self.recorder.setPreInvoiceDiscountsWithoutRoute(
                                    row_discount_dict=preinvoice_row)

                        case _:
                            print('ERROR')

            self.recorder.close()
            self.reader.close()
            self.updater.close()
            print('Inserted Pre Invoice Successfully')

        except OperationalError as e:
            print(e)
            deleter = Deleter()

            deleter.deleteAllInvoiceData(invoice=self.invoice_header['ID pré-fatura'])

            self.recorder.close()
            self.reader.close()
            self.updater.close()