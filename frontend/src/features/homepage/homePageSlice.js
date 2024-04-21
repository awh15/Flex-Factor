import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';
import { PRODUCT_BASE_URL } from '../../constants/Constants';

// Define an async thunk to fetch all products
export const fetchAllProducts = createAsyncThunk(
  'homePage/fetchAllProducts',
  async () => {
    try {
      const response = await axios.get(`${PRODUCT_BASE_URL}fetchAllProducts`);
      return response.data;
    } catch (error) {
      throw error;
    }
  }
);

// Define the initial state for the homePageSlice
const initialState = {
  productsList: [],
  cartItems: [],
  wishlistItems: [],
  status: 'idle', // Add status field for tracking loading state
};

// Define the homePageSlice
const homePageSlice = createSlice({
  name: 'homePage',
  initialState,
  reducers: {
    // Add product to cart
    addToCart(state, action) {
      state.cartItems.push(action.payload);
    },
    // Remove product from cart
    removeFromCart(state, action) {
      state.cartItems = state.cartItems.filter(
        (item) => item.product_id !== action.payload.product_id
      );
    },
    // Add product to wishlist
    addToWishlist(state, action) {
      state.wishlistItems.push(action.payload);
    },
    // Remove product from wishlist
    removeFromWishlist(state, action) {
      state.wishlistItems = state.wishlistItems.filter(
        (item) => item.product_id !== action.payload.product_id
      );
    },
  },
  extraReducers: (builder) => {
    builder
      // Handle the pending state while fetching products
      .addCase(fetchAllProducts.pending, (state) => {
        state.status = 'loading';
      })
      // Handle the fulfilled state after fetching products
      .addCase(fetchAllProducts.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.productsList = action.payload;
      });
  },
});

// Export actions and reducer
export const {
  addToCart,
  removeFromCart,
  addToWishlist,
  removeFromWishlist,
} = homePageSlice.actions;
export default homePageSlice.reducer;
