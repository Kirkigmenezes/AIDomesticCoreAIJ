# AI Platform Mobile App Setup

## Overview

This document provides a comprehensive guide for setting up the AI Platform mobile application for both iOS and Android platforms. It covers technology stack selection, project structure, core features, and deployment strategies.

## 1. Technology Stack

### Cross-Platform Framework
- **Primary Choice**: React Native (v0.72+)
- **Alternative**: Flutter (v3.10+)
- **UI Library**: React Native Paper or NativeBase
- **State Management**: Redux Toolkit with Redux Persist
- **Navigation**: React Navigation v6
- **Networking**: Axios with offline support
- **Storage**: AsyncStorage with SQLite for complex data
- **Push Notifications**: Firebase Cloud Messaging (FCM)
- **Analytics**: Firebase Analytics
- **Crash Reporting**: Firebase Crashlytics

### Development Tools
- **IDE**: Visual Studio Code with React Native Tools
- **iOS Development**: Xcode 14+
- **Android Development**: Android Studio Flamingo+
- **Testing**: Jest, React Native Testing Library
- **Debugging**: React Native Debugger, Flipper
- **Performance**: React DevTools, Performance Monitor

### Project Structure
```
mobile-app/
├── __tests__/
│   ├── components/
│   ├── screens/
│   └── utils/
├── android/
│   ├── app/
│   ├── gradle/
│   └── build.gradle
├── ios/
│   ├── AIPlatform/
│   ├── AIPlatform.xcodeproj/
│   └── AIPlatform.xcworkspace/
├── src/
│   ├── assets/
│   │   ├── images/
│   │   ├── icons/
│   │   └── fonts/
│   ├── components/
│   │   ├── common/
│   │   ├── dashboard/
│   │   ├── models/
│   │   ├── chat/
│   │   └── settings/
│   ├── screens/
│   │   ├── Auth/
│   │   ├── Dashboard/
│   │   ├── Models/
│   │   ├── Chat/
│   │   ├── Analytics/
│   │   └── Settings/
│   ├── navigation/
│   │   ├── AppNavigator.tsx
│   │   └── AuthNavigator.tsx
│   ├── services/
│   │   ├── api.ts
│   │   ├── auth.ts
│   │   ├── push.ts
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
│   │   └── useModels.ts
│   ├── types/
│   │   └── index.ts
│   ├── theme/
│   │   ├── colors.ts
│   │   ├── typography.ts
│   │   └── spacing.ts
│   ├── config/
│   │   └── environment.ts
│   └── App.tsx
├── app.json
├── babel.config.js
├── metro.config.js
├── tsconfig.json
├── package.json
└── README.md
```

## 2. Core Features

### Authentication System
```typescript
// src/screens/Auth/LoginScreen.tsx
import React, { useState } from 'react';
import {
  View,
  ScrollView,
  StyleSheet,
  Alert,
  KeyboardAvoidingView,
  Platform
} from 'react-native';
import {
  TextInput,
  Button,
  Text,
  ActivityIndicator,
  useTheme
} from 'react-native-paper';
import { useAuth } from '../../hooks/useAuth';
import { useNavigation } from '@react-navigation/native';

const LoginScreen: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigation = useNavigation();
  const theme = useTheme();

  const handleLogin = async () => {
    if (!email || !password) {
      Alert.alert('Error', 'Please fill in all fields');
      return;
    }

    setLoading(true);
    try {
      await login(email, password);
      // Navigation handled by auth state change
    } catch (error: any) {
      Alert.alert('Login Failed', error.message || 'Invalid credentials');
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView contentContainerStyle={styles.scrollContainer}>
        <View style={styles.header}>
          <Text style={styles.title}>AI Platform</Text>
          <Text style={styles.subtitle}>Sign in to your account</Text>
        </View>

        <View style={styles.form}>
          <TextInput
            label="Email"
            value={email}
            onChangeText={setEmail}
            keyboardType="email-address"
            autoCapitalize="none"
            mode="outlined"
            style={styles.input}
          />

          <TextInput
            label="Password"
            value={password}
            onChangeText={setPassword}
            secureTextEntry
            mode="outlined"
            style={styles.input}
          />

          <Button
            mode="contained"
            onPress={handleLogin}
            loading={loading}
            disabled={loading}
            style={styles.button}
          >
            Sign In
          </Button>

          <Button
            mode="text"
            onPress={() => navigation.navigate('Register')}
            style={styles.linkButton}
          >
            Don't have an account? Register
          </Button>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5'
  },
  scrollContainer: {
    flexGrow: 1,
    justifyContent: 'center',
    padding: 20
  },
  header: {
    alignItems: 'center',
    marginBottom: 40
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    marginBottom: 8
  },
  subtitle: {
    fontSize: 16,
    color: '#666'
  },
  form: {
    width: '100%'
  },
  input: {
    marginBottom: 16
  },
  button: {
    marginTop: 16,
    paddingVertical: 8
  },
  linkButton: {
    marginTop: 16
  }
});

export default LoginScreen;
```

### Dashboard Screen
```typescript
// src/screens/Dashboard/DashboardScreen.tsx
import React, { useEffect, useState } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  RefreshControl,
  Alert
} from 'react-native';
import {
  Card,
  Title,
  Paragraph,
  Button,
  ActivityIndicator,
  useTheme
} from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { useModels } from '../../hooks/useModels';
import { useAuth } from '../../hooks/useAuth';

const DashboardScreen: React.FC = () => {
  const [refreshing, setRefreshing] = useState(false);
  const { models, loading, error, fetchModels } = useModels();
  const { user } = useAuth();
  const navigation = useNavigation();
  const theme = useTheme();

  useEffect(() => {
    fetchModels();
  }, []);

  const onRefresh = async () => {
    setRefreshing(true);
    try {
      await fetchModels();
    } catch (err) {
      Alert.alert('Error', 'Failed to refresh data');
    } finally {
      setRefreshing(false);
    }
  };

  if (loading && !refreshing) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" />
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.centerContainer}>
        <Paragraph>Error: {error}</Paragraph>
        <Button onPress={fetchModels}>Retry</Button>
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      <View style={styles.header}>
        <Title>Welcome, {user?.name || 'User'}!</Title>
        <Paragraph>Here's your AI Platform overview</Paragraph>
      </View>

      <View style={styles.statsContainer}>
        <Card style={styles.statCard}>
          <Card.Content>
            <Title>{models.length}</Title>
            <Paragraph>Active Models</Paragraph>
          </Card.Content>
        </Card>

        <Card style={styles.statCard}>
          <Card.Content>
            <Title>0</Title>
            <Paragraph>Running Jobs</Paragraph>
          </Card.Content>
        </Card>
      </View>

      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Title>Your Models</Title>
          <Button
            mode="outlined"
            onPress={() => navigation.navigate('Models')}
            compact
          >
            View All
          </Button>
        </View>

        {models.slice(0, 3).map((model) => (
          <Card key={model.id} style={styles.modelCard}>
            <Card.Content>
              <Title>{model.name}</Title>
              <Paragraph>{model.description}</Paragraph>
            </Card.Content>
            <Card.Actions>
              <Button
                onPress={() => navigation.navigate('ModelDetail', { model })}
              >
                Use Model
              </Button>
            </Card.Actions>
          </Card>
        ))}

        {models.length === 0 && (
          <Card style={styles.emptyCard}>
            <Card.Content>
              <Paragraph>No models available</Paragraph>
              <Button
                mode="contained"
                onPress={() => navigation.navigate('Models')}
                style={styles.createButton}
              >
                Create Your First Model
              </Button>
            </Card.Content>
          </Card>
        )}
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5'
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center'
  },
  header: {
    padding: 20,
    paddingBottom: 10
  },
  statsContainer: {
    flexDirection: 'row',
    padding: 20,
    paddingTop: 0
  },
  statCard: {
    flex: 1,
    marginHorizontal: 5
  },
  section: {
    padding: 20,
    paddingTop: 0
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16
  },
  modelCard: {
    marginBottom: 16
  },
  emptyCard: {
    padding: 20,
    alignItems: 'center'
  },
  createButton: {
    marginTop: 16
  }
});

export default DashboardScreen;
```

### Model Interaction Screen
```typescript
// src/screens/Models/ModelInteractionScreen.tsx
import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  KeyboardAvoidingView,
  Platform
} from 'react-native';
import {
  TextInput,
  Button,
  Card,
  Title,
  Paragraph,
  ActivityIndicator,
  useTheme
} from 'react-native-paper';
import { useModels } from '../../hooks/useModels';

interface ModelInteractionScreenProps {
  route: any;
}

const ModelInteractionScreen: React.FC<ModelInteractionScreenProps> = ({
  route
}) => {
  const { model } = route.params;
  const [input, setInput] = useState('');
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);
  const { runInference } = useModels();
  const theme = useTheme();

  const handleRunInference = async () => {
    if (!input.trim()) {
      return;
    }

    setLoading(true);
    setOutput('');
    try {
      const result = await runInference(model.id, { prompt: input });
      setOutput(result.text || result.output || 'No response');
    } catch (error: any) {
      setOutput(`Error: ${error.message || 'Failed to get response'}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView style={styles.scrollContainer}>
        <Card style={styles.modelInfo}>
          <Card.Content>
            <Title>{model.name}</Title>
            <Paragraph>{model.description}</Paragraph>
          </Card.Content>
        </Card>

        <View style={styles.inputContainer}>
          <TextInput
            label="Enter your prompt"
            value={input}
            onChangeText={setInput}
            multiline
            numberOfLines={4}
            mode="outlined"
            style={styles.input}
          />

          <Button
            mode="contained"
            onPress={handleRunInference}
            loading={loading}
            disabled={loading || !input.trim()}
            style={styles.runButton}
          >
            Run Inference
          </Button>
        </View>

        {output ? (
          <Card style={styles.outputCard}>
            <Card.Content>
              <Title>Response</Title>
              <Paragraph style={styles.outputText}>{output}</Paragraph>
            </Card.Content>
          </Card>
        ) : loading ? (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" />
            <Paragraph style={styles.loadingText}>Processing...</Paragraph>
          </View>
        ) : null}
      </ScrollView>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5'
  },
  scrollContainer: {
    flex: 1,
    padding: 20
  },
  modelInfo: {
    marginBottom: 20
  },
  inputContainer: {
    marginBottom: 20
  },
  input: {
    marginBottom: 16
  },
  runButton: {
    paddingVertical: 8
  },
  outputCard: {
    marginTop: 20
  },
  outputText: {
    fontSize: 16,
    lineHeight: 24
  },
  loadingContainer: {
    alignItems: 'center',
    marginTop: 40
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16
  }
});

export default ModelInteractionScreen;
```

## 3. API Integration

### API Service Layer
```typescript
// src/services/api.ts
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_BASE_URL = 'https://api.aiplatform.io';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      await AsyncStorage.removeItem('authToken');
      // Navigation to login would be handled by auth context
    }
    return Promise.reject(error);
  }
);

export default api;
```

### Authentication Service
```typescript
// src/services/auth.ts
import api from './api';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface LoginData {
  email: string;
  password: string;
}

interface RegisterData {
  email: string;
  password: string;
  name: string;
}

export const authService = {
  async login(data: LoginData) {
    try {
      const response = await api.post('/auth/login', data);
      const { token, user } = response.data;
      
      // Store token securely
      await AsyncStorage.setItem('authToken', token);
      await AsyncStorage.setItem('userData', JSON.stringify(user));
      
      return { token, user };
    } catch (error) {
      throw new Error('Invalid credentials');
    }
  },

  async register(data: RegisterData) {
    try {
      const response = await api.post('/auth/register', data);
      const { token, user } = response.data;
      
      // Store token securely
      await AsyncStorage.setItem('authToken', token);
      await AsyncStorage.setItem('userData', JSON.stringify(user));
      
      return { token, user };
    } catch (error) {
      throw new Error('Registration failed');
    }
  },

  async logout() {
    try {
      await api.post('/auth/logout');
    } catch (error) {
      // Ignore logout errors
    } finally {
      // Clear local storage
      await AsyncStorage.removeItem('authToken');
      await AsyncStorage.removeItem('userData');
    }
  },

  async getCurrentUser() {
    try {
      const userData = await AsyncStorage.getItem('userData');
      return userData ? JSON.parse(userData) : null;
    } catch (error) {
      return null;
    }
  },

  async isAuthenticated() {
    const token = await AsyncStorage.getItem('authToken');
    return !!token;
  }
};
```

## 4. Navigation Setup

### Main Navigator
```typescript
// src/navigation/AppNavigator.tsx
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import { useTheme } from 'react-native-paper';
import Icon from 'react-native-vector-icons/MaterialIcons';

// Screens
import DashboardScreen from '../screens/Dashboard/DashboardScreen';
import ModelsScreen from '../screens/Models/ModelsScreen';
import ModelInteractionScreen from '../screens/Models/ModelInteractionScreen';
import AnalyticsScreen from '../screens/Analytics/AnalyticsScreen';
import SettingsScreen from '../screens/Settings/SettingsScreen';

// Auth Navigator
import AuthNavigator from './AuthNavigator';

// Hooks
import { useAuth } from '../hooks/useAuth';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

const MainTabs: React.FC = () => {
  const theme = useTheme();

  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName = '';

          if (route.name === 'Dashboard') {
            iconName = focused ? 'dashboard' : 'dashboard';
          } else if (route.name === 'Models') {
            iconName = focused ? 'psychology' : 'psychology';
          } else if (route.name === 'Analytics') {
            iconName = focused ? 'analytics' : 'analytics';
          } else if (route.name === 'Settings') {
            iconName = focused ? 'settings' : 'settings';
          }

          return <Icon name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: theme.colors.primary,
        tabBarInactiveTintColor: 'gray',
        headerShown: false
      })}
    >
      <Tab.Screen name="Dashboard" component={DashboardScreen} />
      <Tab.Screen name="Models" component={ModelsScreen} />
      <Tab.Screen name="Analytics" component={AnalyticsScreen} />
      <Tab.Screen name="Settings" component={SettingsScreen} />
    </Tab.Navigator>
  );
};

const AppNavigator: React.FC = () => {
  const { isAuthenticated, isLoading } = useAuth();
  const theme = useTheme();

  if (isLoading) {
    return null; // Show splash screen
  }

  return (
    <NavigationContainer theme={theme}>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {isAuthenticated ? (
          <>
            <Stack.Screen name="MainTabs" component={MainTabs} />
            <Stack.Screen
              name="ModelDetail"
              component={ModelInteractionScreen}
              options={{ headerShown: true, title: 'Model Interaction' }}
            />
          </>
        ) : (
          <Stack.Screen name="Auth" component={AuthNavigator} />
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default AppNavigator;
```

## 5. Push Notifications

### Push Notification Service
```typescript
// src/services/push.ts
import messaging from '@react-native-firebase/messaging';
import { Platform } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

export const pushService = {
  async requestPermission() {
    const authStatus = await messaging().requestPermission();
    const enabled =
      authStatus === messaging.AuthorizationStatus.AUTHORIZED ||
      authStatus === messaging.AuthorizationStatus.PROVISIONAL;

    if (enabled) {
      console.log('Authorization status:', authStatus);
      return true;
    }
    return false;
  },

  async getFcmToken() {
    try {
      const fcmToken = await messaging().getToken();
      if (fcmToken) {
        console.log('Your Firebase Token is:', fcmToken);
        await AsyncStorage.setItem('fcmToken', fcmToken);
        return fcmToken;
      }
      console.log('Failed to get FCM token');
      return null;
    } catch (error) {
      console.log('Error getting FCM token:', error);
      return null;
    }
  },

  async onMessageReceived() {
    // Handle foreground messages
    messaging().onMessage(async (remoteMessage) => {
      console.log('A new FCM message arrived!', remoteMessage);
      // Show local notification or update UI
    });

    // Handle background messages
    messaging().setBackgroundMessageHandler(async (remoteMessage) => {
      console.log('Message handled in the background!', remoteMessage);
      // Process background message
    });
  },

  async subscribeToTopic(topic: string) {
    try {
      await messaging().subscribeToTopic(topic);
      console.log(`Subscribed to topic: ${topic}`);
    } catch (error) {
      console.log('Error subscribing to topic:', error);
    }
  }
};
```

## 6. Analytics Integration

### Analytics Service
```typescript
// src/services/analytics.ts
import analytics from '@react-native-firebase/analytics';
import crashlytics from '@react-native-firebase/crashlytics';

export const analyticsService = {
  async logEvent(eventName: string, params?: any) {
    try {
      await analytics().logEvent(eventName, params);
    } catch (error) {
      console.log('Analytics error:', error);
    }
  },

  async setUserProperties(properties: any) {
    try {
      await analytics().setUserProperties(properties);
    } catch (error) {
      console.log('Analytics error:', error);
    }
  },

  async setCurrentScreen(screenName: string) {
    try {
      await analytics().logScreenView({
        screen_name: screenName,
        screen_class: screenName
      });
    } catch (error) {
      console.log('Analytics error:', error);
    }
  },

  async logError(error: Error) {
    try {
      await crashlytics().recordError(error);
    } catch (err) {
      console.log('Crashlytics error:', err);
    }
  },

  async setUserId(userId: string) {
    try {
      await analytics().setUserId(userId);
      await crashlytics().setUserId(userId);
    } catch (error) {
      console.log('Analytics error:', error);
    }
  }
};
```

## 7. Performance Optimization

### Image Optimization
```typescript
// src/components/common/OptimizedImage.tsx
import React from 'react';
import { Image, StyleSheet } from 'react-native';
import FastImage from 'react-native-fast-image';

interface OptimizedImageProps {
  uri: string;
  style?: any;
  resizeMode?: 'cover' | 'contain' | 'stretch' | 'repeat' | 'center';
}

const OptimizedImage: React.FC<OptimizedImageProps> = ({
  uri,
  style,
  resizeMode = 'cover'
}) => {
  return (
    <FastImage
      style={[styles.image, style]}
      source={{
        uri,
        priority: FastImage.priority.normal,
      }}
      resizeMode={FastImage.resizeMode[resizeMode]}
    />
  );
};

const styles = StyleSheet.create({
  image: {
    width: '100%',
    height: 200
  }
});

export default OptimizedImage;
```

### List Optimization
```typescript
// src/components/common/OptimizedFlatList.tsx
import React from 'react';
import { FlatList, RefreshControl } from 'react-native';

interface OptimizedFlatListProps {
  data: any[];
  renderItem: ({ item }: { item: any }) => React.ReactElement;
  keyExtractor: (item: any) => string;
  onRefresh?: () => void;
  refreshing?: boolean;
  [key: string]: any;
}

const OptimizedFlatList: React.FC<OptimizedFlatListProps> = ({
  data,
  renderItem,
  keyExtractor,
  onRefresh,
  refreshing,
  ...props
}) => {
  return (
    <FlatList
      data={data}
      renderItem={renderItem}
      keyExtractor={keyExtractor}
      refreshControl={
        onRefresh ? (
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        ) : undefined
      }
      showsVerticalScrollIndicator={false}
      windowSize={11}
      maxToRenderPerBatch={10}
      updateCellsBatchingPeriod={50}
      initialNumToRender={10}
      removeClippedSubviews={true}
      {...props}
    />
  );
};

export default OptimizedFlatList;
```

## 8. Testing Strategy

### Unit Tests
```typescript
// __tests__/services/auth.test.ts
import { authService } from '../../src/services/auth';
import AsyncStorage from '@react-native-async-storage/async-storage';
import api from '../../src/services/api';

// Mock AsyncStorage
jest.mock('@react-native-async-storage/async-storage', () => ({
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn()
}));

// Mock API
jest.mock('../../src/services/api');

describe('authService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('login', () => {
    it('should store token and user data on successful login', async () => {
      const mockResponse = {
        data: {
          token: 'test-token',
          user: { id: '1', email: 'test@example.com' }
        }
      };
      
      (api.post as jest.Mock).mockResolvedValue(mockResponse);

      const result = await authService.login({
        email: 'test@example.com',
        password: 'password123'
      });

      expect(result).toEqual(mockResponse.data);
      expect(AsyncStorage.setItem).toHaveBeenCalledWith(
        'authToken',
        'test-token'
      );
      expect(AsyncStorage.setItem).toHaveBeenCalledWith(
        'userData',
        JSON.stringify({ id: '1', email: 'test@example.com' })
      );
    });

    it('should throw error on failed login', async () => {
      (api.post as jest.Mock).mockRejectedValue(new Error('Network error'));

      await expect(
        authService.login({
          email: 'test@example.com',
          password: 'wrongpassword'
        })
      ).rejects.toThrow('Invalid credentials');
    });
  });

  describe('logout', () => {
    it('should clear auth data on logout', async () => {
      await authService.logout();

      expect(AsyncStorage.removeItem).toHaveBeenCalledWith('authToken');
      expect(AsyncStorage.removeItem).toHaveBeenCalledWith('userData');
    });
  });
});
```

## 9. Deployment Configuration

### Environment Configuration
```typescript
// src/config/environment.ts
interface EnvironmentConfig {
  apiUrl: string;
  appName: string;
  version: string;
  features: {
    analytics: boolean;
    pushNotifications: boolean;
    offlineMode: boolean;
  };
}

const getEnvironmentConfig = (): EnvironmentConfig => {
  const env = process.env.NODE_ENV || 'development';
  
  const configs: Record<string, EnvironmentConfig> = {
    development: {
      apiUrl: 'http://localhost:8000/api',
      appName: 'AI Platform Dev',
      version: '1.0.0-dev',
      features: {
        analytics: false,
        pushNotifications: false,
        offlineMode: false
      }
    },
    staging: {
      apiUrl: 'https://staging.api.aiplatform.io/api',
      appName: 'AI Platform Staging',
      version: '1.0.0-staging',
      features: {
        analytics: true,
        pushNotifications: true,
        offlineMode: true
      }
    },
    production: {
      apiUrl: 'https://api.aiplatform.io/api',
      appName: 'AI Platform',
      version: '1.0.0',
      features: {
        analytics: true,
        pushNotifications: true,
        offlineMode: true
      }
    }
  };

  return configs[env] || configs.development;
};

export default getEnvironmentConfig();
```

### Build Scripts
```json
// package.json scripts
{
  "scripts": {
    "start": "react-native start",
    "android": "react-native run-android",
    "ios": "react-native run-ios",
    "test": "jest",
    "lint": "eslint . --ext .js,.jsx,.ts,.tsx",
    "build:android": "cd android && ./gradlew assembleRelease",
    "build:ios": "cd ios && xcodebuild -workspace AIPlatform.xcworkspace -scheme AIPlatform -configuration Release -destination generic/platform=iOS -archivePath AIPlatform.xcarchive archive",
    "deploy:android": "cd android && fastlane deploy",
    "deploy:ios": "cd ios && fastlane deploy"
  }
}
```

## 10. App Store Configuration

### iOS App Store Configuration
```xml
<!-- ios/Info.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>CFBundleDevelopmentRegion</key>
	<string>en</string>
	<key>CFBundleDisplayName</key>
	<string>AI Platform</string>
	<key>CFBundleExecutable</key>
	<string>$(EXECUTABLE_NAME)</string>
	<key>CFBundleIdentifier</key>
	<string>$(PRODUCT_BUNDLE_IDENTIFIER)</string>
	<key>CFBundleInfoDictionaryVersion</key>
	<string>6.0</string>
	<key>CFBundleName</key>
	<string>$(PRODUCT_NAME)</string>
	<key>CFBundlePackageType</key>
	<string>APPL</string>
	<key>CFBundleShortVersionString</key>
	<string>1.0</string>
	<key>CFBundleSignature</key>
	<string>????</string>
	<key>CFBundleVersion</key>
	<string>1</string>
	<key>LSRequiresIPhoneOS</key>
	<true/>
	<key>NSAppTransportSecurity</key>
	<dict>
		<key>NSExceptionDomains</key>
		<dict>
			<key>localhost</key>
			<dict>
				<key>NSExceptionAllowsInsecureHTTPLoads</key>
				<true/>
			</dict>
		</dict>
	</dict>
	<key>NSLocationWhenInUseUsageDescription</key>
	<string></string>
	<key>UILaunchStoryboardName</key>
	<string>LaunchScreen</string>
	<key>UIRequiredDeviceCapabilities</key>
	<array>
		<string>armv7</string>
	</array>
	<key>UISupportedInterfaceOrientations</key>
	<array>
		<string>UIInterfaceOrientationPortrait</string>
		<string>UIInterfaceOrientationLandscapeLeft</string>
		<string>UIInterfaceOrientationLandscapeRight</string>
	</array>
	<key>UIViewControllerBasedStatusBarAppearance</key>
	<false/>
</dict>
</plist>
```

### Android App Store Configuration
```xml
<!-- android/app/src/main/AndroidManifest.xml -->
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

    <application
      android:name=".MainApplication"
      android:label="@string/app_name"
      android:icon="@mipmap/ic_launcher"
      android:roundIcon="@mipmap/ic_launcher_round"
      android:allowBackup="false"
      android:theme="@style/AppTheme">
      <activity
        android:name=".MainActivity"
        android:label="@string/app_name"
        android:configChanges="keyboard|keyboardHidden|orientation|screenLayout|screenSize|smallestScreenSize|uiMode"
        android:launchMode="singleTask"
        android:windowSoftInputMode="adjustResize"
        android:exported="true">
        <intent-filter>
            <action android:name="android.intent.action.MAIN" />
            <category android:name="android.intent.category.LAUNCHER" />
        </intent-filter>
      </activity>
    </application>
</manifest>
```

## Conclusion

This mobile app setup provides a comprehensive foundation for the AI Platform mobile application using React Native. The implementation includes:

1. **Cross-platform compatibility** for iOS and Android
2. **Modern architecture** with proper separation of concerns
3. **Robust authentication** and state management
4. **Performance optimization** techniques
5. **Comprehensive testing** strategy
6. **Analytics and crash reporting** integration
7. **Push notification** support
8. **Proper deployment** configurations

The app is designed to be scalable, maintainable, and user-friendly while providing access to all core AI Platform features on mobile devices.

**Mobile App Version**: 1.0
**Last Updated**: December 28, 2025
**Next Review**: March 28, 2026