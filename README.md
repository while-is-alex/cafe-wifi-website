# Coffee and Wi-Fi
A website built with Python and Flask for a SQL database for cafés. Project developed independently.

## Getting started
1. Clone the repository:
```
git clone https://github.com/while-is-alex/cafe-wifi-website.git
```

2. Change the directory to the project folder.

3. Create a virtual environment and activate it:
```
py -m venv venv
source venv/bin/activate
```

4. Install the required packages:
```
pip install -r requirements.txt
```

5. Finally, to get the website running, run the `main.py` file. The website will launch and display the home screen.

![home.png](https://i.ibb.co/CH6TRBD/home.png)

## Features
### Database
A SQL database presented as a table where one can see information for a café, such as: name, location, a Google Maps location address, the price for a basic cup of coffee, the availability for Wi-Fi, the availability for power sockets, the availability for toilet, whether the café takes calls, the number of seats available and an image of the café.

![database.png](https://i.ibb.co/DQbDkhs/all.png)

### Random selection
From the home page, the user has the option of having a random café from the database returned to them.

![random-café.png](https://i.ibb.co/Px16RDS/random.png)

### Search by location
From the top right corner of the page, the user has the option for searching by location. A page is returned containing all the cafés in that location.

![search-café.png](https://i.ibb.co/4F515N4/search.png)

### Adding a new café
From the database page, the user can find the option to add a new café to the database. Through the use of a WTForm, the user can populate all the information necessary to the new registry.

![add-café.png](https://i.ibb.co/K2bd7MK/add.png)

### Update a café
From the database page as well, the user can find the option to edit the information for a café. By clicking on the edit icon, the user is presented with a WTForm pre-populated with the information currently registered for that café. After editing and submiting the information that needs to be updated, the register for that café is updated at the database level and the information present at the table is updated as well.

![update-café.png](https://i.ibb.co/w0bsvxP/update.png)

### Deleting a café

Lastly, from the database page, the user has the option to delete a café from the database.

## Requirements
This app requires the following:

+ Python 3
+ Flask
+ Flask-Bootstrap
+ Flask-SQLAlchemy
+ Flask-WTF
+ WTForms
+ python-dotenv
