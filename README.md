# TP: ETL

## Data

[kaggle amazon-books-dataset](https://www.kaggle.com/datasets/parthdande/amazon-books-dataset)

Se descarga con:

```bash
pip install kaggle
kaggle datasets download -d parthdande/amazon-books-dataset
unzip amazon-books-dataset.zip
```

### Columns and validations

- `Book Name`: String. Puede ser vacío.
- `Author`: String. Si es vacío, se usa `Anonymous`.
- `Number of Pages`: Entero. Tiene que ser mayor o igual a cero. Si es menor que cero se usa `null`.
- `Number of Reviews`: Entero. Tiene que ser mayor o igual a cero. Si es menor que cero se usa `null`.
- `Ratings`: Punto flotante. Tiene que estar entre 1 y 5. Si no se usa `null`.
- `Total Reviews`: Entero. Tiene que ser mayor o igual a cero. Si es menor que cero se usa cero.
- `Price`: Entero. Tiene que ser mayor o igual a cero. Si es menor que cero se usa `null`.
- `Language`: String. Puede ser vacío.
- `Category`: String. Puede ser vacío.

Libros sin nombre y autor son descartados.

El archivo `Test_Amazon_BooksDataset.csv` tiene casos borde de prueba.
Para usarlo:

```bash
export DB_TP_FILE_NAME=Test_Amazon_BooksDataset.csv; python tp.py
```

## Pre-requisitos

```bash
sudo apt install python3.11 python3.11-venv sqlite3
python3.11 -m venv venv
pip install pip --upgrade
pip install -r requirements.txt
```

## Activar virtual environment

```bash
source venv/bin/activate
```

## Comandos

Para correr

```bash
# Inicializar la base de datos
bash init.sh
# Ingresar datos
python tp.py
```

Con variables de entorno se puede:

- Correr en modo debug:

```bash
export DB_TP_LOG_LEVEL=DEBUG; python tp.py
```

- Cambiar el archivo de entrada:

```bash
export DB_TP_FILE_NAME=Another_Amazon_BooksDataset.csv; python tp.py
```

- Cambiar la base de datos:

```bash
export DB_TP_DATABASE_NAME=Another_database.db; python tp.py
```

## Herramientas

- Ver la base de datos:

```bash
sqlite3 amazon_books.db
```

o con [dbeaver](https://dbeaver.io/).
