#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

# Create superuser with auto-completion
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$superuser', '$akmalsalokhiddinov03@gmail.com', '$qwQW12!@')" | python manage.py shell

# Replace $1, $2, $3 with your desired username, email, and password respectively
