echo "Ожидание PostgreSQL..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done
echo "PostgreSQL запущен"

echo "Применяем миграции..."
python manage.py migrate

echo "Создаем суперпользователя..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

echo "Собираем статику..."
python manage.py collectstatic --noinput

echo "Запускаем сервер..."
exec gunicorn shop.wsgi:application --bind 0.0.0.0:8000 --workers=4
