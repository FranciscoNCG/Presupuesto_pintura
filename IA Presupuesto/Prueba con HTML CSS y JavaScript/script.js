const tbody = document.querySelector('#tabla-m2 tbody');
const logo = document.querySelector('.logo');

window.onload = recuperarPresupuesto;
window.addEventListener('scroll', () => logo.classList.toggle('logo-sticky', scrollY > 150));
logo.onclick = () => scrollTo({ top: 0, behavior: 'smooth' });

function agregarFila(e = '', m = '', p = '', s = '0') {
  tbody.innerHTML += `<tr>
    <td><input type="text" value="${e}" placeholder="Ej. Cocina" /></td>
    <td><input type="number" class="m2" value="${m}" /></td>
    <td><input type="number" class="precio" value="${p}" /></td>
    <td class="sub">${s}</td>
  </tr>`;
}

function calcular() {
  let total = 0, datos = [];
  tbody.querySelectorAll('tr').forEach(row => {
    const e = row.querySelector('input[type=text]').value;
    const m = parseFloat(row.querySelector('.m2').value) || 0;
    const p = parseFloat(row.querySelector('.precio').value) || 0;
    const s = (m * p).toFixed(2);
    row.querySelector('.sub').textContent = s;
    total += +s;
    datos.push({ espacio: e, m2: m, precio: p, subtotal: s });
  });
  document.getElementById('total-m2').textContent = total.toFixed(2);
  localStorage.setItem('presupuesto', JSON.stringify(datos));
}

function recuperarPresupuesto() {
  const datos = JSON.parse(localStorage.getItem('presupuesto'));
  if (datos) datos.forEach(f => agregarFila(f.espacio, f.m2, f.precio, f.subtotal));
  else agregarFila();
}

function exportarPDF() {
  html2pdf().set({
    margin: 0.5,
    filename: 'presupuesto-pintura.pdf',
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
  }).from(document.querySelector('.container')).save();
}