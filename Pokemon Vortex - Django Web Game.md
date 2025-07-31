# Pokemon Vortex - Django Web Game

A fully functional Pokemon-inspired web game built with Django, PostgreSQL, Redis, HTMX, and Bootstrap. Features include Pokemon catching, battles, inventory management, and user progression.

## 🎮 Features

### Core Gameplay
- **Pokemon Catching**: Search for and catch wild Pokemon with different rarities
- **Battle System**: Battle wild Pokemon to gain experience and coins
- **Inventory Management**: Manage Pokeballs, items, and caught Pokemon
- **User Progression**: Level up your trainer and Pokemon through gameplay
- **Shop System**: Purchase items and Pokeballs with earned coins

### Technical Features
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Updates**: HTMX for dynamic content without page reloads
- **User Authentication**: Django Allauth with OAuth support
- **Admin Interface**: Django admin for game management
- **Database Models**: Comprehensive Pokemon and user data models

## 🛠 Tech Stack

- **Backend**: Django 5.2.4, Python 3.11
- **Database**: PostgreSQL (SQLite for development)
- **Cache**: Redis
- **Frontend**: Bootstrap 5, HTMX, HTML/CSS/JavaScript
- **Authentication**: Django Allauth

## 📦 Installation & Setup

### Prerequisites
- Python 3.11+
- PostgreSQL (optional, SQLite works for development)
- Redis (optional for development)

### Quick Start

1. **Clone and Setup**
   ```bash
   cd pokemon_vortex
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py populate_pokemon  # Load initial Pokemon data
   ```

3. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

4. **Access the Game**
   - Game: http://localhost:8000/
   - Admin: http://localhost:8000/admin/

## 🎯 Game Features

### Dashboard
- View trainer stats (level, experience, coins)
- Quick access to all game features
- Daily progress tracking
- Inventory overview

### Pokemon Catching
- Search for wild Pokemon in different areas
- Use different types of Pokeballs for better catch rates
- Pokemon have random levels, stats, and rarities
- Daily catch limits to encourage regular play

### Pokemon Collection
- View all caught Pokemon with detailed stats
- Filter and sort by type, level, IV percentage
- Individual Pokemon pages with full details
- HP and stat management

### Battle System
- Battle wild Pokemon to gain experience
- Strategic turn-based combat
- Earn coins and experience from victories
- Pokemon level up through battles

### Shop
- Purchase Pokeballs and items with coins
- Different ball types with varying catch rates
- Inventory management
- Coin earning tips and strategies

## 🗂 Project Structure

```
pokemon_vortex/
├── pokemon_vortex_project/     # Django project settings
├── game/                       # Main game app
│   ├── models.py              # Pokemon and user models
│   ├── views.py               # Game logic and views
│   ├── admin.py               # Admin interface
│   ├── urls.py                # URL routing
│   └── management/commands/   # Custom management commands
├── accounts/                   # User authentication app
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   └── game/                  # Game-specific templates
├── static/                     # CSS, JS, images
├── requirements.txt           # Python dependencies
└── manage.py                  # Django management script
```

## 🎮 How to Play

1. **Sign Up/Login**: Create an account or use OAuth login
2. **Explore Dashboard**: Familiarize yourself with the interface
3. **Catch Pokemon**: Visit the "Catch Pokemon" page and search for wild Pokemon
4. **Build Collection**: View your caught Pokemon in "My Pokemon"
5. **Battle**: Fight wild Pokemon to gain experience and coins
6. **Shop**: Use earned coins to buy better Pokeballs and items
7. **Progress**: Level up your trainer and Pokemon through gameplay

## 🔧 Configuration

### Environment Variables
Create a `.env` file for production:
```
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:password@localhost/pokemon_vortex
REDIS_URL=redis://localhost:6379/0
```

### Production Deployment
1. Set up PostgreSQL database
2. Configure Redis for caching
3. Set environment variables
4. Run migrations
5. Collect static files: `python manage.py collectstatic`
6. Use a production WSGI server (Gunicorn, uWSGI)

## 🎨 Customization

### Adding New Pokemon
1. Use Django admin to add new Pokemon species
2. Or extend the `populate_pokemon` management command
3. Pokemon data includes stats, types, and rarity

### Modifying Game Balance
- Adjust catch rates in `models.py`
- Modify experience gains in battle system
- Change shop prices and item effects
- Customize daily limits and progression

## 🐛 Troubleshooting

### Common Issues
1. **Template Errors**: Ensure all templates use simple filters (avoid complex math)
2. **Database Issues**: Run `python manage.py migrate` after model changes
3. **Static Files**: Run `python manage.py collectstatic` for production
4. **Redis Connection**: Redis is optional for development, uses dummy cache

### Development Tips
- Use Django admin to manage game data
- Check Django logs for debugging
- Use browser developer tools for frontend issues
- Test with different user accounts

## 📝 License

This project is for educational and demonstration purposes. Pokemon is a trademark of Nintendo/Game Freak.

## 🤝 Contributing

Feel free to fork this project and add your own features:
- New Pokemon types and abilities
- Advanced battle mechanics
- Trading system
- Multiplayer features
- Mobile app version

## 🎉 Credits

Built with Django and modern web technologies. Inspired by the Pokemon franchise.

---

**Enjoy playing Pokemon Vortex!** 🎮✨

