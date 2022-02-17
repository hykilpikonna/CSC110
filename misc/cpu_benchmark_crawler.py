import csv
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


@dataclass()
class CPU:
    id: str
    name: str
    bench: int


@dataclass()
class E5(CPU):
    val: int
    ver: int


if __name__ == '__main__':
    html = requests.get('https://www.cpubenchmark.net/cpu_list.php').text
    soup = BeautifulSoup(html, 'html.parser')

    cpus: list[CPU] = []
    table = soup.find('tbody')
    for tr in table.find_all('tr'):
        td = tr.find_all('td')
        cpus.append(CPU(tr.attrs['id'], td[0].text, int(td[1].text.replace(',', ''))))

    # Filter E5
    e5 = [E5(c.id, c.name, c.bench, int(c.name[14:18]),
             (1 if c.name.find(' v') == -1 else int(c.name[c.name.find(' v') + 2])))
          for c in cpus if 'Xeon E5-' in c.name]
    print(e5)

    # To CSV
    with open('cpu_bench.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ID', 'Name', 'Bench', 'Num', 'Version'])
        writer.writerows([(c.id, c.name, c.bench, c.val, c.ver) for c in e5])
