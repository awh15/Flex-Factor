import { createSlice } from '@reduxjs/toolkit';
import axios from 'axios';
import {USER_BASE_URL} from "../../constants/Constants";


export const signupSlice = createSlice({
  name: 'signup',
  initialState: {
    loading: false,
    error: null,
    success: false,
  },
  reducers: {
    signupRequest: (state) => {
      state.loading = true;
      state.error = null;
      state.success = false;
    },
    signupSuccess: (state) => {
      state.loading = false;
      state.success = true;
    },
    signupFailure: (state, action) => {
      state.loading = false;
      state.error = action.payload;
    },
  },
});

export const { signupRequest, signupSuccess, signupFailure } = signupSlice.actions;

export const registerUser = (userData) => async (dispatch) => {
  try {
    dispatch(signupRequest());
    await axios.post(`${USER_BASE_URL}register`, userData);
    dispatch(signupSuccess());
    // Optionally, you can dispatch some action after successful registration
  } catch (error) { 
    if (error.response && error.response.data && error.response.data.Message) {
      const errorMessage = error.response.data.Message;  // Dispatch action with error message
      throw new Error(errorMessage); // Throw the error to be caught by the component
    } else {  // Dispatch generic error message
      throw new Error('An unexpected error occurred');
    }
  }
};

export default signupSlice.reducer;
