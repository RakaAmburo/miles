module.exports = {
  apps: [
    {
      name: "phone-tracker",
      script: "phoneHome.py",
      interpreter: "/home/pablo/repos/miles/.venv/bin/python3"
    },
    {
      name: "security-controller",
      script: "security_controller.py",
      interpreter: "/home/pablo/repos/miles/.venv/bin/python3"
    }
  ]
}

/* module.exports = {
  apps: [
    {
      name: "phone-tracker",
      script: "phoneHome.py",
      interpreter: "/home/pablo/repos/miles/.venv/bin/python3"
    },
    {
      name: "invoice-reader",
      script: "invoiceReader.py",
      interpreter: "/home/pablo/repos/miles/.venv/bin/python3"
    }
  ]
}

bashpm2 restart ecosystem.config.js */