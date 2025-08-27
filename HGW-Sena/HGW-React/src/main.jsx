import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { RouterProvider } from 'react-router-dom';

import router from './router.jsx';
import 'ldrs/react/Infinity.css';
import 'bootstrap/dist/js/bootstrap.min.js';
import 'boxicons/css/boxicons.min.css';
import 'sweetalert2/dist/sweetalert2.min.css';
import './assets/css/fijos/index.css';
import './assets/css/fijos/style.css';

import { AuthProvider } from './pages/Context/AuthContext.jsx';

createRoot(document.getElementById('root')).render(
  <StrictMode>
      <AuthProvider>
        <RouterProvider router={router} />
      </AuthProvider>
  </StrictMode>
);
