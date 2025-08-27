import { useProducts } from "../hooks/useProducts.js";
import { isLoggedIn } from "../../auth";
import { Link } from 'react-router-dom';

// Imagenes
import lactti from '../../assets/img/productos/lactti.jpg';
import soya from '../../assets/img/productos/soya.jpg';
import te from '../../assets/img/productos/te.jpg';
import teazul from '../../assets/img/productos/teazul.jpg';
import unete from '../../assets/img/productos/unete.jpg';
import { ProductosLimitados } from './productos';
import { ProductsList } from './productos';

const InicioView = () => {
    const productos = useProducts();
    const limiteCarusel = 4
return (
    <main className="contenido">
        {/* Primera Sección */}
        <div className="conten-item">
            <div className="anuncio">
                <div className="text-content">
                    <h1>Descubre los Mejores Productos Naturales</h1>
                    <p>¡Es hora de transformar tu salud y tu vida!</p>
                    <p>
                    Con los productos naturales de HGW, no solo fortaleces tu bienestar,
                    sino que también abres las puertas a una oportunidad única para generar ingresos y alcanzar tu
                    libertad financiera.
                    </p>
                    <p>Cuidarte nunca fue tan gratificante. {isLoggedIn()?null:<b>¡Únete ahora!</b>}</p>
                    {
                        isLoggedIn() ?
                        <div className="bts">
                            <Link to="/catalogo" className="button">Compra</Link>
                        </div>
                        :<div className="bts">
                            <Link to="/register" className="button">Únete</Link>
                            <Link to="/login" className="button">Compra</Link>
                        </div>
                    }
                </div>

                {/* Slider de imágenes */}
                <div className="slider-conten">
                    <div className="slider">
                        <ul>
                            {[ lactti, soya, te, teazul, unete].map((img, i) => (
                            <li key={i}>
                                <img src={img} alt={`anuncio-${i+1}`} />
                            </li>
                            ))}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        <div className="conten-item">
            <div className="destacados">
                <h2>Productos destacados</h2>
                <div id="carouselExampleAutoplaying" className="carousel slide destacados-contenido" data-bs-ride="carousel">
                    <div className="carousel-indicators">
                    {[0, 1, 2, 3].map((index) => (
                        <button
                        key={index}
                        type="button"
                        data-bs-target="#carouselExampleAutoplaying"
                        data-bs-slide-to={index}
                        className={index === 0 ? 'active' : ''}
                        aria-current={index === 0 ? 'true' : undefined}
                        aria-label={`Slide ${index + 1}`}
                        ></button>
                    ))}
                    </div>
                    
                    <div className="carousel-inner">
                    {[0, 1, 2, 3].map((_, i) => (
                        <div className={`carousel-item ${i === 0 ? 'active' : ''}`} key={i}>
                            <ProductosLimitados limit={limiteCarusel}
                            start={i*limiteCarusel}
                            productos={productos}/>
                        </div>
                    ))}
                    </div>

                    <button className="carousel-control-prev" type="button" data-bs-target="#carouselExampleAutoplaying" data-bs-slide="prev">
                        <span className="carousel-control-prev-icon" aria-hidden="true">
                            <i className="bx bxs-chevron-left"></i>
                        </span>
                        <span className="visually-hidden">Previous</span>
                    </button>

                    <button className="carousel-control-next" type="button" data-bs-target="#carouselExampleAutoplaying" data-bs-slide="next">
                        <span className="carousel-control-next-icon" aria-hidden="true">
                            <i className="bx bxs-chevron-right"></i>
                        </span>
                        <span className="visually-hidden">Next</span>
                    </button>
                </div>
            </div>
        </div>

      {/* Sección de productos */}
        <div className="conten-item">
            <div className="productos">
                <h2>Productos</h2>
                <div className="productos-container">
                    <ProductosLimitados limit={20} productos={productos}/>
                </div>
            </div>
        </div>
    </main>
);
};

export default InicioView;
