# Quick Start Guide - Hospital Safety Checker

## ⚡ Fast Setup (5 Minutes)

### Step 1: Install MongoDB
Download: https://www.mongodb.com/try/download/community
Or use MongoDB Atlas (cloud): https://www.mongodb.com/cloud/atlas

### Step 2: Backend Setup
```powershell
cd "c:\safety checker\backend"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Frontend Setup
```powershell
cd "c:\safety checker\frontend"
npm install
```

### Step 4: Start Everything

**Terminal 1 - MongoDB** (if local):
```powershell
mongod
```

**Terminal 2 - Backend**:
```powershell
cd "c:\safety checker\backend"
venv\Scripts\activate
python main.py
```

**Terminal 3 - Frontend**:
```powershell
cd "c:\safety checker\frontend"
npm run dev
```

### Step 5: Open Browser
Navigate to: **http://localhost:3000**

---

## 🎯 First Time Usage

1. **Register a Doctor & Patient**
   - Go to "Registration" page
   - Fill in doctor details
   - Capture doctor's face (allow camera permission)
   - Fill in patient details
   - Capture patient's face
   - Click "Register Both"

2. **Verify Doctor**
   - Go to "Verification" page
   - Select the doctor you just registered
   - Capture face photo again
   - Click "Verify Doctor"
   - See assigned patients!

3. **Check Dashboard**
   - Go to "Dashboard" page
   - See the verification entry in waiting list
   - Click "Complete" to mark as done

4. **Try Chatbot**
   - Go to "Chatbot" page
   - Ask: "How many patients are there?"
   - Get instant response!

---

## 🔧 Common Issues

**Issue**: MongoDB connection error
**Fix**: Make sure MongoDB is running (`mongod` command)

**Issue**: Camera not working
**Fix**: Allow camera permissions in browser

**Issue**: Face not detected
**Fix**: Ensure good lighting and face camera directly

**Issue**: Port 8000 already in use
**Fix**: Change PORT in `backend/.env` file

---

## 📱 Test Data

For testing, you can register:
- **Doctor**: Dr. John Smith, Cardiologist
- **Patient**: Jane Doe

Then verify Dr. John Smith to see the patient in dashboard!

---

## 🚀 Next Steps

- Explore Admin Panel for data management
- Export data to Excel
- Add more patients to existing doctors
- Try different chatbot queries

---

**Need Help?** Check the full README.md for detailed documentation.
