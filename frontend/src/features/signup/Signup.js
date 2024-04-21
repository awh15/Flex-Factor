import React, { useState } from 'react';
import { TextField, Typography, Button, Select, MenuItem, FormControl, InputLabel, Card, CardContent, Grid, Snackbar } from '@mui/material';
import { useDispatch } from 'react-redux';
import { registerUser } from './signupSlice';
import { useNavigate } from 'react-router-dom';

const Signup = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    password: '',    
    role: '',
    email: '',
    full_name: '',
    address: '',
    phone_number: '', 
  });

  const [error, setError] = useState('');
  const [openSnackbar, setOpenSnackbar] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleCloseSnackbar = () => {
    setOpenSnackbar(false);
  };

  const handleSubmit = async () => {
    try {
      await dispatch(registerUser(formData));
      navigate('/login');
    } catch (error) {
      setError(error.message);
      setOpenSnackbar(true);
    }
  };

  return (
    <div className='animated-background' style={{ 
      background: 'linear-gradient(to bottom, #dc3416, #ffffff)', /* Gradient from #ff7e5f to #feb47b */
      minHeight: '100vh', /* Ensures the gradient covers the full height of the viewport */
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
    }}>
      <Grid container direction="column" justifyContent="center" alignItems="center">
        <Grid item>
          <Typography variant="h3" style={{ marginBottom: "20px", fontWeight: "bold", color: "#ffffff" }} gutterBottom>
            Signup
          </Typography>
        </Grid>
        <Grid item>
          <Card style={{ maxWidth: "500px" }}>
            <CardContent>
            <TextField
              name="username"
              label="Username"
              value={formData.username}
              onChange={handleChange}
              fullWidth
              margin="normal"
            />
            <TextField
              name="password"
              label="Password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              fullWidth
              margin="normal"
            />
            <TextField
              name="email"
              label="Email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              fullWidth
              margin="normal"
            />
            <FormControl fullWidth margin="normal">
              <InputLabel>Role</InputLabel>
              <Select
                name="role"
                value={formData.role}
                onChange={handleChange}
              >
                <MenuItem value="Vendor">Vendor</MenuItem>
                <MenuItem value="End User">End User</MenuItem>
                <MenuItem value="Admin">Admin</MenuItem>
              </Select>
            </FormControl>
            <TextField
              name="full_name"
              label="Full Name"
              value={formData.full_name}
              onChange={handleChange}
              fullWidth
              margin="normal"
            />
            <TextField
              name="phone_number"
              label="Phone Number"
              value={formData.phone_number}
              onChange={handleChange}
              fullWidth
              margin="normal"
            />
            <TextField
              name="address"
              label="Address" // Label for address input
              value={formData.address}
              onChange={handleChange}
              fullWidth
              margin="normal"
            />
            <Button onClick={handleSubmit} variant="contained" fullWidth style={{ backgroundColor: '#dc3416', color: '#ffffff' }}>
              Signup
            </Button>
            <Snackbar
              open={openSnackbar}
              autoHideDuration={1000}
              onClose={handleCloseSnackbar}
              message={error}
              anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
              sx={{ backgroundColor: 'ff0000' }} // Change snackBar background color to red
            />
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </div>
  );
};

export default Signup;
