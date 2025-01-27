# Complefy

Link to SCRUM-Board: https://trello.com/invite/b/67335ffd8314a50756abf0e9/ATTI45c6471ebdf7419d855cd04340806eec428005A7/complefy

## How to run
### Clone repository
```bash
git clone git@github.com:ivoheck/Complefy.git
```

### Setup API key
Create a file named `secret.py` in the root of the Projekt  
Put the API key in the file as a string named `api_key`

```python
api_key = "your api key"
```

Make sure to never push this key to any repository

### Start Complefy
Build Docker Container
```bash
docker build -t complefy-app .
```
Run Docker Container
```bash
docker run -d --name complefy-app-container -p 5004:5004 complefy-app
```

### Run Docker Container
Stop and delete Container
```bash
docker stop complefy-app-container
docker rm complefy-app-container
```
Complefy can now be started again
```bash
sudo docker run --name complefy-app-container complefy-app
```

## Usage
Running the Docker container will host the web page on `http://172.17.0.2:5004`  
The web page can be accessed through a web browser

## Contributors
Henry  
Ahmad  
Ivo  

## Disclaimer
AI tools like Chat-GPT were used to write parts of the source code.
