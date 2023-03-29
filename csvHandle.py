import csv
import pandas


def 
    with open('duromereadCSV():tro.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            print(row)
            line_count += 1
        print(f'Processed {line_count} lines.')

def writeCSV(data, hora, carga, valor, temperatura, umidade):
    with open('durometro.csv', mode='a') as csv_file:
        fieldnames = ['data','hora','pre-carga','valor','temperatura','umidade']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writerow({'data': data, 'hora': hora, 'pre-carga': carga, 'valor': valor, 'temperatura': temperatura, 'umidade': umidade})
        print("vai corinthians")
