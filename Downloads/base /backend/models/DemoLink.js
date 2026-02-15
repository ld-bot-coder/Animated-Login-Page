const mongoose = require('mongoose');

const demoLinkSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true
    },
    url: {
        type: String,
        required: true
    },
    description: {
        type: String,
        default: ''
    },
    category: {
        type: String,
        required: true
    },
    isVideo: {
        type: Boolean,
        default: false
    },
    isProgress: {
        type: Boolean,
        default: false
    },
    order: {
        type: Number,
        default: 0
    },
    createdAt: {
        type: Date,
        default: Date.now
    },
    updatedAt: {
        type: Date,
        default: Date.now
    }
});

// Update the updatedAt field before saving
demoLinkSchema.pre('save', function (next) {
    this.updatedAt = Date.now();
    next();
});

module.exports = mongoose.model('DemoLink', demoLinkSchema);
