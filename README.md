# Data Visualisation and Data-driven Decision Making 2024
# Final Project: Fernando Alonso's Formula 1 Career in Data

## Table of Contents

- [Group Members](#group-members)
- [Project Description](#project-description)
- [Data](#data)
- [Implementation](#implementation)
- [Folder Structure](#folder-structure)

---

## Group Members

**Bogdan Mihaila**  
|> *email*: bomi@itu.dk  
|> *github*: https://github.com/m3bogdan

**Pedro Prazeres**  
|> *email*: peca@itu.dk  
|> *github*: https://github.com/Pheadar

>[Back to top](#table-of-contents)

---

## Project Description

Exam project in the *Data Visualisation and Data-driven Decision Making* course for the BSc Program in Data Science at the [IT University of Copenhagen](https://www.itu.dk/), academic year 2023/24.

This is a group project, where we explore Fernando Alonso's Formula 1 career in data. We will analyze his performance over the years, his teams, and his results. The goal is to create a few visualizations that will help us understand his career better and draw some conclusions about his performance.

>[Back to top](#table-of-contents)

---

## Data

The data used in this project is sourced from the [Ergast Developer API](http://ergast.com/mrd/). The API provides historical Formula 1 data, including information on drivers, teams, circuits, race results, and more. The data was scraped from the API as json files and then treated and transformed into pandas dataframes for analysis.

>[Back to top](#table-of-contents)

---

## Implementation

The project is implemented in Python 3.11 and uses Jupyter Notebooks. The following libraries are used:
- [plotly](https://plotly.com/python/)
- [dash](https://dash.plotly.com/)
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
├── treated_data
|   ├── csv
│       ├── circuit_info.csv
│       ├── driver_info.csv
│       ├── race_info.csv
│       ├── results.csv
│       └── team_info.csv
|   ├── pickles
│       ├── circuit_info.pkl
│       ├── driver_info.pkl
│       ├── race_info.pkl
│       ├── results.pkl
│       └── team_info.pkl
|   ├── all_quali_results.json
|   ├── all_race_results.json
│   └── alo_season_summary.csv
├── scripts
│   ├── 01-data_scrape.py
│   ├── 02_data_merge.py
│   ├── 03_dataframes.py
│   ├── 04_driver_career.py
├── notebooks
│   ├── 
├── report
│   └── Final_Report.pdf
├── requirements.txt
└── README.md
```

>[Back to top](#table-of-contents)