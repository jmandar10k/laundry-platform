# 🧺 Smart Laundry Operations Platform

A comprehensive web application for managing laundry operations with order management, driver assignment, and analytics.

## ✨ Features

- **Multi-user System**: Owner, Outlet Manager, and Delivery Dashboard
- **Order Management**: Complete order lifecycle from creation to delivery
- **Driver Management**: Assign drivers to deliveries with real-time status updates
- **Analytics Dashboard**: Visual reports and KPIs
- **PDF Generation**: Order receipts and reports
- **Dark Mode UI**: Modern, responsive interface

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- SQLite (built-in with Python)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/laundry-platform.git
   cd laundry-platform
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional)
   ```bash
   # Copy the example file
   cp .env.example .env

   # Edit .env with any environment-specific variables as needed
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the app**
   - Open http://localhost:8501 in your browser
   - Default login: `admin` / `admin123`

## 📊 Database Schema

The application uses SQLite with the following tables:
- `outlets` - Store branches and login credentials
- `orders` - Customer orders and status tracking
- `drivers` - Delivery personnel information
- `notifications` - Notification history
- `batches` - Processing batch management

## 🔧 Configuration

### Default Users
- **Owner**: `admin` / `admin123`
- **West Branch**: `west` / `baner123`
- **East Branch**: `ketan` / `123456`
- **South Branch**: `jeevan` / `123123`

## 🌐 Deployment

### Streamlit Cloud
1. Push to GitHub
2. Connect to [Streamlit Cloud](https://share.streamlit.io/)
3. Set environment variables in Streamlit Cloud settings
4. Deploy!

### Local Development
```bash
# Run with custom port
streamlit run app.py --server.port 8502

# Run with specific address
streamlit run app.py --server.address 0.0.0.0
```

## 📱 Usage

1. **Login** with appropriate credentials
2. **Create Orders** through outlet dashboards
3. **Process Orders** in batches
4. **Assign Drivers** for delivery
5. **Track Deliveries** in real-time
6. **View Analytics** for business insights

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues or questions:
- Check the [Issues](https://github.com/yourusername/laundry-platform/issues) page

---

**Built with ❤️ using Streamlit and SQLite**