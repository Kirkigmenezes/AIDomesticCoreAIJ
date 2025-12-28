# AI Platform Web Dashboard

## Overview

This document provides the design specifications and implementation guide for the AI Platform Web Dashboard, a comprehensive interface for managing AI models, monitoring performance, and accessing platform features.

## 1. Dashboard Architecture

### Technology Stack
- **Frontend Framework**: React 18 with TypeScript
- **State Management**: Redux Toolkit
- **UI Library**: Material-UI (MUI) v5
- **Charting**: Chart.js with React-Chartjs-2
- **Routing**: React Router v6
- **Build Tool**: Vite.js
- **Testing**: Jest and React Testing Library
- **Deployment**: Docker with Nginx

### Project Structure
```
web-dashboard/
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
│   │   ├── dashboard/
│   │   ├── models/
│   │   ├── analytics/
│   │   └── settings/
│   ├── pages/
│   │   ├── Dashboard/
│   │   ├── Models/
│   │   ├── Analytics/
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
│   │   └── useAnalytics.ts
│   ├── types/
│   │   └── index.ts
│   ├── App.tsx
│   └── main.tsx
├── tests/
├── Dockerfile
├── docker-compose.yml
├── vite.config.ts
├── tsconfig.json
└── package.json
```

## 2. Core Components

### Authentication Module
```typescript
// src/components/auth/LoginForm.tsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import {
  Box,
  Button,
  TextField,
  Typography,
  Container,
  Paper,
  Alert
} from '@mui/material';

interface LoginFormProps {
  onLoginSuccess: () => void;
}

const LoginForm: React.FC<LoginFormProps> = ({ onLoginSuccess }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await login(email, password);
      onLoginSuccess();
      navigate('/dashboard');
    } catch (err) {
      setError('Invalid credentials. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <Paper elevation={3} sx={{ p: 4, mt: 8 }}>
        <Typography component="h1" variant="h5" align="center" gutterBottom>
          AI Platform Login
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
            label="Email Address"
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
      </Paper>
    </Container>
  );
};

export default LoginForm;
```

### Dashboard Layout
```typescript
// src/components/layout/DashboardLayout.tsx
import React from 'react';
import { Outlet } from 'react-router-dom';
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
  Toolbar,
  Typography
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  Psychology as ModelsIcon,
  Analytics as AnalyticsIcon,
  Settings as SettingsIcon,
  AccountCircle as ProfileIcon,
  Logout as LogoutIcon
} from '@mui/icons-material';
import { useAuth } from '../../hooks/useAuth';

const drawerWidth = 240;

const DashboardLayout: React.FC = () => {
  const [mobileOpen, setMobileOpen] = React.useState(false);
  const { logout } = useAuth();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const menuItems = [
    { text: 'Dashboard', icon: <DashboardIcon />, path: '/dashboard' },
    { text: 'Models', icon: <ModelsIcon />, path: '/models' },
    { text: 'Analytics', icon: <AnalyticsIcon />, path: '/analytics' },
    { text: 'Settings', icon: <SettingsIcon />, path: '/settings' },
    { text: 'Profile', icon: <ProfileIcon />, path: '/profile' }
  ];

  const drawer = (
    <div>
      <Toolbar>
        <Typography variant="h6" noWrap component="div">
          AI Platform
        </Typography>
      </Toolbar>
      <Divider />
      <List>
        {menuItems.map((item) => (
          <ListItem button key={item.text} component="a" href={item.path}>
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
      </List>
      <Divider />
      <List>
        <ListItem button onClick={logout}>
          <ListItemIcon>
            <LogoutIcon />
          </ListItemIcon>
          <ListItemText primary="Logout" />
        </ListItem>
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
          <Typography variant="h6" noWrap component="div">
            AI Platform Dashboard
          </Typography>
        </Toolbar>
      </AppBar>
      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
        aria-label="mailbox folders"
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
        sx={{ flexGrow: 1, p: 3, width: { sm: `calc(100% - ${drawerWidth}px)` } }}
      >
        <Toolbar />
        <Outlet />
      </Box>
    </Box>
  );
};

export default DashboardLayout;
```

### Main Dashboard Page
```typescript
// src/pages/Dashboard/DashboardPage.tsx
import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  CircularProgress
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
  LineChart,
  Line
} from 'recharts';
import { useAnalytics } from '../../hooks/useAnalytics';

const DashboardPage: React.FC = () => {
  const { analyticsData, loading, error } = useAnalytics();
  const [timeRange, setTimeRange] = useState('7d');

  useEffect(() => {
    // Fetch analytics data when component mounts
  }, [timeRange]);

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
        <Typography color="error">Error loading dashboard data: {error}</Typography>
      </Box>
    );
  }

  const usageData = [
    { name: 'Mon', requests: 4000, tokens: 2400 },
    { name: 'Tue', requests: 3000, tokens: 1398 },
    { name: 'Wed', requests: 2000, tokens: 9800 },
    { name: 'Thu', requests: 2780, tokens: 3908 },
    { name: 'Fri', requests: 1890, tokens: 4800 },
    { name: 'Sat', requests: 2390, tokens: 3800 },
    { name: 'Sun', requests: 3490, tokens: 4300 },
  ];

  const modelPerformanceData = [
    { name: 'GPT-4', accuracy: 95, latency: 120 },
    { name: 'Claude', accuracy: 92, latency: 150 },
    { name: 'Llama', accuracy: 88, latency: 200 },
    { name: 'Custom', accuracy: 94, latency: 180 }
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard Overview
      </Typography>

      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Requests
              </Typography>
              <Typography variant="h5">
                {analyticsData?.totalRequests?.toLocaleString() || '0'}
              </Typography>
              <Typography color="textSecondary">
                +12% from last week
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Active Models
              </Typography>
              <Typography variant="h5">
                {analyticsData?.activeModels || '0'}
              </Typography>
              <Typography color="textSecondary">
                3 new this month
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                API Latency
              </Typography>
              <Typography variant="h5">
                {analyticsData?.avgLatency?.toFixed(2) || '0'}ms
              </Typography>
              <Typography color="textSecondary">
                -5% from last week
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                User Satisfaction
              </Typography>
              <Typography variant="h5">
                {analyticsData?.satisfactionScore || '0'}%
              </Typography>
              <Typography color="textSecondary">
                +2% from last week
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
                API Usage (Last 7 Days)
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={usageData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="requests" fill="#8884d8" name="Requests" />
                  <Bar dataKey="tokens" fill="#82ca9d" name="Tokens" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Model Performance
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={modelPerformanceData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="accuracy" fill="#8884d8" name="Accuracy (%)" />
                  <Bar dataKey="latency" fill="#82ca9d" name="Latency (ms)" />
                </BarChart>
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
                Request Trends
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={usageData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="requests"
                    stroke="#8884d8"
                    name="Requests"
                    strokeWidth={2}
                  />
                  <Line
                    type="monotone"
                    dataKey="tokens"
                    stroke="#82ca9d"
                    name="Tokens"
                    strokeWidth={2}
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default DashboardPage;
```

## 3. API Integration

### API Service Layer
```typescript
// src/services/api.ts
import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';

class ApiService {
  private client: AxiosInstance;
  private baseUrl: string;

  constructor() {
    this.baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
    this.client = axios.create({
      baseURL: this.baseUrl,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('authToken');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor to handle errors
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Handle unauthorized access
          localStorage.removeItem('authToken');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Authentication endpoints
  async login(email: string, password: string) {
    const response = await this.client.post('/auth/login', { email, password });
    return response.data;
  }

  async logout() {
    const response = await this.client.post('/auth/logout');
    return response.data;
  }

  async register(userData: any) {
    const response = await this.client.post('/auth/register', userData);
    return response.data;
  }

  // Model management endpoints
  async getModels() {
    const response = await this.client.get('/models');
    return response.data;
  }

  async getModel(id: string) {
    const response = await this.client.get(`/models/${id}`);
    return response.data;
  }

  async createModel(modelData: any) {
    const response = await this.client.post('/models', modelData);
    return response.data;
  }

  async updateModel(id: string, modelData: any) {
    const response = await this.client.put(`/models/${id}`, modelData);
    return response.data;
  }

  async deleteModel(id: string) {
    const response = await this.client.delete(`/models/${id}`);
    return response.data;
  }

  // Analytics endpoints
  async getAnalytics(params?: any) {
    const response = await this.client.get('/analytics', { params });
    return response.data;
  }

  async getUsageStats(timeRange: string) {
    const response = await this.client.get(`/analytics/usage?range=${timeRange}`);
    return response.data;
  }

  async getModelPerformance(modelId: string) {
    const response = await this.client.get(`/analytics/models/${modelId}/performance`);
    return response.data;
  }

  // Inference endpoints
  async runInference(modelId: string, inputData: any) {
    const response = await this.client.post(`/models/${modelId}/inference`, inputData);
    return response.data;
  }
}

export default new ApiService();
```

### Authentication Hook
```typescript
// src/hooks/useAuth.ts
import { useState, useEffect, useContext, createContext } from 'react';
import api from '../services/api';

interface AuthContextType {
  user: any;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  register: (userData: any) => Promise<void>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<any>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    if (token) {
      // Verify token and fetch user data
      verifyToken(token);
    }
  }, []);

  const verifyToken = async (token: string) => {
    try {
      // In a real app, you would verify the token with the backend
      setIsAuthenticated(true);
      // Fetch user data
      // setUser(userData);
    } catch (error) {
      localStorage.removeItem('authToken');
      setIsAuthenticated(false);
    }
  };

  const login = async (email: string, password: string) => {
    try {
      const response = await api.login(email, password);
      localStorage.setItem('authToken', response.token);
      setUser(response.user);
      setIsAuthenticated(true);
    } catch (error) {
      throw new Error('Invalid credentials');
    }
  };

  const logout = () => {
    localStorage.removeItem('authToken');
    setUser(null);
    setIsAuthenticated(false);
    api.logout();
  };

  const register = async (userData: any) => {
    try {
      const response = await api.register(userData);
      localStorage.setItem('authToken', response.token);
      setUser(response.user);
      setIsAuthenticated(true);
    } catch (error) {
      throw new Error('Registration failed');
    }
  };

  const value = {
    user,
    login,
    logout,
    register,
    isAuthenticated,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
```

## 4. Analytics Integration

### Analytics Hook
```typescript
// src/hooks/useAnalytics.ts
import { useState, useEffect } from 'react';
import api from '../services/api';

interface AnalyticsData {
  totalRequests: number;
  activeModels: number;
  avgLatency: number;
  satisfactionScore: number;
  usageData: any[];
  modelPerformance: any[];
}

export const useAnalytics = () => {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAnalytics = async (timeRange: string = '7d') => {
    try {
      setLoading(true);
      setError(null);
      
      const [usageStats, modelPerformance] = await Promise.all([
        api.getUsageStats(timeRange),
        api.getAnalytics({ type: 'model_performance' })
      ]);

      setAnalyticsData({
        totalRequests: usageStats.totalRequests,
        activeModels: usageStats.activeModels,
        avgLatency: usageStats.avgLatency,
        satisfactionScore: usageStats.satisfactionScore,
        usageData: usageStats.data,
        modelPerformance: modelPerformance.data
      });
    } catch (err) {
      setError('Failed to fetch analytics data');
      console.error('Analytics fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalytics();
  }, []);

  return { analyticsData, loading, error, refetch: fetchAnalytics };
};
```

## 5. Deployment Configuration

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

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  web-dashboard:
    build: .
    ports:
      - "80:80"
    environment:
      - VITE_API_BASE_URL=http://api:8000/api
    depends_on:
      - api
    networks:
      - aiplatform-network

  api:
    image: aiplatform/api:latest
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/aiplatform
    depends_on:
      - db
    networks:
      - aiplatform-network

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: aiplatform
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - db_data:/var/lib/postgresql/data
    networks:
      - aiplatform-network

volumes:
  db_data:

networks:
  aiplatform-network:
    driver: bridge
```

### Nginx Configuration
```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    sendfile        on;
    tcp_nopush      on;
    tcp_nodelay     on;
    keepalive_timeout  65;
    types_hash_max_size 2048;

    gzip  on;

    server {
        listen       80;
        server_name  localhost;

        location / {
            root   /usr/share/nginx/html;
            index  index.html index.htm;
            try_files $uri $uri/ /index.html;
        }

        location /api {
            proxy_pass http://api:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   /usr/share/nginx/html;
        }
    }
}
```

## 6. Testing Strategy

### Unit Tests
```typescript
// tests/components/auth/LoginForm.test.tsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import LoginForm from '../../src/components/auth/LoginForm';

// Mock the useAuth hook
jest.mock('../../src/hooks/useAuth', () => ({
  useAuth: () => ({
    login: jest.fn().mockResolvedValue(undefined)
  })
}));

describe('LoginForm', () => {
  const mockOnLoginSuccess = jest.fn();

  beforeEach(() => {
    mockOnLoginSuccess.mockClear();
  });

  it('renders login form correctly', () => {
    render(
      <BrowserRouter>
        <LoginForm onLoginSuccess={mockOnLoginSuccess} />
      </BrowserRouter>
    );

    expect(screen.getByLabelText(/email address/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
  });

  it('submits form with valid credentials', async () => {
    render(
      <BrowserRouter>
        <LoginForm onLoginSuccess={mockOnLoginSuccess} />
      </BrowserRouter>
    );

    fireEvent.change(screen.getByLabelText(/email address/i), {
      target: { value: 'test@example.com' }
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'password123' }
    });

    fireEvent.click(screen.getByRole('button', { name: /sign in/i }));

    await waitFor(() => {
      expect(mockOnLoginSuccess).toHaveBeenCalled();
    });
  });

  it('shows error message for invalid credentials', async () => {
    // Mock failed login
    jest.spyOn(require('../../src/hooks/useAuth'), 'useAuth').mockReturnValue({
      login: jest.fn().mockRejectedValue(new Error('Invalid credentials'))
    });

    render(
      <BrowserRouter>
        <LoginForm onLoginSuccess={mockOnLoginSuccess} />
      </BrowserRouter>
    );

    fireEvent.change(screen.getByLabelText(/email address/i), {
      target: { value: 'invalid@example.com' }
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'wrongpassword' }
    });

    fireEvent.click(screen.getByRole('button', { name: /sign in/i }));

    await waitFor(() => {
      expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument();
    });
  });
});
```

### Integration Tests
```typescript
// tests/services/api.test.ts
import ApiService from '../../src/services/api';
import axios from 'axios';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('ApiService', () => {
  let apiService: ApiService;

  beforeEach(() => {
    apiService = new ApiService();
    mockedAxios.create = jest.fn(() => mockedAxios);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('login', () => {
    it('should call login endpoint with correct parameters', async () => {
      const mockResponse = { data: { token: 'test-token', user: {} } };
      mockedAxios.post.mockResolvedValue(mockResponse);

      const result = await apiService.login('test@example.com', 'password123');

      expect(mockedAxios.post).toHaveBeenCalledWith('/auth/login', {
        email: 'test@example.com',
        password: 'password123'
      });
      expect(result).toEqual(mockResponse.data);
    });
  });

  describe('getModels', () => {
    it('should fetch models successfully', async () => {
      const mockModels = [{ id: '1', name: 'GPT-4' }];
      mockedAxios.get.mockResolvedValue({ data: mockModels });

      const result = await apiService.getModels();

      expect(mockedAxios.get).toHaveBeenCalledWith('/models');
      expect(result).toEqual(mockModels);
    });
  });
});
```

## 7. Environment Configuration

### Environment Variables
```typescript
// src/utils/config.ts
interface AppConfig {
  apiUrl: string;
  appName: string;
  version: string;
  features: {
    analytics: boolean;
    modelManagement: boolean;
    customModels: boolean;
  };
}

const config: AppConfig = {
  apiUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  appName: import.meta.env.VITE_APP_NAME || 'AI Platform',
  version: import.meta.env.VITE_APP_VERSION || '1.0.0',
  features: {
    analytics: import.meta.env.VITE_FEATURE_ANALYTICS === 'true',
    modelManagement: import.meta.env.VITE_FEATURE_MODEL_MANAGEMENT === 'true',
    customModels: import.meta.env.VITE_FEATURE_CUSTOM_MODELS === 'true',
  }
};

export default config;
```

### Vite Configuration
```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tsconfigPaths from 'vite-tsconfig-paths';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      }
    }
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          ui: ['@mui/material', '@mui/icons-material'],
          charts: ['recharts']
        }
      }
    }
  },
  define: {
    __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
  }
});
```

## 8. Performance Optimization

### Code Splitting
```typescript
// src/App.tsx
import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './hooks/useAuth';
import DashboardLayout from './components/layout/DashboardLayout';
import LoadingSpinner from './components/common/LoadingSpinner';

// Lazy load pages for code splitting
const DashboardPage = lazy(() => import('./pages/Dashboard/DashboardPage'));
const ModelsPage = lazy(() => import('./pages/Models/ModelsPage'));
const AnalyticsPage = lazy(() => import('./pages/Analytics/AnalyticsPage'));
const SettingsPage = lazy(() => import('./pages/Settings/SettingsPage'));
const ProfilePage = lazy(() => import('./pages/Profile/ProfilePage'));
const LoginPage = lazy(() => import('./pages/Auth/LoginPage'));
const RegisterPage = lazy(() => import('./pages/Auth/RegisterPage'));

const App: React.FC = () => {
  return (
    <AuthProvider>
      <Router>
        <Suspense fallback={<LoadingSpinner />}>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route element={<DashboardLayout />}>
              <Route path="/dashboard" element={<DashboardPage />} />
              <Route path="/models" element={<ModelsPage />} />
              <Route path="/analytics" element={<AnalyticsPage />} />
              <Route path="/settings" element={<SettingsPage />} />
              <Route path="/profile" element={<ProfilePage />} />
            </Route>
            <Route path="/" element={<DashboardPage />} />
          </Routes>
        </Suspense>
      </Router>
    </AuthProvider>
  );
};

export default App;
```

### Performance Monitoring
```typescript
// src/utils/performance.ts
class PerformanceMonitor {
  private metrics: any[] = [];

  startMeasurement(name: string): string {
    const id = `${name}-${Date.now()}`;
    this.metrics[id] = {
      name,
      start: performance.now()
    };
    return id;
  }

  endMeasurement(id: string): number {
    const metric = this.metrics[id];
    if (!metric) return 0;

    const duration = performance.now() - metric.start;
    console.log(`${metric.name} took ${duration.toFixed(2)}ms`);
    
    // In production, send to analytics service
    if (process.env.NODE_ENV === 'production') {
      this.sendToAnalytics({
        name: metric.name,
        duration,
        timestamp: new Date().toISOString()
      });
    }

    delete this.metrics[id];
    return duration;
  }

  private sendToAnalytics(data: any) {
    // Send performance data to analytics service
    fetch('/api/analytics/performance', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).catch(console.error);
  }
}

export default new PerformanceMonitor();
```

## 9. Security Considerations

### Content Security Policy
```html
<!-- public/index.html -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta
      http-equiv="Content-Security-Policy"
      content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self' http://localhost:8000;"
    />
    <title>AI Platform Dashboard</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

## 10. Accessibility

### Accessible Components
```typescript
// src/components/common/AccessibleButton.tsx
import React from 'react';
import { Button, ButtonProps } from '@mui/material';

interface AccessibleButtonProps extends ButtonProps {
  ariaLabel: string;
  tooltip?: string;
}

const AccessibleButton: React.FC<AccessibleButtonProps> = ({
  ariaLabel,
  tooltip,
  children,
  ...props
}) => {
  return (
    <Button
      aria-label={ariaLabel}
      title={tooltip}
      {...props}
    >
      {children}
    </Button>
  );
};

export default AccessibleButton;
```

## Conclusion

This web dashboard implementation provides a comprehensive interface for the AI Platform with modern React development practices, responsive design, and robust architecture. The dashboard includes authentication, analytics visualization, model management, and performance monitoring capabilities.

The implementation follows best practices for:
- Component-based architecture
- State management with Redux Toolkit
- API integration with error handling
- Responsive design with Material-UI
- Testing with Jest and React Testing Library
- Performance optimization with code splitting
- Security with proper CSP and authentication
- Accessibility compliance

**Dashboard Version**: 1.0
**Last Updated**: December 28, 2025
**Next Review**: March 28, 2026