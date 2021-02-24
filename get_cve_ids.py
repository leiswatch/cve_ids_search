import csv
import subprocess
import argparse


def replace_chars(string):
    if 'pkgconfig(' in string or 'config(' in string:
        return string.replace('pkgconfig(', '').replace('config(', '').replace(')', '')
    return string


def unique(list1):
    unique_list = []

    for x in list1:
        if x[0] not in unique_list:
            unique_list.append(x[0])
    return unique_list


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-I', '--initial')
    parser.add_argument('-O', '--output')
    parser.add_argument('-V', '--versions', action='store_true')
    args = parser.parse_args()
    packages = []

    with open(args.initial, newline='') as csv_deps:
        csv_deps_reader = csv.reader(csv_deps, delimiter=' ', quotechar='|')

        for row in csv_deps_reader:
            deps = row[0].split(',')
            name = replace_chars(deps[0])
            version = deps[1]

            packages.append([name, version])

    if not args.versions:
        packages = unique(packages)

    PACKAGES_NUM = len(packages)
    print(PACKAGES_NUM)


    with open(args.output, mode='w+') as csv_results:
        if args.versions:
            fieldnames = ['Package', 'Version', 'CEV ID']
        else:
            fieldnames = ['Package', 'CEV ID']
        csv_results_writer = csv.DictWriter(csv_results, fieldnames=fieldnames)


        csv_results_writer.writeheader()
        i = 0
        for package in packages:
            if args.versions:
                result = subprocess.getstatusoutput(f'./bin/search_fulltext.py -q "{package[0]}" -q "{package[1]}"')
                csv_results_writer.writerow({'Package': package[0], 'Version': package[1], 'CEV ID': ', '.join(result[1].split('\n'))})
            else:
                result = subprocess.getstatusoutput(f'./bin/search_fulltext.py -q "{package}"')
                csv_results_writer.writerow({'Package': package, 'CEV ID': ', '.join(result[1].split('\n'))})

            i += 1
            print(f'{(i/PACKAGES_NUM) * 100}%')


if __name__ == '__main__':
    main()
