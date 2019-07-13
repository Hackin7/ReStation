const db = firebase.firestore();

function toMilestones(){
    var user = firebase.auth().currentUser;
    if(user){
        window.location.href = "/myrewards.html";
    }else{
        $(".modal").modal('show');
    }
}

const MILESTONES = {200: "$5 NTUC Voucher", 500: "$10 Starbucks Voucher", 
1000: "$5 NTUC Voucher", 2000: "$10 KOI Card", 5000: "$5 NTUC Voucher", 
10000: "$20 Google Play Gift Card"};
const POINTS = {'list': 50, 'claim': 10};

function checkForMilestoneChange(docRef, ptsToAdd){
    //console.log(docRef);
    let userPts = docRef.points, myMilestoneLvl = docRef.milestoneLevel, counter = 0;
    let rewardsArr = docRef.rewardsArr;
    for(var pts in MILESTONES) {
        //  Alrdy redeemed
        if(counter <= myMilestoneLvl){
            counter ++;
        }else if(counter > myMilestoneLvl){  //  Haven't redeemed
            let userFinalPts = docRef.points + ptsToAdd;
            if(userFinalPts > pts){
                alert("Milestone Level Up!\nCongratulations you have reached the next Milestone Level!");
                myMilestoneLvl ++;
                rewardsArr += MILESTONES[pts];
                userPts += ptsToAdd;
            }
        }
    }
    return {milestoneLevel: myMilestoneLvl, points: userPts, rewardsArray: rewardsArr};
}

function addPoints(type){
    let ptsToAdd = POINTS[type];
    var toUpdateDb;

    var user = firebase.auth().currentUser;
    if(!user) return;
    else{
        let userName = user.displayName;
        db.collection('rewards').where("uid", "==", userName)
        .get().then((querySnapshots) => {
            //console.log("ULTI", querySnapshots.docs[0].data());
            if(querySnapshots.empty){
                //let userPts = 0 + ptsToAdd;

                db.collection('rewards').add({
                    milestoneLevel: 0,
                    points: 0,
                    rewardsArray: new Array(),
                    uid: userName
                }).then((docRef) => {
                    console.log("FROM EMPTY", docRef);
                    toUpdateDb = checkForMilestoneChange(docRef.docs);
                })
            }else{
                let docRef = querySnapshots.docs[0].data();
                //console.log("FROM NOT EMPTY", docRef);
                toUpdateDb = checkForMilestoneChange(docRef);
            }
            console.log(" TO USER DB ", toUpdateDb);

            
            // db.collection('rewards').where("uid", "==", userName)
            // .update(toUpdateDb).then(() => {
            //     console.log("Db Updated!");
            // })

            db.collection('rewards').doc(querySnapshots.docs[0].id)
                .update(toUpdateDb)
                .then(() => {
                    console.log("Database updated!");
                })

            
            // db.collection('rewards').where("uid", "==", userName)
            // .get().then((queryDocs) => {
            //     db.collection('rewards').doc(queryDocs.docs[0].id)
            //     .update(toUpdateDb)
            //     .then(() => {
            //         console.log("Database updated!");
            //     })
            // })
        })
    }
}
//addPoints('list');
