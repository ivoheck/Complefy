# Complefy

Link to SCRUM-Board: https://trello.com/invite/b/67335ffd8314a50756abf0e9/ATTI45c6471ebdf7419d855cd04340806eec428005A7/complefy

## How to run
### Clone repository
```bash
git clone git@github.com:ivoheck/Complefy.git
```

### Start Docker Container
```bash
sudo docker build -t complefy-app .´
sudo docker run --name complefy-app-container complefy-app
```
#### Web page will be published (locally) on http://172.17.0.2:5004 
