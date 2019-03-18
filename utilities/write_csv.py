import csv


def write_csv(file_name, data):
    with open(file_name, 'w', newline='') as csvfile:
        fieldnames = ['word', 'score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        for d in data:
            row = {
                'word': d.txt,
                'score': d.score
            }
            writer.writerow(row)
