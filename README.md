# Pralay Mitra

Pralay Mitra is a disaster alert and weather forecast web application designed to provide real-time updates on floods, droughts, and other natural disasters. The application also includes safety features, emergency contacts, and precautionary measures.

## Features
- **Real-time Weather Forecasts**: Get accurate weather updates.
- **Disaster Alerts**: Receive notifications about potential floods and droughts.
- **Emergency Contact & Safety Tips**: Access emergency contacts and safety measures.
- **Machine Learning Predictions**: Analyze data to predict upcoming weather events.

## Tech Stack
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **Machine Learning**: Integrated for disaster prediction

## Installation & Setup
To run Pralay Mitra locally, follow these steps:

### 1. Clone the Repository
```bash
git clone https://github.com/anujjainbatu/Pralay_Mitra.git
cd Pralay_Mitra
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations
```bash
python manage.py migrate
```

### 5. Run the Development Server
```bash
python manage.py runserver
```

The application will now be accessible at `http://127.0.0.1:8000/`.

## Usage
1. Open the application in a browser.
2. Navigate through disaster alerts, weather reports, and safety guidelines.
3. Use the prediction feature to analyze weather trends.

## Contribution
Feel free to fork this repository and submit pull requests to improve the project. Contributions are always welcome!

## License
This project is licensed under the MIT License.

---

For any issues, please raise a GitHub issue or contact the repository owner.