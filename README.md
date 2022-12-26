This is an antique item seller and bidding website made with [NextJS] and [Django] 

## Getting Started

First, download zip file for both the frontend and backend after that:
Back: [https://github.com/faycal-dev/antique-items-seller-front.git]
Front: [https://github.com/faycal-dev/antique-items-seller-back.git]

for the backend do: 
 -Extract the file
 -run the following commands:
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

for the frontend do:
 -Extract the file
 -run the following commands:

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

[FrontEnd] : Nextjs(reactjs), Bootstrap, Styled components.
[Backend] : Django rest framework, Cloudinary storage (for image storing)
[Database] : SQLlite (only in dev mode in production it well be better to use PostgreSQL but the configuration doesn't change)

[API_Documentation] : (http://127.0.0.1:8000/docs/)