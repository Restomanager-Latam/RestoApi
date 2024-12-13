CREATE TABLE `restaurants` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`nombre` VARCHAR(255) NOT NULL,
	`url_logo` VARCHAR(255),
	`descripcion` TEXT,
	`calificacion_promedio` FLOAT DEFAULT 0,
	`direccion` VARCHAR(255),
	`h_apertura` TIME,
	`h_cierre` TIME,
	`requiere_sena` BOOLEAN DEFAULT false,
	`valor_sena` FLOAT,
	`h_limite_reserva` TIME,
	`h_limite_cancel` TIME,
	`destacado` BOOLEAN DEFAULT false,
	`tags` JSON,
	`pedido_digital` BOOLEAN,
	PRIMARY KEY(`id`)
);


CREATE TABLE `usuarios_restaurantes` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`resto_id` INTEGER NOT NULL,
	`nombre` VARCHAR(255) NOT NULL,
	`email` VARCHAR(255) NOT NULL UNIQUE,
	`password_hash` VARCHAR(255) NOT NULL,
	`permisos_id` INTEGER NOT NULL,
	PRIMARY KEY(`id`)
);


CREATE TABLE `comentarios` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`resto_id` INTEGER NOT NULL,
	`cliente_id` INTEGER NOT NULL,
	`comentario` TEXT,
	`calificacion` INTEGER NOT NULL CHECK(`calificacion` BETWEEN 1 AND 5),
	`respuesta` TEXT,
	`fecha` DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY(`id`)
);


CREATE INDEX `idx_comentarios_calificacion`
ON `comentarios` (`calificacion`);
CREATE INDEX `idx_comentarios_fecha`
ON `comentarios` (`fecha`);
CREATE TABLE `menu` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`resto_id` INTEGER NOT NULL,
	`nombre` VARCHAR(255) NOT NULL,
	`descripcion` TEXT,
	`precio` FLOAT NOT NULL,
	`categoria` VARCHAR(255),
	`apto_celiacos` BOOLEAN DEFAULT false,
	`apto_hipertensos` BOOLEAN DEFAULT false,
	`apto_veganos` BOOLEAN DEFAULT false,
	`apto_diabeticos` BOOLEAN DEFAULT false,
	`otros_restricciones` JSON,
	`imagenes` JSON,
	`agotado` BOOLEAN,
	PRIMARY KEY(`id`)
);


CREATE INDEX `idx_menu_resto_id`
ON `menu` (`resto_id`);
CREATE INDEX `idx_menu_categoria`
ON `menu` (`categoria`);
CREATE TABLE `agregados` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`menu_id` INTEGER NOT NULL,
	`nombre` VARCHAR(255) NOT NULL,
	`descripcion` TEXT,
	`precio` FLOAT NOT NULL,
	`apto_celiacos` BOOLEAN DEFAULT false,
	`apto_hipertensos` BOOLEAN DEFAULT false,
	`apto_veganos` BOOLEAN DEFAULT false,
	`apto_diabeticos` BOOLEAN DEFAULT false,
	`otros_restricciones` JSON,
	PRIMARY KEY(`id`)
);


CREATE INDEX `idx_agregados_menu_id`
ON `agregados` (`menu_id`);
CREATE TABLE `clientes` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`nombre` VARCHAR(255) NOT NULL,
	`apellido` VARCHAR(255) NOT NULL,
	`email` VARCHAR(255) NOT NULL UNIQUE,
	`password_hash` VARCHAR(255) NOT NULL,
	`ubicacion` VARCHAR(255),
	`idioma` VARCHAR(50),
	`suscripto` BOOLEAN DEFAULT false,
	`url_img_user` VARCHAR(255),
	PRIMARY KEY(`id`)
);


CREATE TABLE `reservas` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`cliente_id` INTEGER NOT NULL,
	`resto_id` INTEGER NOT NULL,
	`fecha_reserva` DATETIME NOT NULL,
	`cantidad_personas` INTEGER NOT NULL,
	`pedido_id` INTEGER,
	`estado` ENUM('Pendiente', 'Confirmada', 'Cancelada', 'Finalizada') DEFAULT 'Pendiente',
	`codigo_reserva` VARCHAR(255) UNIQUE,
	PRIMARY KEY(`id`)
);


CREATE INDEX `idx_reservas_fecha`
ON `reservas` (`fecha_reserva`);
CREATE INDEX `idx_reservas_estado`
ON `reservas` (`estado`);
CREATE TABLE `favoritos` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`cliente_id` INTEGER NOT NULL,
	`resto_id` INTEGER NOT NULL,
	PRIMARY KEY(`id`)
);


CREATE TABLE `pedidos` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`cliente_id` INTEGER,
	`resto_id` INTEGER NOT NULL,
	`mesa` VARCHAR(50),
	`fecha_pedido` DATETIME DEFAULT CURRENT_TIMESTAMP,
	`fecha_programada` DATETIME,
	`estado` ENUM('Pendiente', 'Preparando', 'Listo', 'Entregado', 'Cancelado') DEFAULT 'Pendiente',
	`total` FLOAT,
	`codigo_pedido` VARCHAR(255) UNIQUE,
	PRIMARY KEY(`id`)
);


CREATE INDEX `idx_pedidos_estado`
ON `pedidos` (`estado`);
CREATE INDEX `idx_pedidos_fecha`
ON `pedidos` (`fecha_pedido`);
CREATE TABLE `detalles_pedido` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`pedido_id` INTEGER NOT NULL,
	`menu_id` INTEGER NOT NULL,
	`cantidad` INTEGER NOT NULL DEFAULT 1,
	`precio_unitario` FLOAT NOT NULL,
	`agregados` JSON,
	PRIMARY KEY(`id`)
);


CREATE INDEX `idx_detalles_pedido_pedido_id`
ON `detalles_pedido` (`pedido_id`);
CREATE INDEX `idx_detalles_pedido_menu_id`
ON `detalles_pedido` (`menu_id`);
CREATE TABLE `permisos` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`nivel` ENUM('Administrador', 'Colaborador', 'Básico') NOT NULL,
	PRIMARY KEY(`id`)
);


CREATE TABLE `promos` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`resto_id` INTEGER,
	`id_menu` INTEGER,
	`descripcion` VARCHAR(255),
	`descuento` FLOAT,
	`inicio` DATETIME,
	`fin` DATETIME,
	PRIMARY KEY(`id`)
);


CREATE TABLE `calificacion` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`resto_id` INTEGER,
	`calificacion_table` INTEGER,
	PRIMARY KEY(`id`)
);


ALTER TABLE `usuarios_restaurantes`
ADD FOREIGN KEY(`resto_id`) REFERENCES `restaurants`(`id`)
ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE `agregados`
ADD FOREIGN KEY(`menu_id`) REFERENCES `menu`(`id`)
ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE `comentarios`
ADD FOREIGN KEY(`resto_id`) REFERENCES `restaurants`(`id`)
ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE `menu`
ADD FOREIGN KEY(`resto_id`) REFERENCES `restaurants`(`id`)
ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE `reservas`
ADD FOREIGN KEY(`cliente_id`) REFERENCES `clientes`(`id`)
ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE `reservas`
ADD FOREIGN KEY(`resto_id`) REFERENCES `restaurants`(`id`)
ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE `favoritos`
ADD FOREIGN KEY(`cliente_id`) REFERENCES `clientes`(`id`)
ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE `favoritos`
ADD FOREIGN KEY(`resto_id`) REFERENCES `restaurants`(`id`)
ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE `pedidos`
ADD FOREIGN KEY(`cliente_id`) REFERENCES `clientes`(`id`)
ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE `pedidos`
ADD FOREIGN KEY(`resto_id`) REFERENCES `restaurants`(`id`)
ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE `detalles_pedido`
ADD FOREIGN KEY(`pedido_id`) REFERENCES `pedidos`(`id`)
ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE `detalles_pedido`
ADD FOREIGN KEY(`menu_id`) REFERENCES `menu`(`id`)
ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE `promos`
ADD FOREIGN KEY(`resto_id`) REFERENCES `restaurants`(`id`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `promos`
ADD FOREIGN KEY(`id_menu`) REFERENCES `menu`(`id`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `permisos`
ADD FOREIGN KEY(`id`) REFERENCES `usuarios_restaurantes`(`permisos_id`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `reservas`
ADD FOREIGN KEY(`pedido_id`) REFERENCES `pedidos`(`id`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `calificacion`
ADD FOREIGN KEY(`calificacion_table`) REFERENCES `comentarios`(`calificacion`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `calificacion`
ADD FOREIGN KEY(`resto_id`) REFERENCES `comentarios`(`resto_id`)
ON UPDATE NO ACTION ON DELETE NO ACTION;