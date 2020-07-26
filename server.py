import os
import sentry_sdk
from bottle import route, run
from sentry_sdk.integrations.bottle import BottleIntegration

# Задайте адрес в переменную окружения SENTRY_DSN локально или на платформе heroku
# или как переменную "sentry_link" прямо в коде
sentry_link = ""
sentry_dsn=os.environ.get("SENTRY_DSN", sentry_link)

if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        integrations=[BottleIntegration()]
    )

@route("/success")
def success():
    return "success"

@route("/fail")
def fail():
    raise RuntimeError("Fail")

if os.environ.get("APP_LOCATION") == "heroku":
    # print("Sentry_dsn - ", sentry_dsn)
    run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        server="gunicorn",
        workers=3,
    )
else:
    # print("Sentry_dsn - ", sentry_dsn)
    run(host="localhost", port=8080, debug=True)