Roverin Event Micro Service

**Dependencies**

1. Python 3.7.9

2. Mysql 8.x

**Run the project**

 1.Create virtual environment with python3
 
   ```
   python3 -m venv env
   ```

 2.Activate the virtual environment
 
  ```
  source env/bin/activate
  ```
 
 3.Install the requirements
 
  ```
  pip install -r requirements.txt
  ```
 
 4.Update the .env with corresponding values
 
 5.Run the server
  ```
  source export.sh
  ```
  
  
Notes


Initiate migration
```
flask db init --directory apps/database/migrations/
```

Generate new migrations
```
flask db migrate --directory apps/database/migrations/
```

Update existing migrations
```
flask db upgrade --directory apps/database/migrations/ 
```