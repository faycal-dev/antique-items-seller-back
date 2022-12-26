This is an antique item seller and bidding website made with **NextJS** and **Django** <br/>

## Getting Started

First, download zip file for both the frontend and backend after that:<br />
Back: [https://github.com/faycal-dev/antique-items-seller-front.git] <br />
Front: [https://github.com/faycal-dev/antique-items-seller-back.git]<br />

for the backend do: <br />

- Extract the file
- run the following commands:

```bash
cd antique-items-seller-back-main
# then
python -m venv venv
# then
.\venv\Scripts\activate
# then
pip install -r requirements.txt
# when the installation is finished run
python manage.py runserver
# your backend is ready
```

for the frontend do: <br />

- Extract the file
- run the following commands:

```bash
cd antique-items-seller-front-main
# then
npm install
# when the installation is finished run
npm run dev
# or
yarn dev
# your frontend is ready
# if you want to build the front end run:
npm run build
# then
npm start
```

## Details and technologies

**FrontEnd** : Nextjs(reactjs), Bootstrap, Styled components. <br />
**Backend** : Django rest framework, Cloudinary storage (for image storing) <br/>
**Database** : SQLlite (only in dev mode in production it well be better to use PostgreSQL but the configuration doesn't change)<br>

**API Documentation** : http://127.0.0.1:8000/docs/
