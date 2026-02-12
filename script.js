// Отправка данных в Telegram бот
function buy(tariff) {
    if (window.Telegram?.WebApp) {
        const tg = window.Telegram.WebApp;
        tg.sendData(JSON.stringify({
            action: 'buy',
            tariff: tariff
        }));
        tg.close();
    } else {
        alert('Это приложение должно быть открыто через Telegram');
    }
}