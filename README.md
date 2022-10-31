# 449wordleproject1

### Group Members:
##### Akash Avinash Butala
##### Anvit Rajesh Patil
##### Corey New
##### Jarrod Leong

## **Initializing Database & Start Service:**

##### `cd src/database`
##### `python3 setupDB.py`  *use `setupDB.py -p` to populate the database*
##### `cd ..`
##### `foreman start`

---

## **Testing the APIs**

#### *Can test using user_id: 123abc and username: user1.  Username is not checked but included for redundancy*

### **Register Username & Password**
##### `http POST http://127.0.0.1:5000/register username=<username> password=<password>`

### **Check Username & Password**
##### `http POST http://127.0.0.1:5000/checkPassword username=<username> password=<password>`

### **Create a Game**
##### `http POST http://127.0.0.1:5000/game/create user_id:<user_id> username:<username>`

### **Input Word Guess**
##### `http POST http://127.0.0.1:5000/game/guess user_id:<user_id> username:<username> game_id=<game_id> guess=<guess>`

### **List All Games in Progress**
##### `http GET http://127.0.0.1:5000/game/list user_id:<user_id> username:<username>`

### **List a Specific Game in Progress**
##### `http GET http://127.0.0.1:5000/game/{game_id} user_id:<id> username:<username>`














