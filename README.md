# `noticov`

## Installation

The installation requires `poetry`. Poetry can be installed 
from most of the standard package managers like `apt`, `pacman` or `brew`.
Otherwise, take a look at `pip` package of `poetry`.

`noticov` requires some important environment variables for its functioning.
As `noticov` uses CockroachDB, it's important to provide a cockroach DB local or 
free cloud string, which is required to store the data...

This is possible by setting `DB_STRING` variable, preferable in the `.env` file.

* Create a cockroach DB account, or host your own instance. See [cockroach DB docs](https://www.cockroachlabs.com/docs/)
for more information
  
* Create a `.env` file and add `DB_STRING="postgresql://......"`

* Install the dependencies required for it to run.

```bash
poetry shell 
```

* Now run the python backend first...

```bash
python3 -m noticov
```

By design, the backend is independent of the frontend. Both of them are run as separate processes.
The backend handles all the notification part, crawling the API data and storing the data to the 
CockroachDB database. The frontend handles the UI, allows users to register for notifications and 
gives a visualization.

* \[Optional\] Run the frontend too
```bash
python3 -m noticov.frontend 
```

## License 

This project is licensed under the `MIT License` 2021. See [LICENSE](./LICENSE) 
for more information.
