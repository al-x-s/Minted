/**------------------------------------------------------------------------
 *                           Document Objects
 *------------------------------------------------------------------------**/

navLogin = document.getElementById("nav_login")
navSignup = document.getElementById("nav_signup")
dialogLogin = document.getElementById("dialogLogin")
dialogSignup = document.getElementById("dialogSignup")
joinButton = document.getElementById("join_button")


/**------------------------------------------------------------------------
 *                           Login and Signup Dialog
 *------------------------------------------------------------------------**/

/**----------------------
 *    Open Dialogs
 *------------------------**/

navLogin.addEventListener("click", () => {
    dialogLogin.showModal();
})

navSignup.addEventListener("click", () => {
    dialogSignup.showModal();
})

joinButton.addEventListener("click", () => {
    dialogSignup.showModal();
})


/**----------------------
 *    Close Dialogs
 *------------------------**/

const lightDismiss = ({target:dialog}) => {
    if (dialog.nodeName === 'DIALOG')
      dialog.close('dismiss')
}
document.addEventListener('click', lightDismiss);
