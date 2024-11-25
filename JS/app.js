document.getElementById('fetch-data').addEventListener('click', async () => {
    const trophyList = document.getElementById('trophy-list');
    trophyList.innerHTML = 'Loading...';

    try {
        const response = await fetch('http://127.0.0.1:5000/get-trophy-data');
        if (response.ok) {
            const data = await response.json();
            trophyList.innerHTML = '';
            data.trophyTitles.forEach(trophy => {
                const trophyDiv = document.createElement('div');
                trophyDiv.className = 'trophy';
                trophyDiv.innerHTML = `
                    <h3>${trophy.trophyTitleName}</h3>
                    <p>Earned: ${trophy.earnedTrophies}</p>
                `;
                trophyList.appendChild(trophyDiv);
            });
        } else {
            trophyList.innerHTML = 'Failed to fetch data.';
        }
    } catch (error) {
        trophyList.innerHTML = `Error: ${error.message}`;
    }
});
