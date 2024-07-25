# Fall Detection and Emergency SOS System
Check the ANN model [here](https://studio.edgeimpulse.com/public/394878/live) on Edge Impulse
This project is a fall detection and emergency SOS system built with Django, Twilio, and Arduino. It detects falls using an Arduino board and sends emergency SMS messages to designated emergency contacts when a fall is detected.

## Features

- User registration and login
- Dashboard for monitoring fall detection events and user information
- Real-time fall detection using an Arduino board
- Emergency SMS notifications to designated emergency contacts
- Fall detection report in PDF format
- Real-time location tracking and sharing through Google Maps

## Prerequisites

- Python 3.x
- Django 3.x
- Twilio account with SMS capabilities
- Arduino board with fall detection sensors
- Required Python packages (see `requirements.txt`)

## Installation

1. Clone the repository:
   https://github.com/Simeonone/an-embedded-fall-detection-system-and-automatic-emergency-response.git
   
3. Change into the project directory:
   cd fall-detection-system
   
4. Create a virtual environment and activate it:
   python -m venv venv
   source venv/bin/activate  # For Unix/Linux
   venv\Scripts\activate  # For Windows
   
5. Install the required packages:
   pip install -r requirements.txt
   
6. Set up the database:
   python manage.py makemigrations
   python manage.py migrate
   
7. Create a superuser account:
   python manage.py createsuperuser

8. Set up the Arduino board and connect it to your computer.

9. Configure Twilio credentials:
- Create a `.env` file in the project root directory.
- Add your Twilio account SID, auth token, and phone number to the `.env` file:
  ```
  TWILIO_ACCOUNT_SID=your_account_sid
  TWILIO_AUTH_TOKEN=your_auth_token
  TWILIO_PHONE_NUMBER=your_twilio_phone_number
  ```

9. Run the development server:
   python manage.py runserver

10. Access the application in your web browser at `http://localhost:8000`.

## Usage

1. Register a new user account through the registration page.
2. Log in to the dashboard using your credentials.
3. Set up emergency contacts in the dashboard.
4. Ensure the Arduino board is connected, that you have turned on bluetooth, and running the fall detection program.
5. Monitor fall detection events in real-time on the dashboard.
6. When a fall is detected, an emergency SMS will be sent to the designated emergency contacts.
7. View the fall detection report in PDF format from the dashboard.
8. Real-time location of the user will be shared through a Google Maps link in the SMS.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
