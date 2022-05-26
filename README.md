# autostat

Установка зависимостей
```
pip install -r requirements.txt
```
также нужно уснатовить snakemake - https://snakemake.readthedocs.io/en/stable/getting_started/installation.html

--- 
Сырые данные лежат в data/raw
- исходный файл - pledges.csv
- список правил для брендов - brands.jsonl
- список правил для моделей - brands/*.jsonl

----
Чтобы запустить весь процесс обсчета исходного файла пишем в консоли
может понадобится `export PYTHONPATH="${PYTHONPATH}:path/to/project` разрулить это нормально потом
```
snakemake --cores all
```
- Эта команда сгенерирует правила, на которые опирается модель и сохранит их в data/interim/rules
- Далее запустит добавление пробелов в исходном файле - результат сохранит в data/interim/pledges_with_spaces.xls
- Далее найдет в данных марку модель и год выпуска - итоги сохранит в **data/processed/pledges_with_ner.xls**

----
Чтобы посмотреть диаграммы нужно запустить ноутбук
```
python -m notebook
```
после этого зайти в файл src/notebooks/analize.py.ipynb
запускаем код в ячейках

Если нужно еще раз пересчитать результат для файла вводим команду `snakemake --cores all -R add_spaces`
