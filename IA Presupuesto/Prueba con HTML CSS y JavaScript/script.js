
// Mostrar modal y manejar datos del cliente para exportar PDF
function exportarPDF() {
  const modal = document.getElementById('modal-datos');
  const form = document.getElementById('form-datos');
  const cancelar = document.getElementById('cancelar-datos');
  modal.style.display = 'flex';

  cancelar.onclick = () => {
    modal.style.display = 'none';
  };

  form.onsubmit = function(e) {
    e.preventDefault();
    modal.style.display = 'none';
    // Tomar datos del formulario
    const cliente = document.getElementById('input-cliente').value;
    const direccion = document.getElementById('input-direccion').value;
    const telefono = document.getElementById('input-telefono').value;
    const email = document.getElementById('input-email').value;
    const obs = document.getElementById('input-obs').value;

    // Número de presupuesto autoincremental en localStorage
    let nro = parseInt(localStorage.getItem('nroPresupuesto') || '1');
    localStorage.setItem('nroPresupuesto', nro + 1);

    // Obtener datos de la tabla
    const tbody = document.querySelector('#tabla-m2 tbody');
    let filas = '';
    tbody.querySelectorAll('tr').forEach(row => {
      const e = row.querySelector('input[type=text]').value;
      const m = row.querySelector('.m2').value;
      const p = row.querySelector('.precio').value;
      const s = row.querySelector('.sub').textContent;
      filas += `<tr><td style='border:1px solid #ccc;padding:6px;'>${e}</td><td style='border:1px solid #ccc;padding:6px;'>${m}</td><td style='border:1px solid #ccc;padding:6px;'>${p}</td><td style='border:1px solid #ccc;padding:6px;'>${s}</td></tr>`;
    });
    const total = document.getElementById('total-m2').textContent;

    // Rellenar plantilla profesional
    const plantilla = document.getElementById('plantilla-factura');
    document.getElementById('nro-presupuesto').textContent = nro.toString().padStart(4, '0');
    document.getElementById('fecha-presupuesto').textContent = new Date().toLocaleDateString();
    document.getElementById('cliente-presupuesto').textContent = cliente;
    document.getElementById('direccion-presupuesto').textContent = direccion;
    document.getElementById('telefono-presupuesto').textContent = telefono;
    document.getElementById('email-presupuesto').textContent = email;
    document.getElementById('obs-presupuesto').textContent = obs || '________________________';
    document.getElementById('tabla-factura').innerHTML = filas;
    document.getElementById('total-factura').textContent = total;
    plantilla.style.display = 'block';

    html2pdf().set({
      margin: 0,
      filename: `presupuesto-${nro.toString().padStart(4, '0')}.pdf`,
      image: { type: 'jpeg', quality: 0.98 },
      html2canvas: { scale: 2 },
      jsPDF: { unit: 'px', format: [800, 1131], orientation: 'portrait' }
    }).from(plantilla).save().then(() => {
      plantilla.style.display = 'none';
      // Limpiar campos para la próxima vez
      document.getElementById('cliente-presupuesto').textContent = '________________________';
      document.getElementById('direccion-presupuesto').textContent = '________________________';
      document.getElementById('telefono-presupuesto').textContent = '________________________';
      document.getElementById('email-presupuesto').textContent = '________________________';
      document.getElementById('obs-presupuesto').textContent = '________________________';
      document.getElementById('tabla-factura').innerHTML = '';
      document.getElementById('total-factura').textContent = '0';
      // Limpiar formulario
      form.reset();
    });
  };
}