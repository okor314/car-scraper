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
