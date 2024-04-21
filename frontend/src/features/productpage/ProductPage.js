import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useParams } from 'react-router-dom';
import { fetchProduct } from './productPageSlice';
import { Box, CircularProgress, Typography, Button } from '@mui/material';

const ProductPage = () => {
  const { productId } = useParams();
  const dispatch = useDispatch();
  const { product, status, error, faqList } = useSelector(state => state.productPage);
  const [quantity, setQuantity] = useState(1);

  useEffect(() => {
    const fetchData = async () => {
      await dispatch(fetchProduct(productId));
    };

    fetchData();
  }, [dispatch, productId]);

  const handleIncreaseQuantity = () => {
    setQuantity(prevQuantity => prevQuantity + 1);
  };

  const handleDecreaseQuantity = () => {
    if (quantity > 1) {
      setQuantity(prevQuantity => prevQuantity - 1);
    }
  };

  const handleAddToCart = () => {
    // Add to cart logic here
  };

  if (status === 'loading') {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
        <CircularProgress />
      </Box>
    );
  }

  if (status === 'failed') {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
        <Typography variant="h6">Error: {error}</Typography>
      </Box>
    );
  }

  return (
    <Box display="flex" flexDirection="column" alignItems="center" marginTop="100px" marginBottom="50px">
      {product && (
        <Box width="80%" paddingTop="20px" display="flex">
          {product.image_url && (
            <Box marginRight="20px">
              <img src={product.image_url} alt={product.name} style={{ marginTop: '20px', maxWidth: '100%', minWidth: "400px" }} />
            </Box>
          )}
          <Box display="flex" flexDirection="column" justifyContent="center">
            <Typography variant="h2" style={{ fontWeight: "bold" }}>{product.name}</Typography>
            <Typography variant="h5" color="textSecondary">Price: ${product.price}</Typography>
            <Box display="flex" justifyContent="center" alignItems="center" marginTop="20px">
              <Button fullWidth onClick={handleDecreaseQuantity} variant="contained" color="primary" style={{ backgroundColor: '#dc3416' }}>
                -
              </Button>
              <Typography variant="body1" style={{ padding: "10px" }}>{quantity}</Typography>
              <Button fullWidth onClick={handleIncreaseQuantity} variant="contained" color="primary" style={{ backgroundColor: '#dc3416' }}>
                +
              </Button>
            </Box>
            <Button variant="contained" color="primary" onClick={handleAddToCart} marginTop="20px" style={{ backgroundColor: '#dc3416' }}>Add to Cart</Button>
            <Typography variant="body1" marginTop="20px">Description: {product.description}</Typography>
          </Box>
        </Box>
      )}
      {faqList && faqList.length > 0 ? (
        <Box width="80%" marginTop="50px">
          <Typography variant="h3" style={{fontWeight: "bold"}}>Frequently Asked Questions</Typography>
          {faqList.map((faq, index) => (
            <Box key={index} marginTop="20px">
              <Typography variant="h5">{faq.question}</Typography>
              <Typography variant="body1">{faq.answer}</Typography>
            </Box>
          ))}
        </Box>
      ) : <Box width="80%" marginTop="50px"><Typography variant="h3" style={{fontWeight: "bold"}}>No FAQs found</Typography></Box>}
    </Box>
  );
};

export default ProductPage;
