const express = require('express');
const router = express.Router();
const DemoLink = require('../models/DemoLink');
const auth = require('../middleware/auth');
const admin = require('../middleware/admin');

// @route   GET /api/demo-links
// @desc    Get all demo links
// @access  Public
router.get('/', async (req, res) => {
    try {
        const links = await DemoLink.find().sort({ order: 1 });
        res.json(links);
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Server error' });
    }
});

// @route   POST /api/demo-links
// @desc    Create new demo link
// @access  Private (Admin only)
router.post('/', [auth, admin], async (req, res) => {
    try {
        const { name, url, description, category, isVideo, isProgress, order } = req.body;

        // Validate input
        if (!name || !url || !category) {
            return res.status(400).json({ error: 'Name, URL, and category required' });
        }

        const newLink = new DemoLink({
            name,
            url,
            description: description || '',
            category,
            isVideo: isVideo || false,
            isProgress: isProgress || false,
            order: order || 0
        });

        await newLink.save();
        res.json(newLink);
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Server error' });
    }
});

// @route   PUT /api/demo-links/:id
// @desc    Update demo link
// @access  Private (Admin only)
router.put('/:id', [auth, admin], async (req, res) => {
    try {
        const { name, url, description, category, isVideo, isProgress, order } = req.body;

        const updateData = { updatedAt: Date.now() };
        if (name) updateData.name = name;
        if (url) updateData.url = url;
        if (description !== undefined) updateData.description = description;
        if (category) updateData.category = category;
        if (isVideo !== undefined) updateData.isVideo = isVideo;
        if (isProgress !== undefined) updateData.isProgress = isProgress;
        if (order !== undefined) updateData.order = order;

        const link = await DemoLink.findByIdAndUpdate(
            req.params.id,
            updateData,
            { new: true }
        );

        if (!link) {
            return res.status(404).json({ error: 'Demo link not found' });
        }

        res.json(link);
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Server error' });
    }
});

// @route   DELETE /api/demo-links/:id
// @desc    Delete demo link
// @access  Private (Admin only)
router.delete('/:id', [auth, admin], async (req, res) => {
    try {
        const link = await DemoLink.findByIdAndDelete(req.params.id);

        if (!link) {
            return res.status(404).json({ error: 'Demo link not found' });
        }

        res.json({ success: true, message: 'Demo link deleted' });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Server error' });
    }
});

module.exports = router;
