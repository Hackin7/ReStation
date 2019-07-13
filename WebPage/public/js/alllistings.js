const db = firebase.firestore();
const storage = firebase.storage();

var cardText = "";

//  Display Img function leave for later do
function findImg(id){
    //console.log(id);
    let imgUrl = ""
    let allowedExts = ['png', 'jpg', 'jpeg', 'gif', 'svg'];
    allowedExts.forEach((ext) => {
        storage.ref().child(`itemimages/${id}.${ext}.jpg`).getDownloadURL()
        .then((url) => {
            imgUrl = url;
            
        }).catch((err) => {
            
            switch(err.code){
                case "storage/object-not-found":
                    console.log("Object not found!");
                    break;
                default:
                    console.log("Can't find img file");
            }
        })
    })
    return imgUrl;
}

function goToListingPage(title, keyPin){
    
    sessionStorage.setItem('listingTitle', title);

    window.location.href = "/listing.html";
}

// async function showListing(title, datetime){
//     // var doc;
//     // //  Filter out based on 
//     // db.collection('listings').where("title", "==", title)
//     // .where("datetime", "==", datetime)
//     // .get()
//     // .then((doc) => {
//     //     // $.cookie('listToOpen', doc);
//     //     localStorage.setItem("listing", doc);
//     //     goToListingPage();
//     // })
// }

// async function showListing(title, datetime){
//     console.log(datetime);
//     let doc = await queryListing(title, datetime);
//     console.log("Test", doc);
// }

function addListCard(id, doc){
    
    //let imgUrl = findImg(id);

    let imgUrl = "images/loading.jpg";

    // let dt = toDate(doc.datetime);
    // console.log(dt);

    cardText += `<div class="col-3 p-2">
    <div class="card">
        <div style="width: 200px;" class="mx-auto d-block">
            <img src="${imgUrl}" class="card-img-top" alt="${doc.title}" style="width: 100%; height: auto;">
        </div>
        <div class="card-body">
            <h2 class="card-title text-dark">${doc.title}</h2>
            <p class="text-dark card-text">${doc.descrip}</p>
            <p class="text-info card-text">${doc.datetime}</p>
            <a class="btn btn-info stretched-link" onclick="goToListingPage('${doc.title}', '${doc.keyPin}')">View Listing</a>
        </div>
    </div>
</div>`
    $("#all-listings").html(cardText);
    //console.log($("#all-listings btn"));
    // $(document).ready(() => {
    //     // $("#all-listings btn").each((btn) => {
    //     //     $(document).on('click', btn, () => {
    //     //         alert("Fuck");
    //     //     })
    //     // })
    //     $(document).on('click', "#yeet", () => {
    //         alert("Fuck");
    //     })
    // })
}

// function addOnClickListener(){
//     $(document).ready(() => {
//         $("#all-listings btn").each((btn) => {
//             console.log(btn);
//             $(document).on('click', btn, () => {
//                 alert("Fuck");
//             })
//         })
//     })
// }

// function sayFuck(msg){
//     alert(msg);
// }

function getListings(){
    db.collection("listings").get().then(function(querySnapshot) {
        querySnapshot.forEach(function(doc) {
           addListCard(doc.id, doc.data());
        });
    });
}

getListings();