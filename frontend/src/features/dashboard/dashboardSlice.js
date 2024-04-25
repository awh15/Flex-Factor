import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';
import { PRODUCT_BASE_URL } from '../../constants/Constants';
 
export const addFaq = createAsyncThunk(
  'dashboard/addFaq',
  async({faqData, token}, thunkAPI)=>{
    try {
      const response = await axios.post(PRODUCT_BASE_URL + 'faq', faqData, {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });
      console.log(response);
      return response.data;
    } catch (error) {
      throw new Error(error.response ? error.response.data : "An unexpected error occurred while adding faq!");
    }
  }
);

export const getProducts = createAsyncThunk(
  'dashboard/getProducts', 
  async (token, thunkAPI) => {
    try {
      const response = await axios.get(PRODUCT_BASE_URL + 'list', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response ? error.response.data : "An unexpected error occurred while fetching your products");
    }
  }
);

export const addProduct = createAsyncThunk(
  'dashboard/addProduct',
  async ({ productData, token }, thunkAPI) => {
    try {
      const response = await axios.post(PRODUCT_BASE_URL + 'add', productData, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response ? error.response.data : "An unexpected error occurred while adding a product");
    }
  }
);

export const deleteProduct = createAsyncThunk(
  'dashboard/deleteProduct',
  async ({ productData, token }, thunkAPI) => {
    
    try { 
      const response = await axios.post(PRODUCT_BASE_URL + 'delete', productData, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      await thunkAPI.dispatch(getProducts(token));
      return response.data;
    } catch (error) {
      throw new Error(error.response ? error.response.data : "An unexpected error occurred while deleting a product");
    }
  }
);

const dashboardSlice = createSlice({
  name: 'dashboard',
  initialState: {
    vendorProductList: [],
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(getProducts.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(getProducts.fulfilled, (state, action) => {
        state.loading = false;
        state.vendorProductList = action.payload;
      })
      .addCase(getProducts.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(addProduct.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(addProduct.fulfilled, (state, action) => {
        state.loading = false;
        state.vendorProductList.push(action.payload); // Assuming the server returns the added product
      })
      .addCase(addProduct.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(deleteProduct.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteProduct.fulfilled, (state, action) => {
        state.loading = false;  
      })
      .addCase(deleteProduct.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export default dashboardSlice.reducer;
