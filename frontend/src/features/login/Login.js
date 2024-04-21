import React, { useState } from 'react';
import { TextField, Button, Typography, Card, CardContent, Grid, Snackbar } from '@mui/material';
import { useDispatch } from 'react-redux';
import { login } from './loginSlice';
import { useNavigate } from 'react-router-dom';
import './Gradient.css';

const Login = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleCloseSnackbar = () => {
    setOpenSnackbar(false);
  };

  const handleSubmit = async () => {
    try {
      await dispatch(login(formData));
      navigate('/');
    } catch (e) {
      setError(e.message);
      setOpenSnackbar(true);
    }
  };

  return (
    <div className='animated-background' style={{
      background: 'linear-gradient(to bottom, #dc3416, #ffffff)',
      minHeight: '100vh',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
    }}>
      <Grid container direction="column" justifyContent="center" alignItems="center">
        <Grid item>
          <Typography variant="h3" style={{ marginBottom: "20px", fontWeight: "bold", color: "#ffffff" }} gutterBottom>
            Login
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
              <Button onClick={handleSubmit} variant="contained" fullWidth style={{ backgroundColor: '#dc3416', color: '#ffffff', marginTop: '20px' }}>
                Login
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      <Snackbar
        open={openSnackbar}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        message={error}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
        sx={{ backgroundColor: '#ff0000' }} // Change snackBar background color to red
      />
    </div>
  );
};

export default Login;
