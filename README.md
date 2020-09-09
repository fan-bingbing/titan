# Titan project
## a fullstack solution providing RF test interface on GME2 protocol compliant radios
### 1. local development env requirement:
VISA backend (NI or R&S)
### 2. recommend use conda to manage virtual env covering following dependencies:
python>=3.7.5\
Django==2.2.4\
pyvisa==1.10.0\
sounddevice\
pyserial\
libportaudio2\
numpy
### 3. spin up server locally
```bash
cd /your/local/clone/directory/titan
python manage.py runserver
```
#### open link in browser
```bash
http://127.0.0.1:8000/
```

#### create superuser to get access to admin site
```bash
python manage.py createsuperuser # follow prompt then

http://127.0.0.1:8000/admin # check out equipment config values
```


### 4. download sample results(csv file) from UI
```bash
http://127.0.0.1:8000/output/  # give it a name and hit submit
```

### 5. some of screenshot results are arhived in
```bash
/your/local/clone/directory/titan/static/result_images
```
