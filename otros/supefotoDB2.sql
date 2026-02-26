-- Script corregido para SQLite3
-- Base de Datos: superfotopamplona

-- -----------------------------------------------------
-- Table categoria
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS categoria (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(255) DEFAULT NULL
);

-- -----------------------------------------------------
-- Table cliente
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS cliente (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    documento VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(150) DEFAULT NULL,
    telefono VARCHAR(20) DEFAULT NULL,
    correo VARCHAR(100) DEFAULT NULL
);

-- -----------------------------------------------------
-- Table empleado
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS empleado (
    id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
    documento VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    cargo VARCHAR(50) DEFAULT NULL,
    direccion VARCHAR(150) DEFAULT NULL,
    telefono VARCHAR(20) DEFAULT NULL,
    correo VARCHAR(100) DEFAULT NULL,
    foto VARCHAR(255) DEFAULT NULL
);

-- -----------------------------------------------------
-- Table rol
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS rol (
    id_rol INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(255) DEFAULT NULL
);

-- -----------------------------------------------------
-- Table usuario
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario VARCHAR(100) NOT NULL UNIQUE,
    nombre_usuario VARCHAR(50) NOT NULL,
    contraseña VARCHAR(100) NOT NULL,
    id_rol INT DEFAULT NULL,
    FOREIGN KEY (id_rol) REFERENCES rol (id_rol)
);

-- -----------------------------------------------------
-- Table pedido
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS pedido (
    id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INT DEFAULT NULL,
    id_empleado INT DEFAULT NULL,
    id_usuario INT DEFAULT NULL,
    fecha_pedido DATE NOT NULL,
    hora_entrega TIME DEFAULT NULL,
    estado VARCHAR(50) DEFAULT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente (id_cliente),
    FOREIGN KEY (id_empleado) REFERENCES empleado (id_empleado),
    FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario)
);

-- -----------------------------------------------------
-- Table proveedor
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS proveedor (
    id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
    documento_nit VARCHAR(20) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(150) DEFAULT NULL,
    telefono VARCHAR(20) DEFAULT NULL,
    correo VARCHAR(100) DEFAULT NULL,
    web VARCHAR(100) DEFAULT NULL
);

-- -----------------------------------------------------
-- Table producto
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS producto (
    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    cantidad INT DEFAULT NULL,
    id_categoria INT DEFAULT NULL,
    id_proveedor INT DEFAULT NULL,
    precio DECIMAL(10, 2) DEFAULT NULL,
    descripcion TEXT DEFAULT NULL,
    FOREIGN KEY (id_categoria) REFERENCES categoria (id_categoria),
    FOREIGN KEY (id_proveedor) REFERENCES proveedor (id_proveedor)
);

-- -----------------------------------------------------
-- Table detallepedido
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS detallepedido (
    id_detalle_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pedido INT DEFAULT NULL,
    id_producto INT DEFAULT NULL,
    precio_unidad DECIMAL(10, 2) DEFAULT NULL,
    cantidad INT DEFAULT NULL,
    descuento DECIMAL(5, 2) DEFAULT NULL,
    FOREIGN KEY (id_pedido) REFERENCES pedido (id_pedido),
    FOREIGN KEY (id_producto) REFERENCES producto (id_producto)
);