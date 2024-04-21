// Import configureStore from @reduxjs/toolkit for creating a Redux store
import { configureStore } from '@reduxjs/toolkit';
 


// Configure the Redux store
const store = configureStore({
  // Combine reducers from feature slices
  reducer: { 
  },
  // Enable Redux DevTools Extension for debugging (optional)
  devTools: true,
});

// Export the configured store
export default store;
