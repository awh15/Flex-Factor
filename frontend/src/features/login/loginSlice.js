import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';
import { USER_BASE_URL} from '../../constants/Constants';


// Async thunk to handle logging in
export const login = createAsyncThunk(
  'login/login',
  async (credentials, { dispatch }) => {
    try {
      const response = await axios.post(`${USER_BASE_URL}/login`, credentials);
      dispatch(getRole()); // Dispatch getRole thunk after successful login
      return response.data; // Assuming the backend sends back the user data including token
    } catch (error) {
      if (error.response && error.response.data && error.response.data.Message) {
        const errorMessage = error.response.data.Message;  // Dispatch action with error message
        throw new Error(errorMessage);
      } else {
        throw new Error("An unexpected error occurred");
      }
    }
  }
);

// Async thunk to check authentication status and fetch user data
export const getAuth = createAsyncThunk(
  'login/getAuth',
  async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      return null;
    } 
    return token;
  }
);

// Async thunk to fetch user role
export const getRole = createAsyncThunk(
  'login/getRole',
  async (_, { getState }) => {
    const token = getState().login.token;
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      }
    };
    const response = await axios.get(`${USER_BASE_URL}/get_role`, config);
    return response.data.role; // Assuming the response contains the user's role
  }
);


// Slice
const loginSlice = createSlice({
  name: 'login',
  initialState: {
    token: localStorage.getItem('token') || null,
    role: null,
    isAuthenticated: !!localStorage.getItem('token'), // Set isAuthenticated based on whether token exists
    user: null,
    loading: false,
    error: null,
  },
  reducers: {
    logout: (state) => {
      state.user = null;
      state.token = null; // Clear token from state
      localStorage.removeItem('token'); // Remove token from local storage
      state.isAuthenticated = false; // Set isAuthenticated to false
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action) => {
        state.loading = false;
        state.user = action.payload;
        state.token = action.payload.token; // Set token in state
        state.error = null;
        localStorage.setItem('token', action.payload.token); // Store token in local storage
        state.isAuthenticated = true; // Set isAuthenticated to true
      })
      .addCase(login.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload ? action.payload.message : 'Login failed';
        state.isAuthenticated = false; // Set isAuthenticated to false
      })
      .addCase(getAuth.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(getAuth.fulfilled, (state, action) => {
        state.loading = false;
        state.user = action.payload;
        state.error = null;
        state.isAuthenticated = true; // Set isAuthenticated to true
      })
      .addCase(getAuth.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload ? action.payload.message : 'Authentication failed';
        state.isAuthenticated = false; // Set isAuthenticated to false
      })
      .addCase(getRole.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(getRole.fulfilled, (state, action) => {
        state.loading = false;
        state.role = action.payload; // Set role in state
      })
      .addCase(getRole.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload ? action.payload.message : 'Failed to fetch role';
      });
      ;
  },
});

export const { logout } = loginSlice.actions;

export default loginSlice.reducer;
