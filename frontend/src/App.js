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
  AlertTriangle,
  Download,
  FileText,
  Send,
  CheckCircle,
  XCircle,
  RefreshCw,
  Plus,
  Terminal,
  Edit3
} from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'https://escrow-control-hub.preview.emergentagent.com';

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
      navigate('/');
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
  const [stats, setStats] = useState({ users: 0, deals: 0, groups: 0, revenue: 0 });
  const [moderators, setModerators] = useState([]);
  const [botMessages, setBotMessages] = useState({
    welcome_message: '',
    rules_message: '',
    error_messages: {}
  });
  const [fees, setFees] = useState([]);
  const [groups, setGroups] = useState([]);
  const [loading, setLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [godModeActive, setGodModeActive] = useState(true);

  // Fetch real data from backend
  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Fetch real stats
      const statsRes = await axios.get(`${BACKEND_URL}/api/dashboard/stats`);
      setStats(statsRes.data);

      // Fetch moderators
      const moderatorsRes = await axios.get(`${BACKEND_URL}/api/moderators/permissions`);
      setModerators(moderatorsRes.data.moderators || []);

      // Fetch bot messages
      const messagesRes = await axios.get(`${BACKEND_URL}/api/bot/messages`);
      setBotMessages(messagesRes.data);

      // Fetch fees
      const feesRes = await axios.get(`${BACKEND_URL}/api/fees/config`);
      setFees(feesRes.data.networks || []);

      // Fetch groups
      const groupsRes = await axios.get(`${BACKEND_URL}/api/groups/manage`);
      setGroups(groupsRes.data.groups || []);

    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    }
  };

  const showSuccess = (message) => {
    setSuccessMessage(message);
    setTimeout(() => setSuccessMessage(''), 3000);
  };

  const updateModeratorPermission = async (userId, permission, value) => {
    try {
      const moderator = moderators.find(m => m.user_id === userId);
      const updatedModerator = { ...moderator, [permission]: value };
      
      await axios.post(`${BACKEND_URL}/api/moderators/permissions`, updatedModerator);
      
      setModerators(prev => prev.map(m => 
        m.user_id === userId ? updatedModerator : m
      ));
      
      showSuccess(`Permission ${permission} ${value ? 'granted to' : 'revoked from'} ${moderator.username}`);
    } catch (error) {
      console.error('Failed to update permission:', error);
    }
  };

  const updateBotMessages = async () => {
    try {
      setLoading(true);
      await axios.post(`${BACKEND_URL}/api/bot/messages`, botMessages);
      showSuccess('Bot messages updated successfully ✅');
    } catch (error) {
      console.error('Failed to update bot messages:', error);
    } finally {
      setLoading(false);
    }
  };

  const updateFeeConfig = async () => {
    try {
      setLoading(true);
      await axios.post(`${BACKEND_URL}/api/fees/config`, fees);
      showSuccess('Fee configuration updated successfully ✅');
    } catch (error) {
      console.error('Failed to update fees:', error);
    } finally {
      setLoading(false);
    }
  };

  const resetGroup = async (groupId) => {
    if (!window.confirm('Are you sure you want to reset this group? This action cannot be undone.')) {
      return;
    }

    try {
      await axios.post(`${BACKEND_URL}/api/groups/${groupId}/reset`);
      showSuccess('Group reset successfully ✅');
      fetchDashboardData(); // Refresh data
    } catch (error) {
      console.error('Failed to reset group:', error);
    }
  };

  const exportAllKeys = async () => {
    if (!window.confirm('⚠️ DANGER: This will export ALL private keys. Are you absolutely sure?')) {
      return;
    }
    
    try {
      const response = await axios.get(`${BACKEND_URL}/api/keys/export`, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `rahu_private_keys_${new Date().toISOString().slice(0,10)}.zip`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      
      showSuccess('🔑 Private keys exported (HANDLE WITH EXTREME CARE)');
    } catch (error) {
      console.error('Failed to export keys:', error);
    }
  };

  const exportAllData = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/api/export/data`, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `rahu_complete_export_${new Date().toISOString().slice(0,10)}.zip`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      
      showSuccess('📥 Complete data export downloaded successfully');
    } catch (error) {
      console.error('Failed to export data:', error);
    }
  };

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
              <Badge className={`px-4 py-2 ${godModeActive ? 'bg-green-900/50 text-green-200 border-green-500/30 animate-pulse' : 'bg-red-900/50 text-red-200 border-red-500/30'}`}>
                👑 GOD MODE — {godModeActive ? 'ACTIVE' : 'DORMANT'}
              </Badge>
              <div className="text-right">
                <p className="text-amber-200 font-semibold">System State</p>
                <p className="text-amber-400 text-sm">Operational</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Success Alert */}
      {successMessage && (
        <div className="container mx-auto px-6 pt-4">
          <Alert className="bg-green-900/30 border-green-500/50">
            <CheckCircle className="h-4 w-4 text-green-400" />
            <AlertDescription className="text-green-200">{successMessage}</AlertDescription>
          </Alert>
        </div>
      )}

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
          {/* Permission Matrix - Individual Moderator Control */}
          <Card className="bg-black/30 backdrop-blur-sm border border-amber-500/20">
            <CardHeader>
              <CardTitle className="text-amber-200 flex items-center">
                <Shield className="w-5 h-5 mr-2 text-amber-400" />
                Permission Matrix
                <Badge className="ml-2 bg-green-900/30 text-green-300 border-green-500/30">LIVE</Badge>
              </CardTitle>
              <CardDescription className="text-amber-200/60">Individual moderator permission control</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4 max-h-96 overflow-y-auto">
                {moderators.length === 0 ? (
                  <p className="text-amber-200/60 text-center py-4">No moderators found</p>
                ) : (
                  moderators.map((mod) => (
                    <div key={mod.user_id} className="p-4 bg-black/20 rounded-lg border border-amber-500/10 space-y-3">
                      <div className="flex items-center justify-between">
                        <div>
                          <h4 className="text-amber-200 font-semibold">{mod.username}</h4>
                          <p className="text-amber-200/60 text-sm">{mod.deals_handled} deals handled</p>
                        </div>
                        <Badge className="bg-blue-900/30 text-blue-300 border-blue-500/30">MOD</Badge>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-3">
                        <div className="flex items-center justify-between">
                          <span className="text-amber-200 text-sm">Can Ban</span>
                          <Switch 
                            checked={mod.can_ban}
                            onCheckedChange={(checked) => updateModeratorPermission(mod.user_id, 'can_ban', checked)}
                          />
                        </div>
                        <div className="flex items-center justify-between">
                          <span className="text-amber-200 text-sm">Can Freeze</span>
                          <Switch 
                            checked={mod.can_freeze}
                            onCheckedChange={(checked) => updateModeratorPermission(mod.user_id, 'can_freeze', checked)}
                          />
                        </div>
                        <div className="flex items-center justify-between">
                          <span className="text-amber-200 text-sm">Can Broadcast</span>
                          <Switch 
                            checked={mod.can_broadcast}
                            onCheckedChange={(checked) => updateModeratorPermission(mod.user_id, 'can_broadcast', checked)}
                          />
                        </div>
                        <div className="flex items-center justify-between">
                          <span className="text-amber-200 text-sm">Edit Fees</span>
                          <Switch 
                            checked={mod.can_edit_fees}
                            onCheckedChange={(checked) => updateModeratorPermission(mod.user_id, 'can_edit_fees', checked)}
                          />
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </CardContent>
          </Card>

          {/* Bot Message Editor */}
          <Card className="bg-black/30 backdrop-blur-sm border border-amber-500/20">
            <CardHeader>
              <CardTitle className="text-amber-200 flex items-center">
                <Settings className="w-5 h-5 mr-2 text-amber-400" />
                Bot Message Editor
                <Badge className="ml-2 bg-green-900/30 text-green-300 border-green-500/30">LIVE</Badge>
              </CardTitle>
              <CardDescription className="text-amber-200/60">Customize bot responses in real-time</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-amber-200 text-sm mb-2 block">Welcome Message</label>
                <Textarea 
                  value={botMessages.welcome_message}
                  onChange={(e) => setBotMessages(prev => ({...prev, welcome_message: e.target.value}))}
                  placeholder="Enter welcome message..."
                  className="bg-black/20 border-amber-500/20 text-amber-200 resize-none h-20"
                />
              </div>
              <div>
                <label className="text-amber-200 text-sm mb-2 block">Rules Message</label>
                <Textarea 
                  value={botMessages.rules_message}
                  onChange={(e) => setBotMessages(prev => ({...prev, rules_message: e.target.value}))}
                  placeholder="Enter rules message..."
                  className="bg-black/20 border-amber-500/20 text-amber-200 resize-none h-20"
                />
              </div>
              <Button 
                onClick={updateBotMessages}
                disabled={loading}
                className="w-full bg-gradient-to-r from-amber-600 to-yellow-700 hover:from-amber-500 hover:to-yellow-600 text-black font-semibold"
              >
                {loading ? <RefreshCw className="w-4 h-4 mr-2 animate-spin" /> : <Edit3 className="w-4 h-4 mr-2" />}
                Update Messages Live
              </Button>
            </CardContent>
          </Card>

          {/* Fee Editor */}
          <Card className="bg-black/30 backdrop-blur-sm border border-amber-500/20">
            <CardHeader>
              <CardTitle className="text-amber-200 flex items-center">
                <Coins className="w-5 h-5 mr-2 text-amber-400" />
                Fee Configuration
                <Badge className="ml-2 bg-green-900/30 text-green-300 border-green-500/30">LIVE</Badge>
              </CardTitle>
              <CardDescription className="text-amber-200/60">Manage network-specific fees</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-3 max-h-60 overflow-y-auto">
                {fees.map((fee, index) => (
                  <div key={index} className="p-3 bg-black/20 rounded-lg border border-amber-500/10">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-amber-200 font-medium">{fee.network}</span>
                    </div>
                    <div className="grid grid-cols-2 gap-2">
                      <div>
                        <label className="text-amber-200/80 text-xs">Fee %</label>
                        <Input
                          type="number"
                          value={fee.fee_percentage}
                          onChange={(e) => {
                            const newFees = [...fees];
                            newFees[index].fee_percentage = parseFloat(e.target.value);
                            setFees(newFees);
                          }}
                          className="bg-black/20 border-amber-500/20 text-amber-200 text-sm h-8"
                        />
                      </div>
                      <div>
                        <label className="text-amber-200/80 text-xs">Gas Fee</label>
                        <Input
                          type="number"
                          value={fee.gas_deduction || fee.gas_fee_usd || 0}
                          onChange={(e) => {
                            const newFees = [...fees];
                            if (fee.gas_deduction !== undefined) {
                              newFees[index].gas_deduction = parseFloat(e.target.value);
                            } else {
                              newFees[index].gas_fee_usd = parseFloat(e.target.value);
                            }
                            setFees(newFees);
                          }}
                          className="bg-black/20 border-amber-500/20 text-amber-200 text-sm h-8"
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              <Button 
                onClick={updateFeeConfig}
                disabled={loading}
                className="w-full bg-gradient-to-r from-amber-600 to-yellow-700 hover:from-amber-500 hover:to-yellow-600 text-black font-semibold"
              >
                {loading ? <RefreshCw className="w-4 h-4 mr-2 animate-spin" /> : <Coins className="w-4 h-4 mr-2" />}
                Update Fees Live
              </Button>
            </CardContent>
          </Card>

          {/* Group Manager */}
          <Card className="bg-black/30 backdrop-blur-sm border border-amber-500/20">
            <CardHeader>
              <CardTitle className="text-amber-200 flex items-center">
                <MessageSquare className="w-5 h-5 mr-2 text-amber-400" />
                Group Manager
                <Badge className="ml-2 bg-green-900/30 text-green-300 border-green-500/30">LIVE</Badge>
              </CardTitle>
              <CardDescription className="text-amber-200/60">Control all 50 escrow groups</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3 max-h-80 overflow-y-auto">
                {groups.slice(0, 10).map((group) => (
                  <div key={group.id} className="flex items-center justify-between p-3 bg-black/20 rounded-lg border border-amber-500/10">
                    <div>
                      <span className="text-amber-200 font-medium">Group {group.group_number}</span>
                      <Badge className={`ml-2 ${
                        group.status === 'Available' ? 'bg-green-900/30 text-green-300 border-green-500/30' :
                        group.status === 'Occupied' ? 'bg-yellow-900/30 text-yellow-300 border-yellow-500/30' :
                        'bg-red-900/30 text-red-300 border-red-500/30'
                      }`}>
                        {group.status}
                      </Badge>
                      {group.current_deal && (
                        <div className="text-amber-200/60 text-sm mt-1">{group.current_deal}</div>
                      )}
                    </div>
                    <div className="flex space-x-2">
                      <Button 
                        onClick={() => resetGroup(group.id)}
                        size="sm" 
                        variant="outline" 
                        className="border-amber-500/30 text-amber-200 hover:bg-amber-600/10"
                      >
                        <RefreshCw className="w-3 h-3 mr-1" />
                        Reset
                      </Button>
                    </div>
                  </div>
                ))}
                {groups.length > 10 && (
                  <p className="text-amber-200/60 text-center text-sm">... and {groups.length - 10} more groups</p>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Data Export & Key Access */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Data Export */}
          <Card className="bg-black/30 backdrop-blur-sm border border-amber-500/20">
            <CardHeader>
              <CardTitle className="text-amber-200 flex items-center">
                <Download className="w-5 h-5 mr-2 text-amber-400" />
                Data Export
                <Badge className="ml-2 bg-green-900/30 text-green-300 border-green-500/30">LIVE</Badge>
              </CardTitle>
              <CardDescription className="text-amber-200/60">Export complete system data</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-3">
                <div className="flex items-center justify-between p-3 bg-black/20 rounded-lg border border-amber-500/10">
                  <div>
                    <span className="text-amber-200 font-medium">Complete System Export</span>
                    <div className="text-amber-200/60 text-sm">Users, deals, groups, audit logs (CSV/JSON)</div>
                  </div>
                  <Button 
                    onClick={exportAllData}
                    size="sm" 
                    className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-500 hover:to-blue-600 text-white"
                  >
                    <Download className="w-4 h-4 mr-1" />
                    Export
                  </Button>
                </div>
                
                <div className="flex items-center justify-between p-3 bg-black/20 rounded-lg border border-amber-500/10">
                  <div>
                    <span className="text-amber-200 font-medium">Audit Logs Only</span>
                    <div className="text-amber-200/60 text-sm">Complete audit trail export</div>
                  </div>
                  <Button 
                    size="sm" 
                    variant="outline"
                    className="border-amber-500/30 text-amber-200 hover:bg-amber-600/10"
                  >
                    <FileText className="w-4 h-4 mr-1" />
                    Export
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Key Access - DANGER ZONE */}
          <Card className="bg-black/30 backdrop-blur-sm border border-red-500/30">
            <CardHeader>
              <CardTitle className="text-red-300 flex items-center">
                <Key className="w-5 h-5 mr-2 text-red-400" />
                🔑 Private Key Access
                <Badge className="ml-2 bg-red-900/30 text-red-300 border-red-500/30">DANGER</Badge>
              </CardTitle>
              <CardDescription className="text-red-200/60">Ultimate control over escrow wallets</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="bg-red-900/20 border border-red-500/30 rounded-lg p-4">
                <div className="flex items-center space-x-2 mb-3">
                  <AlertTriangle className="w-5 h-5 text-red-400" />
                  <span className="text-red-300 font-semibold">EXTREME CAUTION REQUIRED</span>
                </div>
                <p className="text-red-200/80 text-sm mb-4">
                  This will export ALL private keys for ALL escrow wallets. 
                  Handle with absolute security. All access is logged.
                </p>
                <Button 
                  onClick={exportAllKeys}
                  className="w-full bg-gradient-to-r from-red-600 to-red-700 hover:from-red-500 hover:to-red-600 text-white border border-red-500/50"
                >
                  <Key className="w-4 h-4 mr-2" />
                  🔑 Export All Private Keys
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Manual Payout - DANGER ZONE */}
        <Card className="bg-black/30 backdrop-blur-sm border border-red-500/30">
          <CardHeader>
            <CardTitle className="text-red-300 flex items-center">
              <Send className="w-5 h-5 mr-2 text-red-400" />
              💸 Manual Payout Override
              <Badge className="ml-2 bg-red-900/30 text-red-300 border-red-500/30">DANGER</Badge>
            </CardTitle>
            <CardDescription className="text-red-200/60">Send funds to any address (bypasses normal escrow flow)</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="bg-red-900/20 border border-red-500/30 rounded-lg p-4">
              <div className="flex items-center space-x-2 mb-3">
                <AlertTriangle className="w-5 h-5 text-red-400" />
                <span className="text-red-300 font-semibold">DESTRUCTIVE ACTION</span>
              </div>
              <p className="text-red-200/80 text-sm mb-4">
                This feature allows bypassing the normal escrow flow and sending funds directly to any address. 
                Use only in extreme circumstances. All manual payouts are permanently logged.
              </p>
              <div className="grid grid-cols-2 gap-4 mb-4">
                <Input placeholder="Deal ID" className="bg-black/20 border-red-500/20 text-red-200" />
                <Input placeholder="Recipient Address" className="bg-black/20 border-red-500/20 text-red-200" />
                <Input placeholder="Amount" type="number" className="bg-black/20 border-red-500/20 text-red-200" />
                <Input placeholder="Reason" className="bg-black/20 border-red-500/20 text-red-200" />
              </div>
              <Button className="w-full bg-gradient-to-r from-red-600 to-red-700 hover:from-red-500 hover:to-red-600 text-white border border-red-500/50">
                <Send className="w-4 h-4 mr-2" />
                💸 Execute Manual Payout
              </Button>
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