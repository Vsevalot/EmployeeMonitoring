# Backend
To launch backend just run

`docker compose up --build`

in project's folder.

<details>
  <summary>Possible troubles</summary>
  
If there are any troubles with the database do next:
1. run command `docker compose up db`
2. connect to local database (127.0.0.1, port 5432), user `postgres` password `123`
3. run command `CREATE DATABASE monitoring;`

Run `docker compose up --build` again.
</details>

After that you should be able to connect to the backend on `127.0.0.1:8000`

Check the swagger on [127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
