# Data Eng Tech Exercise

El ejercio se desarrollo para resolver la problematica planteada:

> [!NOTE]
>
> This project is a big data migration to a new database system. You need to create a PoC to solve the next requirements

A continuación se detallan los pasos de cada punto de los requerimientos.

#### Requerimiento 1

> 1. **Move historic data from files in CSV format to the new database.** 

Se creó una una notebook de Jupyter para esto, dentro del repositorio esta contenida en la carpeta csv2pgsql dentro del repositorio

![Captura de pantalla 2024-06-14 a la(s) 9.25.51 a.m.](/Users/omar/Desktop/Captura de pantalla 2024-06-14 a la(s) 9.25.51 a.m..png)

Usando Python, Pandas y SQLAlchemy, se cargan los archivos separados por comas (CSV) y se descargan a los datos. 

Paso 1, cargar base de datos, la bases de datos en cuestión es una PostgreSQL, vía Docker



![imaegen_postgres](/Users/omar/Desktop/imaegen_postgres.png)

Se busca en DockerHub y se descarga (pull), una vez descargada, se ejecuta el siguiente comando en la consola

```bash
docker run -p 5432:5432 --name ttg_pgsql -e POSTGRES_USER=root -e POSTGRES_PASSWORD=root -d postgres
```

Usaremos el usuario "root" para este ejemplo, el contenedor tendrá por nombre "ttg_pgsql", y su puerto será el default, 5432.

Esto nos generará un contenedor basado en la imagen de PostgreSQL

![contenedor](/Users/omar/Desktop/contenedor.png)



Una vez que ya este corriendo, nos conectamos, y vamos a crear una base de datos para el ejercicio, con la siguiente instrucción:

```sql
create database csv_to_sql_globant;
```

Una vez creada la base de datos, procederemos a crear las tablas necesarias

1. departments
2. jobs
3. employees

Usando el diccionario de datos incluido en el correo del reclutador, el script de las tablas (incluido en el repositorio), es el siguiente:

```sql
CREATE TABLE departments (
    id INTEGER PRIMARY KEY NOT NULL,
    department VARCHAR
);

CREATE TABLE jobs (
    id INTEGER PRIMARY KEY NOT NULL,
    job VARCHAR
);

CREATE TABLE hired_employees (
    id INTEGER PRIMARY KEY NOT NULL,
    name VARCHAR,
    datetime VARCHAR,
    department_id INTEGER,
    job_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (job_id) REFERENCES jobs(id)
);
```

Al verificar que todo se haya ejecutado sin problemas, se procede a insertar los archivos

primero, se cargan los datos a un dataframe de pandas

```python
df_jobs = pd.read_csv('jobs.csv', delimiter=',', header=None, names=['id', 'job'])
```

y después de conectarnos, via SQLAlchemy

```python
engine = create_engine('postgresql://root:root@localhost:5432/csv_to_sql_globant')
```

ejecutamos el método to_sql() para insertar la información

```python
df_jobs.to_sql('jobs', engine, if_exists='append', index=False)
```

Después de ejecutar, se revisa que los datos hayan sido importados correctamente.

![jobs](/Users/omar/Desktop/jobs.png)

El proceso es el mismo para el resto de los archivos. 

Para cumplir con la regla 

> Transactions that don't accomplish the rules must not be inserted but they must be logged

Se limpian los datos, quitando de la lista, los registros que tienen faltante en alguna de sus columnas

```python
df_departments_wo_na = df_departments.dropna()
```

Se registran los registros que tinen faltantes, y se quedan en otro dataframe

```python
df_departments_w_na = df_departments[df_departments.isna().any(axis=1)]
```

![with_na](/Users/omar/Desktop/with_na.png)

Con esto se cumple el requerimiento número 1.



#### Requerimiento 2

> 2. Create a Rest API service to receive new data. This service must have: 
>
> 2.1. Each new transaction must fit the data dictionary rules. 
>
> 2.2. Be able to insert batch transactions (1 up to 1000 rows) with one request. 
>
> 2.3. Receive the data for each table in the same service. 
>
> 2.4. Keep in mind the data rules for each table. 

Se crea, con Python, FastAPI y SQLAlchemy, un REST API para cumplir el requerimiento.

Este api crea una base de datos nueva.

Para el requerimiento 2.1, se toma en cuenta el requerimiento 2.4, y se especifica que los campos clave, son autoincrementales, y se especifica en el modelo de SQLAlchemy

```python
class Jobs(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    job = Column(String, nullable=False)
```

En el requerimiento 2.2, se usa SQLAlchemy para un bulk_insert. Si la lista de elementos enviados es mayor a 1000, este sale de la iteración y graba lo que alcanzó a quedar dentro de la lista a insertar.

```python
def batch_insert_jobs(db: Session, jobs: List[schemas.Job]):
    job_list = []
    for count, job in enumerate(jobs, start=1):
        job_item = models.Jobs(**job.dict())
        job_list.append(job_item)
        if count == 1000:
            break
    db.bulk_save_objects(job_list)
    db.commit()
```

Para el requerimiento 2.3, cada tabla tiene su grupo de endpoints

Los endpoints se muestran a continuación:

![jobsendpoins](/Users/omar/Desktop/jobsendpoins.png)

![dependpoints](/Users/omar/Desktop/dependpoints.png)

![empendpoints](/Users/omar/Desktop/empendpoints.png)

#### Requerimiento 3

> Create a feature to backup for each table and save it in the file system in AVRO format. 

El endpoint es tabla/backup/, por medio del método GET, se llama un procedimiento que hace el backup con el formato AVRO

Usando el siguiente esquema:

```json
{
  "doc": "Jobs Schema",
  "namespace": "test",
  "type": "record",
  "name": "jobs",
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "job",  "type": "string"}
    ]
  }
```

Se genera el archivo .avro de respaldo, con la librería oficial.

```python
def create_jobs_backup(db: Session):
    all_jobs = db.query(models.Jobs).all()
    writer = DataFileWriter(open("backup/jobs.avro", "wb"), DatumWriter(), job_schema)
    for job in all_jobs:
        writer.append({"id": job.id, "job": "{}".format(job.job)})
    writer.close()
```

El archivo queda en la carpeta "backup"

El endpoint avisará si no hubo problemas.



#### Requerimiento 4

El restore desde un archivo .avro, se busca que el archivo este presente, y al encontrarlo, se procede a insertar los datos, con la misma definición (esquema) que se usó en backup.

```python
def restore_job_table(db: Session):
    avro_file = os.path.join(os.getcwd(), 'backup/jobs.avro')
    result = 1
    if os.path.exists(avro_file):
        reader = DataFileReader(open('backup/jobs.avro', 'rb'), DatumReader())
        for job in reader:
            db.add(models.Jobs(**job))
            db.commit()
        reader.close()
        result = 0
    return result
```

El endpoint avisará si no hubo problemas.
