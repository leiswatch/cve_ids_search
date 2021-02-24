import requests
import csv
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-F', '--file')
    parser.add_argument('-I', '--initial')
    parser.add_argument('-O', '--output')
    args = parser.parse_args()

    with open(args.file, 'r') as results, open(args.initial, 'r') as initial, open(args.output, 'w+') as output:
        csv_results_reader = csv.reader(results, delimiter=' ', quotechar='|')
        csv_initial_reader = csv.reader(initial, delimiter=' ', quotechar='|')

        CVE_IDS = []
        packages = []

        for row in csv_results_reader:
            cve_ids = (''.join(row[1:]).replace('"', '')).split(',')
            CVE_IDS.append(cve_ids)

        for row in csv_initial_reader:
            name, version = row[0].split(',')
            packages.append([name, version])

        fieldnames = ['Package', 'Version', 'CEV ID']
        csv_output_writer = csv.DictWriter(output, fieldnames=fieldnames)

        for package, cve_id in zip(packages[1:], CVE_IDS[1:]):
            print(package)
            output_ids = []

            if cve_id[0] == '':
                continue

            for id in cve_id:
                found = False
                response =  requests.get(f'https://cve.circl.lu/api/cve/{id}')
                vulnerable_products = response.json()['vulnerable_product']

                for product in vulnerable_products:
                    if package[1] in product:
                        found = True
                        print(package)
                if found:
                    output_ids.append(id)

            csv_output_writer.writerow({'Package': package[0], 'Version': package[1], 'CEV ID': ', '.join(output_ids)})


if __name__ == '__main__':
    main()
