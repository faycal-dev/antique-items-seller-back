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

**features** :

- Athentication : JWT + HTTP only cookies (for secure connection)
- Account creation : Email verification via link and possibility to reset the password via email link
- Product list : list of all products with the possibility of title and description search and order by price
- Product details : The details of the product (Your bid if exists, the winning bid, time left, product features)
- Bidding : The possibility to bid on a product multiple times if you are not the higher bid
- Auto bidding : the possibility to activate and inactivate auto bidding on multiple products (Concurence cases are treated)
- Email notifications : when the auto bidding pass the treshold an email is sent to the user
- profile : The place wher you can set up the auto bidding max amount and notification treshhold
- Web admin : In the profile page if you are an admin you will find a button to navigate to admin page <br/>
  The admin can create, delete, update and see all the bids on a product
- Super admin : You can access the super admin by navigating to (http://127.0.0.1:8000/admin/) where you have more advanced control over users and products ...

**The website is fully responsive**

**Users**:
**_normal users_**
It will be better if you create your own user to recieve email notifications <br/>
username : user1 , password : user1 <br/>
username : user2 , password : user2

**_ users_**
It will be better if you create your own user to recieve email notifications <br/>
username : admin1 , password : admin1 <br/>
username : admin2 , password : admin2
