async function moexTickerLast(ticker) {
    const json = await fetch('https://iss.moex.com/iss/engines/stock/markets/shares/securities/' + ticker + '.json?iss.meta=off')
        .then((res) => { return res.json()});
    return "Текущая цена акции Сбера: "+json.marketdata.data.filter(function(d) { return ['TQBR', 'TQTF'].indexOf(d[1]) !== -1; })[0][12];
    
}

moexTickerLast('SBER').then(sber_price => 
    document.getElementById("stocks-sber").innerHTML = sber_price);


document.addEventListener('DOMContentLoaded', function() {

        const button = document.getElementById('generate-button-1');
        const textMessage = document.getElementById('text-message-1');
        // Обработчик события клика по кнопке
        button.addEventListener('click', function() {
            this.style.display = 'none';  
            textMessage.style.display = 'inline';
        });
    });    



document.addEventListener('DOMContentLoaded', function() {

        const button = document.getElementById('generate-button-7');
        const textMessage = document.getElementById('text-message-7');
        // Обработчик события клика по кнопке
        button.addEventListener('click', function() {
            this.style.display = 'none';  // Скрываем кнопку
            textMessage.style.display = 'inline';
        });
    });

document.addEventListener('DOMContentLoaded', function() {

        const button = document.getElementById('generate-button-30');
        const textMessage = document.getElementById('text-message-30');
        // Обработчик события клика по кнопке
        button.addEventListener('click', function() {
            this.style.display = 'none';  // Скрываем кнопку
            textMessage.style.display = 'inline';
            
            
        });
    });   
    
document.addEventListener('DOMContentLoaded', function() {

        const button = document.getElementById('generate-button-90');
        const textMessage = document.getElementById('text-message-90');
        // Обработчик события клика по кнопке
        button.addEventListener('click', function() {
            this.style.display = 'none';  // Скрываем кнопку
            textMessage.style.display = 'inline';
            

        });
    });        

