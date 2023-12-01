
const followBtn = document.getElementById('followBtn')


let btnChange = document.getElementsByClassName('toggle-follow-btn')
let followersCountDisplay = document.getElementById('followersCountDisplay')
let followingCountDisplay = document.getElementById('followingCountDisplay')

if(followBtn != null) {

    followBtn.addEventListener('click', ()=>{
        profileId = followBtn.getAttribute('profileId')

        let xhr = new XMLHttpRequest();
        xhr.open('GET',`/followOrunfollow/${profileId}`, true);
        xhr.onreadystatechange = () => {
            if(xhr.readyState === XMLHttpRequest.DONE) {
                if(xhr.status === 200) {
                    let response = JSON.parse(xhr.responseText);
                    let data = response


                    followBtn.classList.toggle('followingProfilebtn');

                    followersCountDisplay.innerText = data.followersCount
                    followingCountDisplay.innerText = data.followingCount


                    if (data.is_Following === true) {
                        followBtn.innerText = 'Following'
                    } else {
                        followBtn.innerText = 'Follow'
                    }

                } else {
                    console.error('Error', xhr.status);
                }
            }
        }
        xhr.send()
    })
}
// ----------------------------- in post liking ------------------------ //