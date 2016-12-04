import xlrd
import datetime
import csv
from terminal.models import Kolejnosc

def csv_from_excel(arkusz):
	wb = xlrd.open_workbook(arkusz)
	sh = wb.sheet_by_name('Sheet1')
	your_csv_file = open('scripts/tury.csv', 'w')
	wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)
	for rownum in range(sh.nrows):
	    wr.writerow(sh.row_values(rownum))
	your_csv_file.close()

def zapiszKolejnoscDoBazy(import_file = 'scripts/tury.csv'):
	with open(import_file, 'r') as f:
		csvdata = csv.reader(f, delimiter=',')
		header = next(csvdata)
		for row in csvdata:
			if row:
				if not row == header:			
					try:
						seconds = (float(row[2]) - 25569) * 86400.0
						date = datetime.datetime.utcfromtimestamp(seconds)
						Kolejnosc.objects.get_or_create(tura = row[1], data = date)
					except ValueError as e:
						break	
					

try:
	csv_from_excel('scripts/export30.XLSX')
	zapiszKolejnoscDoBazy()
except Exception as e:
	raise e