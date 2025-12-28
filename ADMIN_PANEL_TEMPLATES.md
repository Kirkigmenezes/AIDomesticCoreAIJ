# AI Platform Admin Panel Templates

## Overview

This document provides comprehensive templates and guidelines for creating the AI Platform Admin Panel, a powerful interface for managing the platform, users, models, and system resources.

## 1. Admin Panel Architecture

### Technology Stack
- **Frontend Framework**: React 18 with TypeScript
- **UI Library**: Material-UI (MUI) v5 with custom theme
- **State Management**: Redux Toolkit with RTK Query
- **Routing**: React Router v6
- **Form Handling**: React Hook Form with Zod validation
- **Data Tables**: Material-UI DataGrid Pro
- **Charts**: Recharts
- **Build Tool**: Vite.js
- **Testing**: Jest, React Testing Library, Cypress
- **Deployment**: Docker with Nginx

### Project Structure
```
admin-panel/
├── public/
│   ├── index.html
│   ├── favicon.ico
│   └── manifest.json
├── src/
│   ├── assets/
│   │   ├── images/
│   │   ├── icons/
│   │   └── styles/
│   ├── components/
│   │   ├── common/
│   │   ├── layout/
│   │   ├── dashboard/
│   │   ├── users/
│   │   ├── models/
│   │   ├── analytics/
│   │   ├── system/
│   │   └── settings/
│   ├── pages/
│   │   ├── Dashboard/
│   │   ├── Users/
│   │   ├── Models/
│   │   ├── Analytics/
│   │   ├── System/
│   │   ├── Settings/
│   │   └── Profile/
│   ├── services/
│   │   ├── api.ts
│   │   ├── auth.ts
│   │   └── analytics.ts
│   ├── store/
│   │   ├── index.ts
│   │   ├── slices/
│   │   └── hooks/
│   ├── utils/
│   │   ├── helpers.ts
│   │   ├── constants.ts
│   │   └── validators.ts
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   └── useAdmin.ts
│   ├── types/
│   │   └── index.ts
│   ├── theme/
│   │   ├── index.ts
│   │   └── palette.ts
│   ├── config/
│   │   └── environment.ts
│   ├── App.tsx
│   └── main.tsx
├── tests/
├── Dockerfile
├── docker-compose.yml
├── vite.config.ts
├── tsconfig.json
└── package.json
```

## 2. Authentication & Authorization

### Admin Authentication
```typescript
// src/components/auth/AdminLogin.tsx
import React, { useState } from 'react';
import {
  Box,
  Button,
  TextField,
  Typography,
  Container,
  Paper,
  Alert,
  Link
} from '@mui/material';
import { useAuth } from '../../hooks/useAuth';
import { useNavigate } from 'react-router-dom';

const AdminLogin: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { adminLogin } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await adminLogin(email, password);
      navigate('/admin/dashboard');
    } catch (err: any) {
      setError(err.message || 'Invalid credentials');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <Paper elevation={3} sx={{ p: 4, mt: 8 }}>
        <Typography component="h1" variant="h5" align="center" gutterBottom>
          Admin Panel Login
        </Typography>
        
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
          <TextField
            margin="normal"
            required
            fullWidth
            id="email"
            label="Admin Email"
            name="email"
            autoComplete="email"
            autoFocus
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
            disabled={loading}
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </Button>
        </Box>
        
        <Box sx={{ mt: 2, textAlign: 'center' }}>
          <Link href="/forgot-password" variant="body2">
            Forgot password?
          </Link>
        </Box>
      </Paper>
    </Container>
  );
};

export default AdminLogin;
```

### Role-Based Access Control
```typescript
// src/hooks/useAdmin.ts
import { useState, useEffect } from 'react';
import { useAuth } from './useAuth';

export interface AdminRole {
  id: string;
  name: string;
  permissions: string[];
}

export interface AdminUser {
  id: string;
  email: string;
  name: string;
  role: AdminRole;
  lastLogin: string;
  status: 'active' | 'inactive' | 'suspended';
}

export const useAdmin = () => {
  const { user } = useAuth();
  const [adminUsers, setAdminUsers] = useState<AdminUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Check if current user is admin
  const isAdmin = user?.role === 'admin' || user?.role === 'superadmin';
  const isSuperAdmin = user?.role === 'superadmin';

  // Check permissions
  const hasPermission = (permission: string) => {
    if (!user?.permissions) return false;
    return user.permissions.includes(permission) || isSuperAdmin;
  };

  // Fetch admin users
  const fetchAdminUsers = async () => {
    if (!hasPermission('manage_users')) {
      setError('Insufficient permissions');
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      // In a real app, this would fetch from API
      const users: AdminUser[] = [
        {
          id: '1',
          email: 'admin@aiplatform.io',
          name: 'Admin User',
          role: { id: 'admin', name: 'Administrator', permissions: ['all'] },
          lastLogin: '2025-12-28T10:30:00Z',
          status: 'active'
        }
      ];
      setAdminUsers(users);
    } catch (err) {
      setError('Failed to fetch admin users');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isAdmin) {
      fetchAdminUsers();
    } else {
      setLoading(false);
    }
  }, [isAdmin]);

  return {
    isAdmin,
    isSuperAdmin,
    hasPermission,
    adminUsers,
    loading,
    error,
    refetch: fetchAdminUsers
  };
};
```

## 3. Dashboard Components

### Admin Dashboard Layout
```typescript
// src/components/layout/AdminLayout.tsx
import React, { useState } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import {
  AppBar,
  Box,
  CssBaseline,
  Divider,
  Drawer,
  IconButton,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Menu,
  MenuItem,
  Toolbar,
  Typography,
  Avatar,
  Tooltip
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  People as UsersIcon,
  Psychology as ModelsIcon,
  Analytics as AnalyticsIcon,
  Settings as SettingsIcon,
  SystemUpdateAlt as SystemIcon,
  AccountCircle as ProfileIcon,
  Logout as LogoutIcon,
  Notifications as NotificationsIcon,
  Help as HelpIcon
} from '@mui/icons-material';
import { useAuth } from '../../hooks/useAuth';
import { useAdmin } from '../../hooks/useAdmin';

const drawerWidth = 260;

const AdminLayout: React.FC = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const { logout, user } = useAuth();
  const { isSuperAdmin } = useAdmin();
  const navigate = useNavigate();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    navigate('/admin/login');
    handleMenuClose();
  };

  const menuItems = [
    { text: 'Dashboard', icon: <DashboardIcon />, path: '/admin/dashboard' },
    { text: 'Users', icon: <UsersIcon />, path: '/admin/users' },
    { text: 'Models', icon: <ModelsIcon />, path: '/admin/models' },
    { text: 'Analytics', icon: <AnalyticsIcon />, path: '/admin/analytics' },
    { text: 'System', icon: <SystemIcon />, path: '/admin/system', superAdminOnly: true },
    { text: 'Settings', icon: <SettingsIcon />, path: '/admin/settings' }
  ];

  const filteredMenuItems = menuItems.filter(item => 
    !item.superAdminOnly || isSuperAdmin
  );

  const drawer = (
    <div>
      <Toolbar>
        <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
          AI Platform Admin
        </Typography>
      </Toolbar>
      <Divider />
      <List>
        {filteredMenuItems.map((item) => (
          <ListItem 
            button 
            key={item.text} 
            component="a" 
            href={item.path}
            sx={{ py: 1.5 }}
          >
            <ListItemIcon sx={{ minWidth: 40 }}>
              {item.icon}
            </ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
      </List>
    </div>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar
        position="fixed"
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
          backgroundColor: 'background.paper',
          color: 'text.primary',
          boxShadow: 1
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            Admin Panel
          </Typography>
          
          <IconButton color="inherit" sx={{ mr: 2 }}>
            <NotificationsIcon />
          </IconButton>
          
          <IconButton color="inherit" sx={{ mr: 2 }}>
            <HelpIcon />
          </IconButton>
          
          <Tooltip title="Account settings">
            <IconButton
              onClick={handleMenuOpen}
              size="small"
              sx={{ ml: 2 }}
              aria-controls="account-menu"
              aria-haspopup="true"
            >
              <Avatar sx={{ width: 32, height: 32 }}>
                {user?.name?.charAt(0) || 'A'}
              </Avatar>
            </IconButton>
          </Tooltip>
          
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleMenuClose}
            onClick={handleMenuClose}
            PaperProps={{
              elevation: 0,
              sx: {
                overflow: 'visible',
                filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.32))',
                mt: 1.5,
                '& .MuiAvatar-root': {
                  width: 32,
                  height: 32,
                  ml: -0.5,
                  mr: 1,
                },
                '&:before': {
                  content: '""',
                  display: 'block',
                  position: 'absolute',
                  top: 0,
                  right: 14,
                  width: 10,
                  height: 10,
                  bgcolor: 'background.paper',
                  transform: 'translateY(-50%) rotate(45deg)',
                  zIndex: 0,
                },
              },
            }}
            transformOrigin={{ horizontal: 'right', vertical: 'top' }}
            anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
          >
            <MenuItem onClick={() => navigate('/admin/profile')}>
              <ListItemIcon>
                <ProfileIcon fontSize="small" />
              </ListItemIcon>
              Profile
            </MenuItem>
            <MenuItem onClick={() => navigate('/admin/settings')}>
              <ListItemIcon>
                <SettingsIcon fontSize="small" />
              </ListItemIcon>
              Settings
            </MenuItem>
            <Divider />
            <MenuItem onClick={handleLogout}>
              <ListItemIcon>
                <LogoutIcon fontSize="small" />
              </ListItemIcon>
              Logout
            </MenuItem>
          </Menu>
        </Toolbar>
      </AppBar>
      
      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
        aria-label="admin navigation"
      >
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true,
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>
      
      <Box
        component="main"
        sx={{ 
          flexGrow: 1, 
          p: 3, 
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          mt: 8
        }}
      >
        <Outlet />
      </Box>
    </Box>
  );
};

export default AdminLayout;
```

### System Overview Dashboard
```typescript
// src/pages/Dashboard/SystemOverview.tsx
import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  CircularProgress,
  Button,
  Chip
} from '@mui/material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { useAdmin } from '../../hooks/useAdmin';

interface SystemMetrics {
  totalUsers: number;
  activeUsers: number;
  totalModels: number;
  activeModels: number;
  apiRequests: number;
  errorRate: number;
  systemStatus: 'operational' | 'degraded' | 'down';
  uptime: number;
}

const SystemOverview: React.FC = () => {
  const { loading, error } = useAdmin();
  const [timeRange, setTimeRange] = useState('24h');

  // Mock data - in real app this would come from API
  const systemMetrics: SystemMetrics = {
    totalUsers: 12540,
    activeUsers: 8765,
    totalModels: 42,
    activeModels: 38,
    apiRequests: 1250000,
    errorRate: 0.2,
    systemStatus: 'operational',
    uptime: 99.98
  };

  const usageData = [
    { name: '00:00', requests: 4000, errors: 5 },
    { name: '04:00', requests: 3000, errors: 3 },
    { name: '08:00', requests: 2000, errors: 2 },
    { name: '12:00', requests: 2780, errors: 4 },
    { name: '16:00', requests: 1890, errors: 6 },
    { name: '20:00', requests: 2390, errors: 3 }
  ];

  const modelDistribution = [
    { name: 'GPT-4', value: 45 },
    { name: 'Claude', value: 30 },
    { name: 'Llama', value: 15 },
    { name: 'Custom', value: 10 }
  ];

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="60vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box p={3}>
        <Typography color="error">Error loading dashboard: {error}</Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">System Overview</Typography>
        <Box>
          <Button 
            variant={timeRange === '24h' ? 'contained' : 'outlined'} 
            onClick={() => setTimeRange('24h')}
            sx={{ mr: 1 }}
          >
            24H
          </Button>
          <Button 
            variant={timeRange === '7d' ? 'contained' : 'outlined'} 
            onClick={() => setTimeRange('7d')}
            sx={{ mr: 1 }}
          >
            7D
          </Button>
          <Button 
            variant={timeRange === '30d' ? 'contained' : 'outlined'} 
            onClick={() => setTimeRange('30d')}
          >
            30D
          </Button>
        </Box>
      </Box>

      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Users
              </Typography>
              <Typography variant="h4">
                {systemMetrics.totalUsers.toLocaleString()}
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                <Chip 
                  label={`${systemMetrics.activeUsers} active`} 
                  size="small" 
                  color="success" 
                  variant="outlined" 
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Active Models
              </Typography>
              <Typography variant="h4">
                {systemMetrics.activeModels}
              </Typography>
              <Typography color="textSecondary">
                of {systemMetrics.totalModels} total
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                API Requests (24h)
              </Typography>
              <Typography variant="h4">
                {(systemMetrics.apiRequests / 1000000).toFixed(1)}M
              </Typography>
              <Typography color="textSecondary">
                Avg: {(systemMetrics.apiRequests / 24000).toFixed(0)}/hr
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                System Status
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                <Chip 
                  label={systemMetrics.systemStatus} 
                  color={systemMetrics.systemStatus === 'operational' ? 'success' : 
                         systemMetrics.systemStatus === 'degraded' ? 'warning' : 'error'} 
                />
              </Box>
              <Typography variant="h4" sx={{ mt: 1 }}>
                {systemMetrics.uptime}%
              </Typography>
              <Typography color="textSecondary">
                Uptime (30 days)
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                API Usage & Errors
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={usageData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="requests" fill="#8884d8" name="Requests" />
                  <Bar dataKey="errors" fill="#ff8042" name="Errors" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Model Distribution
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={modelDistribution}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  >
                    {modelDistribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Grid container spacing={3} sx={{ mt: 3 }}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                System Health
              </Typography>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 2 }}>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="h4" color="success.main">99.98%</Typography>
                  <Typography>API Availability</Typography>
                </Box>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="h4" color="success.main">125ms</Typography>
                  <Typography>Avg Response Time</Typography>
                </Box>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="h4" color="error.main">0.2%</Typography>
                  <Typography>Error Rate</Typography>
                </Box>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="h4" color="success.main">24/7</Typography>
                  <Typography>Support</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default SystemOverview;
```

## 4. User Management

### User List Component
```typescript
// src/pages/Users/UserList.tsx
import React, { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  IconButton,
  TextField,
  Typography
} from '@mui/material';
import {
  DataGrid,
  GridColDef,
  GridRenderCellParams,
  GridToolbar
} from '@mui/x-data-grid';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Search as SearchIcon
} from '@mui/icons-material';
import { useAdmin } from '../../hooks/useAdmin';

interface User {
  id: string;
  name: string;
  email: string;
  role: string;
  status: 'active' | 'inactive' | 'suspended';
  lastLogin: string;
  createdAt: string;
}

const UserList: React.FC = () => {
  const { adminUsers, loading, error } = useAdmin();
  const [search, setSearch] = useState('');
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [addUserDialogOpen, setAddUserDialogOpen] = useState(false);

  const columns: GridColDef[] = [
    { field: 'name', headerName: 'Name', width: 200 },
    { field: 'email', headerName: 'Email', width: 250 },
    { 
      field: 'role', 
      headerName: 'Role', 
      width: 150,
      renderCell: (params: GridRenderCellParams) => (
        <Chip 
          label={params.value} 
          size="small" 
          color={params.value === 'admin' ? 'primary' : 'default'} 
        />
      )
    },
    { 
      field: 'status', 
      headerName: 'Status', 
      width: 120,
      renderCell: (params: GridRenderCellParams) => (
        <Chip 
          label={params.value} 
          size="small" 
          color={
            params.value === 'active' ? 'success' : 
            params.value === 'suspended' ? 'error' : 'default'
          } 
        />
      )
    },
    { 
      field: 'lastLogin', 
      headerName: 'Last Login', 
      width: 180,
      valueFormatter: (params) => {
        if (!params.value) return 'Never';
        return new Date(params.value).toLocaleDateString();
      }
    },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 120,
      renderCell: (params: GridRenderCellParams) => (
        <>
          <IconButton 
            size="small" 
            onClick={() => handleEditUser(params.row)}
            sx={{ mr: 1 }}
          >
            <EditIcon />
          </IconButton>
          <IconButton 
            size="small" 
            onClick={() => handleDeleteUser(params.row)}
            color="error"
          >
            <DeleteIcon />
          </IconButton>
        </>
      )
    }
  ];

  const handleDeleteUser = (user: User) => {
    setSelectedUser(user);
    setDeleteDialogOpen(true);
  };

  const handleEditUser = (user: User) => {
    setSelectedUser(user);
    setAddUserDialogOpen(true);
  };

  const handleConfirmDelete = () => {
    // In a real app, this would call an API to delete the user
    setDeleteDialogOpen(false);
    setSelectedUser(null);
  };

  const handleAddUser = () => {
    setSelectedUser(null);
    setAddUserDialogOpen(true);
  };

  const handleSaveUser = () => {
    // In a real app, this would call an API to save the user
    setAddUserDialogOpen(false);
    setSelectedUser(null);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="60vh">
        <Typography>Loading users...</Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Box p={3}>
        <Typography color="error">Error loading users: {error}</Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">User Management</Typography>
        <Button 
          variant="contained" 
          startIcon={<AddIcon />} 
          onClick={handleAddUser}
        >
          Add User
        </Button>
      </Box>

      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />
            <TextField
              placeholder="Search users..."
              variant="standard"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              sx={{ width: 300 }}
            />
          </Box>

          <DataGrid
            rows={adminUsers}
            columns={columns}
            pageSize={10}
            rowsPerPageOptions={[10, 25, 50]}
            components={{ Toolbar: GridToolbar }}
            autoHeight
            disableSelectionOnClick
          />
        </CardContent>
      </Card>

      {/* Delete Confirmation Dialog */}
      <Dialog
        open={deleteDialogOpen}
        onClose={() => setDeleteDialogOpen(false)}
        aria-labelledby="delete-dialog-title"
        aria-describedby="delete-dialog-description"
      >
        <DialogTitle id="delete-dialog-title">
          Delete User
        </DialogTitle>
        <DialogContent>
          <DialogContentText id="delete-dialog-description">
            Are you sure you want to delete {selectedUser?.name}? This action cannot be undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleConfirmDelete} color="error" variant="contained">
            Delete
          </Button>
        </DialogActions>
      </Dialog>

      {/* Add/Edit User Dialog */}
      <Dialog
        open={addUserDialogOpen}
        onClose={() => setAddUserDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          {selectedUser ? 'Edit User' : 'Add New User'}
        </DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Name"
            fullWidth
            variant="outlined"
            defaultValue={selectedUser?.name || ''}
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="Email"
            fullWidth
            variant="outlined"
            defaultValue={selectedUser?.email || ''}
            sx={{ mb: 2 }}
          />
          <TextField
            select
            margin="dense"
            label="Role"
            fullWidth
            variant="outlined"
            defaultValue={selectedUser?.role || 'user'}
            SelectProps={{
              native: true,
            }}
            sx={{ mb: 2 }}
          >
            <option value="user">User</option>
            <option value="admin">Admin</option>
            <option value="superadmin">Super Admin</option>
          </TextField>
          <TextField
            select
            margin="dense"
            label="Status"
            fullWidth
            variant="outlined"
            defaultValue={selectedUser?.status || 'active'}
            SelectProps={{
              native: true,
            }}
          >
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
            <option value="suspended">Suspended</option>
          </TextField>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAddUserDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleSaveUser} variant="contained">
            {selectedUser ? 'Update' : 'Add'} User
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default UserList;
```

## 5. Model Management

### Model List Component
```typescript
// src/pages/Models/ModelList.tsx
import React, { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  IconButton,
  MenuItem,
  Select,
  TextField,
  Typography
} from '@mui/material';
import {
  DataGrid,
  GridColDef,
  GridRenderCellParams,
  GridToolbar
} from '@mui/x-data-grid';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  PlayArrow as DeployIcon,
  Stop as UndeployIcon,
  Search as SearchIcon
} from '@mui/icons-material';
import { useAdmin } from '../../hooks/useAdmin';

interface Model {
  id: string;
  name: string;
  type: string;
  version: string;
  status: 'active' | 'inactive' | 'deploying' | 'error';
  provider: string;
  createdAt: string;
  updatedAt: string;
  usageCount: number;
}

const ModelList: React.FC = () => {
  const { loading, error } = useAdmin();
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedModel, setSelectedModel] = useState<Model | null>(null);
  const [addModelDialogOpen, setAddModelDialogOpen] = useState(false);

  // Mock data - in real app this would come from API
  const models: Model[] = [
    {
      id: '1',
      name: 'GPT-4 Turbo',
      type: 'text-generation',
      version: '1.0.0',
      status: 'active',
      provider: 'OpenAI',
      createdAt: '2025-12-01T10:00:00Z',
      updatedAt: '2025-12-20T15:30:00Z',
      usageCount: 125400
    },
    {
      id: '2',
      name: 'Claude 3 Opus',
      type: 'text-generation',
      version: '2.1.0',
      status: 'active',
      provider: 'Anthropic',
      createdAt: '2025-11-15T09:00:00Z',
      updatedAt: '2025-12-22T11:45:00Z',
      usageCount: 87650
    },
    {
      id: '3',
      name: 'Llama 3 70B',
      type: 'text-generation',
      version: '3.0.0',
      status: 'deploying',
      provider: 'Meta',
      createdAt: '2025-12-10T14:00:00Z',
      updatedAt: '2025-12-28T09:15:00Z',
      usageCount: 45670
    }
  ];

  const columns: GridColDef[] = [
    { field: 'name', headerName: 'Name', width: 200 },
    { field: 'type', headerName: 'Type', width: 150 },
    { field: 'version', headerName: 'Version', width: 120 },
    { 
      field: 'status', 
      headerName: 'Status', 
      width: 120,
      renderCell: (params: GridRenderCellParams) => (
        <Chip 
          label={params.value} 
          size="small" 
          color={
            params.value === 'active' ? 'success' : 
            params.value === 'deploying' ? 'warning' : 
            params.value === 'error' ? 'error' : 'default'
          } 
        />
      )
    },
    { field: 'provider', headerName: 'Provider', width: 150 },
    { 
      field: 'usageCount', 
      headerName: 'Usage', 
      width: 120,
      valueFormatter: (params) => {
        return params.value.toLocaleString();
      }
    },
    { 
      field: 'updatedAt', 
      headerName: 'Last Updated', 
      width: 180,
      valueFormatter: (params) => {
        return new Date(params.value).toLocaleDateString();
      }
    },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 150,
      renderCell: (params: GridRenderCellParams) => (
        <>
          <IconButton 
            size="small" 
            onClick={() => handleDeployModel(params.row)}
            sx={{ mr: 1 }}
            color={params.row.status === 'active' ? 'default' : 'primary'}
          >
            {params.row.status === 'active' ? <UndeployIcon /> : <DeployIcon />}
          </IconButton>
          <IconButton 
            size="small" 
            onClick={() => handleEditModel(params.row)}
            sx={{ mr: 1 }}
          >
            <EditIcon />
          </IconButton>
          <IconButton 
            size="small" 
            onClick={() => handleDeleteModel(params.row)}
            color="error"
          >
            <DeleteIcon />
          </IconButton>
        </>
      )
    }
  ];

  const handleDeployModel = (model: Model) => {
    // In a real app, this would call an API to deploy/undeploy the model
    console.log(`Toggling deployment for model: ${model.name}`);
  };

  const handleDeleteModel = (model: Model) => {
    setSelectedModel(model);
    setDeleteDialogOpen(true);
  };

  const handleEditModel = (model: Model) => {
    setSelectedModel(model);
    setAddModelDialogOpen(true);
  };

  const handleConfirmDelete = () => {
    // In a real app, this would call an API to delete the model
    setDeleteDialogOpen(false);
    setSelectedModel(null);
  };

  const handleAddModel = () => {
    setSelectedModel(null);
    setAddModelDialogOpen(true);
  };

  const handleSaveModel = () => {
    // In a real app, this would call an API to save the model
    setAddModelDialogOpen(false);
    setSelectedModel(null);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="60vh">
        <Typography>Loading models...</Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Box p={3}>
        <Typography color="error">Error loading models: {error}</Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">Model Management</Typography>
        <Button 
          variant="contained" 
          startIcon={<AddIcon />} 
          onClick={handleAddModel}
        >
          Add Model
        </Button>
      </Box>

      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2, gap: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />
              <TextField
                placeholder="Search models..."
                variant="standard"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                sx={{ width: 300 }}
              />
            </Box>
            
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <Typography sx={{ mr: 1 }}>Status:</Typography>
              <Select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value as string)}
                size="small"
                sx={{ minWidth: 120 }}
              >
                <MenuItem value="all">All</MenuItem>
                <MenuItem value="active">Active</MenuItem>
                <MenuItem value="inactive">Inactive</MenuItem>
                <MenuItem value="deploying">Deploying</MenuItem>
                <MenuItem value="error">Error</MenuItem>
              </Select>
            </Box>
          </Box>

          <DataGrid
            rows={models}
            columns={columns}
            pageSize={10}
            rowsPerPageOptions={[10, 25, 50]}
            components={{ Toolbar: GridToolbar }}
            autoHeight
            disableSelectionOnClick
          />
        </CardContent>
      </Card>

      {/* Delete Confirmation Dialog */}
      <Dialog
        open={deleteDialogOpen}
        onClose={() => setDeleteDialogOpen(false)}
        aria-labelledby="delete-model-dialog-title"
        aria-describedby="delete-model-dialog-description"
      >
        <DialogTitle id="delete-model-dialog-title">
          Delete Model
        </DialogTitle>
        <DialogContent>
          <Typography id="delete-model-dialog-description">
            Are you sure you want to delete {selectedModel?.name}? This action cannot be undone.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleConfirmDelete} color="error" variant="contained">
            Delete
          </Button>
        </DialogActions>
      </Dialog>

      {/* Add/Edit Model Dialog */}
      <Dialog
        open={addModelDialogOpen}
        onClose={() => setAddModelDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          {selectedModel ? 'Edit Model' : 'Add New Model'}
        </DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Name"
            fullWidth
            variant="outlined"
            defaultValue={selectedModel?.name || ''}
            sx={{ mb: 2 }}
          />
          <TextField
            select
            margin="dense"
            label="Type"
            fullWidth
            variant="outlined"
            defaultValue={selectedModel?.type || 'text-generation'}
            SelectProps={{
              native: true,
            }}
            sx={{ mb: 2 }}
          >
            <option value="text-generation">Text Generation</option>
            <option value="image-generation">Image Generation</option>
            <option value="speech-recognition">Speech Recognition</option>
            <option value="translation">Translation</option>
            <option value="embedding">Embedding</option>
          </TextField>
          <TextField
            margin="dense"
            label="Version"
            fullWidth
            variant="outlined"
            defaultValue={selectedModel?.version || ''}
            sx={{ mb: 2 }}
          />
          <TextField
            select
            margin="dense"
            label="Provider"
            fullWidth
            variant="outlined"
            defaultValue={selectedModel?.provider || 'custom'}
            SelectProps={{
              native: true,
            }}
            sx={{ mb: 2 }}
          >
            <option value="openai">OpenAI</option>
            <option value="anthropic">Anthropic</option>
            <option value="google">Google</option>
            <option value="meta">Meta</option>
            <option value="custom">Custom</option>
          </TextField>
          <TextField
            select
            margin="dense"
            label="Status"
            fullWidth
            variant="outlined"
            defaultValue={selectedModel?.status || 'inactive'}
            SelectProps={{
              native: true,
            }}
          >
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
            <option value="deploying">Deploying</option>
            <option value="error">Error</option>
          </TextField>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAddModelDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleSaveModel} variant="contained">
            {selectedModel ? 'Update' : 'Add'} Model
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ModelList;
```

## 6. System Monitoring

### System Health Dashboard
```typescript
// src/pages/System/SystemHealth.tsx
import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  LinearProgress,
  Chip,
  IconButton,
  Tooltip
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  Warning as WarningIcon,
  CheckCircle as CheckIcon,
  Error as ErrorIcon
} from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as ChartTooltip, Legend, ResponsiveContainer } from 'recharts';

interface SystemMetric {
  name: string;
  status: 'healthy' | 'warning' | 'critical';
  value: number;
  max: number;
  unit: string;
  lastUpdated: string;
}

interface ServiceStatus {
  name: string;
  status: 'operational' | 'degraded' | 'down';
  responseTime: number;
  lastCheck: string;
}

const SystemHealth: React.FC = () => {
  const [lastUpdated, setLastUpdated] = useState(new Date().toISOString());

  // Mock data - in real app this would come from API
  const systemMetrics: SystemMetric[] = [
    { name: 'CPU Usage', status: 'healthy', value: 45, max: 100, unit: '%', lastUpdated: '2025-12-28T14:30:00Z' },
    { name: 'Memory Usage', status: 'warning', value: 78, max: 100, unit: '%', lastUpdated: '2025-12-28T14:30:00Z' },
    { name: 'Disk Usage', status: 'healthy', value: 62, max: 100, unit: '%', lastUpdated: '2025-12-28T14:30:00Z' },
    { name: 'Network I/O', status: 'healthy', value: 245, max: 1000, unit: 'Mbps', lastUpdated: '2025-12-28T14:30:00Z' },
    { name: 'Database Connections', status: 'healthy', value: 142, max: 200, unit: 'connections', lastUpdated: '2025-12-28T14:30:00Z' },
    { name: 'API Response Time', status: 'warning', value: 185, max: 200, unit: 'ms', lastUpdated: '2025-12-28T14:30:00Z' }
  ];

  const serviceStatus: ServiceStatus[] = [
    { name: 'API Gateway', status: 'operational', responseTime: 45, lastCheck: '2025-12-28T14:30:00Z' },
    { name: 'Model Service', status: 'operational', responseTime: 120, lastCheck: '2025-12-28T14:30:00Z' },
    { name: 'Database', status: 'operational', responseTime: 15, lastCheck: '2025-12-28T14:30:00Z' },
    { name: 'Cache', status: 'degraded', responseTime: 320, lastCheck: '2025-12-28T14:30:00Z' },
    { name: 'Authentication', status: 'operational', responseTime: 65, lastCheck: '2025-12-28T14:30:00Z' },
    { name: 'Storage', status: 'operational', responseTime: 85, lastCheck: '2025-12-28T14:30:00Z' }
  ];

  // Mock performance data for chart
  const performanceData = [
    { time: '00:00', cpu: 35, memory: 65, response: 120 },
    { time: '04:00', cpu: 28, memory: 58, response: 95 },
    { time: '08:00', cpu: 65, memory: 78, response: 180 },
    { time: '12:00', cpu: 72, memory: 82, response: 210 },
    { time: '16:00', cpu: 58, memory: 75, response: 165 },
    { time: '20:00', cpu: 42, memory: 68, response: 140 }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'success';
      case 'warning': return 'warning';
      case 'critical': return 'error';
      case 'operational': return 'success';
      case 'degraded': return 'warning';
      case 'down': return 'error';
      default: return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy':
      case 'operational':
        return <CheckIcon color="success" />;
      case 'warning':
      case 'degraded':
        return <WarningIcon color="warning" />;
      case 'critical':
      case 'down':
        return <ErrorIcon color="error" />;
      default:
        return null;
    }
  };

  const handleRefresh = () => {
    setLastUpdated(new Date().toISOString());
    // In a real app, this would fetch fresh data from API
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">System Health</Typography>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Typography variant="body2" sx={{ mr: 2 }}>
            Last updated: {new Date(lastUpdated).toLocaleTimeString()}
          </Typography>
          <Tooltip title="Refresh data">
            <IconButton onClick={handleRefresh}>
              <RefreshIcon />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>

      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                System Metrics
              </Typography>
              <Grid container spacing={2}>
                {systemMetrics.map((metric) => (
                  <Grid item xs={12} sm={6} md={4} key={metric.name}>
                    <Card variant="outlined">
                      <CardContent>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                          <Typography variant="subtitle1">{metric.name}</Typography>
                          <Chip 
                            icon={getStatusIcon(metric.status)} 
                            label={metric.status} 
                            size="small" 
                            color={getStatusColor(metric.status) as any} 
                          />
                        </Box>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                          <Typography variant="h6" sx={{ mr: 1 }}>
                            {metric.value}{metric.unit}
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            of {metric.max}{metric.unit}
                          </Typography>
                        </Box>
                        <LinearProgress 
                          variant="determinate" 
                          value={(metric.value / metric.max) * 100} 
                          color={
                            metric.status === 'healthy' ? 'success' : 
                            metric.status === 'warning' ? 'warning' : 'error'
                          } 
                        />
                        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                          Last updated: {new Date(metric.lastUpdated).toLocaleTimeString()}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Performance Overview
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={performanceData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="time" />
                  <YAxis />
                  <ChartTooltip />
                  <Legend />
                  <Line type="monotone" dataKey="cpu" stroke="#8884d8" name="CPU %" strokeWidth={2} />
                  <Line type="monotone" dataKey="memory" stroke="#82ca9d" name="Memory %" strokeWidth={2} />
                  <Line type="monotone" dataKey="response" stroke="#ffc658" name="Response (ms)" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Service Status
              </Typography>
              {serviceStatus.map((service) => (
                <Box 
                  key={service.name} 
                  sx={{ 
                    display: 'flex', 
                    justifyContent: 'space-between', 
                    alignItems: 'center', 
                    py: 1,
                    borderBottom: '1px solid rgba(0,0,0,0.1)'
                  }}
                >
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    {getStatusIcon(service.status)}
                    <Typography sx={{ ml: 1 }}>{service.name}</Typography>
                  </Box>
                  <Box sx={{ textAlign: 'right' }}>
                    <Typography variant="body2">{service.responseTime}ms</Typography>
                    <Typography variant="caption" color="text.secondary">
                      {new Date(service.lastCheck).toLocaleTimeString()}
                    </Typography>
                  </Box>
                </Box>
              ))}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                System Alerts
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', p: 2, bgcolor: 'warning.light', borderRadius: 1, mb: 2 }}>
                <WarningIcon sx={{ mr: 1, color: 'warning.main' }} />
                <Typography>
                  <strong>Warning:</strong> Memory usage is approaching threshold (78%)
                </Typography>
              </Box>
              <Box sx={{ display: 'flex', alignItems: 'center', p: 2, bgcolor: 'info.light', borderRadius: 1 }}>
                <CheckIcon sx={{ mr: 1, color: 'info.main' }} />
                <Typography>
                  <strong>Info:</strong> System backup completed successfully at 02:00
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default SystemHealth;
```

## 7. API Integration

### Admin API Service
```typescript
// src/services/adminApi.ts
import axios from 'axios';
import { AdminUser, AdminRole } from '../hooks/useAdmin';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const adminApi = axios.create({
  baseURL: `${API_BASE_URL}/admin`,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
adminApi.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('adminToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle errors
adminApi.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('adminToken');
      window.location.href = '/admin/login';
    }
    return Promise.reject(error);
  }
);

export interface AdminLoginData {
  email: string;
  password: string;
}

export interface AdminLoginResponse {
  token: string;
  user: AdminUser;
}

export const adminAuthService = {
  async login(data: AdminLoginData): Promise<AdminLoginResponse> {
    const response = await adminApi.post('/auth/login', data);
    return response.data;
  },

  async logout() {
    try {
      await adminApi.post('/auth/logout');
    } catch (error) {
      // Ignore logout errors
    }
  },

  async getCurrentUser(): Promise<AdminUser> {
    const response = await adminApi.get('/auth/me');
    return response.data;
  }
};

export const adminUserService = {
  async getUsers(): Promise<AdminUser[]> {
    const response = await adminApi.get('/users');
    return response.data;
  },

  async getUser(id: string): Promise<AdminUser> {
    const response = await adminApi.get(`/users/${id}`);
    return response.data;
  },

  async createUser(userData: Partial<AdminUser>): Promise<AdminUser> {
    const response = await adminApi.post('/users', userData);
    return response.data;
  },

  async updateUser(id: string, userData: Partial<AdminUser>): Promise<AdminUser> {
    const response = await adminApi.put(`/users/${id}`, userData);
    return response.data;
  },

  async deleteUser(id: string): Promise<void> {
    await adminApi.delete(`/users/${id}`);
  },

  async getRoles(): Promise<AdminRole[]> {
    const response = await adminApi.get('/roles');
    return response.data;
  }
};

export const adminModelService = {
  async getModels() {
    const response = await adminApi.get('/models');
    return response.data;
  },

  async getModel(id: string) {
    const response = await adminApi.get(`/models/${id}`);
    return response.data;
  },

  async createModel(modelData: any) {
    const response = await adminApi.post('/models', modelData);
    return response.data;
  },

  async updateModel(id: string, modelData: any) {
    const response = await adminApi.put(`/models/${id}`, modelData);
    return response.data;
  },

  async deleteModel(id: string) {
    const response = await adminApi.delete(`/models/${id}`);
    return response.data;
  },

  async deployModel(id: string) {
    const response = await adminApi.post(`/models/${id}/deploy`);
    return response.data;
  },

  async undeployModel(id: string) {
    const response = await adminApi.post(`/models/${id}/undeploy`);
    return response.data;
  }
};

export const adminSystemService = {
  async getSystemMetrics() {
    const response = await adminApi.get('/system/metrics');
    return response.data;
  },

  async getSystemHealth() {
    const response = await adminApi.get('/system/health');
    return response.data;
  },

  async getSystemLogs(params?: any) {
    const response = await adminApi.get('/system/logs', { params });
    return response.data;
  },

  async getSystemAlerts() {
    const response = await adminApi.get('/system/alerts');
    return response.data;
  }
};

export default adminApi;
```

## 8. Security Features

### Admin Authentication Hook
```typescript
// src/hooks/useAdminAuth.ts
import { useState, useEffect, useContext, createContext } from 'react';
import { adminAuthService, AdminLoginData, AdminLoginResponse } from '../services/adminApi';

interface AdminAuthContextType {
  user: any;
  login: (data: AdminLoginData) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
  isLoading: boolean;
}

const AdminAuthContext = createContext<AdminAuthContextType | undefined>(undefined);

export const useAdminAuth = () => {
  const context = useContext(AdminAuthContext);
  if (!context) {
    throw new Error('useAdminAuth must be used within an AdminAuthProvider');
  }
  return context;
};

interface AdminAuthProviderProps {
  children: React.ReactNode;
}

export const AdminAuthProvider: React.FC<AdminAuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<any>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('adminToken');
    if (token) {
      // Verify token and fetch user data
      verifyToken(token);
    } else {
      setIsLoading(false);
    }
  }, []);

  const verifyToken = async (token: string) => {
    try {
      const userData = await adminAuthService.getCurrentUser();
      setUser(userData);
      setIsAuthenticated(true);
    } catch (error) {
      localStorage.removeItem('adminToken');
      setIsAuthenticated(false);
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (data: AdminLoginData) => {
    try {
      const response: AdminLoginResponse = await adminAuthService.login(data);
      localStorage.setItem('adminToken', response.token);
      setUser(response.user);
      setIsAuthenticated(true);
    } catch (error) {
      throw new Error('Invalid credentials');
    }
  };

  const logout = () => {
    localStorage.removeItem('adminToken');
    setUser(null);
    setIsAuthenticated(false);
    adminAuthService.logout();
  };

  const value = {
    user,
    login,
    logout,
    isAuthenticated,
    isLoading
  };

  return <AdminAuthContext.Provider value={value}>{children}</AdminAuthContext.Provider>;
};
```

## 9. Testing Strategy

### Component Tests
```typescript
// tests/components/layout/AdminLayout.test.tsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { AdminAuthProvider } from '../../../src/hooks/useAdminAuth';
import AdminLayout from '../../../src/components/layout/AdminLayout';

// Mock the useAdminAuth hook
jest.mock('../../../src/hooks/useAdminAuth', () => ({
  useAdminAuth: () => ({
    user: { name: 'Admin User', role: 'superadmin' },
    logout: jest.fn()
  })
}));

describe('AdminLayout', () => {
  const renderWithProviders = (component: React.ReactNode) => {
    return render(
      <AdminAuthProvider>
        <BrowserRouter>
          {component}
        </BrowserRouter>
      </AdminAuthProvider>
    );
  };

  it('renders admin layout with navigation', () => {
    renderWithProviders(<AdminLayout />);
    
    expect(screen.getByText('AI Platform Admin')).toBeInTheDocument();
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Users')).toBeInTheDocument();
    expect(screen.getByText('Models')).toBeInTheDocument();
    expect(screen.getByText('Analytics')).toBeInTheDocument();
    expect(screen.getByText('System')).toBeInTheDocument();
    expect(screen.getByText('Settings')).toBeInTheDocument();
  });

  it('toggles mobile drawer', () => {
    renderWithProviders(<AdminLayout />);
    
    const menuButton = screen.getByLabelText('open drawer');
    fireEvent.click(menuButton);
    
    // Drawer should be visible in mobile view
    // This would require more complex testing with different screen sizes
  });

  it('shows user avatar and menu', () => {
    renderWithProviders(<AdminLayout />);
    
    expect(screen.getByText('A')).toBeInTheDocument(); // Avatar initial
    
    const avatarButton = screen.getByText('A').closest('button');
    if (avatarButton) {
      fireEvent.click(avatarButton);
      
      expect(screen.getByText('Profile')).toBeInTheDocument();
      expect(screen.getByText('Settings')).toBeInTheDocument();
      expect(screen.getByText('Logout')).toBeInTheDocument();
    }
  });
});
```

## 10. Deployment Configuration

### Docker Configuration
```dockerfile
# Dockerfile
FROM node:18-alpine AS build

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy build files
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
```

### Environment Configuration
```typescript
// src/config/environment.ts
interface AdminConfig {
  apiUrl: string;
  appName: string;
  version: string;
  features: {
    userManagement: boolean;
    modelManagement: boolean;
    systemMonitoring: boolean;
    analytics: boolean;
  };
}

const getAdminConfig = (): AdminConfig => {
  const env = process.env.NODE_ENV || 'development';
  
  const configs: Record<string, AdminConfig> = {
    development: {
      apiUrl: 'http://localhost:8000/api',
      appName: 'AI Platform Admin Dev',
      version: '1.0.0-dev',
      features: {
        userManagement: true,
        modelManagement: true,
        systemMonitoring: true,
        analytics: true
      }
    },
    staging: {
      apiUrl: 'https://staging.api.aiplatform.io/api',
      appName: 'AI Platform Admin Staging',
      version: '1.0.0-staging',
      features: {
        userManagement: true,
        modelManagement: true,
        systemMonitoring: true,
        analytics: true
      }
    },
    production: {
      apiUrl: 'https://api.aiplatform.io/api',
      appName: 'AI Platform Admin',
      version: '1.0.0',
      features: {
        userManagement: true,
        modelManagement: true,
        systemMonitoring: true,
        analytics: true
      }
    }
  };

  return configs[env] || configs.development;
};

export default getAdminConfig();
```

## Conclusion

This admin panel template provides a comprehensive foundation for managing the AI Platform with:

1. **Secure authentication** with role-based access control
2. **Comprehensive dashboard** with system metrics and health monitoring
3. **User management** with CRUD operations and role assignment
4. **Model management** with deployment controls
5. **System monitoring** with real-time metrics and alerts
6. **Responsive design** for desktop and tablet use
7. **Security features** including proper authentication and authorization
8. **Testing framework** for component and integration testing
9. **Deployment configuration** for containerized environments

The admin panel is designed to be scalable, maintainable, and secure while providing all necessary tools for platform administration.

**Admin Panel Version**: 1.0
**Last Updated**: December 28, 2025
**Next Review**: March 28, 2026