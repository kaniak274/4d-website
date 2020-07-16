import './styles/main.scss';
import Cookies from 'js-cookie';

const csrftoken = Cookies.get('csrftoken');

const closeModalListener = () => {
    document.querySelector('.modal').classList.remove('is-active');
}

const link = document.getElementById('password-reset');

if (link) {
    link.addEventListener('click', ({ target: { id }}) => {
        const modal = document.getElementById(`${id}-modal`);
    
        modal.classList.add('is-active');
    
        modal.querySelector('.delete').addEventListener('click', closeModalListener);
        modal.querySelector('.cancel').addEventListener('click', closeModalListener);
    });
    
    const sendEmailButton = document.getElementsByClassName('send-email')[0];
    sendEmailButton.addEventListener('click', () => {
        const email = document.querySelector('input[type="email"]').value.trim();
        const data = { email };
    
        fetch('/password-reset/', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json; charset=utf-8',
                'X-Requested-With': 'XMLHttpRequest',
            },
        }).then(
            (response) => response.json()
        ).then(
            (data) => console.log(data)
        );
    });
}

const updateRanking = (data, page) => {
    const ranks = document.getElementById('player-list');

    ranks.innerHTML = "";

    data.results.forEach((el) => {
        ranks.innerHTML += `<li>${el.name} ${el.kills}</li>`
    });

    const nextButton = ranks.parentNode.parentNode.querySelector('.pagination-next');
    const previousButton = ranks.parentNode.parentNode.querySelector('.pagination-previous');

    ranks.start = (page * 10) - 10 + 1;

    if (data.next) {
        nextButton.dataset.page = page + 1;
        nextButton.disabled = false;
    } else {
        nextButton.disabled = true;
    }

    if (data.previous) {
        previousButton.dataset.page = page - 1;
        previousButton.disabled = false;
    } else {
        previousButton.disabled = true;
    }
}

const sendRankingFetch = (url, page) => {
    fetch(url)
        .then((response) => response.json())
        .then((data) => updateRanking(data, page));
}

Array.from(document.getElementsByClassName('ranking-paginator'))
    .forEach((el) => {
        el.addEventListener('click', ({ target }) => {
            const fetchURL = target.dataset.fetchUrl;
            const page = parseInt(target.dataset.page);

            sendRankingFetch(`${fetchURL}?page=${page}`, page);
        });
    });

Array.from(document.getElementsByClassName('ranking-search'))
    .forEach((el) => {
        el.addEventListener('change', ({ target: { value }}) => {
            sendRankingFetch(`${target.dataset.fetchUrl}?search=${value}`);
        });
    });
