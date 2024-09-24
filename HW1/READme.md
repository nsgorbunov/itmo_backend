
# HW1 Никита Горбунов

## Установка и запуск

### Клонирование репозитория

```bash
git clone git@github.com:nsgorbunov/itmo_backend.git
```
```bash 
cd itmo_backend
```
```bash 
cd HW1
```

### Установка Python 3.10

Требуется Python версии 3.10. 

```bash
brew install python@3.10
```


```bash
python3.10 --version
```

### Создание виртуального окружения

Создайте и активируйте виртуальное окружение:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
```

### Установка зависимостей

Установите все зависимости проекта:

```bash
make dev.install
```

### Запуск приложения и тестов одной командой

Запустите сервер приложения и тесты:

```bash
make test
```

Команда автоматически запустит сервер и выполнит тесты для проверки работы API.