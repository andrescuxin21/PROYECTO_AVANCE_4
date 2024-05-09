function confirmarEliminacion(taskId) {
    // Setear el ID de la tarea que se eliminará
    document.getElementById('deleteTaskId').value = taskId;

    // Mostrar el modal de confirmación
    var confirmDeleteModal = new bootstrap.Modal(document.getElementById('confirmDeleteModal'), {});
    confirmDeleteModal.show();

    // Prevenir el envío del formulario
    return false;
}
