<?php
// Conectar a la base de datos
$conexion = mysqli_connect("localhost", "root", "", "agenda");

// Verificar conexión
if (mysqli_connect_errno()) {
    echo "Error al conectar a la base de datos: " . mysqli_connect_error();
    exit();
}

// Obtener datos del formulario
$nombre = $_POST['nombre'];
$descripcion = $_POST['descripcion'];
$precio = $_POST['precio'];

// Insertar producto en la base de datos
$sql = "INSERT INTO productos (nombre, descripcion, precio) VALUES ('$nombre', '$descripcion', '$precio')";
if (mysqli_query($conexion, $sql)) {
    echo "Producto agregado correctamente.";
} else {
    echo "Error al agregar el producto: " . mysqli_error($conexion);
}

// Cerrar conexión
mysqli_close($conexion);
?>
