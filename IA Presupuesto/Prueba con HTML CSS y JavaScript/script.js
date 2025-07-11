// ===================== EXPORTAR PRESUPUESTO COMO PDF PROFESIONAL =====================
// Toma los datos del formulario y la tabla, los coloca en la plantilla oculta y la exporta como PDF profesional.
// 1. Toma los datos del usuario y presupuesto
// 2. Valida los campos requeridos
// 3. Rellena la plantilla oculta con los datos y la tabla
// 4. Hace visible la plantilla y la exporta como PDF usando html2pdf
// 5. Restaura la visibilidad y limpia la plantilla para el siguiente uso
function exportarPDF() {
  // Tomar datos del formulario en la página principal
  const cliente = document.getElementById('input-cliente').value;
  const direccion = document.getElementById('input-direccion').value;
  const telefono = document.getElementById('input-telefono').value;
  const email = document.getElementById('input-email').value;
  const obs = document.getElementById('input-obs').value;
  // Nuevos campos de presupuesto
  const obra = document.getElementById('input-obra').value;
  const inicio = document.getElementById('input-inicio').value;
  const entrega = document.getElementById('input-entrega').value;
  const validez = document.getElementById('input-validez').value;
  const pago = document.getElementById('input-pago').value;

  // Validar campos requeridos
  if (!cliente || !direccion || !telefono || !email) {
    alert('Por favor, complete todos los datos del cliente.');
    return;
  }

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
  // Nuevos campos en la plantilla (si existen los spans, rellenarlos)
  if(document.getElementById('obra-presupuesto')) document.getElementById('obra-presupuesto').textContent = obra || '________________________';
  if(document.getElementById('inicio-presupuesto')) document.getElementById('inicio-presupuesto').textContent = inicio || '________________________';
  if(document.getElementById('entrega-presupuesto')) document.getElementById('entrega-presupuesto').textContent = entrega || '________________________';
  if(document.getElementById('validez-presupuesto')) document.getElementById('validez-presupuesto').textContent = validez || '________________________';
  if(document.getElementById('pago-presupuesto')) document.getElementById('pago-presupuesto').textContent = pago || '________________________';

  document.getElementById('tabla-factura').innerHTML = filas;
  document.getElementById('total-factura').textContent = total;
  // Hacer la plantilla visible y forzarla a position:static para html2pdf
  plantilla.style.opacity = '1';
  plantilla.style.pointerEvents = 'auto';
  const prevPosition = plantilla.style.position;
  const prevZ = plantilla.style.zIndex;
  plantilla.style.position = 'static';
  plantilla.style.zIndex = 'auto';
  setTimeout(() => {
    html2pdf().set({
      margin: 0,
      filename: `presupuesto-${nro.toString().padStart(4, '0')}.pdf`,
      image: { type: 'jpeg', quality: 0.98 },
      html2canvas: { scale: 2 },
      jsPDF: { unit: 'px', format: [800, 1131], orientation: 'portrait' }
    }).from(plantilla).save().then(() => {
      // Restaurar visibilidad y posición
      plantilla.style.opacity = '0';
      plantilla.style.pointerEvents = 'none';
      plantilla.style.position = prevPosition;
      plantilla.style.zIndex = prevZ;
      // Limpiar campos para la próxima vez
      document.getElementById('cliente-presupuesto').textContent = '________________________';
      document.getElementById('direccion-presupuesto').textContent = '________________________';
      document.getElementById('telefono-presupuesto').textContent = '________________________';
      document.getElementById('email-presupuesto').textContent = '________________________';
      document.getElementById('obs-presupuesto').textContent = '________________________';
      if(document.getElementById('obra-presupuesto')) document.getElementById('obra-presupuesto').textContent = '________________________';
      if(document.getElementById('inicio-presupuesto')) document.getElementById('inicio-presupuesto').textContent = '________________________';
      if(document.getElementById('entrega-presupuesto')) document.getElementById('entrega-presupuesto').textContent = '________________________';
      if(document.getElementById('validez-presupuesto')) document.getElementById('validez-presupuesto').textContent = '________________________';
      if(document.getElementById('pago-presupuesto')) document.getElementById('pago-presupuesto').textContent = '________________________';
      document.getElementById('tabla-factura').innerHTML = '';
      document.getElementById('total-factura').textContent = '0';
      // Limpiar formulario
      document.getElementById('form-datos').reset();
    });
  }, 400);
}

// ===================== AGREGAR FILA A LA TABLA DE ESPACIOS =====================
// Permite agregar una nueva fila para un espacio a presupuestar.
// Cada fila tiene campos para nombre, metros cuadrados, precio y subtotal.
function agregarFila() {
  const tbody = document.querySelector('#tabla-m2 tbody');
  const tr = document.createElement('tr');
  tr.innerHTML = `
    <td><input type="text" placeholder="Espacio" style="width:120px"></td>
    <td><input type="number" class="m2" min="0" step="0.01" style="width:70px" value="0"></td>
    <td><input type="number" class="precio" min="0" step="0.01" style="width:90px" value="0"></td>
    <td class="sub">0</td>
  `;
  tbody.appendChild(tr);
}

// ===================== CALCULAR TOTALES DE LA TABLA =====================
// Calcula los subtotales y el total de la tabla de metros cuadrados.
// Actualiza el campo "Total Cálculo M²" en la interfaz.
function calcular() {
  let total = 0;
  document.querySelectorAll('#tabla-m2 tbody tr').forEach(row => {
    const m2 = parseFloat(row.querySelector('.m2').value) || 0;
    const precio = parseFloat(row.querySelector('.precio').value) || 0;
    const sub = m2 * precio;
    row.querySelector('.sub').textContent = sub.toFixed(2);
    total += sub;
  });
  document.getElementById('total-m2').textContent = total.toFixed(2);
}