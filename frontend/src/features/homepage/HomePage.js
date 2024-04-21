import React, { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { fetchAllProducts } from "./homePageSlice"; // Update the path
import { Link } from "react-router-dom";

// import AddIcon from '@mui/icons-material/Add';

// Import Material-UI components
import {
  Container, 
  Typography,
  Grid,
  CircularProgress,
  Card,
  CardContent,
  CardMedia,
  Box,
} from "@mui/material";

// Import CSS for consistent card heights
import "./HomePage.css";

const HomePage = () => {
  const dispatch = useDispatch();
  const { productsList, status } = useSelector((state) => state.homePage);

  useEffect(() => {
    dispatch(fetchAllProducts());
  }, [dispatch]);

  return (
    <Container
      style={{ marginTop: "100px", display: "flex", justifyContent: "center" }}
    >
      <Box width="80%" style={{ paddingBottom: "20px" }}>
        <Typography
          variant="h3"
          style={{
            marginTop: "20px",
            marginBottom: "40px",
            fontWeight: "bold",
          }}
          gutterBottom
        >
          All Products
        </Typography>
        {status === "loading" ? (
          <CircularProgress />
        ) : (
          <Grid container spacing={3}>
            {productsList.map((product) => (
              <Grid item xs={12} sm={6} md={4} key={product.product_id}>
                <Link
                  to={`/product/${product.product_id}`}
                  style={{ textDecoration: "none", color: "inherit" }}
                >
                  <Card
                    style={{
                      display: "flex",
                      flexDirection: "column",
                      height: "100%",
                      cursor: "pointer",
                    }}
                  >
                    <CardMedia
                      component="img"
                      className="card-media"
                      image={product.image_url}
                      alt={product.name}
                    />
                    <CardContent
                      style={{
                        display: "flex",
                        flexDirection: "column",
                        justifyContent: "space-between",
                        flexGrow: 1,
                      }}
                    >
                      <div>
                        <Typography
                          gutterBottom
                          variant="h5"
                          style={{ fontWeight: "bold" }}
                          component="div"
                        >
                          {product.name}
                        </Typography>
                      </div>
                      <div style={{ marginTop: "auto" }}>
                        <Typography
                          variant="body2"
                          color="text.secondary"
                          className="description"
                        >
                          {product.description}
                        </Typography>
                        <Typography variant="body1">
                          ${product.price}
                        </Typography>
                      </div>
                    </CardContent>
                  </Card>
                </Link>
              </Grid>
            ))}
          </Grid>
        )}
      </Box>
    </Container>
  );
};

export default HomePage;
