# Complefy

Link to SCRUM-Board: https://trello.com/invite/b/67335ffd8314a50756abf0e9/ATTI45c6471ebdf7419d855cd04340806eec428005A7/complefy

## How to run
### Clone repository
```bash
git clone git@github.com:ivoheck/Complefy.git
```

### Setup Api key
Create a file named `secret.py` in the root of the Projekt  
Put the Api key in the file as a string named `api_key`

```python
api_key = "your api key"
```

Make sure to never push this key to any repository

### Start Complefy
Build Docker Container
```bash
sudo docker build -t complefy-app .
```
Run Docker Container
```bash
sudo docker run --name complefy-app-container complefy-app
```

### Stop Docker Container
Stop and delete Container
```bash
sudo docker stop complefy-app-container
sudo docker rm complefy-app-container
```
Complefy can be started again
```bash
sudo docker run --name complefy-app-container complefy-app
```

## Usage
