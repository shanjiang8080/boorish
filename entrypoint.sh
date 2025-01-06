#!/bin/sh

if [ "$DATABASE" = "mariadb" ]
then
    echo "Waiting for mariadb..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "mariadb started"
fi

python manage.py flush --no-input
python manage.py migrate

if [ ! -z "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creating an admin account with password: $DJANGO_SUPERUSER_PASSWORD"
    # Perform your initialization tasks here
    python manage.py createsuperuser --noinput --username=admin --email=admin@example.com
    # After performing tasks, you can unset the variable if needed
    unset DJANGO_SUPERUSER_PASSWORD
    # Save state to indicate initialization has been performed
    touch /usr/src/boorish/initialized.flag
else
    if [ ! -f /usr/src/boorish/initialized.flag ]; then
        echo "Creating an admin account with password: boorish_dev"
        # Perform your initialization tasks here
        export DJANGO_SUPERUSER_PASSWORD=boorish_dev
        python manage.py createsuperuser --noinput --username=admin --email=admin@example.com
        # After performing tasks, create the flag file
        unset DJANGO_SUPERUSER_PASSWORD

        touch /usr/src/boorish/initialized.flag
    else
        echo "not creating an admin account"
    fi
fi

exec "$@"
