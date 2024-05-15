# Data Visualisation and Data-driven Decision Making 2024
# Final Project: The Visual Story of Fernando Alonso's Formula 1 Career

## Table of Contents

- [Webpage](#webpage)
- [Group Members](#group-members)
- [Project Description](#project-description)
- [Data Source](#data-source)
- [Implementation](#implementation)
- [Folder Structure](#folder-structure)

---

## Webpage

The final interactive dashboard and visualizations can be accessed here: [**The Visual Story of Alonso's Career**](https://pheadar.github.io/DataViz_2024/)

---

## Group Members

**Bogdan Mihaila**  
| *email*: bomi@itu.dk  
| *github*: https://github.com/m3bogdan

**Pedro Prazeres**  
| *email*: peca@itu.dk  
| *github*: https://github.com/Pheadar

>[Back to top](#table-of-contents)

---

## Project Description

Exam project in the *Data Visualisation and Data-driven Decision Making* course for the BSc Program in Data Science at the [IT University of Copenhagen](https://www.itu.dk/), academic year 2023/24.

This is a group project, where we explore Fernando Alonso's Formula 1 career in data. We will analyze his performance over the years, his teams, and his results. The goal is to create a few visualizations that will help us understand his career better and draw some conclusions about his performance.

>[Back to top](#table-of-contents)

---

## Data Source

The data used in this project is sourced from the [Ergast Developer API](http://ergast.com/mrd/). The API provides historical Formula 1 data, including information on drivers, teams, circuits, race results, and more. The data was scraped from the API as json files and then treated and transformed into pandas dataframes for analysis.

>[Back to top](#table-of-contents)

---

## Implementation

The project uses Python 3.11 with the following libraries:
- [pandas](https://pandas.pydata.org/)
- [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

Required libraries can be installed using the following command:
```bash
pip install -r requirements.txt
```
>[Back to top](#table-of-contents)

---

## Folder Structure

```
.
├── data
│   └── {season}
│       └── {round number}-{GP name}
|           ├── race_results.json
│           └── quali_results.json (where available)
├── scripts
│   ├── 01-data_scrape.py
│   ├── 02_data_merge.py
│   ├── 03_dataframes.py
│   ├── 04_driver_career.py
│   ├── 05_distance_per_team.py
│   └── 06_timeline.py
├── treated_data
|   ├── csv
│       ├── {season}_sorted_drivers.csv
│       ├── {season}_timeline_short.csv
│       ├── {season}_timeline.csv
│       ├── circuit_info.csv
│       ├── distance_per_team.csv
│       ├── driver_info.csv
│       ├── driver_photos.csv
│       ├── race_info.csv
│       ├── results.csv
│       └── team_info.csv
|   ├── pickles
│       └── (same as csv)
|   ├── all_quali_results.json
|   ├── all_race_results.json
│   └── alonso_career_summary.csv
├── report
│   └── Final_Report.pdf
├── index.html
├── requirements.txt
└── README.md
```

>[Back to top](#table-of-contents)