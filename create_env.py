#!/usr/bin/env python
"""Generate .env file with environment variables."""

with open('.env', 'w') as f:
    f.write("""SECRET_KEY=django-insecure-nh(dosnhki9uco1uimsge5e+834(1t^7&fl*f2i!5tmz(q51xx
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,188.243.125.83,*
DB_HOST=77.239.102.166
DB_NAME=app_db
DB_USER=admin
DB_PASSWORD=your_strong_password
DB_PORT=5432
""") 