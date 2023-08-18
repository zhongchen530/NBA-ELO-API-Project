# NBA-ELO-API-Project

Utilized: Django, Celery, Docker, Redis, HTML, PostgreSQL
• Developed a Django API that provides updated Elo rankings of all NBA players and teams after the year 2000

• Created a tested ETL that periodically fetched game data from an existing API to keep rankings updated

• Incorporated Redis and Celery to ensure a smooth user experience while the database is being updated

• Structured the application as a network of docker containers each running Django, Celery, Redis, and Postgre

