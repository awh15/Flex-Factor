import React, { useState } from 'react';
import { Card, Container, Box, CardContent, TextField, Button, Typography, Snackbar } from '@mui/material';
import { addProduct } from './dashboardSlice';
import { useDispatch } from "react-redux";

const AddProductForm = ({ token }) => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    price: '',
    stock: '',
    category: '',
    image: '',
  });

  const dispatch = useDispatch();
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await dispatch(addProduct({ token, productData: formData }));
      // Dispatch action to post the product data
      // Reset form data after submission
      setFormData({
        name: '',
        description: '',
        price: '',
        stock: '',
        category: '',
        image: '',
      });
    } catch (error) {
      setSnackbarMessage(error.message || 'An error occurred');
      setSnackbarOpen(true);
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbarOpen(false);
  };
  

  return (
    <Container style={{ marginTop: '150px', display: 'flex', justifyContent: 'center' }}>
    <Box width="80%" style={{paddingBottom: "20px"}}> 
    <Typography variant="h3" style={{ fontWeight: "bold" }} gutterBottom>
         Publish a new product
    </Typography>
    <Card style = {{display: "flex"}}>
      <CardContent>
        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            name="name"
            label="Name"
            value={formData.name}
            onChange={handleChange}
            margin="normal"
          />
          <TextField
            fullWidth
            name="description"
            label="Description"
            value={formData.description}
            onChange={handleChange}
            margin="normal"
          />
          <TextField
            fullWidth
            name="price"
            label="Price"
            value={formData.price}
            onChange={handleChange}
            margin="normal"
          />
          <TextField
            fullWidth
            name="stock"
            label="Stock"
            value={formData.stock}
            onChange={handleChange}
            margin="normal"
          />
          <TextField
            fullWidth
            name="category"
            label="Category"
            value={formData.category}
            onChange={handleChange}
            margin="normal"
          />
          <TextField
            fullWidth
            name="image"
            label="Image URL"
            value={formData.image}
            onChange={handleChange}
            margin="normal"
          />
          <Button variant="contained" type="submit" color="primary"  fullWidth style={{ backgroundColor: '#dc3416', color: '#ffffff', marginTop: '20px' }}>
            Submit
          </Button>
        </form>
      </CardContent>
    </Card> 
    </Box>
    <Snackbar
        open={snackbarOpen}
        autoHideDuration={1000}
        onClose={handleCloseSnackbar}
        message={snackbarMessage}/>
    </Container>
  );
};

export default AddProductForm;
