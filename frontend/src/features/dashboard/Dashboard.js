import React from 'react';
import AddProductForm from './AddProductForm';
import {useSelector} from 'react-redux';
import { UserRole } from '../../constants/Constants';
import VendorProducts from './VendorProducts';


const Dashboard = () => {
  const { token, role } = useSelector(state => state.login);

  if(!token || role !== UserRole.VENDOR){
    return <h1 style={{marginTop: "100px"}}>Unauthorized, you are not a VENDOR</h1>
  }

    return (
      <div>
        <AddProductForm token={token} />
        <VendorProducts token={token} />
      </div>
      
    );
  }


export default Dashboard;