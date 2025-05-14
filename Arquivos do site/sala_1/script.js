// Botão para alternar o status da lâmpada
document.getElementById('toggle-btn').addEventListener('click', () => {
  const status = document.getElementById('lamp-status');
  if (status.textContent.includes('desligada')) {
    status.textContent = 'Lâmpada está ligada.';
    // Adicione código para comunicar com ESP32
  } else {
    status.textContent = 'Lâmpada está desligada.';
    // Adicione código para comunicar com ESP32
  }
});

// Valor inicial do tamanho da fonte
let fontSize = 16; // Tamanho base da fonte em pixels

// Botão para aumentar o tamanho da fonte
document.getElementById('increase-font-btn').addEventListener('click', () => {
  fontSize += 3; // Aumenta 3px
  document.body.style.fontSize = fontSize + 'px';
});

// Botão para diminuir o tamanho da fonte
document.getElementById('decrease-font-btn').addEventListener('click', () => {
  fontSize -= 3; // Diminui 3px
  if (fontSize < 10) fontSize = 10; // Limita o tamanho mínimo
  document.body.style.fontSize = fontSize + 'px';
});

// Botão para alternar o contraste
document.getElementById('toggle-contrast-btn').addEventListener('click', () => {
  const body = document.body;
  if (body.style.backgroundColor === 'black') {
    body.style.backgroundColor = '#f9f9f9';
    body.style.color = '#333';
  } else {
    body.style.backgroundColor = 'black';
    body.style.color = 'white';
  }
});
