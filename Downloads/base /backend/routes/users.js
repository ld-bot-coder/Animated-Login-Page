const express = require('express');
const router = express.Router();
const bcrypt = require('bcryptjs');
const User = require('../models/User');
const auth = require('../middleware/auth');
const admin = require('../middleware/admin');

// @route   GET /api/users
// @desc    Get all users
// @access  Private (Admin only)
router.get('/', [auth, admin], async (req, res) => {
    try {
        const users = await User.find().select('-password');
        res.json(users);
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Server error' });
    }
});

// @route   POST /api/users
// @desc    Create new user
// @access  Private (Admin only)
router.post('/', [auth, admin], async (req, res) => {
    try {
        const { email, password, role } = req.body;

        // Validate input
        if (!email || !password) {
            return res.status(400).json({ error: 'Email and password required' });
        }

        // Check if user already exists
        const existingUser = await User.findOne({ email: email.toLowerCase() });
        if (existingUser) {
            return res.status(409).json({ error: 'User already exists' });
        }

        // Hash password
        const salt = await bcrypt.genSalt(10);
        const hashedPassword = await bcrypt.hash(password, salt);

        const newUser = new User({
            email: email.toLowerCase(),
            password: hashedPassword,
            role: role || 'user'
        });

        await newUser.save();

        res.json({
            id: newUser._id,
            email: newUser.email,
            role: newUser.role
        });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Server error' });
    }
});

// @route   PUT /api/users/:id
// @desc    Update user
// @access  Private (Admin only)
router.put('/:id', [auth, admin], async (req, res) => {
    try {
        const { email, password, role } = req.body;

        const updateData = {};
        if (email) updateData.email = email.toLowerCase();
        if (role) updateData.role = role;
        if (password) {
            const salt = await bcrypt.genSalt(10);
            updateData.password = await bcrypt.hash(password, salt);
        }

        const user = await User.findByIdAndUpdate(
            req.params.id,
            updateData,
            { new: true }
        ).select('-password');

        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }

        res.json(user);
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Server error' });
    }
});

// @route   DELETE /api/users/:id
// @desc    Delete user
// @access  Private (Admin only)
router.delete('/:id', [auth, admin], async (req, res) => {
    try {
        // Prevent deleting self
        if (req.params.id === req.user.userId) {
            return res.status(400).json({ error: 'Cannot delete your own account' });
        }

        const user = await User.findByIdAndDelete(req.params.id);

        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }

        res.json({ success: true, message: 'User deleted' });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Server error' });
    }
});

module.exports = router;
