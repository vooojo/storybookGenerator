# AI Storybook Generator

## Overview
A personalized storybook generation portal powered by Google's Gemini AI. Users can create custom 10-page illustrated storybooks by providing character information and optional photos. The app generates both story text and AI-generated images in various art styles.

## Features
- **Character Customization**: Enter character name, age, interests, and story theme
- **Photo Upload**: Upload 1-5 photos to help AI understand character appearance
- **Art Style Selection**: Choose from Anime, Watercolor, Digital Art, Cartoon, Realistic, or Classic Storybook styles
- **AI-Powered Generation**: 
  - Uses Gemini 2.5 Pro for story text generation
  - Uses Gemini 2.0 Flash for image generation
  - Creates 10-page storybooks with alternating images and text
- **Interactive Viewer**: Book-style interface with page-turning navigation

## Project Structure
```
├── app.py                  # Main Flask application
├── gemini_helper.py        # Gemini AI integration functions
├── templates/
│   ├── index.html         # Input form page
│   └── storybook.html     # Storybook viewer
├── static/
│   └── storybooks/        # Generated storybook storage
└── uploads/               # Temporary uploaded photos
```

## Technology Stack
- **Backend**: Flask (Python)
- **AI**: Google Gemini API (gemini-2.5-pro, gemini-2.0-flash-preview-image-generation)
- **Frontend**: HTML, CSS, JavaScript

## Configuration
- **API Key**: GEMINI_API_KEY (stored in Replit Secrets)
- **Port**: 5000
- **Max Upload Size**: 16MB

## How It Works
1. User fills out character information form and uploads photos
2. Form data sent to `/generate` endpoint
3. Gemini AI generates 10-page story structure (alternating image/text)
4. Each image page triggers Gemini image generation
5. Storybook saved with unique ID
6. User redirected to interactive viewer at `/storybook/<id>`
7. Viewer displays two pages at a time with navigation controls

## Recent Changes
- **Oct 12, 2025**: Initial implementation
  - Set up Gemini AI integration
  - Created Flask web application with file upload
  - Built user input form with photo upload
  - Implemented storybook generation logic
  - Created interactive book viewer with page navigation

## User Preferences
- None documented yet

## Known Issues
- None currently identified

## Future Enhancements (Suggested)
- Add validation to ensure exactly 10 pages are generated
- Implement storybook cleanup/pagination for storage management
- Add download/share functionality
- Support for multiple languages
