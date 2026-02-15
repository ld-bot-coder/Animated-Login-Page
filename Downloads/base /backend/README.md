# Multiplier AI Demo Portal - Node.js Backend

Node.js/Express backend with MongoDB Atlas for the Multiplier AI Demo Portal.

## Features

- ✅ RESTful API with Express
- ✅ MongoDB Atlas integration
- ✅ JWT authentication
- ✅ Role-based access control (Admin/User)
- ✅ CRUD operations for demo links and users
- ✅ Ready for deployment on Render

## Quick Setup

### 1. Install Dependencies

```bash
cd backend
npm install
```

### 2. Configure Environment

Edit `.env` file and add your MongoDB Atlas URI:

```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/multiplier_demo?retryWrites=true&w=majority
JWT_SECRET=your-secret-key-here
PORT=8000
NODE_ENV=development
```

### 3. Seed Database

This will create default users and populate all existing demo links:

```bash
npm run seed
```

### 4. Start Server

**Development:**
```bash
npm run dev
```

**Production:**
```bash
npm start
```

Server will run on `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /api/auth` - Login

### Demo Links
- `GET /api/demo-links` - Get all links
- `POST /api/demo-links` - Create link (admin)
- `PUT /api/demo-links/:id` - Update link (admin)
- `DELETE /api/demo-links/:id` - Delete link (admin)

### Users
- `GET /api/users` - Get all users (admin)
- `POST /api/users` - Create user (admin)
- `PUT /api/users/:id` - Update user (admin)
- `DELETE /api/users/:id` - Delete user (admin)

### Health Check
- `GET /api/health` - Server status

## Default Users

- **Admin**: sarabjeet@multipliersolutions.com / sarbjeet123
- **User**: rahul@gmail.com / rahul123

## Deploy to Render

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect your repository
4. Set environment variables:
   - `MONGODB_URI`
   - `JWT_SECRET`
   - `NODE_ENV=production`
5. Build command: `npm install`
6. Start command: `npm start`
7. Run seed command once: `npm run seed`

## Project Structure

```
backend/
├── models/          # Mongoose models
│   ├── User.js
│   └── DemoLink.js
├── routes/          # API routes
│   ├── auth.js
│   ├── demoLinks.js
│   └── users.js
├── middleware/      # Custom middleware
│   ├── auth.js
│   └── admin.js
├── server.js        # Express app
├── seed.js          # Database seeder
├── .env             # Environment variables
└── package.json
```
