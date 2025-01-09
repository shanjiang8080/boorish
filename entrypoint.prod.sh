#!/bin/sh

if [ "$DATABASE" = "mariadb" ]
then
    echo "Waiting for mariadb..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "MariaDB started"
fi



# python manage.py flush --no-input don't do this!
python manage.py makemigrations # if you update the system, you want things to carry over.
python manage.py migrate --noinput
python manage.py collectstatic --no-input --clear

if [ ! -z "$DJANGO_SUPERUSER_PASSWORD" ] && [ ! -f ./initialized.flag ]; then # fix this to be proper and
    echo "Creating an admin account with password: $DJANGO_SUPERUSER_PASSWORD"
    # Perform your initialization tasks here
    python manage.py createsuperuser --noinput --username=admin --email=admin@example.com
    # After performing tasks, you can unset the variable if needed
    unset DJANGO_SUPERUSER_PASSWORD
    # Save state to indicate initialization has been performed
    touch /home/boorish/web/initialized.flag
else
    if [ ! -f ./initialized.flag ]; then
        echo "Creating an admin account with default password: boorish_web"
        # Perform your initialization tasks here
        export DJANGO_SUPERUSER_PASSWORD=boorish_web
        python manage.py createsuperuser --noinput --username=admin --email=admin@example.com
        # After performing tasks, create the flag file
        unset DJANGO_SUPERUSER_PASSWORD

        touch /home/boorish/web/initialized.flag
    else
        echo "not creating an admin account"
    fi
fi

gunicorn boorish.wsgi:application --bind 0.0.0.0:7999

exec "$@"
