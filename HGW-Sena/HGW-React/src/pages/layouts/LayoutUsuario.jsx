import { Outlet } from 'react-router-dom';
import { isLoggedIn } from '../../auth';
import Header from '../../User/Components/Fijos/header';
import HeaderView from '../../View/Components/header';
import FooterView from '../../View/Components/footer';
import ChatBot from '../../User/Components/Fijos/chatBot';
import LoginModal from '../../View/Components/login/modalLogin';
import PrivateRoute from '../Context/PrivateRoute';
import { ModalProvider } from '../Context/ModalContext';

export default function LayoutUsuario() {
    return (
        isLoggedIn() ?
        <PrivateRoute>
            <Header />
            <Outlet />
            <FooterView />
            <ChatBot />
        </PrivateRoute>
        :
        <ModalProvider>
            <HeaderView />
            <Outlet />
            <FooterView />
            <LoginModal />
        </ModalProvider>
    );
}