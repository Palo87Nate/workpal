# Work Pal HR

## Descrption

Work Pal HR is a back-end web application designed for a human resource system. The application is built using the Flask python framework and provides api endpoints.

The goal of this project was to create a system that assists operations within the Human Resource Management (HRM) field. It does so by integrating various aspects of HRM such as Employee Information Management EIM into features, reducing whole operations into easier and faster ones.

The application is designed for use mainly in Small and Medium Entreprises (SMEs). It is also designed for scaling with emphasis on modularity and security of data.


## Table of Contents
- [Installation](#Installation)
- [Features & Usage](#Features-and-Usage)
- [License](#license)


## Installation
To install the application, follow these steps:

0. (Optional) Create a new virtual environment and activate it with the following commands:
```bash
  python3 -m venv venv
  source venv/bin/activate
```
1. Clone the repository using the following command:
```bash
  git clone https://github.com/palo87nate/workpal.git
```
2. Install dependencies:
```bash
  pip install -r requirements.txt
```
3. Configure your database connections in the `config.py` file in the app directory.
4. Run the application using the following command:
```bash
  python -m run
```
5. Access the application at `http://localhost:5000` in your web browser.

## Features and Usage

Work Pal HR is a back-end only applicaion and can be used by sending requests the api edpoints provided from a front-end client. By sending requests these endpoints, the user is allowed to carry out HRM operations such as registering and retrieving employee data and many more.

It is worth noting that the method used in a request is as important as the request body. Incorrect methods may produce unwanted results such as data loss.

### Employee Information Management

- This feature offers users (HRM teams) to easily and efficiently manage employee information from one place. 

- This is achieved by giving the users the capability to create, update and retrieve employee information and communicating with other features to retrieve important information such as employee attendance.

#### API Endpoints

1. /employees/new
  Methods: POST
  Description: Creates a new employee in the database.
  Request Body:
  - last_name (str)
  - first_name (str)
  - department_id (str)
  - role (str)
  - email (str)
  - phone_number (str)


2. /employees/<employee_id>
  Methods: GET, PUT
  Description: Retireves or Updates an employee from the database.
  Request Body:
  - employee_id (int)
  - department_id (string)  <!-- To update the department id with PUT method -->

3. /employees/<employee_id>/tasks
  Methods: GET
  Description: Retrieves all tasks assigned to an employee.
  Request Body:
  - employee_id (int)

4. /employees/<employee_id>/contact
  Methods: GET
  Description: Retrieves contact information for an employee.
  Request Body:
  - employee_id (int)

5. /employees/all
  Methods: GET
  Description: Retrieves all employees in the database.
  Request Body: None

### Time and Attendance Tracking

- This feature allows users to track employee attendance and time spent at work by registering when an employee clocks in and clocks out.

- Furthermore, users can also retrieve a list of employees who clocked in or did not clock in for work on a particular date.

#### API Endpoints

6. /clock-in
  Methods: POST
  Description: Clocks in an employee.
  Request Body:
  - employee_id (int)

7. /clock-out
  Methods: POST
  Description: Clocks out an employee.
  Request Body:
  - employee_id (int)

8. /attendance/<employee_id>
  Methods: GET
  Description: Retrieves attendance information for an employee.
  Request Body:
  - employee_id (int)

9. /presence/<date_str>
  Methods: GET
  Description: Retrieves a list of employees present on a given date.
  Request Body:
  - date_str (str)

10. /absence/<date_str>
  Methods: GET
  Description: Retrieves a list of employees absent on a given date.
  Request Body:
  - date_str (str)

### Recruitement Candidate Management

- This feature allows users to manage the information and documents of candidates who apply for a job in their organisation.

- This is done by giving users the capability to create candidates and retrieve their information and documents.

- Furthermore, users can also retrieve a list of candidates who applied for a particular job.

#### API Endpoints

11. /candidates/new
  Methods: POST
  Description: Creates a new candidate applying for employment.
  Request Body:
  - last_name (str)
  - first_name (str)
  - department_id (str)
  - position (str)
  - experience (float)
  - email (str)
  - phone_number (str)

12. /candidates/<candidate_id>
  Methods: GET
  Description: Retrieves information about a candidate.
  Request Body:
  - candidate_id (float)

13. /candidates/<candidate_id>/contact
  Methods: GET
  Description: Retrieves contact information for a candidate.
  Request Body:
  - candidate_id (float)

14. /candidates/post/<position>
  Methods: GET
  Description: Retrieves candidates applying for a specific position.
  Request Body:
  - position (str)

15. /candidates/<candidate_id>/documents
  Methods: POST, GET
  Description: Uploads or retrieves documents for a candidate.
  Request Body:
  - candidate_id (float)

### Department Mnagement

- This feature allows users to manage the departments in their organisation.

- Users can create new departments and assign (and reassign) them a manager. They can also retrieve employees and tasks that are registered in a department.

#### API Endpoints

16. /departments/new
  Methods: POST
  Description: Creates a new department.
  Request Body:
  - department_name (str)

17. /departments/<department_id>/employees
  Methods: GET
  Description: Retrieves employees working in a specific department.
  Request Body:
  - department_id (float)

18. /departments/<department_id>/tasks
  Methods: GET
  Description: Retrieves tasks assigned to employees in a specific department.
  Request Body:
  - department_id (float)

19. /departments/all
  Methods: GET
  Description: Retrieves all departments.
  Request Body: None

20. /departments/<department_id>
  Methods: GET, PUT, DELETE
  Description: Retrieves, updates, or deletes a department.
  Request Body:
  - department_id (float)
  - manager_id (float) <!-- to update the department manager with PUT method -->

### Task Management

- This feature simply allows users to create tasks, monitor them to see progress and assign them to employees and departments.

#### API Endpoints

21. /tasks/new
  Methods: POST
  Description: Creates a new task.
  Request Body:
  - task_name (str)
  - department_id (str)
  - employee_id (int)
  - completed (bool)

22. /tasks/all
  Methods: GET
  Description: Retrieves all tasks.
  Request Body: None

23. /tasks/<task_id> 
  Methods: GET, PUT, DELETE
  Description: Retrieves, updates, or deletes a task.
  Request Body:
  - task_id (int)
  - completed (bool) <!-- to update the task complete status with PUT method -->
  - employee_id (int) <!-- to reassign a task to another employee with PUT method -->

### Conclusion

These features can be organised to the liking of the users depending on their needs, i.e. not only HRM personel can interact with the application, this can be arranged within the front-end client.

## License
This project is licensed under the GPL License - see the [LICENSE](LICENSE) file for details.

## Contact
If you have any enquiries concerning my project, feel free to contact me on my [email](mailto:nathannkweto@devpalo.tech)