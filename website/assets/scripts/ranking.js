const guildRanking = document.getElementsByClassName('guild-ranking')[0];
const playerRanking = document.getElementsByClassName('players-ranking')[0];
const nolifeRanking = document.getElementsByClassName('nolife-ranking')[0];

guildRanking.style.display = "none";

if (nolifeRanking) {
    nolifeRanking.style.display = "none";
}

const addPlayerToRanking = (player, newTbody) => {
    const row = document.createElement('tr');

    row.innerHTML = `
        <td>${player.place}</td>
        <td>${player.name}</td>
        <td>${player.kills}</td>
        <td>${player.job}</td>
        <td>${player.empire}</td>
    `

    newTbody.appendChild(row);
}

const addPlayerWithPlaytimeToRanking = (player, newTbody) => {
    const row = document.createElement('tr');

    row.innerHTML = `
        <td>${player.place}</td>
        <td>${player.name}</td>
        <td>${player.playtime}</td>
        <td>${player.job}</td>
        <td>${player.empire}</td>
    `

    newTbody.appendChild(row);
}

const addGuildToRanking = (guild, newTbody) => {
    const row = document.createElement('tr');

    row.innerHTML = `
        <td>${guild.place}</td>
        <td>${guild.name}</td>
        <td>${guild.ladder_point}</td>
        <td>${guild.win}</td>
        <td>${guild.draw}</td>
        <td>${guild.loss}</td>
    `

    newTbody.appendChild(row);
}

let searchQuery = '';

const updateRanking = (data, page) => {
    const rankingList = Array.from(document.getElementsByClassName('ranking-list'))
        .find((el) => el.parentNode.parentNode.style.display !== "none");


    const newTbody = document.createElement('tbody');
    rankingList.replaceChild(newTbody, rankingList.querySelector('tbody'));

    data.results.forEach((el) => {
        if (el.kills) {
            addPlayerToRanking(el, newTbody);
        }

        else if ('playtime' in el) {
            addPlayerWithPlaytimeToRanking(el, newTbody);
        }
        
        else {
            addGuildToRanking(el, newTbody);
        }
    });

    const nextButton = rankingList.parentNode.parentNode.querySelector('.pagination-next');
    const previousButton = rankingList.parentNode.parentNode.querySelector('.pagination-previous');

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

            sendRankingFetch(`${fetchURL}?page=${page}&search=${searchQuery}`, page);
        });
    });

Array.from(document.getElementsByClassName('ranking-search'))
    .forEach((el) => {
        el.addEventListener('click', ({ target }) => {
            const query = target
                .parentNode
                .parentNode
                .querySelector('input')
                .value

            searchQuery = query;

            sendRankingFetch(`${target.dataset.fetchUrl}?search=${query}`, 1);
        });
    });

Array.from(document.getElementsByClassName('ranking-header')[0].children)
    .forEach((el) => {
        el.addEventListener('click', ({ target }) => {
            const toShow = target.dataset.show;

            if (toShow === 'guilds') {
                guildRanking.style.display = "";
                playerRanking.style.display = "none";

                if (nolifeRanking) {
                    nolifeRanking.style.display = "none";
                }
            }
            
            else if (toShow === 'nolife') {
                guildRanking.style.display = "none";
                playerRanking.style.display = "none";
                nolifeRanking.style.display = "";
            }
            
            else {
                guildRanking.style.display = "none";
                playerRanking.style.display = "";

                if (nolifeRanking) {
                    nolifeRanking.style.display = "none";
                }
            }
        })
    });
