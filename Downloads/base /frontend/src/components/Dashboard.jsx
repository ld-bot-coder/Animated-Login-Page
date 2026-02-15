import React, { useState, useEffect } from 'react';
import Navbar from './Navbar';
import apiService from '../services/api';

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('demo');
  const [showModal, setShowModal] = useState(false);
  const [modalMessage, setModalMessage] = useState('');
  const [demoLinks, setDemoLinks] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDemoLinks();
  }, []);

  const fetchDemoLinks = async () => {
    try {
      setLoading(true);
      const links = await apiService.getDemoLinks();

      // Group links by category
      const grouped = links.reduce((acc, link) => {
        if (!acc[link.category]) {
          acc[link.category] = [];
        }
        acc[link.category].push(link);
        return acc;
      }, {});

      setDemoLinks(grouped);
      setError('');
    } catch (err) {
      console.error('Error fetching demo links:', err);
      setError('Failed to load demo links');
      // Fallback to empty object
      setDemoLinks({});
    } finally {
      setLoading(false);
    }
  };

  const handleLinkClick = (url, isVideo, isProgress) => {
    if (isProgress) {
      setModalMessage('This feature is currently under development and will be available soon.');
      setShowModal(true);
      return;
    }
    if (isVideo) {
      window.open('https://drive.google.com/drive/folders/1Wd44KPsRyyK9Zo0p5M8swkYxdpYxd7dc', '_blank');
      return;
    }
    window.open(url, '_blank');
  };

  const handleScheduleSession = () => {
    setModalMessage('Live sessions scheduling feature coming soon! Please contact your administrator for more information.');
    setShowModal(true);
  };

  return (
    <div>
      <Navbar />

      <div className="min-h-screen flex flex-col bg-gray-100">
        <main className="flex-grow p-6 md:p-8">
          <div className="container mx-auto max-w-6xl">
            <h2 className="text-2xl md:text-3xl font-semibold mb-8 text-center" style={{ color: '#7C3783' }}>
              Welcome to Dashboard
            </h2>

            {/* Tab Navigation */}
            <div className="flex justify-center mb-8 gap-4">
              <button
                onClick={() => setActiveTab('demo')}
                className={`px-8 py-3 rounded-lg font-semibold transition duration-300 ${activeTab === 'demo'
                  ? 'text-white shadow-lg'
                  : 'bg-white text-gray-700 hover:bg-gray-50'
                  }`}
                style={activeTab === 'demo' ? { backgroundColor: '#7C3783' } : {}}
              >
                Demo Links
              </button>
              <button
                onClick={() => setActiveTab('sessions')}
                className={`px-8 py-3 rounded-lg font-semibold transition duration-300 ${activeTab === 'sessions'
                  ? 'text-white shadow-lg'
                  : 'bg-white text-gray-700 hover:bg-gray-50'
                  }`}
                style={activeTab === 'sessions' ? { backgroundColor: '#7C3783' } : {}}
              >
                Live Sessions
              </button>
            </div>

            {/* Demo Links Content */}
            {activeTab === 'demo' && (
              <div className="space-y-10">
                {Object.entries(demoLinks).map(([domain, links]) => (
                  <div key={domain}>
                    <h3 className="text-xl font-semibold mb-6" style={{ color: '#7C3783' }}>
                      {domain}
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                      {links.map((link, index) => (
                        <div
                          key={index}
                          onClick={() => handleLinkClick(link.url, link.isVideo, link.isProgress)}
                          className={`bg-white p-6 rounded-lg shadow-md hover:shadow-xl transition duration-300 flex flex-col min-h-[120px] ${link.isProgress ? 'opacity-60 cursor-not-allowed' : 'cursor-pointer'
                            }`}
                        >
                          <div className="flex items-start justify-between mb-3">
                            <h4 className="font-semibold text-gray-800 text-base flex-1 pr-2">{link.name}</h4>
                            {link.isVideo ? (
                              <svg className="w-6 h-6 flex-shrink-0" style={{ color: '#7C3783' }} fill="currentColor" viewBox="0 0 20 20">
                                <path d="M2 6a2 2 0 012-2h6a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V6zM14.553 7.106A1 1 0 0014 8v4a1 1 0 00.553.894l2 1A1 1 0 0018 13V7a1 1 0 00-1.447-.894l-2 1z" />
                              </svg>
                            ) : link.isProgress ? (
                              <svg className="w-6 h-6 flex-shrink-0 text-orange-500" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                              </svg>
                            ) : (
                              <svg className="w-6 h-6 flex-shrink-0" style={{ color: '#7C3783' }} fill="currentColor" viewBox="0 0 20 20">
                                <path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z" />
                                <path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z" />
                              </svg>
                            )}
                          </div>
                          <p className="text-gray-600 text-sm mt-auto">{link.description}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}

                {/* Solution Videos Link */}
                <div className="p-8 bg-white rounded-lg shadow-md">
                  <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
                    <div>
                      <h4 className="font-semibold text-gray-800 text-lg mb-2">Solution Videos</h4>
                      <p className="text-gray-600 text-sm">Access all solution demonstration videos</p>
                    </div>
                    <button
                      onClick={() => window.open('https://drive.google.com/drive/folders/1Wd44KPsRyyK9Zo0p5M8swkYxdpYxd7dc', '_blank')}
                      className="px-8 py-3 rounded-lg text-white font-semibold hover:opacity-90 transition duration-300 whitespace-nowrap"
                      style={{ backgroundColor: '#7C3783' }}
                    >
                      View Videos
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Live Sessions Content */}
            {activeTab === 'sessions' && (
              <div className="bg-white p-8 rounded-lg shadow-lg text-center">
                <svg
                  className="w-20 h-20 mx-auto mb-4"
                  style={{ color: '#7C3783' }}
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path d="M2 6a2 2 0 012-2h6a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V6zM14.553 7.106A1 1 0 0014 8v4a1 1 0 00.553.894l2 1A1 1 0 0018 13V7a1 1 0 00-1.447-.894l-2 1z" />
                </svg>
                <h3 className="text-xl font-semibold mb-4" style={{ color: '#7C3783' }}>Live Sessions</h3>
                <p className="text-gray-600 mb-6">Schedule and join live demonstration sessions with our team</p>
                <button
                  className="px-8 py-3 rounded-lg text-white font-semibold hover:opacity-90 transition duration-300"
                  style={{ backgroundColor: '#7C3783' }}
                  onClick={handleScheduleSession}
                >
                  Schedule a Session
                </button>
              </div>
            )}
          </div>
        </main>
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" onClick={() => setShowModal(false)}>
          <div className="bg-white rounded-lg p-8 max-w-md mx-4 shadow-2xl" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-center mb-4">
              <svg className="w-16 h-16" style={{ color: '#7C3783' }} fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-center mb-4" style={{ color: '#7C3783' }}>Information</h3>
            <p className="text-gray-700 text-center mb-6">{modalMessage}</p>
            <button
              onClick={() => setShowModal(false)}
              className="w-full px-6 py-3 rounded-lg text-white font-semibold hover:opacity-90 transition duration-300"
              style={{ backgroundColor: '#7C3783' }}
            >
              Got it
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
