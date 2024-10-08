# Store Inventory Management Application

A robust desktop application built using Django and Electron, designed specifically for managing inventory in electronic stores. This solution combines the power of Django's backend capabilities with Electron's desktop interface for a seamless user experience.

## ✨ Features

- 📦 Efficient inventory tracking and management
- 🔄 Real-time updates and synchronization
- 🎯 User-friendly desktop interface powered by Electron
- 🔒 Secure backend infrastructure using Django
- 📊 Comprehensive reporting and analytics
- 🔍 Advanced search and filtering capabilities

## 🔧 Prerequisites

- Python 3.x
- Node.js (v14 or higher)
- Django
- Electron

  
## 🚀 Installation

### Backend (Django)

1. Navigate to the Django project directory:
   ```bash
   cd store
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   ```

   - On Unix or MacOS:
     ```bash
     source env/bin/activate
     ```

   - On Windows:
     ```bash
     env\Scripts\activate
     ```

3. Install required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations and start the Django server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

### Frontend (Electron)

1. Navigate to the Electron app directory:
   ```bash
   cd electron-app
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the Electron app:
   ```bash
   npm start
   ```

## 💻 Usage

1. Launch the application using the steps above.
2. Log in with your credentials.
3. Use the intuitive interface to manage your inventory:
   - Add/remove items
   - Update stock levels
   - Generate reports
   - Track sales and restocking

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## 🔮 Future Enhancements

1. Barcode scanning integration
2. Cloud synchronization
3. Mobile companion app
4. Advanced reporting features

## 📞 Contact

For any queries or issues, please reach out:

- **Maintainer:** Abraham Alemayehu
- **Email:** [abr099684@gmail.com](mailto:abr099684@gmail.com)
- **Project Link:** [https://github.com/abalex12/store](https://github.com/abalex12/store)
