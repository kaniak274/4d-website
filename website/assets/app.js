import './styles/main.scss';
import Cookies from 'js-cookie';

const csrftoken = Cookies.get('csrftoken');

const closeModalListener = () => {
    document.querySelector('.modal').classList.remove('is-active');
}

const link = document.getElementById('password-reset');
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
