# **ATM-machine & Back Office Operation**


_My mini-project by self-learning ( based on a 1.5-month learning duration )._

_This project demonstrates my skills in Python programming, problem-solving, and data handling._


--------------------------------------------------------------------------------------

### **Contact:** 

>  **_Ashok_** | [G-Mail](ashokdr.paul@gmail.com) | [Telegram](https://t.me/Kum_1)

-----------------------------------------------------------------------------------------------------------------------


> ## *Projects:*
>
>>  1. ATM Machine
>>  2. Back Office Operation
>
>
> ## *Main:*
>>  * Run **_ATM machine.py._** for the ATM Machine simulation.
>>   
>>  * Run **_Back_Office_Operation.py_** for the back office operation.


## *ATM Machine (Machine_operation.py):*

 - Simulates an ATM machine using Python
 - Utilizes Object-Oriented Programming (OOP) concepts
 - Handles user input and output
 - Demonstrates error handling and debugging

## *Back Office Operation (Back_Office_Operation.py):*

 - Provides back office access for administrative tasks
 - Handles JSON data for storing, retrieving, and manipulating data
 - Implements user input and output
 - Demonstrates error handling and debugging


--------------------------------------------------------------------------------------


## *Description of files:*
### ATM_machine.py 
  * Which is the **_ATM machine Simulation.__*

### Back_Office_Operation.py 
  * This is a Simulation of the back office operation of an imaginary Banking Enterprise.

### BO_credentials.json
> * Contains credentials for **_Master Control access._**
> * Data in the file are as below

   | Master Access ID | Key | Override Key |
   |------------------|-----|--------------|
   | 1                | 9   | 9            |
    
### admin_data.json
> * Contains credentials for **_Admin Dashboard access._**
> * Data in the file are as below

   | Admin ID | Key |
   |----------|-----|
   | ashok    | 91  |
   | kumar    | 92  |
   | 01       | 11  |
   | 1        | 1   |
    
### client_data.json
> * Contains data of all the clients which is **_Client ID, Name, PIN, wrong PIN limit, available balance, minimum limit, and maximum limit._**
> * An example overview of the data in this .JSON file is below

 | Client ID | Client Name      | Wrong PIN Limit | Client PIN | Client Available Balance | Min Limit | Max Limit |
 |-----------|------------------|-----------------|------------|--------------------------|-----------|-----------|
 | 01        | raghul           | 5               | 1111       | 1,707,600                | 100       | 50,000    |
 | c_02      | siyamala devi    | 5               | 2222       | 42,400                   | 100       | 50,000    |
 | c_03      | balu             | 5               | 3333       | 20,000                   | 100       | 50,000    |

### machine_data.json
> * Contains machine data of **_Machine ID, machine available balance, machine status, and cash denomination_**.
> * An example overview of the data in this .JSON file is below

| Machine ID | Machine Status | Machine Available Balance |
|------------|----------------|---------------------------|
| m_01       | Running        | 300,000                   |

**Cash Denomination**

| Denomination | Count |
|--------------|-------|
| 500          | 300   |
| 200          | 500   |
| 100          | 500   |

### transaction_book.json
> * contains the last 5 transactions of all the clients.


--------------------------------------------------------------------------------------

## **_Technologies Used_**:

 - Python programming language
 - JSON data handling
 - Data storage and manipulation
 - Object-Oriented Programming (OOP) concepts

--------------------------------------------------------------------------------------

## *_How to Run:_*

1. Clone the repository
2. Run the Python scripts using a Python interpreter



