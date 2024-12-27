# EduVance-Backend

EduVance-Backend is a Django-based backend system that includes user registration, admin panel, authentication with email, permission authorization, private API access, and a student panel.

## Features

- **User Registration**: Allows users to register an account through an easy-to-use sign-up form.
- **Admin Panel**: Provides administrative access to manage users, permissions, and monitor system activity.
- **Authentication with Email**: Secure user authentication via email with a verification system.
- **Permission Authorization**: Role-based access control for users, allowing different permissions based on user roles (admin, student, etc.).
- **Private API Access**: Exposes private APIs accessible only to authenticated and authorized users, ensuring secure data handling.
- **Student Panel**: A dedicated section for students to manage their profiles, view their data, and interact with the system as required.

## Installation

To get a local copy of this project up and running, follow these simple steps.

### Prerequisites

1. **Python**: Ensure you have **Python 3.13.x** installed. If not, download it from [python.org](https://www.python.org/downloads/).
2. **Django**: Install Django by running:
    ```bash
    pip install django
    ```
3. **Database**: This project uses Django's ORM, so a database like PostgreSQL or SQLite can be used. Make sure to install necessary database connectors if needed (e.g., `psycopg2` for PostgreSQL).

### Clone the repository

```bash
git clone https://github.com/SYN606/EduVance-Backend.git
cd EduVance-Backend
```
### Install dependencies

Use `pip` to install the required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

## License

This project is licensed under the GPL-3.0 License.

## Acknowledgements

- Thanks to the EduVance-Backend team for their contributions and support.
- Special thanks to the open-source community for the various libraries used in this project.
