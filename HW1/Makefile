.PHONY: dev.install test

dev.install:
	pip install -r reqirements.txt

test:
	# Запускаем приложение
	uvicorn Gorbunov_HW1:app --host 0.0.0.0 --port 8000 &

	sleep 2
	# Запуск тестов
	pytest test_hw1.py
	# Останавливаем приложение после тестов. Если вдруг что-то не так: tg @nikita_gbn
	kill $$(ps aux | grep 'uvicorn Gorbunov_HW1:app' | grep -v grep | awk '{print $$2}')
	# Нажмите Enter.
