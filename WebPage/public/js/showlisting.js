const db = firebase.firestore();
const storageRef = firebase.storage().ref();

var listedItem = {id:-1};
//  FIX THE FKING DATE
//Button Claimed

function showListing(){
    var docTitle = sessionStorage.getItem('listingTitle');

    //  Filter out based on 
    db.collection('listings')
    .where("title", "==", docTitle)
    .get()
    .then((querySnapshot) => {
        //var doc = querySnapshot[0];
        querySnapshot.forEach((doc) => {
            console.log(doc.data());
            initListingDetails(doc.data());
            listedItem = doc;
            listedItem.claimed = listedItem.data().claimed;
            listedItem.pin = listedItem.data().keyPin;
            claimedUpdate();
        })
    })
}

async function setListingImg(filePath){
    storageRef.child(filePath).getDownloadURL().then((url) => {
        $("#list-img").attr('src', url);
    })
}

function initListingDetails(data){
    var dateNow = new Date(data.datetime['seconds']);
    //  Add 7 days
    var dateExpiry = new Date(data.datetime['seconds'] + 604800);
    console.log(data.id);

    $("#list-title").html(data.title);

    setListingImg(data.filePath);

    $("#list-datetime").html(dateNow);
    $("#list-datetime-expiry").html(dateExpiry);
    

    $("#list-uid").html(data.uid);
    $("#list-descrip").html(data.descrip);
    $("#list-lockerLoc").html(data.lockerLocation);
    $("#list-lockerNum").html(data.lockerNumber);
}

showListing();
