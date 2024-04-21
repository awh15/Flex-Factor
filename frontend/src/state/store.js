// Import configureStore from @reduxjs/toolkit for creating a Redux store
import { configureStore } from '@reduxjs/toolkit';
import homePageSlice from '../features/homepage/homePageSlice';
import signupSlice from '../features/signup/signupSlice';
import loginSlice from '../features/login/loginSlice';
import dashboardSlice from '../features/dashboard/dashboardSlice';

// Configure the Redux store
const store = configureStore({
  // Combine reducers from feature slices
  reducer: { 
    homePage: homePageSlice,
    signup: signupSlice,
    login: loginSlice,
    dashboard: dashboardSlice,
  },
  // Enable Redux DevTools Extension for debugging (optional)
  devTools: true,
});

// Export the configured store
export default store;
