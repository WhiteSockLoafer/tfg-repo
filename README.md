### Crear entorno virtual de python
> python3 venv venv 

> source venv/bin/activate

> pip install requirements.txt

### Descargar el corpus
> mkdir corpus

> cd trainer/boeextractor

> python3 boe_extractor.py 15 ../corpus 'https://www.boe.es/buscar/legislacion.php?accion=Mas&id_busqueda=_cGhXenk1dEdldTRsT0JSRFkzVjBNNGpJWlg3aFBkZ0V5cTRMWTRJMjZDdjI1aEZVOWV5dENxWWRpUzNlQ0phVXdlR0xwV0RVNCtyb1hWZnNBaithamVzZWp1cjBSN0xqbkhzOGZnVGs3enhBTDJ4SDBKTENoSXU2ckRZUkpGdGtEdHErN0RCWTRKcWNFMSt3cEJIbnp3ekVIMVhLZjliTnk1RzAvTHowNFdjPQ%2C%2C-0-2000&page_hits=2000&sort_field%5B0%5D=FPU&sort_order%5B0%5D=desc'


### Entrenar y evaluar los modelos
> cd ../model_trainer 

> python3 train.py ../corpus ../analogies/dataset

### Iniciar la interfaz web

> cd ../../legal_search

> python manage.py runserver
