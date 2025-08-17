import React, { useState, useEffect } from 'react';
import { 
  FileText, 
  Calendar, 
  Clock, 
  Trash2, 
  Eye, 
  Copy, 
  BarChart3, 
  User,
  LogOut,
  RefreshCw,
  Loader2,
  ArrowLeft
} from 'lucide-react';

const UserDashboard = ({ user, onLogout, token, onBackToApp }) => {
  const [extractions, setExtractions] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedExtraction, setSelectedExtraction] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [deletingId, setDeletingId] = useState(null);
  const [backendAvailable, setBackendAvailable] = useState(true);

  useEffect(() => {
    console.log('🔍 UserDashboard mounted with user:', user);
    console.log('🔍 User ID:', user?.id);
    console.log('🔍 User email:', user?.email);
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      setLoading(true);
      console.log('🔍 Fetching user data for user:', user);
      console.log('🔍 User ID:', user.id);
      console.log('🔍 User email:', user.email);
      console.log('🔍 API URL:', import.meta.env.VITE_API_URL);
      
      // Check if API URL is configured
      if (!import.meta.env.VITE_API_URL) {
        console.error('❌ VITE_API_URL is not configured');
        setExtractions([]);
        setStats(null);
        return;
      }

      // Test API connectivity first
      try {
        const healthCheck = await fetch(`${import.meta.env.VITE_API_URL}/health`);
        if (!healthCheck.ok) {
          console.error('❌ Backend server is not responding');
          setBackendAvailable(false);
          setExtractions([]);
          setStats(null);
          return;
        }
        setBackendAvailable(true);
      } catch (error) {
        console.error('❌ Cannot connect to backend server:', error.message);
        setBackendAvailable(false);
        setExtractions([]);
        setStats(null);
        return;
      }

      // Fetch extractions
      let extractionsData = [];
      try {
        const extractionsRes = await fetch(`${import.meta.env.VITE_API_URL}/api/user/extractions`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        console.log('📊 Extractions response status:', extractionsRes.status);

        if (extractionsRes.ok) {
          const contentType = extractionsRes.headers.get('content-type');
          if (contentType && contentType.includes('application/json')) {
            extractionsData = await extractionsRes.json();
            console.log('📄 Extractions data:', extractionsData);
            console.log('📄 Number of extractions:', extractionsData.length);
          } else {
            console.error('❌ Extractions response is not JSON');
            extractionsData = [];
          }
        } else {
          console.error('❌ Failed to fetch extractions:', extractionsRes.status, extractionsRes.statusText);
          extractionsData = [];
        }
      } catch (error) {
        console.error('❌ Error fetching extractions:', error.message);
        extractionsData = [];
      }

      // Fetch stats
      let statsData = null;
      try {
        const statsRes = await fetch(`${import.meta.env.VITE_API_URL}/api/user/stats`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        console.log('📊 Stats response status:', statsRes.status);

        if (statsRes.ok) {
          const contentType = statsRes.headers.get('content-type');
          if (contentType && contentType.includes('application/json')) {
            statsData = await statsRes.json();
            console.log('📈 Stats data:', statsData);
          } else {
            console.error('❌ Stats response is not JSON');
            statsData = null;
          }
        } else {
          console.error('❌ Failed to fetch stats:', statsRes.status, statsRes.statusText);
          statsData = null;
        }
      } catch (error) {
        console.error('❌ Error fetching stats:', error.message);
        statsData = null;
      }

      // Update state
      setExtractions(extractionsData);
      setStats(statsData);

    } catch (error) {
      console.error('❌ Error in fetchUserData:', error.message);
      setExtractions([]);
      setStats(null);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (documentId) => {
    if (!confirm('Are you sure you want to delete this extraction?')) {
      return;
    }

    try {
      setDeletingId(documentId);
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/user/extractions/${documentId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        setExtractions(prev => prev.filter(ext => ext.id !== documentId));
        fetchUserData(); // Refresh stats
      } else {
        alert('Failed to delete extraction');
      }
    } catch (error) {
      console.error('Error deleting extraction:', error);
      alert('Error deleting extraction');
    } finally {
      setDeletingId(null);
    }
  };

  const handleViewExtraction = (extraction) => {
    setSelectedExtraction(extraction);
    setShowModal(true);
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    // You could add a toast notification here
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const truncateText = (text, maxLength = 100) => {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin mx-auto text-blue-600" />
          <p className="mt-2 text-gray-600">Loading your data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <div className="h-10 w-10 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
                <User className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-semibold text-gray-900">Welcome, {user.full_name}</h1>
                <p className="text-sm text-gray-500">{user.email}</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={onBackToApp}
                className="flex items-center space-x-2 px-3 py-2 text-sm text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded-lg transition-colors"
              >
                <ArrowLeft className="h-4 w-4" />
                <span>Back to App</span>
              </button>
              <button
                onClick={fetchUserData}
                className="flex items-center space-x-2 px-3 py-2 text-sm text-gray-600 hover:text-gray-900 transition-colors"
              >
                <RefreshCw className="h-4 w-4" />
                <span>Refresh</span>
              </button>
              <button
                onClick={onLogout}
                className="flex items-center space-x-2 px-4 py-2 text-sm text-red-600 hover:text-red-700 hover:bg-red-50 rounded-lg transition-colors"
              >
                <LogOut className="h-4 w-4" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Cards */}
        {backendAvailable && stats && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-white rounded-lg shadow-sm border p-6">
              <div className="flex items-center">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <FileText className="h-6 w-6 text-blue-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Total Extractions</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.total_extractions}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-sm border p-6">
              <div className="flex items-center">
                <div className="p-2 bg-green-100 rounded-lg">
                  <BarChart3 className="h-6 w-6 text-green-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Total Analyses</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.total_analyses}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-sm border p-6">
              <div className="flex items-center">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <Clock className="h-6 w-6 text-purple-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Recent Activity</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.recent_extractions}</p>
                  <p className="text-xs text-gray-500">Last 7 days</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Extractions List */}
        <div className="bg-white rounded-lg shadow-sm border">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Your Extractions</h2>
            <p className="text-sm text-gray-500">Manage and view your past text extractions</p>
          </div>

          {!backendAvailable && (
            <div className="p-6 bg-yellow-50 border-l-4 border-yellow-400">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <p className="text-sm text-yellow-700">
                    <strong>Backend server is not available.</strong> Please make sure the backend server is running on port 8000.
                  </p>
                  <button
                    onClick={fetchUserData}
                    className="mt-2 text-sm text-yellow-700 underline hover:text-yellow-600"
                  >
                    Try again
                  </button>
                </div>
              </div>
            </div>
          )}

          {backendAvailable && extractions.length === 0 && (
            <div className="p-8 text-center">
              <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No extractions yet</h3>
              <p className="text-gray-500">Start by uploading an image to extract text</p>
            </div>
          )}

          {backendAvailable && extractions.length > 0 && (
            <div className="divide-y divide-gray-200">
              {extractions.map((extraction) => (
                <div key={extraction.id} className="p-6 hover:bg-gray-50 transition-colors">
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center space-x-3 mb-2">
                        <FileText className="h-5 w-5 text-gray-400" />
                        <span className="text-sm text-gray-500">
                          {formatDate(extraction.created_at)}
                        </span>
                      </div>
                      <p className="text-sm text-gray-900 mb-2">
                        {truncateText(extraction.extracted_text, 200)}
                      </p>
                      <div className="flex items-center space-x-4 text-xs text-gray-500">
                        <span>{extraction.analyses?.length || 0} analyses</span>
                        <span>•</span>
                        <span>{extraction.extracted_text.length} characters</span>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2 ml-4">
                      <button
                        onClick={() => handleViewExtraction(extraction)}
                        className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                        title="View details"
                      >
                        <Eye className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => copyToClipboard(extraction.extracted_text)}
                        className="p-2 text-gray-400 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                        title="Copy text"
                      >
                        <Copy className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => handleDelete(extraction.id)}
                        disabled={deletingId === extraction.id}
                        className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors disabled:opacity-50"
                        title="Delete extraction"
                      >
                        {deletingId === extraction.id ? (
                          <Loader2 className="h-4 w-4 animate-spin" />
                        ) : (
                          <Trash2 className="h-4 w-4" />
                        )}
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Modal for viewing extraction details */}
      {showModal && selectedExtraction && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
              <h3 className="text-lg font-semibold text-gray-900">Extraction Details</h3>
              <button
                onClick={() => setShowModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                ×
              </button>
            </div>
            <div className="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
              <div className="mb-4">
                <p className="text-sm text-gray-500 mb-2">Created: {formatDate(selectedExtraction.created_at)}</p>
                <div className="bg-gray-50 rounded-lg p-4">
                  <h4 className="font-medium text-gray-900 mb-2">Extracted Text:</h4>
                  <p className="text-gray-700 whitespace-pre-wrap">{selectedExtraction.extracted_text}</p>
                </div>
              </div>

              {selectedExtraction.analyses && selectedExtraction.analyses.length > 0 && (
                <div>
                  <h4 className="font-medium text-gray-900 mb-3">Analyses:</h4>
                  <div className="space-y-3">
                    {selectedExtraction.analyses.map((analysis, index) => (
                      <div key={index} className="border border-gray-200 rounded-lg p-4">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-sm font-medium text-gray-900 capitalize">
                            {analysis.type} Analysis
                          </span>
                          <span className="text-xs text-gray-500">
                            {formatDate(analysis.timestamp)}
                          </span>
                        </div>
                        {analysis.prompt && (
                          <p className="text-sm text-gray-600 mb-2">
                            <strong>Prompt:</strong> {analysis.prompt}
                          </p>
                        )}
                        <div className="bg-gray-50 rounded p-3">
                          <pre className="text-sm text-gray-700 whitespace-pre-wrap">
                            {JSON.stringify(analysis.result, null, 2)}
                          </pre>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default UserDashboard;
