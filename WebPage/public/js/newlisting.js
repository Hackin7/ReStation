const db = firebase.firestore();

// CHECKLIST
// 1. func to get all available lockers & assign lockerNum
// 2. Use google maps for locker location

function setNewQuizErrorMsg(msg){
    $("#new-quiz-error-msg").html(
        `<p class="alert alert-danger mx-auto text-center">${msg}</p>`);
}

function generateKeyPin(){
    return Math.floor(100000 + Math.random() * 900000)
}

//  Get all available lockers from db
function getAvailableLockers(){

}

function goHomePage(){
    window.location.href = "/";
}

function storeImgToStorage(file, id){
    let fileExt = file.name.split(".")[file.name.split(".").length - 1];
    let filePath = `itemimages/${id}.${fileExt}`;
    let imgRef = firebase.storage().ref(`itemimages/${id}.${fileExt}`);
    imgRef.put(file).then(() => {
        alert("Listed Successfully!");
        goHomePage();
    })
}

function addNewListing(){
    let title = $("#title-input").val();
    let img = $("#img-file-input").prop('files')[0];
    let descrip = $("#descrip-input").val();
    let lockerLoc = $("#location-input").val();

    //console.log(img.name);
    let returnMe = false;

    let allInputFields = $("#add-quiz-form .form-control");
    $.each(allInputFields, (key, value) => {
        if(value.value == "" || value.value == null){
            setNewQuizErrorMsg("Please fill in all input fields!");
            returnMe = true;
        }
    })

    if(returnMe) return;

    // let fileExt = img.name.split(".")[img.name.split(".").length - 1];
    // let filePath = `itemimages/${id}.${fileExt}`;

    let currentDate = new Date(), keyPin = generateKeyPin();
    let user = firebase.auth().currentUser.displayName;

    listData = {claimed: false, confirmed: false, title: title, 
    datetime: currentDate, descrip: descrip, keyPin: keyPin, 
    lockerLocation: lockerLoc, lockerNumber: 1234, uid: user};

    db.collection('listings').add(listData).then((docRef) => {
        let fileExt = img.name.split(".")[img.name.split(".").length - 1];
        let filePath = `itemimages/${docRef.id}.${fileExt}`;

        docRef.update({filePath: filePath}).then(() => {
            storeImgToStorage(img, docRef.id);
        })
    })
    console.log("Added to db!");
}