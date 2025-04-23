# Run code via `gunicorn`
```shell
gunicorn main.app
```

## Windows uchun `gunicorn` orniga `waitress` install qilinadi
```shell
waitress-serve --host 127.0.0.1 --port 8000 main:app
```

## Testlarni ishlatish uchun
```shell
pytest test_app.py
```

## Kodning qancha qismi testlanganini bilish uchun quyidagi buyruqni yuriting
```shell
pytest --cov=. test_app.py 
```


## PyPi'ga upload qilish uchun `twine` dan foydalanamiz

```shell
python setup.py sdist bdist_wheel --universal

twine check dist/*

twine upload dist/*
```