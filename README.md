# MindCheck - Mental Health Self-Assessment Platform

A comprehensive Django web application that helps users self-identify their mental health status and get personalized guidance for support and wellness resources.

## Features

### Public Pages
- **Home**: Welcome page with featured content and quick access to assessments
- **About**: Information about the platform and its mission
- **How it Works**: Step-by-step guide on using the platform
- **Resources & Support**: Mental health resources, crisis support, and reference links

### Self-Assessment Module
- **Quick Assessment**: 5-question rapid assessment for immediate results
- **Full Assessments**: Comprehensive questionnaires (10-20 questions) covering:
  - Mood and emotional state
  - Sleep quality
  - Stress levels
  - Social interactions
  - Energy levels
  - Appetite and physical health
- **Risk Level Classification**: Results categorized as Low, Moderate, or High risk
- **Personalized Recommendations**: Tailored advice based on assessment results

### User Authentication
- **Sign Up & Login**: Secure user registration and authentication
- **Profile Management**: Update personal information and preferences
- **Password Reset**: Secure password recovery system

### Dashboard for Logged-in Users
- **Assessment History**: View past assessments and results
- **Progress Tracking**: Visual charts showing score changes over time
- **Bookmarks**: Save favorite resources for quick access
- **Personalized Recommendations**: Customized mental health resources

### Guidance System
- **Risk-based Content**: Different guidance based on assessment results
- **Self-care Tips**: Practical advice for mental health maintenance
- **Professional Help Guidelines**: When and how to seek professional support
- **Crisis Resources**: Emergency helplines and immediate support options

### Admin Interface
- **User Management**: View and manage user accounts
- **Assessment Data**: Monitor user responses and results
- **Content Management**: Manage questions, resources, and guidance content
- **Analytics**: Track platform usage and user engagement

### Security & Privacy
- **Secure Authentication**: Django's built-in user model with password hashing
- **Data Protection**: Secure data storage and transmission
- **Privacy Controls**: User consent management and data anonymization
- **HTTPS Ready**: Prepared for secure deployment

### Responsive Design
- **Mobile-First**: Optimized for all device sizes
- **Tailwind CSS**: Modern, clean UI with consistent styling
- **Accessibility**: WCAG compliant design patterns

## Technology Stack

- **Backend**: Django 4.2.7 with Django REST Framework
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Database**: SQLite (development), PostgreSQL (production)
- **Authentication**: Django's built-in user system
- **API**: RESTful API for future mobile app integration

## Project Structure

```
mindcheck/
├── manage.py
├── requirements.txt
├── README.md
├── mindcheck/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/
│   ├── models.py          # Custom User model
│   ├── views.py           # Authentication views
│   ├── forms.py           # Registration and login forms
│   └── urls.py
├── assessment/
│   ├── models.py          # Questionnaire, Question, Response models
│   ├── views.py           # Assessment views and API
│   ├── forms.py           # Assessment forms
│   ├── utils.py           # Scoring and utility functions
│   ├── urls.py
│   └── api_urls.py
├── resources/
│   ├── models.py          # Resource, Guidance, FAQ models
│   ├── views.py           # Resource views
│   └── urls.py
├── core/
│   ├── views.py           # Home, About, Dashboard views
│   └── urls.py
└── templates/
    ├── base.html          # Base template with navigation
    └── core/
        └── home.html      # Home page template
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mindcheck
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create a .env file in the project root
   echo "SECRET_KEY=your-secret-key-here" > .env
   echo "DEBUG=True" >> .env
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Load sample data (optional)**
   ```bash
   python manage.py loaddata sample_data.json
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000`
   - Admin interface: `http://127.0.0.1:8000/admin`

### Production Deployment

#### Using Render.com

1. **Prepare for deployment**
   ```bash
   # Install production dependencies
   pip install gunicorn whitenoise
   
   # Update settings for production
   # Set DEBUG=False, ALLOWED_HOSTS, etc.
   ```

2. **Create render.yaml**
   ```yaml
   services:
     - type: web
       name: mindcheck
       env: python
       buildCommand: pip install -r requirements.txt && python manage.py migrate
       startCommand: gunicorn mindcheck.wsgi:application
       envVars:
         - key: SECRET_KEY
           generateValue: true
         - key: DEBUG
           value: False
   ```

3. **Deploy to Render**
   - Connect your GitHub repository
   - Render will automatically build and deploy

#### Using Heroku

1. **Install Heroku CLI**
   ```bash
   # Follow instructions at https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

3. **Configure environment variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   ```

4. **Deploy**
   ```bash
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

## Usage

### For Users

1. **Take a Quick Assessment**
   - Visit the home page
   - Click "Take Quick Assessment"
   - Answer 5 simple questions
   - View your results and recommendations

2. **Create an Account**
   - Click "Sign Up" in the navigation
   - Fill in your information
   - Verify your email (if configured)

3. **Access Your Dashboard**
   - Log in to your account
   - View your assessment history
   - Track your progress over time
   - Bookmark helpful resources

### For Administrators

1. **Access Admin Interface**
   - Go to `/admin/`
   - Log in with superuser credentials

2. **Manage Content**
   - Add/edit questionnaires and questions
   - Manage resources and guidance content
   - View user data and analytics

3. **Monitor Usage**
   - Track assessment completions
   - Monitor user engagement
   - Review feedback and reports

## API Endpoints

The application includes REST API endpoints for future mobile app integration:

- `GET /api/assessments/` - List all available assessments
- `GET /api/results/<id>/` - Get assessment results
- `POST /api/assessments/<id>/submit/` - Submit assessment responses

## Security & Privacy Best Practices

### Data Protection
- All user data is encrypted in transit and at rest
- Personal information is anonymized in analytics
- Regular security audits and updates

### Privacy Controls
- Users can delete their accounts and data
- Clear consent management for data processing
- No sharing of personal data with third parties

### Security Measures
- CSRF protection on all forms
- XSS protection headers
- Secure session management
- Rate limiting on API endpoints

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Email: support@mindcheck.com
- Documentation: [Link to documentation]
- Issues: [GitHub Issues page]

## Disclaimer

This application is for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified health providers with questions about medical conditions.

## Crisis Support

If you're experiencing a mental health crisis:
- **988 Suicide & Crisis Lifeline**: 988
- **Crisis Text Line**: Text HOME to 741741
- **Emergency Services**: 911

---

**WellNest** - Your trusted companion for self-identifying mental health status and getting personalized guidance for support.
