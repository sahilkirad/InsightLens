import React from 'react'
import { Eye, Brain, User, LogOut, Database } from 'lucide-react'

const Header = ({ user, onLogout, onShowDashboard, showDashboard }) => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo and Title */}
          <div className="flex items-center space-x-3">
            <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-700 rounded-lg">
              <Eye className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gradient">
                InsightLens
              </h1>
              <p className="text-sm text-gray-600">
                Text Extraction & AI Analysis
              </p>
            </div>
          </div>

          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-6">
            {user ? (
              <>
                <button
                  onClick={onShowDashboard}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-colors duration-200 ${
                    showDashboard 
                      ? 'bg-primary-100 text-primary-700' 
                      : 'text-gray-600 hover:text-primary-600 hover:bg-gray-50'
                  }`}
                >
                  <Database className="w-4 h-4" />
                  <span>My Data</span>
                </button>
                <a
                  href="#features"
                  className="text-gray-600 hover:text-primary-600 transition-colors duration-200"
                >
                  Features
                </a>
                <a
                  href="#about"
                  className="text-gray-600 hover:text-primary-600 transition-colors duration-200"
                >
                  About
                </a>
                <a
                  href="https://github.com/sahilkirad"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-600 hover:text-primary-600 transition-colors duration-200"
                >
                  GitHub
                </a>
              </>
            ) : (
              <>
                <a
                  href="#features"
                  className="text-gray-600 hover:text-primary-600 transition-colors duration-200"
                >
                  Features
                </a>
                <a
                  href="#about"
                  className="text-gray-600 hover:text-primary-600 transition-colors duration-200"
                >
                  About
                </a>
                <a
                  href="https://github.com/sahilkirad"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-600 hover:text-primary-600 transition-colors duration-200"
                >
                  GitHub
                </a>
              </>
            )}
          </nav>

          {/* User Menu / Mobile Menu Button */}
          {user ? (
            <div className="flex items-center space-x-4">
              <div className="hidden md:flex items-center space-x-2 text-sm text-gray-600">
                <User className="w-4 h-4" />
                <span>{user.full_name}</span>
              </div>
              <button
                onClick={onLogout}
                className="flex items-center space-x-2 px-3 py-2 text-sm text-red-600 hover:text-red-700 hover:bg-red-50 rounded-lg transition-colors"
              >
                <LogOut className="w-4 h-4" />
                <span className="hidden md:inline">Logout</span>
              </button>
            </div>
          ) : (
            <button className="md:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors duration-200">
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
            </button>
          )}
        </div>
      </div>
    </header>
  )
}

export default Header 