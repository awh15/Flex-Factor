import React, { useState, useEffect } from 'react';
import { Card, Grid, Box, Container, CardMedia, CardContent, Typography, CircularProgress, Button, Dialog, DialogTitle, DialogContent, DialogActions, TextField } from '@mui/material';
import { useSelector, useDispatch } from 'react-redux';
import { getProducts, deleteProduct, addFaq } from './dashboardSlice';

const VendorProducts = ({ token }) => {
  const dispatch = useDispatch();
  const { vendorProductList, loading, error } = useSelector(state => state.dashboard);
  const [selectedProductId, setSelectedProductId] = useState(null);
  const [openDeleteDialog, setOpenDeleteDialog] = useState(false);
  const [openFaqDialog, setOpenFaqDialog] = useState(false);
  const [faqQuestion, setFaqQuestion] = useState('');
  const [faqAnswer, setFaqAnswer] = useState('');

  useEffect(() => {
    dispatch(getProducts(token));
  }, [dispatch, token]);

  const handleDeleteClick = (productId) => { 
    setSelectedProductId(productId);
    setOpenDeleteDialog(true);
  };

  const handleDeleteConfirm = () => {
    dispatch(deleteProduct({ token, productData: { product_id : selectedProductId } }));
    setOpenDeleteDialog(false);
  };

  const handleDeleteCancel = () => {
    setSelectedProductId(null);
    setOpenDeleteDialog(false);
  };

  const handleAddFaq = (productId) => {
    setSelectedProductId(productId);
    setOpenFaqDialog(true);
  };

  const handleAddFaqSubmit = () => {
    dispatch(addFaq( {token, faqData: {question: faqQuestion, answer: faqAnswer, product_id: selectedProductId}} ));
    setOpenFaqDialog(false);
    setFaqQuestion('');
    setFaqAnswer('');
  };

  return (
    <Container style={{ marginTop: '40px', display: 'flex', justifyContent: 'center' }}>
      <Box width="80%" style={{paddingBottom: "20px"}}>
        <Typography variant="h3" style={{ marginTop: "20px", marginBottom: "40px", fontWeight: "bold" }} gutterBottom>
          My Products
        </Typography>
        {loading ? (
          <CircularProgress />
        ) : error ? (
          <Typography variant="body1" color="error">
            {error}
          </Typography>
        ) : (
          <Grid container spacing={3}>
            {vendorProductList.map((product) => (
              <Grid item xs={12} sm={6} md={4} key={product.product_id}>
                <Card style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
                  <Button onClick={() => handleDeleteClick(product.product_id)} style={{ alignSelf: 'flex-end', margin: '5px' }}>X</Button>
                  <CardMedia
                    component="img"
                    className="card-media"
                    image={product.image_url}
                    alt={product.name}
                  />
                  <CardContent style={{display: 'flex', flexDirection: 'column', justifyContent: 'space-between', flexGrow: 1 }}>
                    <div>
                      <Typography gutterBottom variant="h5" style={{ fontWeight: "bold" }} component="div">
                        {product.name}
                      </Typography>
                    </div>
                    <div style={{marginTop: "auto" }}>
                      <Typography variant="body2" color="text.secondary" className="description">
                        {product.description}
                      </Typography>
                      <Typography variant="body1">${product.price}</Typography>
                      <Button fullWidth  style={{ backgroundColor: '#dc3416', color: '#ffffff', marginTop: '5px' }} onClick={() => handleAddFaq(product.product_id)}>Edit FAQ</Button>
                    </div>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        )}
      </Box> 

      {/* Delete confirmation dialog */}
      <Dialog open={openDeleteDialog} onClose={handleDeleteCancel}>
        <DialogTitle>Are you sure you want to delete this product?</DialogTitle>
        <DialogActions>
          <Button onClick={handleDeleteCancel} color="primary">Cancel</Button>
          <Button onClick={handleDeleteConfirm} color="primary">Delete</Button>
        </DialogActions>
      </Dialog>

      {/* FAQ dialog */}
      <Dialog open={openFaqDialog} onClose={() => setOpenFaqDialog(false)}>
        <DialogTitle>Add a frequently asked question and answer</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            id="faq-question"
            label="Question"
            type="text"
            fullWidth
            value={faqQuestion}
            onChange={(e) => setFaqQuestion(e.target.value)}
          />
          <TextField
            margin="dense"
            id="faq-answer"
            label="Answer"
            type="text"
            fullWidth
            value={faqAnswer}
            onChange={(e) => setFaqAnswer(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenFaqDialog(false)} color="primary">Cancel</Button>
          <Button onClick={handleAddFaqSubmit} color="primary">Submit</Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default VendorProducts;
