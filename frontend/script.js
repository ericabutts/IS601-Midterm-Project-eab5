console.log('loaded')

document.getElementById('add').onclick = async () => {
    console.log('Add')
    const a = document.getElementById('a').value;
    const b = document.getElementById('b').value;

    const res = await fetch(`http://127.0.0.1:8000/add?a=${a}&b=${b}`);
    const data = await res.json();
    document.getElementById('result').textContent = data.result;


};