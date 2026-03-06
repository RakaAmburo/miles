pip freeze > requirements.txt
pip install -r requirements.txt

pm2 module.exports = {
  apps: [
    {
      name: "phone-tracker",
      script: "phone_tracker.py",
      interpreter: "/ruta/.venv/bin/python3"
    },
    {
      name: "invoice-reader",
      script: "invoice_reader.py",
      interpreter: "/ruta/.venv/bin/python3"
    },
    {
      name: "dashboard",
      script: "dashboard.py",
      interpreter: "/ruta/.venv/bin/python3"
    }
  ]
}
Y arrancás todo con:
bashpm2 start ecosystem.config.js