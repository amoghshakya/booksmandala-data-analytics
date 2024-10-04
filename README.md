# BooksMandala Dataset

This project involves web scraping books data from [BooksMandala](https://booksmandala.com) using Selenium. The collected data includes book metadata like titles, authors, genres, prices, and more, and will be used for statistical analysis and machine learning.

## Contents

- [BooksMandala Dataset](#booksmandala-dataset)
  - [Contents](#contents)
  - [Project Overview](#project-overview)
  - [Technologies Used](#technologies-used)
  - [Project Structure](#project-structure)
  - [Setup Instructions](#setup-instructions)
  - [Usage](#usage)

## Project Overview

The goal of this project is to scrape book data from BooksMandala across various genres and use this data for data analytics and machine learning tasks. The dataset generated will contain valuable metadata such as book titles, authors, prices, ratings, page count, weight, language, and associated genres.

## Technologies Used

- Python 3.11
- Selenium Webdriver
- CSV (for data export)
- Conda (for environment management)

## Project Structure

`tree -F`

```sh
├── data/
├── logs/
├── src/
│   ├── config/
│   │   └── settings.py
│   ├── main.py
│   ├── models.py
│   └── scraper.py
├── README.md
└── requirements.txt
```

## Setup Instructions

1. Clone the repository

    ```sh
    git clone https://github.com/amoghshakya/booksmandala-data-analytics.git
    cd booksmandala-data-analytics/
    ```

2. Install dependencies

    ```sh
    conda create --name books-scraper python=3.11
    conda activate books-scraper
    pip install -r requirements.txt
    ```

3. Download the appropriate `chromedriver` for your browser version [here](https://googlechromelabs.github.io/chrome-for-testing/) (if you're using Google Chrome) and add it to your `PATH`.

    ```py
    import os
    os.environ["PATH"] += r"/path/to/chromedriver"
    ```

4. Update the `BASE_URL` and `WAIT_TIME` if necessary.

## Usage

```sh
python src/main.py
```

The scraped data will be saved as a CSV file in the `data/` folder
