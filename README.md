# Car Scraper

Asynchronous web scraper for auto listings with daily scheduled execution and PostgreSQL backups.

---

## Features

- Daily scraping using Playwright
- PostgreSQL storage
- Automatic database dumps
- Dockerized setup
- Scheduling via cron (time configured in `.env`)

---

## Requirements

- Docker
- Docker Compose

---

## Installation

Clone the repository
```
git clone https://github.com/okor314/car-scraper.git
```

---

## Configuration

Create `.env` file in the project root:

```env
POSTGRES_DB=<YOUR-DATABASE>
POSTGRES_USER=<YOUR-USERNAME>
POSTGRES_PASSWORD=<YOUR-PASSWORD>
POSTGRES_HOST=<YOUR-HOST>
POSTGRES_PORT=<YOUR-PORT>

SCRAPE_TIME=12:00
DUMP_TIME=12:00
```
---

## Running the application

Build and start services:

```bash
docker compose up --build
```
---

🛑 Stopping the application

```bash
docker compose down
```
---

## Explanation of main directories and files

- `src/` — directory with main scraping code.  
- `database/` — function for database connection, creation of table and saving data.  
- `scripts/` — bash-scripts for automatisation: database dump and run cron jobs.  
- `dumps/` — results of scheduled database dump.  
- `.env` — configuration: database credentials and scheduling of scraping and dump.  

### Scraping files
 - `main.py` — main script to run scraper.
 - `scraper.py` — scraper logic (scraping catalog, detail pages, pagination).
 - `page.py` — classes for parsing HTML pages.
 - `playwright_client.py` — Initialisation of Playwright.
---
