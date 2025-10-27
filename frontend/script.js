console.log('loaded')

document.querySelectorAll('button[data-op]').forEach(button => {
    button.onclick = async () => {
        const op = button.dataset.op;
        const a = document.getElementById('a').value;
        const b = document.getElementById('b').value;

        try {
            const res = await fetch(`http://127.0.0.1:8000/calculate/${op}?a=${a}&b=${b}`);
            const data = await res.json();
            document.getElementById('result').textContent = data.result;

        } catch (err) {
            console.error(err);
        }
    }
})