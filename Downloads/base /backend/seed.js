const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
require('dotenv').config();

const User = require('./models/User');
const DemoLink = require('./models/DemoLink');

// Default users
const defaultUsers = [
    {
        email: 'sarabjeet@multipliersolutions.com',
        password: 'sarbjeet123',
        role: 'admin'
    },
    {
        email: 'rahul@gmail.com',
        password: 'rahul123',
        role: 'user'
    }
];

// Existing demo links data
const demoLinksData = [
    // R&D Category
    {
        name: 'Clinical Trial Suite',
        url: 'https://multiplierai.co/agent/Clinical_Trial_Suite/',
        description: 'Comprehensive clinical trial management',
        category: 'R&D',
        order: 1
    },
    {
        name: 'Regulatory Intelligence',
        url: 'https://multiplierai.co/agent/Regulatory-Intelligence-Platform-2/',
        description: 'Regulatory insights and intelligence',
        category: 'R&D',
        order: 2
    },
    {
        name: 'Medical Writing',
        url: 'video',
        description: 'Medical writing solutions (Video)',
        category: 'R&D',
        isVideo: true,
        order: 3
    },
    {
        name: 'Scientific Experts',
        url: 'https://multiplierai.co/se/',
        description: 'Investigator identification platform',
        category: 'R&D',
        order: 4
    },
    // Commercial Category
    {
        name: 'Data Cloud',
        url: 'https://multipliersolutions.in/data_product/#/scientific-profiles',
        description: 'Scientific profiles and data',
        category: 'Commercial',
        order: 1
    },
    {
        name: 'Competitive Insights',
        url: 'https://multiplierai.co/agent/competitive-insights/',
        description: 'Market competitive analysis',
        category: 'Commercial',
        order: 2
    },
    {
        name: 'Campaign Ops',
        url: 'https://multiplierai.co/agent/Campaign-Agent/',
        description: 'Campaign operations management',
        category: 'Commercial',
        order: 3
    },
    {
        name: 'Scientific Experts (with Veeva)',
        url: 'progress',
        description: 'Under Progress',
        category: 'Commercial',
        isProgress: true,
        order: 4
    },
    // Medical Affairs Category
    {
        name: 'Social Listening - SML Platform',
        url: 'https://multipliersolutions.in/agent/social-listening-platform3/',
        description: 'Social media listening platform',
        category: 'Medical Affairs',
        order: 1
    }
];

async function seedDatabase() {
    try {
        // Connect to MongoDB
        await mongoose.connect(process.env.MONGODB_URI, {
            useNewUrlParser: true,
            useUnifiedTopology: true
        });
        console.log('✅ MongoDB Connected');

        // Clear existing data
        console.log('🗑️  Clearing existing data...');
        await User.deleteMany({});
        await DemoLink.deleteMany({});

        // Seed users
        console.log('👥 Seeding users...');
        for (const userData of defaultUsers) {
            const salt = await bcrypt.genSalt(10);
            const hashedPassword = await bcrypt.hash(userData.password, salt);

            await User.create({
                email: userData.email,
                password: hashedPassword,
                role: userData.role
            });
            console.log(`   ✓ Created ${userData.role}: ${userData.email}`);
        }

        // Seed demo links
        console.log('🔗 Seeding demo links...');
        for (const linkData of demoLinksData) {
            await DemoLink.create(linkData);
            console.log(`   ✓ Created: ${linkData.name} (${linkData.category})`);
        }

        console.log('\n✅ Database seeded successfully!');
        console.log('\n📊 Summary:');
        console.log(`   Users: ${await User.countDocuments()}`);
        console.log(`   Demo Links: ${await DemoLink.countDocuments()}`);
        console.log('\n👤 Default Users:');
        console.log('   Admin: sarabjeet@multipliersolutions.com / sarbjeet123');
        console.log('   User: rahul@gmail.com / rahul123');

        process.exit(0);
    } catch (err) {
        console.error('❌ Error seeding database:', err);
        process.exit(1);
    }
}

seedDatabase();
