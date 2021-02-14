-- Insert de estados
INSERT INTO estado VALUES(1,"Generado",1);
INSERT INTO estado VALUES(2,"Asignado",2);
INSERT INTO estado VALUES(3,"Recogido",3);
INSERT INTO estado VALUES(4,"Camino",4);
INSERT INTO estado VALUES(5,"Destino",5);
INSERT INTO estado VALUES(6,"Entregado",6);

-- Insert usuarios
INSERT INTO usuario VALUES(1169315312, 'Camilo Andrés', 'L', 1201201926, 'caanledu@gmail.com' )

--Insert Paquetes
INSERT INTO paquete (id,numero_guia, nombre_remitente, peso_kg, direccion_destino, direccion_recogida, cliente_id, estado_id)
                VALUES(1, '12356', 'Pedro Antonio', 12.2, 'Cra 23 # 23 - 87', 'Cra 41 # 65 - 98', 11693153129, 1 )
INSERT INTO paquete (id,numero_guia, nombre_remitente, peso_kg, direccion_destino, direccion_recogida, cliente_id, estado_id)
                VALUES(2, '12357', 'Luis Pérez', 21.5, 'Cra 21 # 9 - 87', 'Cra 31 # 66 - 91', 11693153129, 1 )
--Insert clientes
