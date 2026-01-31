import requests
from bs4 import BeautifulSoup as Soup
from operator import itemgetter

def get_contents_from_file(url):
    response = requests.get(url)
    if response.status_code == 200:
        contents = response.text
        return contents
    else:
        print("Failed to retrieve file")

def convert_to_table(contents):
    soup = Soup(contents)
    table = soup.find('table')
    return table

def get_values_from_table(table):
    coords = []
    rows = table.find_all('tr')
    for row in rows:
        columns = row.find_all('td')
        rowcoords = []
        for col in columns:
            text = col.contents[0].text
            if text.isdecimal():
                text = int(text)
            rowcoords.append(text)
        if rowcoords[1] != "Character":
            coords.append(tuple(rowcoords))
    return coords

def draw_from_coords(coords):
    startRow = 0
    startCol = 0
    while startRow <= max(coords, key=itemgetter(2))[2]:
        y_coord = [tup for tup in coords if startRow == tup[2]]
        if len(y_coord) == 0:
                print(" ")
        line = ""
        while startCol <= max(y_coord, key=itemgetter(0))[0]:
            item = [val for val in y_coord if startCol == val[0]]
            if len(item) == 0:
                line+=" "
            else:
                line+= item[0][1]
            startCol += 1
        startCol = 0
        startRow += 1
        print(line)



def main_flow(url):
    contents = get_contents_from_file(url)
    table = convert_to_table(contents)
    coords = get_values_from_table(table)
    draw_from_coords(coords)

main_flow('https://docs.google.com/document/d/e/2PACX-1vQiVT_Jj04V35C-YRzvoqyEYYzdXHcRyMUZCVQRYCu6gQJX7hbNhJ5eFCMuoX47cAsDW2ZBYppUQITr/pub')