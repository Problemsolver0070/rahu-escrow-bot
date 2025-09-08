import React, { useState, useEffect } from 'react';
import './App.css';
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/card';
import { Button } from './components/ui/button';
import { Input } from './components/ui/input';
import { Badge } from './components/ui/badge';
import { Separator } from './components/ui/separator';
import { Switch } from './components/ui/switch';
import { Textarea } from './components/ui/textarea';
import { Alert, AlertDescription } from './components/ui/alert';
import { 
  Crown, 
  Shield, 
  Users, 
  MessageSquare, 
  Settings, 
  Key, 
  BarChart3, 
  Zap,
  Lock,
  Eye,
  EyeOff,
  Activity,
  Coins,
  AlertTriangle
} from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

// Login Component
const Login = ({ onLogin }) => {
  const [credentials, setCredentials] = useState({ username: '', password: '' });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    if (credentials.username === 'Rahul' && credentials.password === '123456') {
      onLogin(true);
      setError('');
      navigate('/'); // Navigate to dashboard after successful login
    } else {
      setError('Invalid credentials. Access denied.');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-amber-900 flex items-center justify-center p-6">
      <div className="w-full max-w-md">
        <Card className="bg-black/40 backdrop-blur-lg border border-amber-500/30 shadow-2xl">
          <CardHeader className="text-center space-y-4">
            <div className="mx-auto w-16 h-16 bg-gradient-to-r from-amber-400 to-yellow-600 rounded-full flex items-center justify-center">
              <Crown className="w-8 h-8 text-black" />
            </div>
            <div>
              <CardTitle className="text-2xl font-bold bg-gradient-to-r from-amber-400 to-yellow-600 bg-clip-text text-transparent">
                Rahu God Mode Console
              </CardTitle>
              <CardDescription className="text-amber-200/80 mt-2">
                ☢️ Omnipotent Access Portal
              </CardDescription>
            </div>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleLogin} className="space-y-6">
              <div className="space-y-4">
                <div>
                  <Input
                    type="text"
                    placeholder="Username"
                    value={credentials.username}
                    onChange={(e) => setCredentials({...credentials, username: e.target.value})}
                    className="bg-black/30 border-amber-500/30 text-white placeholder-amber-200/50 focus:border-amber-400"
                  />
                </div>
                <div className="relative">
                  <Input
                    type={showPassword ? "text" : "password"}
                    placeholder="Password"
                    value={credentials.password}
                    onChange={(e) => setCredentials({...credentials, password: e.target.value})}
                    className="bg-black/30 border-amber-500/30 text-white placeholder-amber-200/50 focus:border-amber-400 pr-10"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-amber-400 hover:text-amber-300"
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              {error && (
                <Alert className="bg-red-900/30 border-red-500/50">
                  <AlertTriangle className="h-4 w-4 text-red-400" />
                  <AlertDescription className="text-red-200">{error}</AlertDescription>
                </Alert>
              )}

              <Button 
                type="submit" 
                className="w-full bg-gradient-to-r from-amber-600 to-yellow-700 hover:from-amber-500 hover:to-yellow-600 text-black font-semibold h-12 text-lg shadow-lg hover:shadow-amber-500/25 transition-all duration-300"
              >
                <Crown className="w-5 h-5 mr-2" />
                Enter God Mode
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

// Dashboard Component
const Dashboard = () => {
  const [stats] = useState({
    users: 247,
    deals: 18,
    groups: 5,
    revenue: 12450
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-950 to-amber-950">
      {/* God Mode Header */}
      <div className="border-b border-amber-500/20 bg-black/20 backdrop-blur-sm">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gradient-to-r from-amber-400 to-yellow-600 rounded-lg flex items-center justify-center">
                <Crown className="w-6 h-6 text-black" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-amber-400 to-yellow-600 bg-clip-text text-transparent">
                  Rahu Escrow - God Mode
                </h1>
                <p className="text-amber-200/60 text-sm">Omnipotent Control Center</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Badge className="bg-purple-900/50 text-purple-200 border-purple-500/30 px-4 py-2 animate-pulse">
                👑 GOD MODE — AWAITING ACTIVATION (Phase 2)
              </Badge>
              <div className="text-right">
                <p className="text-amber-200 font-semibold">System State</p>
                <p className="text-amber-400 text-sm">Dormant</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-6 py-8 space-y-8">
        {/* Stats Dashboard */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card className="bg-black/30 backdrop-blur-sm border border-amber-500/20 hover:border-amber-400/40 transition-all duration-300">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-amber-200">Total Users</CardTitle>
                <Users className="w-5 h-5 text-amber-400" />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-white">{stats.users}</div>
              <p className="text-amber-200/60 text-sm mt-1">Active participants</p>
            </CardContent>
          </Card>

          <Card className="bg-black/30 backdrop-blur-sm border border-amber-500/20 hover:border-amber-400/40 transition-all duration-300">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-amber-200">Active Deals</CardTitle>
                <BarChart3 className="w-5 h-5 text-amber-400" />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-white">{stats.deals}</div>
              <p className="text-amber-200/60 text-sm mt-1">In escrow</p>
            </CardContent>
          </Card>

          <Card className="bg-black/30 backdrop-blur-sm border border-amber-500/20 hover:border-amber-400/40 transition-all duration-300">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-amber-200">Escrow Groups</CardTitle>
                <MessageSquare className="w-5 h-5 text-amber-400" />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-white">{stats.groups}</div>
              <p className="text-amber-200/60 text-sm mt-1">Available</p>
            </CardContent>
          </Card>

          <Card className="bg-black/30 backdrop-blur-sm border border-amber-500/20 hover:border-amber-400/40 transition-all duration-300">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-amber-200">Revenue</CardTitle>
                <Coins className="w-5 h-5 text-amber-400" />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-white">${stats.revenue}</div>
              <p className="text-amber-200/60 text-sm mt-1">Total earned</p>
            </CardContent>
          </Card>
        </div>

        {/* God Mode Features */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Permission Matrix */}
          <Card className="bg-black/30 backdrop-blur-sm border border-amber-500/20">
            <CardHeader>
              <CardTitle className="text-amber-200 flex items-center">
                <Shield className="w-5 h-5 mr-2 text-amber-400" />
                Permission Matrix
              </CardTitle>
              <CardDescription className="text-amber-200/60">Control moderator capabilities</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {['Can Ban Users', 'Can Freeze Deals', 'Can Broadcast', 'Can Edit Fees'].map((permission, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-black/20 rounded-lg border border-amber-500/10">
                    <span className="text-amber-200">{permission}</span>
                    <div className="relative group">
                      <Switch disabled className="opacity-50" />
                      <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-black/80 text-amber-200 text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                        Phase 2: Edit permissions
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Bot Message Editor */}
          <Card className="bg-black/30 backdrop-blur-sm border border-amber-500/20">
            <CardHeader>
              <CardTitle className="text-amber-200 flex items-center">
                <Settings className="w-5 h-5 mr-2 text-amber-400" />
                Bot Message Editor
              </CardTitle>
              <CardDescription className="text-amber-200/60">Customize bot responses</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-amber-200 text-sm mb-2 block">Welcome Message</label>
                <Textarea 
                  disabled 
                  placeholder="✨ Welcome to Rahu Escrow..."
                  className="bg-black/20 border-amber-500/20 text-amber-200/50 resize-none opacity-50"
                />
              </div>
              <div className="relative group">
                <Button disabled className="w-full bg-amber-600/30 hover:bg-amber-600/30 text-amber-200/50 cursor-not-allowed">
                  <Lock className="w-4 h-4 mr-2" />
                  Save Changes
                </Button>
                <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-black/80 text-amber-200 text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                  Phase 2: Edit bot messages
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Fee Editor */}
          <Card className="bg-black/30 backdrop-blur-sm border border-amber-500/20">
            <CardHeader>
              <CardTitle className="text-amber-200 flex items-center">
                <Coins className="w-5 h-5 mr-2 text-amber-400" />
                Fee Configuration
              </CardTitle>
              <CardDescription className="text-amber-200/60">Manage escrow fees</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-amber-200 text-sm mb-2 block">Small Deals (≤$100)</label>
                  <Input disabled placeholder="$5" className="bg-black/20 border-amber-500/20 text-amber-200/50 opacity-50" />
                </div>
                <div>
                  <label className="text-amber-200 text-sm mb-2 block">Large Deals (&gt;$100)</label>
                  <Input disabled placeholder="5%" className="bg-black/20 border-amber-500/20 text-amber-200/50 opacity-50" />
                </div>
              </div>
              <div className="relative group">
                <Button disabled className="w-full bg-amber-600/30 hover:bg-amber-600/30 text-amber-200/50 cursor-not-allowed">
                  <Lock className="w-4 h-4 mr-2" />
                  Update Fees
                </Button>
                <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-black/80 text-amber-200 text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                  Phase 2: Edit fees
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Group Manager */}
          <Card className="bg-black/30 backdrop-blur-sm border border-amber-500/20">
            <CardHeader>
              <CardTitle className="text-amber-200 flex items-center">
                <MessageSquare className="w-5 h-5 mr-2 text-amber-400" />
                Group Manager
              </CardTitle>
              <CardDescription className="text-amber-200/60">Control escrow groups</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {['ESCROW-ABC123', 'ESCROW-DEF456', 'ESCROW-GHI789'].map((group, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-black/20 rounded-lg border border-amber-500/10">
                    <div>
                      <span className="text-amber-200 font-medium">{group}</span>
                      <Badge className="ml-2 bg-green-900/30 text-green-300 border-green-500/30">Available</Badge>
                    </div>
                    <div className="flex space-x-2">
                      <Button disabled size="sm" variant="outline" className="border-amber-500/30 text-amber-200/50 hover:bg-amber-600/10 cursor-not-allowed opacity-50">
                        Reset
                      </Button>
                      <Button disabled size="sm" variant="outline" className="border-amber-500/30 text-amber-200/50 hover:bg-amber-600/10 cursor-not-allowed opacity-50">
                        Join
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Key Access */}
        <Card className="bg-black/30 backdrop-blur-sm border border-red-500/30">
          <CardHeader>
            <CardTitle className="text-red-300 flex items-center">
              <Key className="w-5 h-5 mr-2 text-red-400" />
              🔑 Private Key Access
            </CardTitle>
            <CardDescription className="text-red-200/60">Ultimate control over escrow wallets</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="relative group">
              <Button disabled className="w-full bg-red-900/30 hover:bg-red-900/30 text-red-200/50 cursor-not-allowed border border-red-500/30">
                <Lock className="w-4 h-4 mr-2" />
                🔑 View Private Keys
              </Button>
              <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-black/80 text-red-200 text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                Phase 3: Access escrow keys
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

// Main App Component
function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login onLogin={setIsAuthenticated} />} />
          <Route 
            path="/" 
            element={
              isAuthenticated ? (
                <Dashboard />
              ) : (
                <Navigate to="/login" replace />
              )
            } 
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;