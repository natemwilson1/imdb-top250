from bs4 import BeautifulSoup
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
import csv

# Scrapes the IMDB's site
source = requests.get('http://www.imdb.com/chart/top').text
soup = BeautifulSoup(source, 'html.parser')
movie_scrap_lines = soup.find_all('td', attrs={'class': 'titleColumn'})

def get_movie_info(movie_info):
    return (movie_info.contents[0][7:-8],
            movie_info.contents[1].text,
            movie_info.find('span').text[1:-1])


movie_infos = [get_movie_info(movie_scrap_line) for movie_scrap_line in movie_scrap_lines]

# Dump the result into a csv file
df = pd.DataFrame(movie_infos, columns=['number', 'title', 'year'])
df.to_csv('movielist.csv', index=False, encoding='utf-8')
print(df)
print(input("Press enter to close"))

with open('movielist.csv','r') as df:
    plots = csv.reader(df, delimiter=',')
    x = [column[2] for column in plots if column[2] != 'year']

# Plot a graph top movies per year
x2 = Counter(x)
counted = sorted(x2.items())
x, y = zip(*counted)

sns.barplot(list(map(int, x)), y)
plt.xticks(rotation=70)
plt.title('IMDB Top 250 by Year')
plt.xlabel('year')
plt.ylabel('number of movies in the top 250')
plt.tick_params(axis='x', which='major', labelsize=6)
plt.tight_layout()
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())
plt.show()
