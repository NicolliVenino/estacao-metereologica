if (document.getElementById('graficoEvolucao') && typeof dadosHistoricos !== 'undefined') {
    const ctx = document.getElementById('graficoEvolucao').getContext('2d');

    const dadosChart = [...dadosHistoricos].reverse();
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dadosChart.map(d => d.timestamp.split(' ')[1]), 
            datasets: [{
                label: 'Temperatura (°C)',
                data: dadosChart.map(d => d.temperatura),
                borderColor: '#c71585',
                tension: 0.1
            }, {
                label: 'Umidade (%)',
                data: dadosChart.map(d => d.umidade),
                borderColor: '#00bfff',
                tension: 0.1
            }]
        }
    });

    setTimeout(() => location.reload(), 10000);
}

async function deletarLeitura(id) {
    if(confirm("Tem certeza que deseja excluir esta leitura?")) {
        const res = await fetch(`/leituras/${id}`, { method: 'DELETE' });
        if(res.ok) {
            document.getElementById(`linha-${id}`).remove();
        } else {
            alert("Erro ao excluir.");
        }
    }
}

async function atualizarLeitura(event, id) {
    event.preventDefault();
    const dados = {
        temperatura: parseFloat(document.getElementById('temp').value),
        umidade: parseFloat(document.getElementById('umid').value),
        pressao: document.getElementById('press').value ? parseFloat(document.getElementById('press').value) : null
    };

    const res = await fetch(`/leituras/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
    });

    if(res.ok) {
        alert("Atualizado com sucesso!");
        window.location.href = '/historico';
    } else {
        alert("Erro ao atualizar.");
    }
}