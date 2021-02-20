I have used middlewares to check for the expired tokens.
Otherwise we can also use Celery or cron jobs to schedule the events
which i have registered in the custom middleware.

No need of postman apis since i have configured swagger in this.
Use: HOSTNAME/swagger/