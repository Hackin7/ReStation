// WHEN USER LOGS IN OR LOGS OUT
$(() => {
	firebase.auth().onAuthStateChanged(user => {
		if(user){
			userSignedIn(user);
		}else{
			userNotSignedIn();
		}
	})
})

function logOut(){
	firebase.auth().signOut().then(() => {
		console.log("Sign Out Successful");
	})
	.catch((err) => {
	})
}

function userSignedIn(user){
	var signInDropDown = $("#sign-in-dropdown"), accDropdown = $("#account-dropdown");
	signInDropDown.css("display", "none");
	accDropdown.css("display", "block");

	accDropdown.children("button").html(user.displayName);
}

function userNotSignedIn(){
	var signInDropDown = $("#sign-in-dropdown"), accDropdown = $("#account-dropdown");
	signInDropDown.css("display", "block");
	accDropdown.css("display", "none");
}

function filterInputs(){
	var emailRegex = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/;
	var pwdRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/;

	var email = document.getElementById("email").value;
	var uid = document.getElementById("uid").value;
	var pwd1 = document.getElementById("pwd1").value;
	var pwd2 = document.getElementById("pwd2").value;

	if(email == "" || uid == "" || pwd1 == "" || pwd2 == ""){
		setErrorMsg("Please fill in all fields!");
	}else if(!emailRegex.test(email)){
		setErrorMsg("Please enter a valid email");
	}else if(pwd1 != pwd2){
		setErrorMsg("Passwords have to be identical");
	}else if(!pwdRegex.test(pwd1)){
		setErrorMsg("Password must be at least 8 characters in length, have 1 lowercase letter, 1 uppercase letter and 1 digit");
	}else{
		firebase.auth().createUserWithEmailAndPassword(email, pwd1).then(() => {
			console.log("Sign up successful!");

			updateUserDisplayName(uid);
		})
		.catch(function(error)
		{
			var errorCode = error.code;
			var errorMsg = error.message;

			if(errorCode == "auth/email-already-in-use"){
				setErrorMsg("Email already in use!");
			}else{
				setErrorMsg(errorMsg);
			}
		});
	}
}

function updateUserDisplayName(uid){
	var user = firebase.auth().currentUser;
	console.log(user);
	if (user){
		user.updateProfile({
			displayName: uid
		}).then(() => {
			console.log(user.displayName);

			goHome();
		}).catch((error) => {

		})
	}else{
		console.log("Nobody is signed in");
	}
}

function goHome(){
	window.location.href = "index.html";
}

function setErrorMsg(msg){
	var errorMsg = $("#signup-error-msg");
	errorMsg.html(`<p class="alert alert-danger">${msg}</p>`);
}
function setSignInErrorMsg(msg){
	var errLabel = $("#signin-error-msg");
	errLabel.html(`<p class="alert alert-danger">${msg}</p>`);
}

function resetAllInputFields(){
	console.log("Reset!");

	document.getElementById("email").value = "";
	document.getElementById("uid").value = "";
	document.getElementById("pwd1").value = "";
	document.getElementById("pwd2").value = "";

	$("uid-input").val("");
	$("pwd-input").val("");

	$("#signup-error-msg").children("p").remove();
	$("#signin-error-msg").children("p").remove();

	$("#open-signup").data('clicked', false);
	console.log("From rest, ");
}

function signUpWithEmail(){
	filterInputs();
}

function signInWithEmail(){
	var email = $("#uid-input").val();
	var pwd = $("#pwd-input").val();

	if(email == "" || pwd == ""){
		setSignInErrorMsg("Please fill in all fields!");
	}else{
		firebase.auth().signInWithEmailAndPassword(email, pwd).then(() => {
			resetAllInputFields();
		})
		.catch((err) => {
			var errorCode = err.code;
			var errorMsg = err.message;
	
			switch(errorCode){
				case "auth/invalid-email":
					setSignInErrorMsg("Invalid email!");
					break;
				case "auth/user-disabled":
					setSignInErrorMsg("This user is disabled!");
					break;
				case "auth/user-not-found":
					setSignInErrorMsg("No such user!");
					break;
				case "auth/wrong-password":
					setSignInErrorMsg("Ensure all fields input correctly!");
					break;
				default:
					setSignInErrorMsg(errorMsg);
			}
		})
	}
}

function signInWithGoogle(){
	console.log("Signing in with google...");
	var googleProvider = new firebase.auth.GoogleAuthProvider();
	firebase.auth().signInWithRedirect(googleProvider);
}
