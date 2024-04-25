import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';
import { PRODUCT_BASE_URL } from "../../constants/Constants"; 

export const fetchProduct = createAsyncThunk(
  'productPage/fetchProduct',
  async (productId, thunkAPI) => {
    const response = await axios.get(`${PRODUCT_BASE_URL}product/${productId}`);
    await thunkAPI.dispatch(fetchFAQs(productId));
    return response.data;
  }
);

export const fetchFAQs = createAsyncThunk(
  'productPage/fetchFAQs',
  async (productId) => {
    const response = await axios.get(`${PRODUCT_BASE_URL}faq/${productId}`);
    return response.data;
  }
);

const productPageSlice = createSlice({
  name: 'productPage',
  initialState: {
    product: null,
    faqList: [],
    status: 'idle',
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchProduct.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchProduct.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.product = action.payload;
      })
      .addCase(fetchProduct.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
      })
      .addCase(fetchFAQs.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchFAQs.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.faqList = action.payload;
      })
      .addCase(fetchFAQs.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
      });
  },
});

export default productPageSlice.reducer;
